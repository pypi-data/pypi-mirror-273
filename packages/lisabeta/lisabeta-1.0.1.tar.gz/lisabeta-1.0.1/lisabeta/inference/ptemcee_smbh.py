#
# Copyright (C) 2020 Sylvain Marsat.
#
#


"""
    Python functions for ptemcee simulated inference of MBHBs with LISA.
"""


import os
import sys
import copy
import json
import h5py
import argparse
import numpy as np

import lisabeta
import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pytools as pytools
import lisabeta.lisa.lisatools as lisatools
import lisabeta.lisa.snrtools as snrtools
import lisabeta.lisa.lisa as lisa
import lisabeta.lisa.lisa_fisher as lisa_fisher
import lisabeta.inference.inference as inference

import ptemcee
import ptemcee.mpi_pool as mpi_pool

try:
    from mpi4py import MPI
except ModuleNotFoundError:
    MPI = None


################################################################################
# Parse arguments, default params

# Parse arguments
parser = argparse.ArgumentParser(description='Run SMBH parameter inference \
                                              using lisabeta and ptemcee with sky jumps.')
parser.add_argument('input_file', type=str, help='Input json file \
                                                  with all parameters.')
args = parser.parse_args()

# Full list of physical params - infer_params are a subset
# TODO: generalize to other choices of mass and spin parameters
# TODO: at the moment, infer_params can only be a subset of this, not flexible
list_params_default = [
    "Mchirp",
    "q",
    "chi1",
    "chi2",
    "Deltat",
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
    "t0": 0.0,
    "timetomerger_max": 1.0,
    "fend": None,
    "tmin": None,
    "tmax": None,
    "Mfmax_model": 0.2,
    "phiref": 0.0,
    "fref_for_phiref": 0.0,
    "tref": 0.0,
    "fref_for_tref": 0.0,
    "force_phiref_fref": True,
    "toffset": 0.0,
    "modes": None,
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
    "WDbackground": True,
    "WDduration" : 3.0
    },
    "waveform_params_update_for_template": {}
}

# Default pymultinest params
# TODO: print_info, n_iter_info very rudimentary at the moment
run_params_musthave = ['out_dir', 'out_name']
run_params_default = {
    "sampler": "ptemcee",
    "sample_Lframe": True,
    "multimodal": False,
    "multimodal_pattern": "1mode",
    "p_jump": 0.,
    "params_map": None,
    "ensemble_proposal": "ptemcee",
    "likelihood_method": "fresnel",
    "likelihood_residuals_ngrid": None,
    "skip_fisher": False,
    "init_method": "prior",
    "init_file": None,
    "init_scale_cov": 1.,
    "zerolike": False,
    "n_temps": 5,
    "temp_max": None,
    "adaptive_temp": False,
    "n_walkers": 100,
    "n_iter": 1000,
    "burn_in": 100,
    "autocor_method": "acor",
    "thin_samples": True,
    "upsample": 1,
    "seed": None,
    "print_info": False,
    "n_iter_info": 10,
    "output": True,
    "output_raw": True
}

# Default parameter range for angular parameters
params_range_default = {
    "inc": [0., np.pi],
    "phi": [-np.pi, np.pi],
    "lambda": [-np.pi, np.pi],
    "beta": [-np.pi/2, np.pi/2],
    "psi": [0., np.pi]
}


################################################################################
# Main

