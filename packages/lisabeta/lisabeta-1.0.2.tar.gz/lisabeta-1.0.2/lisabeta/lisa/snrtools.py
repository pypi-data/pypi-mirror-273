import os
import numpy as np
import lisabeta
import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pytools as pytools
import lisabeta.lisa.pyLISAnoise as pyLISAnoise
import lisabeta.lisa.ldcnoise as ldcnoise
import lisabeta.lisa.lisa as lisa
import lisabeta.lisa.lisatools as lisatools
from astropy.cosmology import Planck15 as cosmo


################################################################################
# Definition to randomize orientations

def draw_random_angles():
    phi = np.random.uniform(low=-np.pi, high=np.pi)
    inc = np.arccos(np.random.uniform(low=-1., high=1.))
    lambd = np.random.uniform(low=-np.pi, high=np.pi)
    beta = np.arcsin(np.random.uniform(low=-1., high=1.))
    psi = np.random.uniform(low=0., high=np.pi)
    return np.array([phi, inc, lambd, beta, psi])

################################################################################
# New interface with params, waveform_params as dictionaries
# Simple SNR wrapper
# Clunky because we might have DeltatL_cut already specified in waveform_params
# time_to_merger > 0 in s
# TODO: use time_to_merger in waveform_params
def lisa_mbhb_snr(params, time_to_merger_cut=None, **waveform_params):
    if 'DeltatL_cut' in waveform_params.keys():
        if not (time_to_merger_cut is None):
            raise ValueError('Cannot specify both time_to_merger and DeltatL_cut, possible conflict.')
        try:
            tdisignal = lisa.GenerateLISATDISignal_SMBH(params, **waveform_params)
        except lisa.SignalEmptyValueError:
            return 0.
    else:
        DeltatL_cut = None
        if not (time_to_merger_cut is None):
            DeltatL_cut = lisatools.DeltatL_cut_from_time_to_merger(time_to_merger_cut, params, **waveform_params)
        try:
            tdisignal = lisa.GenerateLISATDISignal_SMBH(params, DeltatL_cut=DeltatL_cut, **waveform_params)
        except lisa.SignalEmptyValueError:
            return 0.
    return tdisignal['SNR']

################################################################################
# New interface with params, waveform_params as dictionaries
# TODO: complete to all functions
# TODO: only 22 mode supported for now -- ok for SNR ?

def lisa_snr_AET(params, **waveform_params):

    snrcumul = lisa.CumulSNRLISATDI_SMBH(params, **waveform_params)

    return snrcumul['SNRcumul'][-1], snrcumul['SNR1cumul'][-1], snrcumul['SNR2cumul'][-1], snrcumul['SNR3cumul'][-1]

def lisa_tofSNR(SNR, params, **waveform_params):

    cumulsnr = lisa.CumulSNRLISATDI_SMBH(params, **waveform_params)

    tf = cumulsnr['tf']
    cumul_SNR = cumulsnr['SNRcumul']

    # Detectability threshold
    if not np.any(cumul_SNR > SNR):
        tthreshold = np.nan
    else:
        # Cut freq at first max of tf
        if not np.any(np.diff(tf) <= 0):
            ilast_tf = len(tf) - 1
        else:
            ilast_tf = np.where(np.logical_not(np.diff(tf) > 0))[0][0]
        last_tf = tf[ilast_tf]
        margin = 1. # Margin for representing ln(tflast - tf + margin)
        cumul_SNR = cumul_SNR[:ilast_tf]
        tf = tf[:ilast_tf]
        if np.any(np.diff(cumul_SNR) <= 0.):
            ilast_snr = np.where(np.logical_not(np.diff(cumul_SNR) > 0))[0][0]
            cumul_SNR = cumul_SNR[:ilast_snr]
            tf = tf[:ilast_snr]

        tthreshold = last_tf - pytools.spline(cumul_SNR, tf)(SNR) + margin

    return tthreshold

