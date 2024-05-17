#
# Copyright (C) 2020 Sylvain Marsat.
#
#


"""
    Python functions for multiemcee simulated inference of MBHBs with LISA.
"""


import os
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
import lisabeta.inference.multiemcee as multiemcee
import lisabeta.inference.inference as inference


################################################################################
# Parse arguments, default params

# Parse arguments
parser = argparse.ArgumentParser(description='Run SMBH parameter inference \
                                              using lisabeta and multiemcee.')
parser.add_argument('input_file', type=str, help='Input json file \
                                                  with all parameters.')
args = parser.parse_args()

# Full list of physical params - infer_params are a subset
# TODO: generalize to other choices of mass and spin parameters
# TODO: at the moment, infer_params can only be a subset of this, not flexible
list_params = [
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
    "sampler": "multiemcee",
    "sample_Lframe": True,
    "multimodal": True,
    "multimodal_pattern": "8modes",
    "p_jump": 0.5,
    "init_scale_cov": 1.,
    "zerolike": False,
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

    # Check run params are meant to be for the multiemcee sampler
    if not (run_params['sampler'] == 'multiemcee'):
        raise ValueError('run_params sampler flag is %s instead of multiemcee.'\
                          % (run_params['sampler']))
    # run params must contain output prefix for files -- no default here
    for musthave in run_params_musthave:
        if not (musthave in run_params):
            raise ValueError('run_params must contain %s.' % (musthave))
    # If n_iter=0, stop at initialization stage; then no burn-in, thinning
    if run_params['n_iter']==0:
        if (not run_params['burn_in']==0) or run_params['thin_samples']:
            raise ValueError('With n_iter=0 (stop at initialization) we cannot \
                                have burn_in or thinning.')
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

    # TODO: implement wrapped parameters
    # wrapped_params = [0] * n_dim
    # for i in range(n_dim):
    #     wrapped_params[i] = int(prior_params['wrap_params'][i])
    # run_params['wrapped_params'] = wrapped_params

    # Multimodal jumps
    # TODO: support both 2-mode and 8-mode jumps
    # TODO: be more flexible when some parameters are pinned to their value
    # For now we require all ['inc', 'lambda', 'beta', 'psi'] to be
    # inferred params
    # TODO: improve the back-and-forth between vector and dict
    multimodal = run_params['multimodal']
    multimodal_pattern = run_params['multimodal_pattern']
    dim_extra = 0
    map_extra = None
    proposal_extra = None
    if multimodal:
        if not sample_Lframe:
            raise ValueError('The multimodal option is only supported \
                                together with sample_Lframe.')
        dim_extra = 2

        list_angle_params = ['inc', 'lambda', 'beta', 'psi']
        index_map_angles = {}
        for param in list_angle_params:
            if not param in infer_params:
                raise ValueError('For multimodality, infer_params must contain \
                                        [inc, phi, lambda, beta, psi]')
            index_map_angles[param] = infer_params.index(param)
        # x is array with physical parameters + skymode indices
        # returns x_map, with physical parameters only
        def map_extra(x):
            dim = len(x) - dim_extra
            skymode_index0, skymode_index1 = x[dim:]
            angle_params = {}
            for param in list_angle_params:
                angle_params[param] = x[index_map_angles[param]]
            angle_params_map = inference.map_skymode(angle_params, skymode_index0, skymode_index1)
            x_map = np.copy(x[:dim])
            for param in list_angle_params:
                x_map[index_map_angles[param]] = angle_params_map[param]
            return x_map
        def proposal_extra(x_extra):
            return inference.proposal_skymode(pattern=multimodal_pattern) # in fact independent of skymode indices

    # Prior function (assumes independent multiplicative prior in all params)
    def prior(x):
        p = 1.
        for i in range(n_dim):
            p *= inference.compute_prior(prior_type[i], params_range[i], x[i])
        return p
    # Set up prior bounds for x vector of parameters, dimension (n_dim, 2)
    prior_bounds = np.array(params_range)
    # Check the injection is within the prior bounds
    if not inference.prior_check(x_inj, prior_bounds):
        raise ValueError('Source parameters not within the prior bounds!')

    # Waveform params to be used for template waveforms
    # May differ from the waveform params for injection, given as an update
    waveform_params_template = copy.deepcopy(waveform_params)
    if 'waveform_params_update_for_template' in waveform_params:
        waveform_params_template.update(
                         waveform_params['waveform_params_update_for_template'])

    # Set up likelihood class
    likelihoodClass = lisa.LikelihoodLISASMBH(source_params_Lframe,
                                              **waveform_params)

    # Define likelihood function, wrapped for use in multiemcee
    # TODO: add m1>m2 to prior range checks
    def lnlikelihood(x):
        if not inference.prior_check(x, prior_bounds):
            return -1e99
        template_params = {}
        for i in range(n_dim):
            template_params[infer_params[i]] = x[i]
        for p in fixed_params:
            template_params[p] = fixed_params_dict[p]
        template_params = pytools.complete_mass_params(template_params)
        template_params = pytools.complete_spin_params(template_params)
        template_params['Lframe'] = sample_Lframe
        lnL = likelihoodClass.lnL(template_params, **waveform_params_template)
        return lnL

    # Read run_params
    init_scale_cov = run_params['init_scale_cov']
    p_extra = run_params['p_jump']
    n_walkers = run_params['n_walkers']
    n_iter = run_params['n_iter']
    burn_in = run_params['burn_in']
    autocor_method = run_params['autocor_method']
    upsample = run_params['upsample']
    seed = run_params['seed']
    print_info = run_params['print_info']
    n_iter_info = run_params['n_iter_info']

    if print_info:
        print('Source parameters SSBframe:')
        print(source_params_SSBframe)
        print('Source parameters Lframe:')
        print(source_params_Lframe)

    # Compute Fisher matrix
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
    fishercov = lisa_fisher.fisher_covariance_smbh(source_params_SSBframe,
                        steps=lisa_fisher.default_steps, freqs=['log', None],
                        list_params=infer_params, list_fixed_params=fixed_params,
                        Lframe=sample_Lframe,
                        **waveform_params_fisher)

    if print_info:
        print('Fisher covariance matrix:')
        print(fishercov['cov'])

    # Initialize points drawing from the Fisher matrix
    x_ini = np.zeros((n_walkers, n_dim + dim_extra))
    if sample_Lframe:
        mean = np.array([source_params_Lframe[p] for p in infer_params])
    else:
        mean = np.array([source_params_SSBframe[p] for p in infer_params])
    # We allow for the possibility of scaling the covariance for initialization
    cov = fishercov['cov'] * init_scale_cov
    try:
        for i in range(n_walkers):
            x_ini[i,:n_dim] = inference.draw_multivariate_normal_constrained(
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
            for j in range(n_dim):
                x_ini[:,j] = inference.draw_prior(prior_type[j], prior_bounds[j], n_walkers)
    # Initial points all start on the main mode (1,0)
    if multimodal:
        x_ini[:,n_dim] = 1
        x_ini[:,n_dim+1] = 0
    # Enforce range of phase parameters in case Fisher uncertainties are large
    # TODO: we should have proper rejection based on the prior ranges
    if 'inc' in infer_params:
        iinc = infer_params.index('inc')
        x_ini[:,iinc] = pytools.modpi(x_ini[:,iinc])
    if 'phi' in infer_params:
        iphi = infer_params.index('phi')
        x_ini[:,iphi] = pytools.mod2pi(x_ini[:,iphi])
    if 'lambda' in infer_params:
        ilambda = infer_params.index('lambda')
        x_ini[:,ilambda] = pytools.mod2pi(x_ini[:,ilambda])
    if 'beta' in infer_params:
        ibeta = infer_params.index('beta')
        x_ini[:,ibeta] = pytools.modpi2(x_ini[:,ibeta])
    if 'psi' in infer_params:
        ipsi = infer_params.index('psi')
        x_ini[:,ipsi] = pytools.mod2pi(x_ini[:,ipsi])

    # A la grace de dieu
    if print_info:
        print('Running multiemcee...')
    chain, lnlikevals, lnpostvals, acceptvals = multiemcee.multiemcee_run(
        lnlikelihood, prior, n_walkers, n_iter, x_ini,
        prior_bounds=prior_bounds, dim_extra=dim_extra, p_extra=p_extra,
        map_extra=map_extra, proposal_extra=proposal_extra, seed=seed,
        print_info=print_info, n_iter_info=n_iter_info)

    # TODO: output meta information, acceptance rate and likelihood speed

    # Post-processing: unfold if multimodal was used
    if print_info:
        print('Post-processing...')
    if multimodal:
        # For niter=0, we unfold/output the initial samples
        chain_unfold_shape = (n_walkers, max(n_iter, 1), n_dim)
        chain_unfold = np.zeros(chain_unfold_shape, dtype=float)
        for k in range(n_walkers):
            chain_unfold[k] = multiemcee.unfold_chain(chain[k],
                                                      dim_extra, map_extra)
    else:
        chain_unfold = chain

    # Post-processing: burn-in, autocor. length and thinning, merge walkers
    # Also complete with params that were fixed to their values
    # Only if niter>0; if niter=0 we stop at initialization stage for testing
    thin_len = 1
    if n_iter>0:
        if burn_in>=n_iter:
            print('WARNING: burn_in is larger than n_iter, ignoring burn_in.')
            burn_in = 0
        if run_params['thin_samples']:
            autocor_len = {}
            for i,param in enumerate(infer_params):
                # Note: autocorr_new computes a mean across walkers
                autocor_len[param] = multiemcee.get_autocor(chain_unfold[:,burn_in:,i], method=autocor_method)
                if print_info:
                    print('Autocorrelation length for %s: %g' % (param,autocor_len[param]))
            # The thinning length is the worse autocor length for all params
            thin_len = int(np.ceil(np.max([autocor_len[param] for param in infer_params])))
            thin_len = int(np.ceil(thin_len / float(upsample)))
        if print_info:
            print('Autocorrelation thinning: %d' % (thin_len,))
    # Processed output: thinned and merged chain (completed with fixed params)
    if n_iter>0:
        n_out = n_walkers * ((n_iter-burn_in-1) // thin_len + 1)
    else:
        n_out = n_walkers
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
    acceptvals_processed = np.ravel(acceptvals[:,burn_in::thin_len], order='F')

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
            f.create_dataset('accept', data=acceptvals_processed)
            fishercov_gr = f.create_group('fishercov')
            lisa_fisher.write_h5py_fishercov(fishercov_gr, fishercov)
    # Extra output: full chains, walker-separated, for testing and diagnostics
    if run_params['output_raw']:
        with h5py.File(basename + '_raw.h5', 'w') as f:
            for i,param in enumerate(infer_params):
                f.create_dataset(param, data=chain[:,:,i])
            f.create_dataset('lnlike', data=lnlikevals)
            f.create_dataset('lnpost', data=lnpostvals)
            f.create_dataset('accept', data=acceptvals)
