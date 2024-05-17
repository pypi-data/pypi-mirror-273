#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython wrapping of C generic waveforms tools, python tools.
"""


import numpy as np
cimport numpy as np

import h5py

import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pyspline as pyspline
from lisabeta.pyconstants cimport *
from lisabeta.struct.pystruct cimport *

from scipy.interpolate import InterpolatedUnivariateSpline as spline

################################################################################
# Functions to manipulate physical parameters
################################################################################

# List of mass and spin parameters
list_mass_params = ['m1', 'm2', 'M', 'q', 'Mchirp', 'eta']
list_spin_params = ['chi1', 'chi2', 'chip', 'chim', 'chis', 'chia', 'chiPN']

# Physical check on inntrinsic params
def check_physical_params(params):
    return np.all(np.array([
        params['m1'] > 0.,
        params['m2'] > 0.,
        params['M'] > 0.,
        params['q'] >= 1.,
        params['Mchirp'] > 0.,
        params['eta'] > 0.,
        params['eta'] <= 0.25,
        params['m1'] >= params['m2'],
        params['chi1'] >= -1.,
        params['chi1'] <= 1.,
        params['chi2'] >= -1.,
        params['chi2'] <= 1.,
        params['chip'] >= -1.,
        params['chip'] <= 1.,
        params['chim'] >= -1.,
        params['chim'] <= 1.,
        params['chis'] >= -1.,
        params['chis'] <= 1.,
        params['chia'] >= -1.,
        params['chia'] <= 1.,
        params['chiPN'] >= -1.,
        params['chiPN'] <= 1.,
    ]))

# Conversion between  mass ratio and symmetric mass ratio
def qofeta(eta):
    return (1.0 + np.sqrt(1.0 - 4.0*eta) - 2.0*eta) / (2.0*eta)
def etaofq(q):
    return q/(1.0 + q)**2
# Mass difference delta = (m1-m2) / (m1+m2)
def deltaofq(q):
    return (q-1.) / (q+1.)

# Conversion between mass parameters
def Mchirpofm1m2(m1, m2):
    return (m1*m2)**(3./5) / (m1+m2)**(1./5)
def etaofm1m2(m1, m2):
    return (m1*m2)/(m1+m2)**2.
def m1ofMchirpeta(Mchirp, eta):
    M = Mchirp * np.power(eta, -3./5)
    delta = np.sqrt(1 - 4*eta)
    return M * (1+delta)/2.
def m2ofMchirpeta(Mchirp, eta):
    M = Mchirp * np.power(eta, -3./5)
    delta = np.sqrt(1 - 4*eta)
    return M * (1-delta)/2.
def Mofm1m2(m1, m2):
    return m1 + m2
def qofm1m2(m1, m2):
    return m1/m2
def m1ofMq(M, q):
    return M * q/(1 + q)
def m2ofMq(M, q):
    return M * 1/(1 + q)
def MofMchirpeta(Mchirp, eta):
    return Mchirp * np.power(eta, -3./5)
def qofMchirpeta(Mchirp, eta):
    return qofeta(eta)
def MchirpofMq(M, q):
    eta = etaofq(q)
    return M * np.power(eta, 3./5)
def etaofMq(M, q):
    return etaofq(q)

# Conversion between spin parameters
def chisofchi1chi2(chi1, chi2):
    return (chi1 + chi2) / 2.
def chiaofchi1chi2(chi1, chi2):
    return (chi1 - chi2) / 2.
def chi1ofchischia(chis, chia):
    return chis + chia
def chi2ofchischia(chis, chia):
    return chis - chia
def chipofchi1chi2(chi1, chi2, q):
    return q / (1.+q) * chi1 + 1 / (1.+q) * chi2
def chimofchi1chi2(chi1, chi2, q):
    return q / (1.+q) * chi1 - 1 / (1.+q) * chi2
def chi1ofchipchim(chip, chim, q):
    return (1.+q) / (2*q) * (chip + chim)
def chi2ofchipchim(chip, chim, q):
    return (1.+q) / (2) * (chip - chim)
def chipofchischia(chis, chia, q):
    return chis + (q-1) / (1.+q) * chia
def chimofchischia(chis, chia, q):
    return chia + (q-1) / (1.+q) * chis
def chisofchipchim(chip, chim, q):
    return (1+q)**2/(4.*q) * (chip - (q-1) / (1.+q) * chim)
def chiaofchipchim(chip, chim, q):
    return (1+q)**2/(4.*q) * (chim - (q-1) / (1.+q) * chip)
def chiPNofchi1chi2(chi1, chi2, q):
    return 1./113 * etaofq(q) * ((113*q + 75.)*chi1 + (113/q + 75.)*chi2)
def chiPNofchipchim(chip, chim, q):
    return 1./113 * (94*chip + (q-1.)/(q+1.)*19*chim)
def chiPNofchischia(chis, chia, q):
    return 1./113 * etaofq(q) * ((113*q + 113/q + 150.)*chis + (113*q - 113/q)*chia)
def chipofchiPNchim(chiPN, chim, q):
    return 1./94 * (113*chiPN - (q-1.)/(q+1.)*19*chim)

# Complete mass parameters: from any set (m1,m2), (M,q), (Mchirp, eta), (Mchirp, q)
# compute the other two if not yet present
# p can be a posterior or a single set of source params
def complete_mass_params(p_in):
    p = dict(p_in)
    if ('m1' in p.keys() and 'm2' in p.keys()):
        if not 'Mchirp' in p.keys():
            p['Mchirp'] = Mchirpofm1m2(p['m1'], p['m2'])
        if not 'eta' in p.keys():
            p['eta'] = etaofm1m2(p['m1'], p['m2'])
        if not 'M' in p.keys():
            p['M'] = Mofm1m2(p['m1'], p['m2'])
        if not 'q' in p.keys():
            p['q'] = qofm1m2(p['m1'], p['m2'])
    elif ('Mchirp' in p.keys() and 'eta' in p.keys()):
        if not 'm1' in p.keys():
            p['m1'] = m1ofMchirpeta(p['Mchirp'], p['eta'])
        if not 'm2' in p.keys():
            p['m2'] = m2ofMchirpeta(p['Mchirp'], p['eta'])
        if not 'M' in p.keys():
            p['M'] = MofMchirpeta(p['Mchirp'], p['eta'])
        if not 'q' in p.keys():
            p['q'] = qofMchirpeta(p['Mchirp'], p['eta'])
    elif ('M' in p.keys() and 'q' in p.keys()):
        if not 'm1' in p.keys():
            p['m1'] = m1ofMq(p['M'], p['q'])
        if not 'm2' in p.keys():
            p['m2'] = m2ofMq(p['M'], p['q'])
        if not 'Mchirp' in p.keys():
            p['Mchirp'] = MchirpofMq(p['M'], p['q'])
        if not 'eta' in p.keys():
            p['eta'] = etaofMq(p['M'], p['q'])
    elif ('Mchirp' in p.keys() and 'q' in p.keys()):
        eta = etaofq(p['q'])
        if not 'm1' in p.keys():
            p['m1'] = m1ofMchirpeta(p['Mchirp'], eta)
        if not 'm2' in p.keys():
            p['m2'] = m2ofMchirpeta(p['Mchirp'], eta)
        if not 'M' in p.keys():
            p['M'] = MofMchirpeta(p['Mchirp'], eta)
        if not 'eta' in p.keys():
            p['eta'] = eta
    else:
        raise ValueError('Incomplete mass parameters.')
    return p
# Complete spin parameters: from any set (chi1, chi2), (chis, chia), (chip, chim)
# compute the other two if not yet present
# p can be a posterior or a single set of source params
# Assumes input has mass parameters for chip, chim
def complete_spin_params(p_in):
    p = dict(p_in)
    if ('chi1' in p.keys() and 'chi2' in p.keys()):
        if not ('chis' in p.keys() and 'chia' in p.keys()):
            p['chis'] = chisofchi1chi2(p['chi1'], p['chi2'])
            p['chia'] = chiaofchi1chi2(p['chi1'], p['chi2'])
        if not ('chip' in p.keys() and 'chim' in p.keys()):
            p['chip'] = chipofchi1chi2(p['chi1'], p['chi2'], p['q'])
            p['chim'] = chimofchi1chi2(p['chi1'], p['chi2'], p['q'])
        if not 'chiPN' in p.keys():
            p['chiPN'] = chiPNofchi1chi2(p['chi1'], p['chi2'], p['q'])
    elif ('chis' in p.keys() and 'chia' in p.keys()):
        if not ('chi1' in p.keys() and 'chi2' in p.keys()):
            p['chi1'] = chi1ofchischia(p['chis'], p['chia'])
            p['chi2'] = chi2ofchischia(p['chis'], p['chia'])
        if not ('chip' in p.keys() and 'chim' in p.keys()):
            p['chip'] = chipofchischia(p['chis'], p['chia'], p['q'])
            p['chim'] = chimofchischia(p['chis'], p['chia'], p['q'])
        if not 'chiPN' in p.keys():
            p['chiPN'] = chiPNofchischia(p['chis'], p['chia'], p['q'])
    elif ('chip' in p.keys() and 'chim' in p.keys()):
        if not ('chi1' in p.keys() and 'chi2' in p.keys()):
            p['chi1'] = chi1ofchipchim(p['chip'], p['chim'], p['q'])
            p['chi2'] = chi2ofchipchim(p['chip'], p['chim'], p['q'])
        if not ('chis' in p.keys() and 'chia' in p.keys()):
            p['chis'] = chisofchipchim(p['chip'], p['chim'], p['q'])
            p['chia'] = chiaofchipchim(p['chip'], p['chim'], p['q'])
        if not 'chiPN' in p.keys():
            p['chiPN'] = chiPNofchipchim(p['chip'], p['chim'], p['q'])
    elif ('chiPN' in p.keys() and 'chim' in p.keys()):
        p['chip'] = chipofchiPNchim(p['chiPN'], p['chim'], p['q'])
        if not ('chi1' in p.keys() and 'chi2' in p.keys()):
            p['chi1'] = chi1ofchipchim(p['chip'], p['chim'], p['q'])
            p['chi2'] = chi2ofchipchim(p['chip'], p['chim'], p['q'])
        if not ('chis' in p.keys() and 'chia' in p.keys()):
            p['chis'] = chisofchipchim(p['chip'], p['chim'], p['q'])
            p['chia'] = chiaofchipchim(p['chip'], p['chim'], p['q'])
    else:
        raise ValueError('Incomplete spin parameters.')
    return p
# Complete AGN params from the set of params used in PE
def complete_AGN_params(p_in):
    p = dict(p_in)
    R_AGN_s = np.sqrt(p['Rcostheta_AGN']**2 + p['Rsintheta_AGN']**2)
    M_AGN_s = p['Omega_AGN']**2 * R_AGN_s**3
    p['M_AGN'] = M_AGN_s / pyconstants.MTSUN_SI
    p['R_AGN'] = R_AGN_s / M_AGN_s
    p['theta_AGN'] = np.arctan2(p['Rsintheta_AGN'], p['Rcostheta_AGN'])
    return p

# Newtonian estimate of the relation Mf(deltat/M) (for the 22 mode) - gives the starting geometric frequency for a given mass ratio and a given geometric duration of the observations
def funcNewtonianfoftGeom(q, deltat):
    nu = q/(1. + q)/(1. + q)
    return 1./np.pi*(256*nu/5.*deltat)**(-3./8)
# Newtonian estimate of the relation f(deltat) (for the 22 mode) - gives the starting geometric frequency for a given mass ratio and a given geometric duration of the observations-output in Hz -- m1,m2,t in solar masses and s
def funcNewtonianfoft(m1, m2, deltat):
    mtot = m1 + m2
    q = m1/m2
    return funcNewtonianfoftGeom(q, deltat/(mtot * pyconstants.MTSUN_SI))/(mtot * pyconstants.MTSUN_SI)
# Newtonian estimate of the relation deltat/M(Mf) (for the 22 mode) - gives the time to merger from a given starting geometric frequency for a given mass ratio
def funcNewtoniantoffGeom(q, f):
    nu = q/(1. + q)/(1. + q)
    return 5./256/nu*(np.pi*f)**(-8./3)
# Newtonian estimate of the relation deltat(f) (for the 22 mode) - gives the time to merger from a given starting  frequency for a given mass ratio - output in s -- m1,m2,f in solar masses and Hz
def funcNewtoniantoff(m1, m2, f):
    mtot = m1 + m2
    q = m1/m2
    return funcNewtoniantoffGeom(q, (mtot * pyconstants.MTSUN_SI)*f)*(mtot * pyconstants.MTSUN_SI)

################################################################################
# Various utilities
################################################################################

# Logarithmic sampling
def logspace(start, stop, nb):
    ratio = (stop/start)**(1./(nb-1))
    vals = start * np.power(ratio, np.arange(nb))
    # Eliminate rounding errors at extremities
    vals[0] = start
    vals[-1] = stop
    return vals
# Sqrt sampling
def sqrtspace(start, stop, nb):
    sqrtvals = np.linspace(np.sqrt(start), np.sqrt(stop), nb)
    vals = np.power(sqrtvals, 2)
    # Eliminate rounding errors at extremities
    vals[0] = start
    vals[-1] = stop
    return vals

# mod functions for angles
# Mod 2pi - shifted to return a result in [-pi, pi[
def mod2pi(x):
    rem = np.remainder(x, 2*np.pi)
    if isinstance(x, np.ndarray) and x.shape is not ():
        mask = (rem>np.pi)
        rem[mask] -= 2*np.pi
    else:
        if rem>np.pi:
            rem -= 2*np.pi
    return rem
# Mod pi
def modpi(x):
    return np.remainder(x, np.pi)
# Mod pi, result in ]-pi/2, pi/2]
def modpi2(x):
    return np.pi/2 - np.remainder(np.pi/2 - x, np.pi)
# Mod with generic modulus, result symmetric around 0
def modsym(x, a):
    rem = np.remainder(x, a)
    if isinstance(x, np.ndarray) and x.shape is not ():
        mask = (rem>a/2.)
        rem[mask] -= a
    else:
        if rem>np.pi:
            rem -= a
    return rem
def mod_interval(x, interval=None):
    """
    Remainder of x (can be a vector) on an interval ]a,b]
    Args:
      x          # Input data, can be a vector (no check)
    Kwargs:
      interval   # Target interval, list [a,b] for mod in ]a,b]
                   (default None, ignore)
    """
    if interval is None:
        return x
    else:
        a, b = interval
        return b - np.remainder(b-x, b-a)

# Fold a list : get n elements by cycling through the list
def fold_list(xlist, n):
    l = len(xlist)
    return (xlist * (n//l + 1))[:n]

# Restrict data to an interval according to first column
# If data[:,0]=x and interval=[a,b], selects data such that a<=x<=b
# Typically results in data being entirely inside interval
def restrict_data(data, interval):
    if not interval: # test if interval==[]
        return data
    else:
        # Make an initial guess based on global length - then adjust starting and ending indices
        x = data[:,0]
        n = len(data)
        deltax = (x[-1] - x[0]) / n
        if interval[0] < x[0]:
            ibeg = 0
        else:
            ibeg = min(int((interval[0]-x[0]) / deltax), n-1)
            while ibeg < n and x[ibeg] < interval[0]:
                ibeg += 1
            while ibeg > 0 and x[ibeg-1] > interval[0]:
                ibeg -= 1
        if interval[-1] > x[-1]:
            iend = n-1
        else:
            iend = n-1 - min(int((x[-1] - interval[-1]) / deltax), n-1)
            while iend > 0 and x[iend] > interval[-1]:
                iend -= 1
            while iend < n-1 and x[iend+1] < interval[-1]:
                iend += 1
        return data[ibeg:iend+1]
# Restrict data to an interval according to first column
# If data[:,0]=x and interval=[a,b], selects data from the last point such that x<=a to the first point such that b<=x
# Typically results in interval being entirely covered by data
def restrict_data_soft(data, interval):
    if not interval: # test if interval==[]
        return data
    else:
        # Make an initial guess based on global length - then adjust starting and ending indices
        x = data[:,0]
        n = len(data)
        deltax = (x[-1] - x[0]) / n
        if interval[0] < x[0]:
            ibeg = 0
        else:
            ibeg = min(int((interval[0]-x[0]) / deltax), n-1)
            while ibeg < n-1 and x[ibeg+1] <= interval[0]:
                ibeg += 1
            while ibeg > 0 and x[ibeg] > interval[0]:
                ibeg -= 1
        if interval[-1] > x[-1]:
            iend = n-1
        else:
            iend = n-1 - min(int((x[-1] - interval[-1]) / deltax), n-1)
            while iend > 0 and x[iend-1] >= interval[-1]:
                iend -= 1
            while iend < n-1 and x[iend+1] < interval[-1]:
                iend += 1
        return data[ibeg:iend+1]
# Trim zeros from a waveform according to chosen columns
def trim_zeros_bycol(data, cols, ifallzero_returnvoid=False):
    ilastnonzero = len(data)-1
    while (ilastnonzero>=0) and all([data[ilastnonzero, i]==0. for i in cols]):
        ilastnonzero -= 1
    ifirstnonzero = 0
    while (ifirstnonzero<=len(data)-1) and all([data[ifirstnonzero, i]==0. for i in cols]):
        ifirstnonzero += 1
    if ifirstnonzero>ilastnonzero and not ifallzero_returnvoid: # if everything is zero, do nothing
        return data
    else:
        return data[ifirstnonzero:ilastnonzero+1]
# Restrict data according to given column
# if x=data[:,col], return data such that interval[0]<=x<=interval[1]
def restrict_data_bycol(data, interval, col=0):
    if not interval: # test if interval==[]
        return data
    else:
        x = data[:,col]
        mask = np.logical_and(interval[0]<=x, x<=interval[1])
        return data[mask]

################################################################################
# Utilities for FFT/IFFT
################################################################################

# Definitions for the windowing function -- function for vectorial argument
# In order to avoid overflows in the exponentials, we set the boundaries (di, df) so that anything below 10^-20 is considered zero
def window_planck_vec(x, xi, xf, deltaxi, deltaxf):
    di = deltaxi/(20*np.log(10))
    df = deltaxf/(20*np.log(10))
    w = np.zeros(len(x), dtype=float)
    #
    mask = np.logical_or(x <= xi + di, x >= xf - df)
    w[mask] = 0.
    #
    mask = np.logical_and(xi + di < x, x < xi + deltaxi - di)
    xm = x[mask]
    w[mask] = 1./(1 + np.exp(deltaxi/(xm - xi) + deltaxi/(xm - (xi + deltaxi))))
    #
    mask = np.logical_and(xi + deltaxi - di <= x, x <= xf - deltaxf + df)
    w[mask] = 1.
    #
    mask = np.logical_and(xf - deltaxf + df < x, x < xf - df)
    xm = x[mask]
    w[mask] = 1./(1 + np.exp(-(deltaxf/(xm - (xf - deltaxf))) - deltaxf/(xm - xf)))
    #
    return w

# The FFT function - accepts real or complex (real+real) input, discards negative frequencies
# Fourier convention: Ftilde(f) = \int dt exp(+2 i pi f t) * F(t)
def fft_positivef(timeseries):
    n = len(timeseries)
    ncol = timeseries.shape[1] - 1
    deltat = timeseries[1,0] - timeseries[0,0]
    deltaf = 1./(n*deltat)
    # Fast Fourier Transform
    freqs = deltaf*np.arange(n)
    # Input values for the fft - accomodate for the real and complex cases
    if ncol==1:
        vals = timeseries[:,1]
    elif ncol==2:
        vals = timeseries[:,1] + 1j*timeseries[:,2]
    else:
        raise Exception('Incorrect number of columns in array.')
    # BEWARE: due to the different convention for the sign of Fourier frequencies, we have to reverse the FFT output
    # Beware also that the FFT treats effectively the initial time as 0
    # BEWARE: in the reversion of the numpy-convention FFT output, we have to set aside the 0-frequency term
    fftvals_np = deltat * np.fft.fft(vals)
    fdvals = np.zeros_like(fftvals_np, dtype=complex)
    fdvals[0] = fftvals_np[0]
    fdvals[1:] = fftvals_np[1:][::-1]
    # Discarding information on negative frequencies - if real timeseries in input, no information loss as the deleted values are the conjugate
    fdvals = fdvals[:n//2]
    freqs = freqs[:n//2]
    # Coming back to the initial times
    tshift = timeseries[0,0]
    fac_timeshift = np.exp(1j*2*np.pi*freqs*tshift)
    fdvals = fdvals * fac_timeshift
    freqseries = np.array([freqs, np.real(fdvals), np.imag(fdvals)]).T
    return freqseries
# The IFFT function - input format (f, real, imag) expected to be FFT of complex data, assumes negative frequencies are zero (not conjugated as for the FFT of real data)
# Fourier convention: Ftilde(f) = \int dt exp(+2 i pi f t) * F(t)
# WORK IN PROGRESS
def ifft_positivef(freqseries):
    n = len(freqseries)
    ncol = freqseries.shape[1] - 1
    deltaf = freqseries[1,0] - freqseries[0,0]
    # Input values for the ifft - has no reason to bea real, check we have real and imag
    if not ncol==2:
        raise Exception('Incorrect number of columns in array.')
    # Zero-pad to next power of 2, then 0-pad by factor 2 for the negative frequencies
    freqseries_pad = zeropad(freqseries, extend=1)
    npad = len(freqseries_pad)
    # 1D FD values
    fdvals = freqseries_pad[:,1] + 1j*freqseries_pad[:,2]
    # BEWARE: due to the different convention for the sign of Fourier frequencies, we have to reverse the IFFT input
    # Beware also that the FFT treats effectively the initial time as 0
    # BEWARE: in the reversion of the numpy-convention IFFT input, we have to set aside the 0-frequency term
    fdvals_np = np.zeros_like(fdvals, dtype=complex)
    fdvals_np[0] = fdvals[0]
    fdvals_np[1:] = fdvals[1:][::-1]
    # Inverse FFT
    deltat = 1./(npad*deltaf)
    ifftvals_np = 1./deltat * np.fft.ifft(fdvals_np)
    # Rebuild time series from positive and negative times
    tdvals = np.concatenate((ifftvals_np[npad//2:], ifftvals_np[:npad//2]))
    # Rebuild times
    times = deltat*np.arange(-npad//2, npad//2)
    timeseries = np.array([times, np.real(tdvals), np.imag(tdvals)]).T
    return timeseries
# The IFFT function - input format (f, real, imag) expected to be FFT of real data, assumes negative frequencies are conjugate (as for the FFT of real data)
# Fourier convention: Ftilde(f) = \int dt exp(+2 i pi f t) * F(t)
# WORK IN PROGRESS
# NOTE: could be implemented with irfft, here for simplicity we keep close to the already-tested setting of the IFFT for complex TD data
def ifft_real(freqseries):
    n = len(freqseries)
    ncol = freqseries.shape[1] - 1
    deltaf = freqseries[1,0] - freqseries[0,0]
    # Input values for the ifft - has no reason to bea real, check we have real and imag
    if not ncol==2:
        raise Exception('Incorrect number of columns in array.')
    # Zero-pad to next power of 2, 0-pad by factor 2 to make room for the negative frequencies (conjugate data)
    freqseries_pad = zeropad(freqseries, extend=1)
    npad = len(freqseries_pad)
    # 1D FD values
    fdvals = freqseries_pad[:,1] + 1j*freqseries_pad[:,2]
    # Restore negative frequencies as conjugate of values for positive frequencies
    # NOTE: both values at 0 and n//2 are real and untouched here
    fdvals[npad//2+1:] = np.conjugate(fdvals[1:npad//2][::-1])
    # BEWARE: due to the different convention for the sign of Fourier frequencies, we have to reverse the IFFT input
    # Beware also that the FFT treats effectively the initial time as 0
    # BEWARE: in the reversion of the numpy-convention IFFT input, we have to set aside the 0-frequency term
    fdvals_np = np.zeros_like(fdvals, dtype=complex)
    fdvals_np[0] = fdvals[0]
    fdvals_np[1:] = fdvals[1:][::-1]
    # Inverse FFT
    deltat = 1./(npad*deltaf)
    ifftvals_np = 1./deltat * np.fft.ifft(fdvals_np)
    # Rebuild time series from positive and negative times
    tdvals = np.concatenate((ifftvals_np[npad//2:], ifftvals_np[:npad//2]))
    # Rebuild times
    times = deltat*np.arange(-npad//2, npad//2)
    # Discard imaginary part, must be 0 to machine precision
    timeseries_real = np.array([times, np.real(tdvals)]).T
    return timeseries_real

# Function for zero-padding a real array at the end
# Assumes a constant x-spacing - works with any number of columns
def zeropad(series, extend=0):
    n = len(series)
    ncol = series.shape[1]
    deltax = series[1,0] - series[0,0]
    xf = series[-1,0]
    nzeros = pow(2, extend + int(np.ceil(np.log(n)/np.log(2)))) - n
    res = np.zeros((n+nzeros, ncol), dtype=float)
    xextension = xf + deltax*np.arange(1, nzeros+1)
    res[:n, :] = series
    res[n:, 0] = xextension
    return res

################################################################################
# Stationary Phase Approximation (SPA)
################################################################################

# Stationary Phase Approximation for a time-domain signal
# Allows for chirping or anti-chirping signal with the sign option
def signal_spa(signal_td, sign=1):
    t, amp, phi = signal_td.T
    spline_phi = pyspline.CubicSpline(t, phi)
    # NOTE: here omega means phidot, not omega_orb
    omega = spline_phi.get_spline_d()[:,1]
    omegadot = spline_phi.get_spline_dd()[:,1]
    f = -omega / (2*np.pi)
    A_spa = amp * np.sqrt(2*np.pi / (-sign*omegadot))
    Psi_spa = -phi - 2*np.pi*f*t - sign*np.pi/4
    signal_fd = np.array([f, A_spa, -Psi_spa]).T
    if sign==1:
        return signal_fd
    else:
        signal_fd_reverse = np.zeros_like(signal_fd)
        signal_fd_reverse[:] = signal_fd[::-1]
        return signal_fd_reverse

# Inverse Stationary Phase Approximation for a Fourier-domain signal
# Allows for chirping or anti-chirping signal with the sign option
def signal_inverse_spa(signal_fd, sign=1):
    f, amp_fd, phi_fd = signal_fd.T
    spline_phi_fd = pyspline.CubicSpline(f, phi_fd)
    tf = 1./(2*np.pi) * spline_phi_fd.get_spline_d()[:,1]
    # NOTE: Tf^2 here is positive by convention
    Tf2 = sign * 1./(2*np.pi)**2 * spline_phi_fd.get_spline_dd()[:,1]
    # NOTE: here omega means phidot, not omega_orb
    omegadot_abs = 1./Tf2
    amp_td = amp_fd * np.sqrt(omegadot_abs / (2*np.pi))
    # NOTE: phi_fd = -Psi
    phi_td = phi_fd - 2*np.pi*f*tf - sign*np.pi/4
    signal_td = np.array([tf, amp_td, phi_td]).T
    return signal_td

################################################################################
# Utilities for frequency scaling between mode when not using m/2*f22
################################################################################

# Scales an array of frequencies to new bounds, using log-affine scaling
def log_affine_scaling(freq, fLow, fHigh):
    lp1 = np.log(fLow)
    lp2 = np.log(fHigh)
    l = np.log(freq)
    l1 = l[0]
    l2 = l[-1]
    a = (lp2 - lp1) / (l2 - l1)
    b = (lp1*l2 - l1*lp2) / (l2 - l1)
    lp = a*l + b
    return np.exp(lp)

################################################################################
# Utilities for decomposing a signal in chirping and anti-chirping bands
################################################################################

def func_sign_interval(y, interval):
    if y < interval[0]: return -1
    elif interval[0] <= y <= interval[1]: return 0
    else: return 1

def func_solve_linear_interp(X1, X2, yval):
    x1, y1 = X1
    x2, y2 = X2
    xval = x1 + (x2 - x1) / (y2 - y1) * (yval - y1)
    return xval

def func_domain_decomp_linear(x, y, interval):
    N = len(x)
    nband_max = 2*N - 1
    iband = 0
    bands = np.zeros((nband_max,3), dtype=float)
    sign = func_sign_interval(y[0], interval)
    bands[0][0] = x[0]
    bands[0][2] = sign
    for i in range(1,N):
        sign_new = func_sign_interval(y[i], interval)
        sign_diff = sign_new - sign
        X1 = [x[i-1], y[i-1]]
        X2 = [x[i], y[i]]
        if np.abs(sign_diff)==1:
            if sign==-1 or sign_new==-1:
                yval = interval[0]
            elif sign==1 or sign_new==1:
                yval = interval[1]
            xval = func_solve_linear_interp(X1, X2, yval)
            bands[iband][1] = xval
            bands[iband+1][0] = xval
            bands[iband+1][2] = sign_new
            iband += 1
        elif np.abs(sign_diff)==2:
            if sign==-1:
                yval1, yval2 = interval[0], interval[1]
            elif sign==1:
                yval1, yval2 = interval[1], interval[0]
            xval1 = func_solve_linear_interp(X1, X2, yval1)
            xval2 = func_solve_linear_interp(X1, X2, yval2)
            bands[iband][1] = xval1
            bands[iband+1][0] = xval1
            bands[iband+1][1] = xval2
            bands[iband+1][2] = 0
            bands[iband+2][0] = xval2
            bands[iband+2][2] = sign_new
            iband += 2
        else:
            pass
        sign = sign_new
    bands[iband][1] = x[-1]
    bands = bands[:iband+1]
    return bands

################################################################################
# I/O utilities
################################################################################

# Write a dictionary of type {str:val} to hdf5 as separate 1-element datasets
# At first sight, no way around using 1-element numpy arrays...
# TODO: support string types
def write_h5py_dict(h5gr, dic):
    for p in dic:
        h5gr.create_dataset(p, data=np.array([dic[p]]))
    return
def read_h5py_dict(h5gr):
    dic = {}
    for p in list(h5gr.keys()):
        dic[p] = h5gr[p][:][0] # We assume datasets are 1-element arrays
    return dic

################################################################################
# Spin-weighted spherical harmonics
################################################################################

cpdef sYlm(l, m, theta, phi, s=-2):
    return SpinWeightedSphericalHarmonic (
        theta,
        phi,
        s,
        l,
        m
    )

################################################################################
# Functions to build frequency grids
################################################################################

cdef class WaveformGeomFrequencyGrid:
    """ Geom frequency grid suitable for waveform amp/phase interpolation.
    """

    cdef real_vector* CMfreq  # pointer to C frequency vector

    cdef Mfmin                # Minimal geometric frequency
    cdef Mfmax                # Maximal geometric frequency
    cdef eta                  # Symmetric mass ratio
    cdef length               # Size of the frequency data
    cdef acc                  # Target accuracy for inspiral

    cdef Mfreq                # numpy array of frequencies


    def __init__(self, Mfmin, Mfmax, eta, acc=1e-4):
        """Constructor
        Args:
          Mfmin                 # Minimal geometric frequency
          Mfmax                 # Maximal geometric frequency
          eta                   # Symmetric mass ratio
        Keyword args:
          acc                   # Target accuracy for inspiral (default 1e-4)
        """
        self.Mfmin = Mfmin
        self.Mfmax = Mfmax
        self.eta = eta
        self.acc = acc

        self.CMfreq = NULL

        ret = BuildWaveformGeomFrequencyGrid(
            &self.CMfreq,
            self.Mfmin,
            self.Mfmax,
            self.eta,
            self.acc
        );
        if ret == _FAILURE:
            raise ValueError("Call to BuildWaveformGeomFrequencyGrid() failed.")

        # Cast C double array to numpy via a MemoryView
        cdef double[::1] view_Mfreq = \
          <(double)[:self.CMfreq.size]> self.CMfreq.data
        self.Mfreq = np.asarray(view_Mfreq)
        #self.Mfreq = real_vector_to_np_array(self.CMfreq)

    def __dealloc__(self):
        """Destructor
        """
        if self.CMfreq != NULL:
            real_vector_free(self.CMfreq)

    def get_Mfreq(self):
        return np.copy(self.Mfreq)

cdef class ResponseFrequencyGrid:
    """ Geom frequency grid suitable for waveform amp/phase interpolation.
    """

    cdef real_vector* Cfreq     # pointer to C frequency vector
    cdef real_matrix* Ctfspline # pointer to C spline matrix for tf

    cdef f_min                  # Minimal frequency (default None: use tf)
    cdef f_max                  # Maximal frequency (default None: use tf)
    cdef Deltat_max             # Maximal time step, in years (default 2 weeks)
    cdef Deltaf_max             # Maximal frequency step, in Hz (default 1mHz)
    cdef nptlogmin              # Minimal number of points with log-spacing

    cdef freq                   # numpy array of frequencies

    def __init__(self, np.ndarray[np.float_t, ndim=2] tfspline,
                       f_min=None, f_max=None, Deltat_max=0.02083335,
                       Deltaf_max=0.001, nptlogmin=150):
        """Constructor
        Args:
          tfspline              # Input tf cubic spline (numpy array)
        Keyword args:
          f_min                 # Minimal frequency (default None: use tf)
          f_max                 # Maximal frequency (default None: use tf)
          Deltat_max            # Maximal time step, in years (default 2 weeks)
          Deltaf_max            # Maximal frequency step, in Hz (default 1mHz)
          nptlogmin             # Minimal number of points with log-spacing
        """
        n_tf = tfspline.shape[0]
        f_min_tf = tfspline[0, 0]
        f_max_tf = tfspline[n_tf-1, 0]
        if f_min is None:
            self.f_min = f_min_tf
        else:
            self.f_min = f_min
        if f_max is None:
            self.f_max = f_max_tf
        else:
            self.f_max = f_max
        self.Deltat_max = Deltat_max
        self.Deltaf_max = Deltaf_max
        self.nptlogmin = nptlogmin

        self.Cfreq = NULL

        # Build a real_matrix representation of the input numpy array spline
        if not tfspline.flags['C_CONTIGUOUS']:
            raise ValueError('Input np array tfspline is not C_CONTIGUOUS.')
        cdef double* tfspline_data = <double *> &tfspline[0,0]
        self.Ctfspline = real_matrix_view(tfspline_data,
                                      tfspline.shape[0], tfspline.shape[1])

        ret = BuildResponseFrequencyGrid(
            &self.Cfreq,
            self.Ctfspline,
            self.f_min,
            self.f_max,
            self.Deltat_max,
            self.Deltaf_max,
            self.nptlogmin
        );
        if ret == _FAILURE:
            raise ValueError("Call to BuildResponseFrequencyGrid() failed.")

        # Cast C double array to numpy via a MemoryView
        cdef double[::1] view_freq = \
          <(double)[:self.Cfreq.size]> self.Cfreq.data
        self.freq = np.asarray(view_freq)
        #self.freq = real_vector_to_np_array(self.Cfreq)

    def __dealloc__(self):
        """Destructor
        """
        if self.Cfreq != NULL:
            real_vector_free(self.Cfreq)

    def get_freq(self):
        return np.copy(self.freq)

cdef class FrequencyGrid:
    """ Frequency grid suitable for both the waveform and the response.
    """

    cdef real_vector* Cfreq     # pointer to C frequency vector

    cdef f_min                  # Minimal frequency (default None: use tf)
    cdef f_max                  # Maximal frequency (default None: use tf)
    cdef M                      # Total mass (solar masses)
    cdef q                      # Mass ratio
    cdef Deltat_max             # Maximal time step, in years (default 2 weeks)
    cdef Deltaf_max             # Maximal frequency step, in Hz (default 1mHz)
    cdef DeltalnMf_max          # Maximal ln(Mf) step (default 0.025)
    cdef acc                    # Target phase interp. error (default 1e-4)
    cdef nptlogmin              # Minimal number of points (default 100)

    cdef freq                   # numpy array of frequencies

    def __init__(self, f_min, f_max, M, q,
                       Deltat_max=0.02083335, Deltaf_max=0.001,
                       DeltalnMf_max=0.025,
                       acc=1e-4, nptlogmin=100):
        """Constructor
        Args:
          f_min                 # Minimal frequency (Hz)
          f_max                 # Maximal frequency (Hz)
          M                     # Total mass (solar masses)
          q                     # Mass ratio
        Keyword args:
          Deltat_max            # Maximal time step, in years (default 2 weeks)
          Deltaf_max            # Maximal frequency step, in Hz (default 1mHz)
          DeltalnMf_max         # Maximal ln(Mf) step (default 0.025)
          acc                   # Target phase interp. error (default 1e-4)
          nptlogmin             # Minimal number of points (default 100)
        """
        self.f_min = f_min
        self.f_max = f_max
        self.M = M
        self.q = q
        self.Deltat_max = Deltat_max
        self.Deltaf_max = Deltaf_max
        self.DeltalnMf_max = DeltalnMf_max
        self.acc = acc
        self.nptlogmin = nptlogmin

        self.Cfreq = NULL

        ret = BuildFrequencyGrid(
            &self.Cfreq,
            self.f_min,
            self.f_max,
            self.M,
            self.q,
            self.Deltat_max,
            self.Deltaf_max,
            self.DeltalnMf_max,
            self.acc,
            self.nptlogmin
        );
        if ret == _FAILURE:
            raise ValueError("Call to BuildFrequencyGrid() failed.")

        # Cast C double array to numpy via a MemoryView
        cdef double[::1] view_freq = \
          <(double)[:self.Cfreq.size]> self.Cfreq.data
        self.freq = np.asarray(view_freq)
        #self.freq = real_vector_to_np_array(self.Cfreq)

    def __dealloc__(self):
        """Destructor
        """
        if self.Cfreq != NULL:
            real_vector_free(self.Cfreq)

    def get_freq(self):
        return np.copy(self.freq)

cdef class MergeGrids:
    """ Merge two grids with increasing values (e.g. two frequency grids)
    Discards duplicate values
    Allows for safeguarding: can ignore points that are almost identical
    """

    cdef real_vector* Cgrid   # pointer to output C vector
    cdef real_vector* Cgrid1  # pointer to inupt C vector 1
    cdef real_vector* Cgrid2  # pointer to input C vector 2

    cdef xmin                 # Minimal value
    cdef xmax                 # Maximal value
    cdef usedeltaxmin         # Use minimal x step
    cdef usedeltalnxmin       # Use minimal x relative step in ln
    cdef deltaxmin            # Minimal x step
    cdef deltalnxmin          # Minimal x relative step in ln

    cdef grid                 # numpy array of frequencies


    def __init__(self,
                 np.ndarray[np.float_t, ndim=1] grid1,
                 np.ndarray[np.float_t, ndim=1] grid2,
                 deltaxmin=None, deltalnxmin=-11.512925465):
        """Constructor
        Args:
          grid1                # First vector of frequencies to be merged
          grid2                # Second vector of frequencies to be merged
        Keyword args:
          xmin                  # Minimal value
          xmax                  # Maximal value
          deltaxmin             # Minimal step
          deltalnxmin           # Minimal step ratio, in ln (default ratio=1e-5)
        """
        if deltaxmin is not None:
            self.usedeltaxmin = True
            self.deltaxmin = deltaxmin
        else:
            self.usedeltaxmin = False
            self.deltaxmin = 0. # will be ignored
        if deltalnxmin is not None:
            self.usedeltalnxmin = True
            self.deltalnxmin = deltalnxmin
        else:
            self.usedeltalnxmin = False
            self.deltalnxmin = 0. # will be ignored
        cdef int Cusedeltaxmin = <int> self.usedeltaxmin
        cdef int Cusedeltalnxmin = <int> self.usedeltalnxmin

        if not grid1.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array grid1 is not C_CONTIGUOUS')
        if not grid2.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array grid2 is not C_CONTIGUOUS')
        cdef double* grid1_data = <double *> &grid1[0]
        self.Cgrid1 = real_vector_view(grid1_data, grid1.shape[0])
        cdef double* grid2_data = <double *> &grid2[0]
        self.Cgrid2 = real_vector_view(grid2_data, grid2.shape[0])

        self.Cgrid = NULL

        ret = BuildMergedGrid(
            &self.Cgrid,
            self.Cgrid1,
            self.Cgrid2,
            Cusedeltaxmin,
            self.deltaxmin,
            Cusedeltalnxmin,
            self.deltalnxmin
        );
        if ret == _FAILURE:
            raise ValueError("Call to BuildMergedGrid() failed.")

        # Cast C double array to numpy via a MemoryView
        cdef double[::1] view_grid = \
          <(double)[:self.Cgrid.size]> self.Cgrid.data
        self.grid = np.asarray(view_grid)

    def __dealloc__(self):
        """Destructor
        """
        if self.Cgrid != NULL:
            real_vector_free(self.Cgrid)

    def get_grid(self):
        return np.copy(self.grid)

# Function that uses the 1/(2T) Nyquist sampling, then breaks to log-sampling
# No C extension, used primarily for Fisher where it is not the dominating cost
def composite_nyquist_log_freq_grid(f0, f1, m1, m2, Deltalnf=5e-5, refine=0):
    Ms = (m1 + m2) * pyconstants.MTSUN_SI
    nu = etaofm1m2(m1, m2)
    lambd = 128*nu/3. * 1./Ms * (np.pi*Ms)**(8./3)
    xi = np.exp(Deltalnf) - 1.
    f_break = (3*lambd/5./xi)**(-3./5)
    if f_break > f1:
        N_nyq = int(np.floor(1./lambd * (f0**(-5./3) - f1**(-5./3)))) + 1
        freq = np.zeros(N_nyq, dtype=float)
        n = np.arange(N_nyq-1)
        freq[:N_nyq-1] = (f0**(-5./3) - lambd*n)**(-3./5)
        freq[N_nyq-1] = f1
    elif f_break > f0:
        N_nyq = int(np.floor(1./lambd * (f0**(-5./3) - f_break**(-5./3)))) # Does not include f_break
        N_log = int(np.ceil(np.log(f1/f_break) / Deltalnf))
        freq = np.zeros(N_nyq + N_log, dtype=float)
        n = np.arange(N_nyq)
        freq[:N_nyq] = (f0**(-5./3) - lambd*n)**(-3./5)
        freq[N_nyq:] = np.geomspace(f_break, f1, N_log)
    else:
        N_log = int(np.ceil(np.log(f1/f0) / Deltalnf))
        freq = np.geomspace(f0, f1, N_log)
    while refine > 0:
        freq_refine = np.zeros(2*len(freq) - 1, dtype=float)
        freq_refine[0::2] = freq
        freq_refine[1::2] = (freq[1:] + freq[:-1]) / 2.
        freq = freq_refine
        refine -= 1
    return freq

################################################################################
# Helper function for residuals likelihood
################################################################################

cpdef linear_interp_multimode_3chan_resid_norm(
        np.ndarray[np.complex_t, ndim=3] alpha0,
        np.ndarray[np.complex_t, ndim=3] alpha1,
        np.ndarray[np.complex_t, ndim=3] w0,
        np.ndarray[np.complex_t, ndim=3] w1,
        np.ndarray[np.complex_t, ndim=3] w2):
    """ Helper function for residuals likelihood.
    """

    cdef complex_array_3d* Calpha0  # pointer to C alpha0
    cdef complex_array_3d* Calpha1  # pointer to C alpha1
    cdef complex_array_3d* Cw0      # pointer to C w0
    cdef complex_array_3d* Cw1      # pointer to C w1
    cdef complex_array_3d* Cw2      # pointer to C w2

    # Build a complex_array_3d representation of the input numpy arrays
    if not alpha0.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array alpha0 is not C_CONTIGUOUS')
    if not alpha1.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array alpha1 is not C_CONTIGUOUS')
    if not w0.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array w0 is not C_CONTIGUOUS')
    if not w1.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array w1 is not C_CONTIGUOUS')
    if not w2.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array w2 is not C_CONTIGUOUS')
    cdef double complex* alpha0_data = <double complex *> &alpha0[0,0,0]
    Calpha0 = complex_array_3d_view(alpha0_data, alpha0.shape[0],
                                              alpha0.shape[1], alpha0.shape[2])
    cdef double complex* alpha1_data = <double complex *> &alpha1[0,0,0]
    Calpha1 = complex_array_3d_view(alpha1_data, alpha1.shape[0],
                                              alpha1.shape[1], alpha1.shape[2])
    cdef double complex* w0_data = <double complex *> &w0[0,0,0]
    Cw0 = complex_array_3d_view(w0_data, w0.shape[0], w0.shape[1], w0.shape[2])
    cdef double complex* w1_data = <double complex *> &w1[0,0,0]
    Cw1 = complex_array_3d_view(w1_data, w1.shape[0], w1.shape[1], w1.shape[2])
    cdef double complex* w2_data = <double complex *> &w2[0,0,0]
    Cw2 = complex_array_3d_view(w2_data, w2.shape[0], w2.shape[1], w2.shape[2])

    residual_norm = LinearInterpMultiMode3ChannelsResidualNorm(Calpha0, Calpha1,
                                                                  Cw0, Cw1, Cw2)

    if Calpha0 != NULL:
        complex_array_3d_view_free(Calpha0)
    if Calpha1 != NULL:
        complex_array_3d_view_free(Calpha1)
    if Cw0 != NULL:
        complex_array_3d_view_free(Cw0)
    if Cw1 != NULL:
        complex_array_3d_view_free(Cw1)
    if Cw2 != NULL:
        complex_array_3d_view_free(Cw2)

    return residual_norm