def lisa_SNRoft(times, params, **waveform_params):

    cumulsnr = lisa.CumulSNRLISATDI_SMBH(params, **waveform_params)

    tf = cumulsnr['tf']
    cumul_SNR = cumulsnr['SNRcumul']

    # Cut freq at first max of tf
    if not np.any(np.diff(tf) <= 0):
        ilast_tf = len(tf) - 1
    else:
        ilast_tf = np.where(np.logical_not(np.diff(tf) > 0))[0][0]
    last_tf = tf[ilast_tf]

    SNRoft_spline = pytools.spline(tf[:ilast_tf], cumul_SNR[:ilast_tf])

    return SNRoft_spline(times)

################################################################################
# Old interface, parameters passed individually and using redshift

def LISASNRAET(M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, t0=0., tobs=2., minf=1e-5, maxf=1., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst="Proposal"):
    zval = z
    Mval = M
    qval = q

    # Masses
    m1 = Mval*qval/(1.+qval)
    m2 = Mval*1/(1.+qval)

    dist = cosmo.luminosity_distance(zval).value

    params = {}
    params['m1'] = m1
    params['m2'] = m2
    params['chi1'] = chi1
    params['chi2'] = chi2
    params['Deltat'] = 0.
    params['dist'] = dist
    params['inc'] = inc
    params['phi'] = phi
    params['lambda'] = lambd
    params['beta'] = beta
    params['psi'] = psi

    waveform_params = {}
    waveform_params['t0'] = t0
    waveform_params['timetomerger_max'] = tobs
    waveform_params['minf'] = minf
    waveform_params['maxf'] = maxf
    waveform_params['LISAnoise'] = LISAnoise
    waveform_params['LISAconst'] = LISAconst

    snrcumul = lisa.CumulSNRLISATDI_SMBH(params, **waveform_params)

    return snrcumul['SNRcumul'][-1], snrcumul['SNR1cumul'][-1], snrcumul['SNR2cumul'][-1], snrcumul['SNR3cumul'][-1]

def LISAtimetomergerofSNR(SNR, M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, t0=0., tobs=2., minf=1e-5, maxf=1., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst='Proposal'):
    zval = z
    Mval = M
    qval = q

    # Masses
    m1 = Mval*qval/(1.+qval)
    m2 = Mval*1/(1.+qval)

    dist = cosmo.luminosity_distance(zval).value

    params = {}
    params['m1'] = m1
    params['m2'] = m2
    params['chi1'] = chi1
    params['chi2'] = chi2
    params['Deltat'] = 0.
    params['dist'] = dist
    params['inc'] = inc
    params['phi'] = phi
    params['lambda'] = lambd
    params['beta'] = beta
    params['psi'] = psi

    waveform_params = {}
    waveform_params['t0'] = t0
    waveform_params['timetomerger_max'] = tobs
    waveform_params['minf'] = minf
    waveform_params['maxf'] = maxf
    waveform_params['LISAnoise'] = LISAnoise
    waveform_params['LISAconst'] = LISAconst

    cumulsnr = lisa.CumulSNRLISATDI_SMBH(params, **waveform_params)

    tf = cumulsnr['tf']
    cumul_SNR = cumulsnr['SNRcumul']

    # Detectability threshold
    if not np.any(cumul_SNR > SNR):
        tthreshold = np.nan
    else:
        # Cut freq at first max of tf
        if not np.any(np.diff(tf) <= 0):
            ilast_tf = len(tf) - 1
        else:
            ilast_tf = np.where(np.logical_not(np.diff(tf) > 0))[0][0]
        last_tf = tf[ilast_tf]
        margin = 1. # Margin for representing ln(tflast - tf + margin)
        cumul_SNR = cumul_SNR[:ilast_tf]
        tf = tf[:ilast_tf]
        if np.any(np.diff(cumul_SNR) <= 0.):
            ilast_snr = np.where(np.logical_not(np.diff(cumul_SNR) > 0))[0][0]
            cumul_SNR = cumul_SNR[:ilast_snr]
            tf = tf[:ilast_snr]

        tthreshold = last_tf - pytools.spline(cumul_SNR, tf)(SNR) + margin

    return tthreshold

