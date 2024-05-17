#
# Copyright (C) 2020 Sylvain Marsat.
#
#

import json
import numpy as np
import pymultinest

import lisabeta
import lisabeta.tools.pytools as pytools
import lisabeta.tools.pyspline as pyspline
import lisabeta.lvk.pyLVKresponse as pyLVKresponse
import lisabeta.lvk.lvk as lvk

import argparse

parser = argparse.ArgumentParser(description='Run LVK parameter inference \
                                              using lisabeta and pymultinest.')

parser.add_argument('input_file', type=str, help='Input json file \
                                                  with all parameters.')
args = parser.parse_args()

# Full list of physical params - infer_params are a subset
# TODO: generalize
listparams = [
    "Mchirp",
    "eta",
    "chi1",
    "chi2",
    "Deltat",
    "dist",
    "inc",
    "phi",
    "ra",
    "dec",
    "psi"]

# Default waveform params
waveform_params_default = {
    "minf": 10.,
    "maxf": 2048.,
    "fstart": None,
    "fend": None,
    "tstart": None,
    "tend": None,
    "phiref": 0.0,
    "fref_for_phiref": 0.0,
    "tref": 0.0,
    "fref_for_tref": 0.0,
    "force_phiref_fref": True,
    "toffset": 0.0,
    "acc": 1e-4,
    "order_fresnel_stencil": 0,
    "approximant": "IMRPhenomD",
    "detectors": ["LHO", "LLO", "VIRGO"]
}

# Default pymultinest params
run_params_musthave = ['outputfiles_basename']
run_params_default = {
    "lisabeta_data_dir": lvk.default_lisabeta_data_dir,
    "zerolike": False,
    "n_live_points": 1000,
    "evidence_tolerance": 0.1,
    "sampling_efficiency": 0.5,
    "seed": -1,
    "resume": False,
    "max_iter": 0,
    "verbose": False,
    "write_output": True,
    "n_iter_before_update": 100,
    "importance_nested_sampling": False,
    "multimodal": False,
    "const_efficiency_mode": False
}

# Default parameter range for angular parameters
params_range_default = {
    "inc": [0., np.pi],
    "phi": [-np.pi, np.pi],
    "ra": [-np.pi, np.pi],
    "dec": [-np.pi/2, np.pi/2],
    "psi": [0., np.pi]
}

# Utility to go from Mchirp-eta variables to m1-m2
def convert_params_m1m2(params_Mchirpeta):
    params_m1m2 = params_Mchirpeta.copy()
    Mchirp = params_m1m2.pop('Mchirp')
    eta = params_m1m2.pop('eta')
    m1 = pytools.m1ofMchirpeta(Mchirp, eta)
    m2 = pytools.m2ofMchirpeta(Mchirp, eta)
    params_m1m2['m1'] = m1
    params_m1m2['m2'] = m2
    return params_m1m2
# Utility to go from m1-m2 variables to Mchirp-eta
def convert_params_Mchirpeta(params_m1m2):
    params_Mchirpeta = params_m1m2.copy()
    m1 = params_Mchirpeta.pop('m1')
    m2 = params_Mchirpeta.pop('m2')
    Mchirp = pytools.Mchirpofm1m2(m1, m2)
    eta = pytools.etaofm1m2(m1, m2)
    params_Mchirpeta['Mchirp'] = Mchirp
    params_Mchirpeta['eta'] = eta
    return params_Mchirpeta

# Utilities for cube-to-param mapping
def map_cube_to_param(priortype, paramrange, x):
    if priortype=='uniform':
        return paramrange[0] + x * (paramrange[1] - paramrange[0])
    elif priortype=='sin': # NOTE: cos decreasing on [0,pi]
        cosrange = [np.cos(paramrange[1]), np.cos(paramrange[0])]
        return np.arccos(cosrange[0] + x * (cosrange[1] - cosrange[0]))
    elif priortype=='cos': # NOTE: sin increasing on [-pi/2,pi/2]
        sinrange = [np.sin(paramrange[0]), np.sin(paramrange[1])]
        return np.arcsin(sinrange[0] + x * (sinrange[1] - sinrange[0]))
    else:
        raise ValueError('priortype not recognized.')