if __name__ == '__main__':

    # Using MPI or not
    # We allow for different cases: MPI used or not, master or worker
    use_mpi = False
    is_master = True
    mapper = map
    if MPI is not None:
        MPI_size = MPI.COMM_WORLD.Get_size()
        MPI_rank = MPI.COMM_WORLD.Get_rank()
        use_mpi = (MPI_size > 1)
        if use_mpi:
            print("MPI rank/size: %d / %d" % (MPI_rank, MPI_size), flush=True)
            pool = ptemcee.mpi_pool.MPIPool(debug=False)
            is_master = pool.is_master()
            mapper = pool.map
        else:
            print("No MPI", flush=True)
            is_master = True
            mapper = map

    # Load json file with all parameters
    with open(args.input_file, 'r') as input_file:
        input_params = json.load(input_file)
    # Source params and prior params must be given
    source_params = input_params['source_params']
    source_params = pytools.complete_mass_params(source_params)
    prior_params = input_params['prior_params']
    # Source params can be specified in the Lframe
    source_params_are_Lframe = source_params.get('Lframe', False)
    # Waveform params and run params have predefined default values
    # Need to cast from json to python, list of modes list[list] -> list[tuple]
    waveform_params = waveform_params_default.copy()
    input_params['waveform_params'] = inference.waveform_params_json2py(
                                                input_params['waveform_params'])
    waveform_params.update(input_params['waveform_params'])
    run_params = run_params_default.copy()
    run_params.update(input_params['run_params'])
    zerolike = run_params.pop('zerolike', False)
    sample_Lframe = run_params.pop('sample_Lframe', False)
    simple_likelihood = run_params.pop('simple_likelihood', False)

    # Only master will print info
    print_info = run_params['print_info'] and is_master

    # Check run params are meant to be for the ptemcee sampler
    if not (run_params['sampler'] == 'ptemcee'):
        raise ValueError('run_params sampler flag is %s instead of ptemcee.'\
                          % (run_params['sampler']))
    # run params must contain output prefix for files -- no default here
    for musthave in run_params_musthave:
        if not (musthave in run_params):
            raise ValueError('run_params must contain %s.' % (musthave))
    # Check that the output directory exists
    if (run_params['output'] or run_params['output_raw']):
        if not os.path.isdir(run_params['out_dir']):
            raise ValueError('Output dir %s does not exist.' % run_params['out_dir'])

    # If source params are given in the Lframe, convert to SSB
    if source_params_are_Lframe:
        source_params_SSBframe = lisatools.convert_Lframe_to_SSBframe(
                                    source_params,
                                    t0=waveform_params['t0'],
                                    frozenLISA=waveform_params['frozenLISA'])
        source_params_Lframe = source_params.copy()
    else:
        source_params_SSBframe = source_params.copy()
        source_params_Lframe = lisatools.convert_SSBframe_to_Lframe(
                                    source_params,
                                    t0=waveform_params['t0'],
                                    frozenLISA=waveform_params['frozenLISA'])
    # Complete mass and spin injection parameters
    source_params_SSBframe = pytools.complete_mass_params(source_params_SSBframe)
    source_params_SSBframe = pytools.complete_spin_params(source_params_SSBframe)
    source_params_Lframe = pytools.complete_mass_params(source_params_Lframe)
    source_params_Lframe = pytools.complete_spin_params(source_params_Lframe)

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

    # Parameters inferred and parameters fixed
    list_params = prior_params.get('list_params', list_params_default)
    infer_params = prior_params['infer_params']
    fixed_params = [p for p in list_params if p not in infer_params]
    n_dim = len(infer_params)
    n_fixed = len(fixed_params)
    # Vector x of infer_params for the injection
    # Also store values of fixed params in dict for later use
    if sample_Lframe:
        fixed_params_dict = dict([(p, source_params_Lframe[p]) for p in fixed_params])
        x_inj = np.array([source_params_Lframe[p] for p in infer_params])
    else:
        fixed_params_dict = dict([(p, source_params_SSBframe[p]) for p in fixed_params])
        x_inj = np.array([source_params_SSBframe[p] for p in infer_params])

    # Wrapped parameters
    wrap_params = prior_params.get('wrap_params', None)
    if wrap_params is None:
        wrap_params = inference.func_default_wrap(infer_params)
    else:
        if np.array(wrap_params).dtype == 'bool':
            raise ValueError('wrap_params in outdated format, expecting None (for default) or a list of [None or [a,b]] with [a,b] the wrap moduli, typically [-np.pi, np.pi].')
    # When using a parameter map, wrap_params is given for the mapped params
    # Length must match n_dim_ensemble, see below the part about maps

    # Ensemble proposal:
    # ~1/sqrt(z) with volume element z^(d-1) for emcee
    # ~1/z with volume element z^d for ptemcee
    ensemble_proposal = run_params['ensemble_proposal']

    # Multimodal jumps
    # TODO: support both 2-mode and 8-mode jumps
    # TODO: be more flexible when some parameters are pinned to their value
    # For now we require all ['inc', 'lambda', 'beta', 'psi'] to be
    # inferred params
    # TODO: improve the back-and-forth between vector and dict
    multimodal = run_params['multimodal']
    multimodal_pattern = run_params['multimodal_pattern']
    extra_proposal_prob = run_params['p_jump']
    extra_proposal_jump = None
    if multimodal:
        if not sample_Lframe:
            raise ValueError('The multimodal option is only supported \
                                together with sample_Lframe.')

        list_angle_params = ['inc', 'lambda', 'beta', 'psi']
        index_map_angles = {}
        for param in list_angle_params:
            if not param in infer_params:
                raise ValueError('For multimodality, infer_params must contain \
                                        [inc, phi, lambda, beta, psi]')
            index_map_angles[param] = infer_params.index(param)
        # x is (n, ndim) array with physical parameters (for n walkers)
        # returns x_jump
        def jump_extra(x, random_state=np.random):
            angle_params = {}
            for param in list_angle_params:
                angle_params[param] = x[:,index_map_angles[param]]
            skymodes = inference.proposal_skymode(size=len(x), pattern=multimodal_pattern, random_state=random_state)
            angle_params_map = inference.map_skymode(angle_params, skymodes[:,0], skymodes[:,1])
            x_jump = x.copy()
            for param in list_angle_params:
                x_jump[:,index_map_angles[param]] = angle_params_map[param]
            return x_jump
        extra_proposal_jump = jump_extra

    # Prior function (assumes independent multiplicative prior in all params)
    # prior_funcs is a list of pure lambda functions
    prior_funcs = []
    for i in range(n_dim):
        prior_funcs += [inference.def_prior_func(prior_type[i], params_range[i])]
    def prior(x):
        p = 1.
        for i in range(n_dim):
            p *= prior_funcs[i](x[i])
        return p
    # Set up prior bounds for x vector of parameters, dimension (n_dim, 2)
    prior_bounds = np.array(params_range)
    # Check the injection is within the prior bounds
    if not inference.prior_check(x_inj, prior_bounds):
        print("x_inj:")
        print(x_inj)
        print("prior_bounds:")
        print(prior_bounds)
        raise ValueError('Source parameters not within the prior bounds!')

    # Set up likelihood class
    if run_params['likelihood_method']=="simple_likelihood":
        #TODO: check if all options are right (intrinsic params pinned)
        likelihoodClass = lisa.SimpleLikelihoodLISASMBH(source_params_Lframe,
                                                        **waveform_params)
    elif run_params['likelihood_method']=="fresnel":
        likelihoodClass = lisa.LikelihoodLISASMBH(source_params_Lframe,
                                                  **waveform_params)
    elif run_params['likelihood_method']=="residuals":
        ngrid = run_params['likelihood_residuals_ngrid']
        likelihoodClass = lisa.LikelihoodLISASMBH_LinearResiduals(
                                                  source_params_Lframe,
                                                  ngrid=ngrid,
                                                  **waveform_params)
    else:
        raise ValueError('Likelihood method %s not recognized.' \
                                            % run_params['likelihood_method'])

    # Waveform params to be used for template waveforms
    # May differ from the waveform params for injection, given as an update
    waveform_params_template = copy.deepcopy(waveform_params)
    if 'waveform_params_update_for_template' in waveform_params:
        waveform_params_template.update(
                         waveform_params['waveform_params_update_for_template'])

    # Option to use a parameter map inspired from the simple 22-mode response
    # Sampling extrinsic params (see (74) in arXiv:2003.00357):
    # A_\pm exp(i Phi_\pm) = sigma^22_\pm
    # Set of params: (A_+, A_-, Phi_+ - Phi_-, Phi_+ + Phi_-, lambdaL, betaL)
    params_map = run_params['params_map']
    if params_map is None: # When not using a parameter map
        n_dim_map = n_dim
        n_dim_ensemble = n_dim
        def map_params(x):
            return x
        def invmap_params_and_jacobian(x):
            return x, 1.
        # When not using a map, prior ranges in original parameters take care of
        # checking the range
        def physical_check_map(x):
            return True
    elif params_map=='simple_response_22':
        if print_info:
            print("Using params_map: simple_response_22", flush=True)
        # Indices of extrinsic parameters, must sample_Lframe, have the full set
        if not sample_Lframe:
            raise ValueError('sample_simple22_map requires sample_Lframe=True.')
        list_params_extr = ['dist', 'inc', 'phi', 'lambda', 'beta', 'psi']
        list_params_extr_map = ['Aplus', 'Aminus', 'Phiplus', 'Phiminus', 'lambda', 'sbeta', 'indexpsi']
        map_wrap_dict = {
            'Phiplus': [-np.pi, np.pi],
            'Phiminus': [-np.pi, np.pi],
            'lambda': [-np.pi, np.pi]
            }
        indices_extr = np.zeros(6, dtype=int)
        for i,p in enumerate(list_params_extr):
            indices_extr[i] = infer_params.index(p)
        indices_intr = np.array([infer_params.index(p) for p in infer_params if not p in list_params_extr])
        # Place first 6 map params where the original extrinsic params were
        # This is arbitrary, just making sure we don't touch intrinsic params
        indices_extr_map = np.zeros(7, dtype=int)
        indices_extr_map[:6] = indices_extr
        # We require an extra discrete param, indexpsi=0,1, for the map
        # Will be placed last in extended x used for internal sampling
        # The ensemble proposal with still only use the first n_dim
        indices_extr_map[6] = n_dim
        n_dim_map = n_dim + 1
        n_dim_ensemble = n_dim
        # List of infer_params mapped
        infer_params_map = infer_params.copy()
        for i in range(6):
            infer_params_map[indices_extr[i]] = list_params_extr_map[i]
        infer_params_map += ['indexpsi']
        # We need to adjust extra_proposal to work with the mapped parameters
        if multimodal:
            list_angle_params = ['lambda', 'sbeta', 'indexpsi']
            indices_map_angles = [list_params_extr_map.index(p) for p in list_angle_params]
            def jump_extra(x, random_state=np.random):
                angle_params = {}
                for i,p in enumerate(list_angle_params):
                    angle_params[p] = x[:,indices_extr_map[indices_map_angles[i]]]
                skymodes = inference.proposal_skymode_simple22map(size=len(x), pattern=multimodal_pattern, random_state=random_state)
                angle_params_map = inference.map_skymode_simple22map(angle_params, skymodes[:,0], skymodes[:,1], skymodes[:,2])
                x_jump = x.copy()
                for i,p in enumerate(list_angle_params):
                    x_jump[:,indices_extr_map[indices_map_angles[i]]] = angle_params_map[p]
                return x_jump
            extra_proposal_jump = jump_extra
        # When using a parameter map, wrap_params is given for the mapped params
        # Length must match n_dim_ensemble
        # If None was given as input (default), set the wrap automatically
        if prior_params.get('wrap_params', None) is None:
            list_wrap_moduli = []
            for i in range(n_dim_ensemble):
                list_wrap_moduli += [map_wrap_dict.get(infer_params_map[i], None)]
            # Overriding previous default initialization when input is None
            wrap_params = list_wrap_moduli
        # Functions working with a vector x
        injdist = source_params['dist']
        # Function to check the physical range of mapped params
        def physical_check_map(x):
            params_map = {}
            for i,p in enumerate(list_params_extr_map):
                params_map[p] = x[indices_extr_map[i]]
            return inference.physical_check_simple_response_22(params_map)
        # Map from ordinary params x to mapped internal params X
        def map_params(x):
            params = {}
            for i,p in enumerate(list_params_extr):
                params[p] = x[indices_extr[i]]
            params_map = inference.map_params_simple_response_22(params, injdist)
            x_map = np.zeros(len(x)+1, dtype=float) # Add a slot for indexpsi
            x_map[indices_intr] = x[indices_intr]
            for i,p in enumerate(list_params_extr_map):
                x_map[indices_extr_map[i]] = params_map[p]
            return x_map
        # Inverse map from mapped internal params X to ordinary params x
        # Also compute jacobian J = |\partial X / \partial x|
        def invmap_params_and_jacobian(x):
            params_map = {}
            for i,p in enumerate(list_params_extr_map):
                params_map[p] = x[indices_extr_map[i]]
            params = inference.invmap_params_simple_response_22(params_map, injdist)
            jacobian = inference.jacobian_map_simple_response_22(params, params_map, injdist)
            x_invmap = np.zeros(len(x)-1, dtype=float) # Cutting the slot added for indexpsi
            x_invmap[indices_intr] = x[indices_intr]
            for i,p in enumerate(list_params_extr):
                x_invmap[indices_extr[i]] = params[p]
            return x_invmap, jacobian
    else:
        raise ValueError('params_map %s not recognized.' % params_map)

    # Define ln-likelihood and ln-prior function, wrapped for use in ptemcee
    # TODO: add m1>m2 to prior range checks
    def lnlikelihood(x):
        # Allowing to use a parameter map, like for simple22_map
        # Check physical range in the possibly mapped params
        if not physical_check_map(x):
            return -1e99
        x_invmap, jacobian_map = invmap_params_and_jacobian(x)
        # Check prior range
        if not inference.prior_check(x_invmap, prior_bounds):
            return -1e99
        # Convert to dictionary of params
        template_params = {}
        for i in range(n_dim):
            template_params[infer_params[i]] = x_invmap[i]
        for p in fixed_params:
            template_params[p] = fixed_params_dict[p]
        template_params = pytools.complete_mass_params(template_params)
        template_params = pytools.complete_spin_params(template_params)
        template_params['Lframe'] = sample_Lframe
        if zerolike: return 0.
        lnL = likelihoodClass.lnL(template_params, **waveform_params_template)
        return lnL
    def lnprior(x):
        # Allowing to use a parameter map, like for simple22_map
        # Check physical range in the possibly mapped params
        if not physical_check_map(x):
            return -1e99
        x_invmap, jacobian_map = invmap_params_and_jacobian(x)
        if not inference.prior_check(x_invmap, prior_bounds):
            return -1e99
        p = prior(x_invmap)
        if p==0.: return -1e99
        lnp = np.log(p)
        # Include effect of the (inverse) jacobian of the parameter map, if any
        lnjacobian = -np.log(np.abs(jacobian_map))
        return lnp + lnjacobian

    # Read run_params
    # p_extra = run_params['p_jump']
    init_method = run_params['init_method']
    init_scale_cov = run_params['init_scale_cov']
    n_temps = run_params['n_temps']
    temp_max = run_params['temp_max']
    adaptive_temp = run_params['adaptive_temp']
    n_walkers = run_params['n_walkers']
    n_iter = run_params['n_iter']
    burn_in = run_params['burn_in']
    autocor_method = run_params['autocor_method']
    upsample = run_params['upsample']
    seed = run_params['seed']
    n_iter_info = run_params['n_iter_info']
    n_dim = len(infer_params)

    if print_info:
        print('Source parameters SSBframe:')
        print(source_params_SSBframe)
        print('Source parameters Lframe:')
        print(source_params_Lframe)

    # Random seed for the sampling
    if seed is not None:
        np.random.seed(seed)

    # Compute Fisher matrix - not available for all waveform models
    if not run_params['skip_fisher']:
        # NOTE: might be slow if timetomerger_max is set at generic value like 1yr
        # NOTE: numerical problems in Fisher when timetomerger_max is too large
        # For Fisher only, we set timetomerger_max based on SNR=1 threshold
        waveform_params_22 = waveform_params.copy()
        waveform_params_22['modes'] = [(2,2)]
        t_SNR1_s = snrtools.lisa_tofSNR(1., source_params_SSBframe, **waveform_params_22)
        t_SNR1_yr = t_SNR1_s / pyconstants.YRSID_SI
        # Ensure at least 1d of signal for fisher regardless of SNR threshold
        t_threshold_yr = np.fmax(t_SNR1_yr, 1./365.25)
        waveform_params_fisher = waveform_params.copy()
        waveform_params_fisher['timetomerger_max'] = t_threshold_yr
        # TODO: improve handling of different choices of infer_params
        if print_info:
            print('Computing Fisher matrix...')
            print('Threshold max(t(SNR=1), 1d) used for Fisher: %g yr' % (t_threshold_yr))
        # Computing Fisher matrix and covariance
        fishercov = lisa_fisher.fisher_covariance_smbh(source_params_SSBframe,
                            steps=lisa_fisher.default_steps, freqs=['log', None],
                            list_params=infer_params, list_fixed_params=fixed_params,
                            Lframe=sample_Lframe,
                            **waveform_params_fisher)
        if print_info:
            print('Fisher covariance matrix:')
            print(fishercov['cov'])

    # Initialize walkers, drawing from the prior or from Fisher matrix
    x_ini = np.zeros((n_temps, n_walkers, n_dim))
    if init_method=='prior':
        # Drawing from the prior -- assumes independent priors in all params
        for k in range(n_temps):
            for j in range(n_dim):
                x_ini[k,:,j] = inference.draw_prior(prior_type[j], prior_bounds[j], n_walkers)
    elif init_method=='fisher':
        if run_params['skip_fisher']:
            raise ValueError('Cannot have skip_fisher and init_method=fisher.')
        # Drawing from the Fisher matrix - same for each temperature
        if sample_Lframe:
            mean = np.array([source_params_Lframe[p] for p in infer_params])
        else:
            mean = np.array([source_params_SSBframe[p] for p in infer_params])
        # We allow for the possibility of scaling the covariance for initialization
        cov = fishercov['cov'] * init_scale_cov
        try:
            for k in range(n_temps):
                for i in range(n_walkers):
                    x_ini[k,i,:] = inference.draw_multivariate_normal_constrained(
                                          mean, cov, params_range, infer_params)
        except:
            # Regularizing Fisher with a prior inverse covariance in spins
            print('Fisher initialization failed, adding regularizing prior invcov at sigma=0.5 for spins.')
            # By default, add a Gaussian prior with sigma=0.5 in both spins
            fisher_prior_invcov = np.zeros((n_dim,n_dim), dtype=float)
            if 'chi1' in infer_params:
                ichi1 = infer_params.index('chi1')
                fisher_prior_invcov[ichi1,ichi1] = 1./0.5**2
            if 'chi2' in infer_params:
                ichi2 = infer_params.index('chi2')
                fisher_prior_invcov[ichi2,ichi2] = 1./0.5**2
            fishercov_reg = lisa_fisher.fisher_covariance_smbh(source_params_SSBframe,
                                steps=lisa_fisher.default_steps, freqs=['log', None],
                                list_params=infer_params, list_fixed_params=fixed_params,
                                Lframe=sample_Lframe, prior_invcov=fisher_prior_invcov,
                                **waveform_params_fisher)
            print('Fisher covariance matrix, regularized in spins:')
            print(fishercov_reg['cov'])
            cov_reg = fishercov_reg['cov'] * init_scale_cov
            try:
                for k in range(n_temps):
                    for i in range(n_walkers):
                        x_ini[k,i,:] = inference.draw_multivariate_normal_constrained(
                                              mean, cov_reg, params_range, infer_params)
            except:
                print('Fisher initialization failed with regularization, initializing from prior.')
                # Drawing from the prior -- assumes independent priors in all params
                for k in range(n_temps):
                    for j in range(n_dim):
                        x_ini[k,:,j] = inference.draw_prior(prior_type[j], prior_bounds[j], n_walkers)
    elif init_method=='file':
        init_file = run_params['init_file']
        with h5py.File(init_file, 'r') as hf:
            # NOTE: hf['Lframe'] is expected as a dataset of just one element
            if (hf['Lframe'][0] != sample_Lframe):
                raise ValueError('sample_Lframe and Lframe in posterior loaded from file must match.')
            for j in range(n_dim):
                p = infer_params[j]
                x_ini[:,:,j] = np.reshape(hf[p][:], (n_temps, n_walkers))
    else:
        raise ValueError('Option init_method = %s not recognized.' % init_method)

    # Initial points all start on the main mode (1,0)
    # if multimodal:
    #     x_ini[:,n_dim] = 1
    #     x_ini[:,n_dim+1] = 0

    # Enforce range of phase parameters in case Fisher uncertainties are large
    # TODO: we should have proper rejection based on the prior ranges
    if 'inc' in infer_params:
        iinc = infer_params.index('inc')
        x_ini[:,:,iinc] = pytools.modpi(x_ini[:,:,iinc])
    if 'phi' in infer_params:
        iphi = infer_params.index('phi')
        x_ini[:,:,iphi] = pytools.mod2pi(x_ini[:,:,iphi])
    if 'lambda' in infer_params:
        ilambda = infer_params.index('lambda')
        x_ini[:,:,ilambda] = pytools.mod2pi(x_ini[:,:,ilambda])
    if 'beta' in infer_params:
        ibeta = infer_params.index('beta')
        x_ini[:,:,ibeta] = pytools.modpi2(x_ini[:,:,ibeta])
    if 'psi' in infer_params:
        ipsi = infer_params.index('psi')
        x_ini[:,:,ipsi] = pytools.mod2pi(x_ini[:,:,ipsi])

    # When using a parameter map, map the initial x
    x_ini_map = np.zeros((n_temps, n_walkers, n_dim_map), dtype=float)
    for i in range(n_temps):
        for j in range(n_walkers):
            x_ini_map[i,j,:] = map_params(x_ini[i,j,:])

    # Temperature ladder
    betas = ptemcee.sampler.make_ladder(n_dim, ntemps=n_temps, Tmax=temp_max)

    # If using mpi, workers are simply told to wait
    # They will be sollicited by master for likelihood computations via pool.map
    if use_mpi and (not is_master):
        pool.wait()
        # Is that exit necessary ? Was in the emcee/schwimmbad example
        # Maybe there to ensure exits if pool.close() is not called
        sys.exit(0)

    # Whether using mpi and being master or simply not using mpi
    # Sampler set-up, running, post-processing and output all done by master
    if is_master:
        # Set up and initialize sampler
        sampler = ptemcee.sampler.Sampler(n_walkers, n_dim_map,
                                          lnlikelihood, lnprior,
                                          ndim_ensemble=n_dim_ensemble,
                                          betas=betas, mapper=mapper,
                                          adaptive=adaptive_temp,
                                          extra_proposal_prob=extra_proposal_prob,
                                          extra_proposal_jump=extra_proposal_jump,
                                          ensemble_proposal=ensemble_proposal,
                                          list_param_wrap=wrap_params)
        chain = sampler.chain(x_ini_map)

        # A la grace de dieu
        if print_info:
            print('Running ptemcee...')
        chain.run(n_iter)

        # TODO: output meta information, acceptance rate and likelihood speed

        # Post-processing: unfold if multimodal was used
        if print_info:
            print('Post-processing...')

        # Only keep 0-temperature chain for post-processing
        # TODO: allow to output other temperatures, and temp. adjustments, for debug
        # ptemcee format: (niter, ntemp, nwalker, ndim)
        # We translate to multiemcee format: (nwalker, niter, ndim) for temp=0
        # NOTE: when using a map, chain.x has mapped values and dimension
        chain_unfold_map = np.transpose(chain.x[:,0,:,:], axes=(1,0,2))
        # Same format without ndim for like and post values
        lnlikevals = np.transpose(chain.logl[:,0,:], axes=(1,0))
        lnpostvals = np.transpose(chain.logP[:,0,:], axes=(1,0))
        # Format: (niter, ntemp)
        betavals = chain.betas
        # ptemcee does not seem to store individual acceptance, only their count
        acceptance_ratios = chain.jump_acceptance_ratio[0,:]

        # When using a map, do the inverse mapping for the chain's x values
        chain_unfold = np.zeros((n_walkers, n_iter, n_dim), dtype=float)
        for i in range(n_walkers):
            for j in range(n_iter):
                chain_unfold[i,j,:], _ = invmap_params_and_jacobian(chain_unfold_map[i,j,:])

        # Post-processing: burn-in, autocor. length and thinning, merge walkers
        # Also complete with params that were fixed to their values
        if burn_in>=n_iter:
            print('WARNING: burn_in is larger than n_iter, ignoring burn_in.')
            burn_in = 0
        if run_params['thin_samples']:
            autocor_len = {}
            for i,param in enumerate(infer_params):
                # Note: autocorr_new computes a mean across walkers
                autocor_len[param] = inference.get_autocor(chain_unfold[:,burn_in:,i], method=autocor_method)
                if print_info:
                    print('Autocorrelation length for %s: %g' % (param,autocor_len[param]))
            # The thinning length is the worse autocor length for all params
            thin_len = int(np.ceil(np.max([autocor_len[param] for param in infer_params])))
            thin_len = int(np.ceil(thin_len / float(upsample)))
        else:
            thin_len = 1
        if print_info:
            print('Autocorrelation thinning: %d' % (thin_len,))
        # Processed output: thinned and merged chain (completed with fixed params)
        n_out = n_walkers * ((n_iter-burn_in-1) // thin_len + 1)
        chain_processed = np.zeros((n_out, n_dim + n_fixed), dtype=float)
        # Here ravel with order='F' flattens by reading along columns first
        for i in range(n_dim):
            i_out = list_params.index(infer_params[i])
            chain_processed[:,i_out] = np.ravel(chain_unfold[:,burn_in::thin_len,i],
                                                order='F')
        for i in range(n_fixed):
            i_out = list_params.index(fixed_params[i])
            if sample_Lframe:
                chain_processed[:,i_out] = source_params_Lframe[fixed_params[i]]
            else:
                chain_processed[:,i_out] = source_params_SSBframe[fixed_params[i]]
        # Thin and merge likelihood, posterior, acceptance vals
        lnlikevals_processed = np.ravel(lnlikevals[:,burn_in::thin_len], order='F')
        lnpostvals_processed = np.ravel(lnpostvals[:,burn_in::thin_len], order='F')
        # acceptvals_processed = np.ravel(acceptvals[:,burn_in::thin_len], order='F')

        # Output
        basename = run_params['out_dir'] + run_params['out_name']
        # Main output: processed, thinned chains and Fisher matrix
        # TODO: hierarchy, create a level (group ?) samples
        if run_params['output']:
            with h5py.File(basename + '.h5', 'w') as f:
                # Source params
                source_params_Lframe_gr = f.create_group('source_params_Lframe')
                pytools.write_h5py_dict(source_params_Lframe_gr, source_params_Lframe)
                source_params_SSBframe_gr = f.create_group('source_params_SSBframe')
                pytools.write_h5py_dict(source_params_SSBframe_gr, source_params_SSBframe)
                for i,param in enumerate(list_params):
                    f.create_dataset(param, data=chain_processed[:,i])
                f.create_dataset('lnlike', data=lnlikevals_processed)
                f.create_dataset('lnpost', data=lnpostvals_processed)
                f.create_dataset('acceptance_ratios', data=acceptance_ratios)
                f.create_dataset('betas', data=betavals)
                # f.create_dataset('accept', data=acceptvals_processed)
                if not run_params['skip_fisher']:
                    fishercov_gr = f.create_group('fishercov')
                    lisa_fisher.write_h5py_fishercov(fishercov_gr, fishercov)
        # Extra output: full chains, walker-separated, for testing and diagnostics
        if run_params['output_raw']:
            with h5py.File(basename + '_raw.h5', 'w') as f:
                for i,param in enumerate(infer_params):
                    f.create_dataset(param, data=chain_unfold[:,:,i])
                f.create_dataset('lnlike', data=lnlikevals)
                f.create_dataset('lnpost', data=lnpostvals)
                # f.create_dataset('accept', data=acceptvals)

        # If using mpi, close the pool
        if use_mpi:
            pool.close()
