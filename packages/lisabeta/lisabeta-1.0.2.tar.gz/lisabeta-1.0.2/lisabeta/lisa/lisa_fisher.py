#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Python functions for Fisher matrix computations for LISA.
"""


import numpy as np
import copy

import lisabeta
import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pytools as pytools
import lisabeta.tools.pyspline as pyspline
import lisabeta.tools.pyoverlap as pyoverlap
import lisabeta.lisa.pyresponse as pyresponse
import lisabeta.lisa.pyLISAnoise as pyLISAnoise
import lisabeta.lisa.lisatools as lisatools
import lisabeta.lisa.lisa as lisa
import lisabeta.waveforms.bbh.pyIMRPhenomD as pyIMRPhenomD
import lisabeta.waveforms.bbh.pyIMRPhenomHM as pyIMRPhenomHM
import lisabeta.waveforms.bbh.pyEOBNRv2HMROM as pyEOBNRv2HMROM

default_list_fisher_params = ['M', 'q', 'chi1', 'chi2', 'Deltat', 'dist', 'inc', 'phi', 'lambda', 'beta', 'psi']

dict_params_fractional = {
    'M':True,
    'Mchirp':True,
    'm1':True,
    'm2':True,
    'q':False,
    'eta':False,
    'chi1':False,
    'chi2':False,
    'chip':False,
    'chim':False,
    'chis':False,
    'chia':False,
    'chiPN':False,
    'Deltat':False,
    'fstart':False,
    'dist':True,
    'inc':False,
    'phi':False,
    'lambda':False,
    'beta':False,
    'psi':False
}

default_steps = {
    'M':2e-8,
    'Mchirp':1e-8,
    'm1':2e-6,
    'm2':2e-6,
    'q':1e-7,
    'eta':1e-7,
    'chi1':1e-7,
    'chi2':1e-7,
    'chip':1e-7,
    'chim':1e-7,
    'chis':1e-7,
    'chia':1e-7,
    'chiPN':1e-7,
    'Deltat':1e-4,
    'fstart':1e-10,
    'dist':2e-8,
    'inc':1e-7,
    'phi':1e-7,
    'lambda':1e-7,
    'beta':1e-7,
    'psi':1e-7
}

def complete_params_dict(params):
    params_ext = params.copy()
    m1 = params['m1']
    m2 = params['m2']
    params_ext['M'] = m1 + m2
    params_ext['q'] = m1 / m2
    return params_ext

def fisher_element(params, param1, param2, step1, step2, freqs, Lframe=False, **waveform_params):
    if Lframe:
        raise ValueError('Lframe not implemented yet, sorry.')

    # Parameters
    m1 = params['m1']
    m2 = params['m2']
    M = m1 + m2
    q = m1 / m2
    params['M'] = M
    params['q'] = q

    LISAnoise = waveform_params.pop('LISAnoise', pyLISAnoise.LISAnoiseSciRDv1)
    TDI = waveform_params.get('TDI', 'TDIAET')
    TDIrescaled = waveform_params.get('TDIrescaled', True)
    LISAconst = waveform_params.get('LISAconst', pyresponse.LISAconstProposal)

    # Parameter steps
    frac1 = dict_params_fractional[param1]
    frac2 = dict_params_fractional[param2]
    params_base = params.copy()
    params_step_1 = params.copy()
    params_step_2 = params.copy()
    if frac1:
        params_step_1[param1] *= 1 + step1
    else:
        params_step_1[param1] += step1
    if frac2:
        params_step_2[param2] *= 1 + step2
    else:
        params_step_2[param2] += step2
    M1 = params_step_1['M']
    q1 = params_step_1['q']
    M2 = params_step_2['M']
    q2 = params_step_2['q']
    params_step_1['m1'] = M1 * q1 / (1+q1)
    params_step_1['m2'] = M1 * 1 / (1+q1)
    params_step_2['m1'] = M2 * q2 / (1+q2)
    params_step_2['m2'] = M2 * 1 / (1+q2)

    # Generate tdi freqseries
    tdifreqseries_base = lisa.GenerateLISATDIFreqseries_SMBH(params_base, freqs, **waveform_params)
    tdifreqseries_step_1 = lisa.GenerateLISATDIFreqseries_SMBH(params_step_1, freqs, **waveform_params)
    tdifreqseries_step_2 = lisa.GenerateLISATDIFreqseries_SMBH(params_step_2, freqs, **waveform_params)

    # Compute noises
    noise_evaluator = pyLISAnoise.initialize_noise(LISAnoise,
                                        TDI=TDI, TDIrescaled=TDIrescaled,
                                        LISAconst=LISAconst)
    Sn1_vals, Sn2_vals, Sn3_vals = pyLISAnoise.evaluate_noise(
                          LISAnoise, noise_evaluator, freqs,
                          TDI=TDI, TDIrescaled=TDIrescaled, LISAconst=LISAconst)

    # Compute derivatives d1h, d2h
    modes = tdifreqseries_base['modes']
    channels = ['chan1', 'chan2', 'chan3']
    Snvals = {}
    Snvals['chan1'] = Sn1_vals
    Snvals['chan2'] = Sn2_vals
    Snvals['chan3'] = Sn3_vals
    d1h = {}
    d2h = {}
    for chan in channels:
        d1h[chan] = np.zeros_like(freqs, dtype=complex)
        d2h[chan] = np.zeros_like(freqs, dtype=complex)
        for lm in modes:
            d1h[chan] += (tdifreqseries_step_1[lm][chan] - tdifreqseries_base[lm][chan]) / step1
            d2h[chan] += (tdifreqseries_step_2[lm][chan] - tdifreqseries_base[lm][chan]) / step2

    # Compute (d1h|d2h)
    # We do not assume that deltaf is constant
    df = np.diff(freqs)
    Fij = 0.
    for chan in channels:
        Fij += 4*np.sum(df * np.real(d1h[chan] * np.conj(d2h[chan]) / Snvals[chan])[:-1])

    return Fij

def fisher_covariance_smbh(params, freqs=None, steps=default_steps, list_params=default_list_fisher_params, list_fixed_params=[], Lframe=False, prior_invcov=None, fLow_from_22=True, **waveform_params):
    '''
    This updated version of Fisher computation:
      1. Adds options for additional mass parameter combinations
      2. Adds option for providing a "prior" inverse covariance which is added to the Fisher matrix
      3. Default is as before
    '''

    waveform_params = copy.deepcopy(waveform_params)

    # Parameters
    Npar = len(list_params)

    LISAnoise = waveform_params.get('LISAnoise', pyLISAnoise.LISAnoiseSciRDv1)
    TDI = waveform_params.get('TDI', 'TDIAET')
    TDIrescaled = waveform_params.get('TDIrescaled', True)
    LISAconst = waveform_params.get('LISAconst', pyresponse.LISAconstProposal)

    # Convert input parameters to either Lframe or SSBframe
    if not params.get('Lframe', False) and Lframe:
        params_base = lisatools.convert_SSBframe_to_Lframe(
                            params,
                            t0=waveform_params['t0'],
                            frozenLISA=waveform_params['frozenLISA'])
    elif params.get('Lframe', False) and not Lframe:
        params_base = lisatools.convert_Lframe_to_SSBframe(
                            params,
                            t0=waveform_params['t0'],
                            frozenLISA=waveform_params['frozenLISA'])
    else:
        params_base = params.copy()

    # Masses and spins
    params_base = pytools.complete_mass_params(params_base)
    params_base = pytools.complete_spin_params(params_base)
    m1 = params_base['m1']
    m2 = params_base['m2']
    M = params_base['M']
    Ms = M * pyconstants.MTSUN_SI

    channels = ['chan1', 'chan2', 'chan3']

    # Generate base waveform, with frequency bounds from waveform_params
    # e.g. scale_freq_hm might be True or False
    wftdi_base = lisa.GenerateLISATDI_SMBH(params_base, **waveform_params)

    # Read set of modes and dict of mode-by-mode freq bounds from base waveform
    modes = wftdi_base['modes']
    fLow_lm = dict([(lm,wftdi_base[lm]['freq'][0]) for lm in modes])
    fHigh_lm = dict([(lm,wftdi_base[lm]['freq'][-1]) for lm in modes])
    # Option to ignore low freqs where only 21 has support
    # This 21-specific frequency range is costly to cover with 22-based grid
    # but normally low SNR
    if fLow_from_22:
        fLow = fLow_lm[(2,2)]
    else:
        fLow = np.min([fLow_lm[lm] for lm in modes])
    fHigh = np.max([fHigh_lm[lm] for lm in modes])

    # Default frequencies (safe and slow):
    # linear spacing, adjust deltaf=1/(2T) with T approximate duration
    if freqs is None:
        freqs = ['linear', None]
    # Determine the frequencies to use for the overlaps, if not given as input
    if not isinstance(freqs, np.ndarray):

        # Format: freqs = ['log', npt], npt=None for auto setting with T
        if freqs[0]=='log':
            if freqs[1] is not None:
                nptlog = int(freqs[1])
            else:
                # Estimate length and choose deltaf according to Nyquist
                # NOTE: No safety margin, so set timetomerger_max must carefully
                T = pytools.funcNewtoniantoff(m1, m2, fLow)
                deltaf = 1./(2*T)
                nptlog = np.ceil(np.log(fHigh/fLow) / np.log(1. + deltaf/fLow))
            freqs = pytools.logspace(fLow, fHigh, nptlog)

        # Format: freqs = ['linear', deltaf], deltaf=None for auto setting with T
        if freqs[0]=='linear':
            if freqs[1] is not None:
                deltaf = freqs[1]#int(freqs[1])
            else:
                # Estimate length and choose deltaf according to Nyquist
                # NOTE: No safety margin, so set timetomerger_max must carefully
                T = pytools.funcNewtoniantoff(m1, m2, fLow)
                deltaf = 1./(2*T)
            freqs = np.arange(fLow, fHigh, deltaf)

        # Format: freqs = ['nyquist_log', pars], pars=(Deltalnf,refine)
        if freqs[0]=='nyquist_log':
            if freqs[1] is not None:
                Deltatlnf, refine = freqs[1]
            else:
                Deltatlnf, refine = 5e-5, 0
            freqs = pytools.composite_nyquist_log_freq_grid(fLow, fHigh, m1, m2, Deltalnf=Deltatlnf, refine=refine)

    # We do not assume that deltaf is constant
    df = np.diff(freqs)

    # Freq series at base point - force the use of the same gridfreq everywhere
    # gridfreq is a dictionary if hm present, a np array if not
    if modes==[(2,2)]:
        gridfreq = wftdi_base[(2,2)]['freq'].copy()
    else:
        gridfreq = dict([(lm,wftdi_base[lm]['freq'].copy()) for lm in modes])
    waveform_params['gridfreq'] = gridfreq
    # This generates the wf on the input gridfreq, fixed to be the same as base
    # and then interpolates on the large frequency array freqs
    tdifreqseries_base = lisa.GenerateLISATDIFreqseries_SMBH(params_base, freqs, **waveform_params)

    # Get pair of mass/spin params
    # Must have 2 mass, spin params in list_params + list_fixed_params together
    # When varying one param, one needs to specify which 2nd param is fixed
    list_mass_params = [p for p in list_params if p in pytools.list_mass_params]
    list_spin_params = [p for p in list_params if p in pytools.list_spin_params]
    list_fixed_mass_params = [p for p in list_fixed_params if p in pytools.list_mass_params]
    list_fixed_spin_params = [p for p in list_fixed_params if p in pytools.list_spin_params]
    list_pair_mass_params = list_mass_params + list_fixed_mass_params
    list_pair_spin_params = list_spin_params + list_fixed_spin_params
    if (not len(list_mass_params)+len(list_fixed_mass_params)==2) or (not len(list_spin_params)+len(list_fixed_spin_params)==2):
        raise ValueError('list_params + list_fixed_params must have 2 mass and spin params.')
    # The only fully degenerate pair is (q,eta)
    if list_pair_mass_params==['q', 'eta'] or list_pair_mass_params==['eta', 'q']:
        raise ValueError('Mass params pair (q,eta) is fully degenerate.')
    # Remove redundant parameters: keep only relevant pair of mass/spin params
    params_base_pair_massspin = params_base.copy()
    for p in pytools.list_mass_params:
        params_base_pair_massspin.pop(p, None)
    for p in pytools.list_spin_params:
        params_base_pair_massspin.pop(p, None)
    for p in list_pair_mass_params + list_pair_spin_params:
        params_base_pair_massspin[p] = params_base[p]

    # Compute noises
    noise_evaluator = pyLISAnoise.initialize_noise(LISAnoise,
                                        TDI=TDI, TDIrescaled=TDIrescaled,
                                        LISAconst=LISAconst)
    Sn1_vals, Sn2_vals, Sn3_vals = pyLISAnoise.evaluate_noise(
                          LISAnoise, noise_evaluator, freqs,
                          TDI=TDI, TDIrescaled=TDIrescaled, LISAconst=LISAconst)
    Snvals = {}
    Snvals['chan1'] = Sn1_vals
    Snvals['chan2'] = Sn2_vals
    Snvals['chan3'] = Sn3_vals

    # Signals shifted by parameter steps
    steps = dict(steps)
    params_step = {}
    dh = {}
    for p in list_params:
        frac = dict_params_fractional[p]
        params_step = params_base_pair_massspin.copy()
        if frac:
            params_step[p] *= 1 + steps[p]
        else:
            params_step[p] += steps[p]
        params_step = pytools.complete_mass_params(params_step)
        params_step = pytools.complete_spin_params(params_step)

        tdifreqseries_step = lisa.GenerateLISATDIFreqseries_SMBH(params_step, freqs, **waveform_params)

        # Compute signal derivatives dh/dp
        dh[p] = {}
        for chan in channels:
            dh[p][chan] = np.zeros_like(freqs, dtype=complex)
            for lm in modes:
                dh[p][chan] += (tdifreqseries_step[lm][chan] - tdifreqseries_base[lm][chan]) / steps[p]

    # Compute (d1h|d2h)
    F = np.zeros((Npar, Npar), dtype=float)
    for i in range(Npar):
        for j in range(i, Npar):
            Fij = 0.
            pi = list_params[i]
            pj = list_params[j]
            for chan in channels:
                Fij += 4*np.sum(df * np.real(dh[pi][chan] * np.conj(dh[pj][chan]) / Snvals[chan])[:-1])
            F[i,j] = Fij
            #print("Fij:",pi,pj,Fij,Fij*steps[pi]*steps[pj])

    # Symmetrize
    for i in range(Npar):
        for j in range(0, i):
            F[i,j] = F[j,i]

    # Scale back parameters with fractional steps
    scales = np.ones(len(list_params))
    for i,p in enumerate(list_params):
        if dict_params_fractional[p]:
            scales[i] = 1./params_base[p]
    scales_diag = np.diag(scales)
    scales_diag_inv = np.diag(1./scales)

    fisher = np.dot(scales_diag, np.dot(F, scales_diag))
    if prior_invcov is not None:
        F = F + np.dot(scales_diag, np.dot(prior_invcov, scales_diag))
    cov = np.dot(scales_diag_inv, np.dot(np.linalg.inv(F), scales_diag_inv))

    fisher_dict = {}
    fisher_dict['params'] = params.copy()
    fisher_dict['list_params'] = list_params
    fisher_dict['fisher'] = fisher
    fisher_dict['cov'] = cov
    fisher_dict['Lframe'] = Lframe

    return fisher_dict

def fisher_covariance_sobh(params, freqs=None, steps=default_steps, list_params=default_list_fisher_params, prior_invcov=None, Lframe=False, **waveform_params):
    '''
    This is based on fisher_covariance_smbh (as recently enhanced), but adapted for sobh signals
    '''

    waveform_params = copy.deepcopy(waveform_params)

    # Parameters
    Npar = len(list_params)
    m1 = params['m1']
    m2 = params['m2']
    M = m1 + m2
    q = m1 / m2
    params['M'] = M
    params['q'] = q
    Ms = M * pyconstants.MTSUN_SI
    #for SOBH we support Mchirp and eta params
    params['Mchirp'] = pytools.Mchirpofm1m2(m1,m2)
    params['eta']    = pytools.etaofq(q)
    chi1 = params['chi1']
    chi2 = params['chi2']
    fstart = params['fstart']
    dist = params['dist']
    #inc = params['inc']
    #phi = params['phi']
    #lambd = params['lambda']
    #beta = params['beta']
    #psi = params['psi']

    if Lframe:
        raise ValueError('Lframe not implemented (not relevant ?) for SBHBs.')

    LISAnoise = waveform_params.get('LISAnoise', pyLISAnoise.LISAnoiseSciRDv1)
    TDI = waveform_params.get('TDI', 'TDIAET')
    TDIrescaled = waveform_params.get('TDIrescaled', True)
    LISAconst = waveform_params.get('LISAconst', pyresponse.LISAconstProposal)
    minf = waveform_params.get('minf',1e-5)
    maxf = waveform_params.get('maxf',0.5)
    fend=waveform_params.get('fend',None)
    tstart=waveform_params.get('tstart',0.)
    tmin=waveform_params.get('tmin',None)
    tmax=waveform_params.get('tmax',None)
    fref_for_phiref=waveform_params.get('fref_for_phiref',None)
    phiref=waveform_params.get('phiref',0.)

    # Default frequencies (safe and slow):
    # linear spacing, adjust deltaf=1/(2T) with T approximate duration
    if freqs is None:
        freqs = ['linear', None]

    # Determine the frequencies to use for the overlaps, if not given as input
    if not isinstance(freqs, np.ndarray):

        # Determine (2,2) frequency bounds based on frequency and time limits
        fLow = np.fmax(fstart, minf)
        fHigh = maxf
        if fend is not None: fHigh = np.fmin(fHigh, fend)

        # Setting fref for time and phase
        # tref, fref_for_tref are not free, we set tf=0 (tSSB=t0) at fstart
        tref = 0.
        fref_for_tref = fstart
        # Specifying fref_for_phiref, phiref defines the source frame
        # If fref_for_phiref is None (default), use fstart
        if fref_for_phiref is None: fref_for_phiref = fstart
        # No Deltat allowed in principle, since we set the time at fstart
        Deltat = 0.

        # Take into account time cuts if specified
        # TODO: this repeats the initialization of the waveform, not optimal
        # NOTE: the cut in tmax is ignored if tmax > tpeak
        if (tmin is not None) or (tmax is not None):
            fstart_t_acc = 1e-6 # Hardcoded accuracy of f(t) function in s
            mock_gridfreq = np.array([fLow, fHigh])
            mock_wfClass = pyIMRPhenomD.IMRPhenomDh22AmpPhase(mock_gridfreq, m1, m2, chi1, chi2, dist, tref=tref, phiref=phiref, fref_for_tref=fref_for_tref, fref_for_phiref=fref_for_phiref, force_phiref_fref=False, Deltat=Deltat)
            mock_tpeak = mock_wfClass.get_tpeak()
            if tmin is not None:
                tmin_s = tmin * pyconstants.YRSID_SI
                fLow_tmin = mock_wfClass.compute_foft(tmin_s, fLow, fstart_t_acc)
                fLow = np.fmax(fLow, fLow_tmin)
            if tmax is not None:
                tmax_s = tmax * pyconstants.YRSID_SI
                if tmax_s < mock_tpeak:
                    fHigh_tmax = mock_wfClass.compute_foft(tmax_s, fHigh, fstart_t_acc)
                    fHigh = np.fmin(fHigh, fHigh_tmax)

        # Format: freqs = ['log', npt], npt=None for auto setting with T
        if freqs[0]=='log':
            if freqs[1] is not None:
                nptlog = freqs[1]
            else:
                # Estimate length and choose deltaf according to Nyquist
                # NOTE: No safety margin, so set timetomerger_max must carefully
                T = pytools.funcNewtoniantoff(m1, m2, fLow)
                deltaf = 1./(2*T)
                nptlog = np.ceil(np.log(fHigh/fLow) / np.log(1. + deltaf/fLow))
            freqs = pytools.logspace(fLow, fHigh, nptlog)

        # Format: freqs = ['linear', deltaf], deltaf=None for auto setting with T
        if freqs[0]=='linear':
            if freqs[1] is not None:
                deltaf = freqs[1]
            else:
                # Estimate length and choose deltaf according to Nyquist
                # NOTE: No safety margin, so set timetomerger_max must carefully
                T = pytools.funcNewtoniantoff(m1, m2, fLow)
                deltaf = 1./(2*T)
            freqs = np.arange(fLow, fHigh, deltaf)

    # We do not assume that deltaf is constant
    df = np.diff(freqs)

    # Base point - force the use of the same gridfreq everywhere
    params_base = params.copy()
    wftdi_base = lisa.GenerateLISATDI_SOBH(params_base, **waveform_params)
    gridfreq = wftdi_base[(2,2)]['freq'].copy()
    waveform_params['gridfreq'] = gridfreq
    tdifreqseries_base = lisa.GenerateLISATDIFreqseries_SOBH(params_base, freqs, **waveform_params)

    # Signals shifted by parameter steps
    params_step = {}
    tdifreqseries_step = {}
    for p in list_params:
        frac = dict_params_fractional[p]
        params_step = params.copy()
        if frac:
            params_step[p] *= 1 + steps[p]
        else:
            params_step[p] += steps[p]
        if 'M' in list_params:  #Assume using M/q parameters
            M_step = params_step['M']
            q_step = params_step['q']
            params_step['m1'] = M_step * q_step / (1+q_step)
            params_step['m2'] = M_step * 1 / (1+q_step)
        if 'Mchirp' in list_params: #Assume using Mchirp/eta parameters
            Mchirp_step = params_step['Mchirp']
            eta_step = params_step['eta']
            params_step['m1']=pytools.m1ofMchirpeta(Mchirp_step,eta_step)
            params_step['m2']=pytools.m2ofMchirpeta(Mchirp_step,eta_step)
        tdifreqseries_step[p] = lisa.GenerateLISATDIFreqseries_SOBH(params_step, freqs, **waveform_params)

    # Compute noises
    noise_evaluator = pyLISAnoise.initialize_noise(LISAnoise,
                                        TDI=TDI, TDIrescaled=TDIrescaled,
                                        LISAconst=LISAconst)
    Sn1_vals, Sn2_vals, Sn3_vals = pyLISAnoise.evaluate_noise(
                          LISAnoise, noise_evaluator, freqs,
                          TDI=TDI, TDIrescaled=TDIrescaled, LISAconst=LISAconst)

    # Compute derivatives dh
    modes = tdifreqseries_base['modes']  #This should only be (2,2) for SOBH
    channels = ['chan1', 'chan2', 'chan3']
    Snvals = {}
    Snvals['chan1'] = Sn1_vals
    Snvals['chan2'] = Sn2_vals
    Snvals['chan3'] = Sn3_vals
    dh = {}
    for p in list_params:
        dh[p] = {}
        for chan in channels:
            dh[p][chan] = np.zeros_like(freqs, dtype=complex)
            for lm in modes:
                dh[p][chan] += (tdifreqseries_step[p][lm][chan] - tdifreqseries_base[lm][chan]) / steps[p]

    # Compute (d1h|d2h)
    F = np.zeros((Npar, Npar), dtype=float)
    for i in range(Npar):
        for j in range(i, Npar):
            Fij = 0.
            pi = list_params[i]
            pj = list_params[j]
            for chan in channels:
                Fij += 4*np.sum(df * np.real(dh[pi][chan] * np.conj(dh[pj][chan]) / Snvals[chan])[:-1])
            F[i,j] = Fij

    # Symmetrize
    for i in range(Npar):
        for j in range(0, i):
            F[i,j] = F[j,i]

    # Scale back parameters with fractional steps
    scales = np.ones(len(list_params))
    for i,p in enumerate(list_params):
        if dict_params_fractional[p]:
            scales[i] = 1./params[p]
    scales_diag = np.diag(scales)
    scales_diag_inv = np.diag(1./scales)

    fisher = np.dot(scales_diag, np.dot(F, scales_diag))
    if prior_invcov is not None:
        F = F + np.dot(scales_diag, np.dot(prior_invcov, scales_diag))
    cov = np.dot(scales_diag_inv, np.dot(np.linalg.inv(F), scales_diag_inv))

    fisher_dict = {}
    fisher_dict['params'] = params.copy()
    fisher_dict['list_params'] = list_params
    fisher_dict['prior_invcov'] = np.copy(prior_invcov)
    fisher_dict['fisher'] = fisher
    fisher_dict['cov'] = cov
    fisher_dict['Lframe'] = Lframe

    return fisher_dict

################################################################################
# I/O utilities

# Write a fishercov dictionary to hdf5
# NOTE: complications for lists of strings (UTF8/ascii) with h5py ?
def write_h5py_fishercov(h5gr, fishercov):
    params_gr = h5gr.create_group('params')
    pytools.write_h5py_dict(params_gr, fishercov['params'])
    h5gr.create_dataset('list_params', data=np.array(fishercov['list_params'], dtype='S'))
    h5gr.create_dataset('cov', data=fishercov['cov'])
    h5gr.create_dataset('fisher', data=fishercov['fisher'])
    # Need to create a 1-element array for a single value, here boolean
    h5gr.create_dataset('Lframe', data=np.array([fishercov['Lframe']]))
    return
def read_h5py_fishercov(h5gr):
    fishercov = {}
    for k in ['cov', 'fisher']:
        fishercov[k] = h5gr[k][:]
    # Need to read a 1-element array for a single value, here boolean
    fishercov['Lframe'] = h5gr['Lframe'][:][0]
    fishercov['params'] = pytools.read_h5py_dict(h5gr['params'])

    # Need to convert strings from bytestrings to utf-8 -- is this ok ?
    fishercov['list_params'] = [s.decode('utf-8') for s in h5gr['list_params']]
    return fishercov

################################################################################
def lisa_fischer():
    print('''
    Lisa Fischer: How Can I Ease the Pain (1991)
    All alone, on my knees I pray
    For the strength to stay away
    In and out, out and in you go
    I feel your fire
    Then I lose my self control
    How can I ease the pain
    When I know your coming back again
    And how can I ease the pain in my heart
    How can I ease the pain
    Everytime that I let you in
    You take away something deep within
    A fool for love is a fool for pain
    But I refuse to love you again
    How can I ease the pain
    When I know your coming back again
    And how can I ease the pain in my heart
    How can I ease the pain
    If it's not love you've come here for
    Tell me baby why you're here?
    Knock, knock, knockin at my door
    I can't take it, no more
    No more, no more, no more baby
    Give me all or nothing at all
    How can I ease the pain
    When I know your coming back again
    And how can I ease the pain in my heart
    How can I ease the pain
    When I know your coming back again
    And how can I ease the pain in my heart
    I need to know how
    How can I, ease it
    Oo, how can I ease the pain
    I need to know baby
    Oo, how can I ease the pain
    I need to know how to ease it
    How can I ease the pain
    ''')
