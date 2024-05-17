#
# Copyright (C) 2020 Sylvain Marsat.
#
#

#Note some assumptions about relative code and data locations
import sys
import os
here=os.path.dirname(os.path.abspath(__file__))
sys.path.append(here+"/../..")

import json
import numpy as np

import lisabeta
import lisabeta.tools.pytools as pytools
import lisabeta.lisa.pyresponse as pyresponse
import lisabeta.lisa.pyLISAnoise as pyLISAnoise
import lisabeta.lisa.lisa as lisa


# Full list of physical params - infer_params are a subset
# TODO: generalize
listparams = [
    "Mchirp",
    "eta",
    "chi1",
    "chi2",
    "fstart",
    "dist",
    "inc",
    "phi",
    "lambda",
    "beta",
    "psi"]

# Default waveform params
waveform_params_default = {
    "minf": 1e-5,
    "maxf": 0.5,
    "fend": None,
    "tstart": 0.0,
    "tmin": 0.0,
    "tmax": 4.0,
    "phiref": 0.0,
    "fref_for_phiref": None,
    "toffset": 0.0,
    "TDI": "TDIAET",
    "acc": 1e-4,
    "order_fresnel_stencil": 0,
    "approximant": "IMRPhenomD",
    "LISAconst": "Proposal",
    "responseapprox": "full",
    "frozenLISA": False,
    "TDIrescaled": True,
    "LISAnoise": {
        "InstrumentalNoise": "SciRDv1",
        "WDbackground": False,
        "WDduration" : 0.0,
        "lowf_add_pm_noise_f0": 0.0,
        "lowf_add_pm_noise_alpha": 2.0
    }
}

# Default pymultinest params
run_params_musthave = ['outputfiles_basename']
run_params_default = {
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
    "lambda": [-np.pi, np.pi],
    "beta": [-np.pi/2, np.pi/2],
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

def process_params(input_file_string):

    # Load json file with all parameters
    with open(input_file_string, 'r') as input_file:
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

    # Convert in-place LISA constellation from string to dict
    LISAconst = pyresponse.LISAconstDict[waveform_params['LISAconst']]
    waveform_params['LISAconst'] = LISAconst
    # Convert in-place LISA instrumental noise from string to internal enum
    LISAnoise = waveform_params['LISAnoise']
    LISAnoise['InstrumentalNoise'] = pyLISAnoise.LISAnoiseDict[
                                                 LISAnoise['InstrumentalNoise']]

    # Convert source params to standard m1-m2 physical params
    # TODO: generalize
    source_params_Mchirpeta = convert_params_Mchirpeta(source_params)

    # Generate injection signal
    tdisignal_inj = lisa.GenerateLISATDISignal_SOBH(source_params,
                                                    **waveform_params)
    print("injection SNR=",tdisignal_inj['SNR'])

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
    return n_params, prior_type, params_range, zerolike, infer_params, fixed_params, source_params_Mchirpeta, tdisignal_inj, waveform_params, run_params

if __name__ == '__main__':
    import pymultinest
    import argparse
    parser = argparse.ArgumentParser(description='Run SOBH parameter inference \
                                              using lisabeta and pymultinest.')

    parser.add_argument('input_file', type=str, help='Input json file \
                                                  with all parameters.')
    args = parser.parse_args()

    n_params, prior_type, params_range, zerolike, infer_params, fixed_params, source_params_Mchirpeta, tdisignal_inj, waveform_params, run_params = process_params(args.input_file)
    n_dim=n_params

    # Define function mapping unit cube to physical params according to priors
    # NOTE: this function is in-place for cube and does not return
    def cubeparams_to_physparams(cube, ndim, nparams):
        assert nparams==n_params and ndim==n_dim
        for i in range(n_dim):
            cube[i] = map_cube_to_param(prior_type[i], params_range[i], cube[i])

    # def test_cubeparams_to_physparams(cube, ndim, nparams):
    # 	assert nparams==n_params and ndim==n_params
    # 	cube_phys = [0] * n_params
    # 	for i in range(n_params):
    # 		cube_phys[i] = map_cube_to_param(prior_type[i], params_range[i], cube[i])
    # 	return cube_phys

    # Define loglikelihood function
    # NOTE: here cube contains already physical parameters, not unit cube values
    def loglike(cube, ndim, nparams):
        assert nparams==n_params and ndim==n_dim
        if zerolike: return 0.
        template_params = {}
        for i in range(n_dim):
            template_params[infer_params[i]] = cube[i]
        for i in range(len(fixed_params)):
            template_params[fixed_params[i]] = \
                                    source_params_Mchirpeta[fixed_params[i]]
        #print(template_params)
        template_params_m1m2 = convert_params_m1m2(template_params)
        lnL = lisa.LogLikelihoodLISA_SOBH(template_params_m1m2, tdisignal_inj,
                                          **waveform_params)
        #print(lnL)
        return lnL

    # A la grace de dieu
    pymultinest.run(loglike, cubeparams_to_physparams, n_dim, n_params=n_params,
                    **run_params)