if __name__ == '__main__':

    # Load json file with all parameters
    with open(args.input_file, 'r') as input_file:
        input_params = json.load(input_file)
    # Source params and prior params must be given
    source_params = input_params['source_params']
    prior_params = input_params['prior_params']
    # Waveform params and run params have predefined default values
    waveform_params = waveform_params_default.copy()
    waveform_params.update(input_params['waveform_params'])
    run_params = run_params_default.copy()
    run_params.update(input_params['run_params'])
    zerolike = run_params.pop('zerolike', False)
    lisabeta_data_dir = run_params.pop('lisabeta_data_dir', lvk.default_lisabeta_data_dir)
    # run params must contain output prefix for files -- no default here
    for musthave in run_params_musthave:
        if not (musthave in run_params):
            raise ValueError('run_params must contain %s.' % (musthave))

    # Use default param ranges to complete input ranges -- check completeness
    prior_type = prior_params['prior_type']
    params_range = prior_params['params_range']
    infer_params = prior_params['infer_params']
    for i, param in enumerate(infer_params):
        if params_range[i] == []:
            params_range[i] = params_range_default[param]
    if [] in params_range:
        raise ValueError('Some parameter ranges are neither given \
                      nor covered by the defaults.')

    # Load and interpolate noise data
    noises = {}
    for det in waveform_params['detectors']:
        noisedata = np.loadtxt(lisabeta_data_dir + lvk.noise_data_files[det])
        noise_f = np.copy(noisedata[:,0])
        noise_Sn = np.copy(noisedata[:,1]**2) # sqrt(Sn) in files
        noisesplineClass = pyspline.CubicSpline(noise_f, noise_Sn)
        noises[det] = noisesplineClass.get_spline()

    # Generate injection signal
    signalground_inj = lvk.GenerateLVKSignal(source_params, noises,
                                             **waveform_params)

    # Parameters inferred and parameters fixed
    infer_params = prior_params['infer_params']
    fixed_params = [p for p in listparams if p not in infer_params]
    n_dim = len(infer_params)
    n_fixed = len(fixed_params)
    # NOTE: should be able to set n_params and carry along extra fixed params
    # but did not succeed: was getting undefined behaviour in outputs
    n_params = n_dim

    # Wrapped parameters
    wrapped_params = [0] * n_dim
    for i in range(n_dim):
        wrapped_params[i] = int(prior_params['wrap_params'][i])
    run_params['wrapped_params'] = wrapped_params

    # Define function mapping unit cube to physical params according to priors
    # NOTE: this function is in-place for cube and does not return
    def cubeparams_to_physparams(cube, ndim, nparams):
        assert nparams==n_params and ndim==n_dim
        for i in range(n_dim):
            cube[i] = map_cube_to_param(prior_type[i], params_range[i], cube[i])

    # Define loglikelihood function
    # NOTE: here cube contains already physical parameters, not unit cube values
    def loglike(cube, ndim, nparams):
        assert nparams==n_params and ndim==n_dim
        if zerolike: return 0.
        template_params = {}
        for i in range(n_dim):
            template_params[infer_params[i]] = cube[i]
        for i in range(n_fixed):
            template_params[fixed_params[i]] = \
                                    source_params_Mchirpeta[fixed_params[i]]
        #print(template_params)
        template_params_m1m2 = convert_params_m1m2(template_params)
        lnL = lvk.LogLikelihoodLVK(template_params_m1m2, signalground_inj,
                                   noises, **waveform_params)
        #print(lnL)
        return lnL

    # A la grace de dieu
    pymultinest.run(loglike, cubeparams_to_physparams, n_dim, n_params=n_params,
                    **run_params)