def LISASNRoftimetomerger(times, M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, t0=0., tobs=2., minf=1e-5, maxf=1., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst="Proposal"):
    zval = z
    Mval = M
    qval = q

    # Masses
    m1 = Mval*qval/(1.+qval)
    m2 = Mval*1/(1.+qval)

    dist = cosmo.luminosity_distance(zval).value

    params = {}
    params['m1'] = m1
    params['m2'] = m2
    params['chi1'] = chi1
    params['chi2'] = chi2
    params['Deltat'] = 0.
    params['dist'] = dist
    params['inc'] = inc
    params['phi'] = phi
    params['lambda'] = lambd
    params['beta'] = beta
    params['psi'] = psi

    waveform_params = {}
    waveform_params['t0'] = t0
    waveform_params['timetomerger_max'] = tobs
    waveform_params['minf'] = minf
    waveform_params['maxf'] = maxf
    waveform_params['LISAnoise'] = LISAnoise
    waveform_params['LISAconst'] = LISAconst

    cumulsnr = lisa.CumulSNRLISATDI_SMBH(params, **waveform_params)

    tf = cumulsnr['tf']
    cumul_SNR = cumulsnr['SNRcumul']

    # Cut freq at first max of tf
    if not np.any(np.diff(tf) <= 0):
        ilast_tf = len(tf) - 1
    else:
        ilast_tf = np.where(np.logical_not(np.diff(tf) > 0))[0][0]
    last_tf = tf[ilast_tf]

    SNRoft_spline = pytools.spline(tf[:ilast_tf], cumul_SNR[:ilast_tf])

    return SNRoft_spline(times)

def LISASNR_average_angles(M, q, chi1, chi2, z, N=1000, tobs=5., minf=1e-5, maxf=1., t0=0., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst="Proposal", ignore_nan=True, return_std=False, channel='all'):
    SNR_arr = np.zeros(N)
    for i in range(N):
        phi, inc, lambd, beta, psi = draw_random_angles()
        if t0=='av':
            t0val = np.random.uniform(low=0., high=1.)
        else:
            t0val = t0
        SNRAET = LISASNRAET(M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, tobs=tobs, minf=minf, maxf=maxf, t0=t0val, LISAnoise=LISAnoise, LISAconst=LISAconst)
        chan = {'all':0, 'A':1, 'E':2, 'T':3}.get(channel)
        SNR_arr[i] = SNRAET[chan]
    SNR_av = np.mean(SNR_arr)
    SNR_std = np.std(SNR_arr)
    if not return_std:
        return SNR_av
    else:
        return SNR_av, SNR_std

def LISASNR_average_angles_spin(M, q, z, N=1000, tobs=5., minf=1e-5, maxf=1., t0=0., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst="Proposal", ignore_nan=True, return_std=False, channel='all'):
    SNR_arr = np.zeros(N)
    for i in range(N):
        phi, inc, lambd, beta, psi = draw_random_angles()
        chi1 = np.random.uniform(low=-1., high=1.)
        chi2 = np.random.uniform(low=-1., high=1.)
        if t0=='av':
            t0val = np.random.uniform(low=0., high=1.)
        else:
            t0val = t0
        SNRAET = LISASNRAET(M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, tobs=tobs, minf=minf, maxf=maxf, t0=t0val, LISAnoise=LISAnoise, LISAconst=LISAconst)
        chan = {'all':0, 'A':1, 'E':2, 'T':3}.get(channel)
        SNR_arr[i] = SNRAET[chan]
    SNR_av = np.mean(SNR_arr)
    SNR_std = np.std(SNR_arr)
    if not return_std:
        return SNR_av
    else:
        return SNR_av, SNR_std

def LISAtimetomergerofSNR_average_angles(SNR, M, q, chi1, chi2, z, N=1000, tobs=5., minf=1e-5, maxf=1., t0=0., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst="Proposal", ignore_nan=True, return_std=False):
    tSNR_arr = np.zeros(N)
    for i in range(N):
        phi, inc, lambd, beta, psi = draw_random_angles()
        if t0=='av':
            t0val = np.random.uniform(low=0., high=1.)
        else:
            t0val = t0
        tSNR_arr[i] = LISAtimetomergerofSNR(SNR, M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, tobs=tobs, minf=minf, maxf=maxf, t0=t0val, LISAnoise=LISAnoise, LISAconst=LISAconst)
    if ignore_nan:
        mask = np.logical_not(np.isnan(tSNR_arr))
        tSNR_arr = tSNR_arr[mask]
        if len(tSNR_arr)==0:
            if not return_std:
                return np.nan
            else:
                return np.nan, np.nan
    tSNR_av = np.mean(tSNR_arr)
    tSNR_std = np.std(tSNR_arr)
    if not return_std:
        return tSNR_av
    else:
        return tSNR_av, tSNR_std

def LISAtimetomergerofSNR_average_angles_spin(SNR, M, q, z, N=1000, tobs=5., minf=1e-5, maxf=1., t0=0., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst="Proposal", ignore_nan=True, return_std=False):
    tSNR_arr = np.zeros(N)
    for i in range(N):
        phi, inc, lambd, beta, psi = draw_random_angles()
        chi1 = np.random.uniform(low=-1., high=1.)
        chi2 = np.random.uniform(low=-1., high=1.)
        if t0=='av':
            t0val = np.random.uniform(low=0., high=1.)
        else:
            t0val = t0
        tSNR_arr[i] = LISAtimetomergerofSNR(SNR, M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, tobs=tobs, minf=minf, maxf=maxf, t0=t0val, LISAnoise=LISAnoise, LISAconst=LISAconst)
    if ignore_nan:
        mask = np.logical_not(np.isnan(tSNR_arr))
        tSNR_arr = tSNR_arr[mask]
        if len(tSNR_arr)==0:
            if not return_std:
                return np.nan
            else:
                return np.nan, np.nan
    tSNR_av = np.mean(tSNR_arr)
    tSNR_std = np.std(tSNR_arr)
    if not return_std:
        return tSNR_av
    else:
        return tSNR_av, tSNR_std

# For Fig 3 of FOM Astro document
def LISASNRoftimetomerger_average_angles_spin_invq(times, M, z, qrange=[1,10], N=1000, tobs=5., minf=1e-5, maxf=1., t0=0., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst='Proposal'):
    SNRt_arr = np.zeros((len(times), N+1))
    SNRt_arr[:,0] = times
    for j in range(N):
        phi, inc, lambd, beta, psi = draw_random_angles()
        chi1 = np.random.uniform(low=-1., high=1.)
        chi2 = np.random.uniform(low=-1., high=1.)
        invq = np.random.uniform(low=1./qrange[1], high=1./qrange[0])
        q = 1./invq
        if t0=='av':
            t0val = np.random.uniform(low=0., high=1.)
        else:
            t0val = t0
        SNRt_arr[:,1+j] = LISASNRoftimetomerger(times, M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, tobs=tobs, minf=minf, maxf=maxf, t0=t0val, LISAnoise=LISAnoise, LISAconst=LISAconst)
    return SNRt_arr

def LISASNRoftimetomerger_average_angles(times, M, q, chi1, chi2, z, N=1000, tobs=5., minf=1e-5, maxf=1., t0=0., LISAnoise=pyLISAnoise.LISAnoiseSciRDv1, LISAconst='Proposal'):
    SNRt_arr = np.zeros((len(times), N+1))
    SNRt_arr[:,0] = times
    for j in range(N):
        phi, inc, lambd, beta, psi = draw_random_angles()
        if t0=='av':
            t0val = np.random.uniform(low=0., high=1.)
        else:
            t0val = t0
        SNRt_arr[:,1+j] = LISASNRoftimetomerger(times, M, q, chi1, chi2, z, phi, inc, lambd, beta, psi, tobs=tobs, minf=minf, maxf=maxf, t0=t0val, LISAnoise=LISAnoise, LISAconst=LISAconst)
    return SNRt_arr
