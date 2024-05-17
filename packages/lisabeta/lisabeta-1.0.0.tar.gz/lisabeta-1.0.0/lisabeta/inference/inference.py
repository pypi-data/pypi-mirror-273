#
# Copyright (C) 2020 Sylvain Marsat.
#
#


"""
    Python tools for Bayesian inference.
"""


import time
import numpy as np
import copy
import h5py

import lisabeta
import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pytools as pytools

# Make this a soft dependency -- will only be needed if the user asks for this
# tool in computing autocorrelations
try:
    import acor
except ImportError:
    pass


################################################################################
# Wrap parameters

# Params that are wrapped -- by default we wrap psi mod pi
# phi is wrapped mod 2pi by default for the general HM case
default_wrap_dict = {
    'phi': [-np.pi, np.pi],
    'lambda': [-np.pi, np.pi],
    'ra': [-np.pi, np.pi],
    'psi': [0., np.pi],
    }
def func_default_wrap(list_params):
    list_wrap_moduli = []
    for p in list_params:
        list_wrap_moduli += [default_wrap_dict.get(p, None)]
    return list_wrap_moduli

################################################################################
# Priors

def prior_check(x, prior_bounds):
    if prior_bounds is None:
        return True
    else:
        return np.all([(prior_bounds[i][0]<=x[i] and x[i]<=prior_bounds[i][1]) for i in range(len(x))])

# Computing simple priors
# Assumes paramrange[0] < paramrange[1]
# TODO: add support for non-trivial mass priors (flat in m1/m2 -> Mchirp/eta)
# TODO: add automatic ranges for dimensionful parameters like masses, distance
# TODO: for now the extra options are clunky (also unnormalized)
# ever-growing if/elif -  we should map once and for all to a function
def compute_prior(priortype, paramrange, x):
    if priortype=='uniform':
        return 1. / (paramrange[1] - paramrange[0])
    elif priortype=='sin': # NOTE: cos decreasing on [0,pi]
        return np.sin(x) / (np.cos(paramrange[0]) - np.cos(paramrange[1]))
    elif priortype=='cos': # NOTE: sin increasing on [-pi/2,pi/2]
        return np.cos(x) / (np.sin(paramrange[1]) - np.sin(paramrange[0]))
    elif priortype=='quadratic':
        return x*x / 3. / (paramrange[1]**3 - paramrange[0]**3)
    elif priortype=='Mchirp_Mchirpqchipchim_flatlnMinvqchi1chi2':
        return 1e6/x # Unnormalized Mchirpref/Mchirp, arbitrary Mchirpref
    elif priortype=='q_Mchirpqchipchim_flatlnMinvqchi1chi2':
        return (1+x)**2/x**3 # Unnormalized (1+q)**2/q**3
    else:
        raise ValueError('priortype not recognized.')

# Set priors as pure functions
# Avoids going through if/elif at evaluation, still multiplicative only
def def_prior_func(priortype, paramrange):
    if priortype=='uniform':
        norm = 1 / (paramrange[1] - paramrange[0])
        return lambda x: 1. * norm
    elif priortype=='sin': # NOTE: cos decreasing on [0,pi]
        norm = 1 / (np.cos(paramrange[0]) - np.cos(paramrange[1]))
        return lambda x: np.sin(x) * norm
    elif priortype=='cos': # NOTE: sin increasing on [-pi/2,pi/2]
        norm  = 1 / (np.sin(paramrange[1]) - np.sin(paramrange[0]))
        return lambda x: np.cos(x) * norm
    elif priortype=='quadratic':
        norm = 1 / 3. / (paramrange[1]**3 - paramrange[0]**3)
        return lambda x: x*x * norm
    elif priortype=='Mchirp_Mchirpqchipchim_flatlnMinvqchi1chi2':
        return lambda x: 1e6/x # Unnormalized Mchirpref/Mchirp, arbitrary Mchirpref
    elif priortype=='q_Mchirpqchipchim_flatlnMinvqchi1chi2':
        return lambda x: (1+x)**2/x**3 # Unnormalized (1+q)**2/q**3
    else:
        raise ValueError('priortype not recognized.')

# Draw from simple priors
def draw_prior(priortype, paramrange, n):
    u = np.random.uniform(size=n)
    if priortype=='uniform':
        return paramrange[0] + u * (paramrange[1] - paramrange[0])
    elif priortype=='sin': # NOTE: cos decreasing on [0,pi]
        return np.arccos(np.cos(paramrange[1]) + u * (np.cos(paramrange[0]) - np.cos(paramrange[1])))
    elif priortype=='cos': # NOTE: sin increasing on [-pi/2,pi/2]
        return np.arcsin(np.sin(paramrange[0]) + u * (np.sin(paramrange[1]) - np.sin(paramrange[0])))
    elif priortype=='quadratic':
        return np.power(paramrange[0]**3 + u * (paramrange[1]**3 - paramrange[0]**3), 1./3)
    else:
        raise ValueError('priortype not recognized for drawing.')

################################################################################
# Autocorrelation
# see https://dfm.io/posts/autocorr/
# see https://github.com/dfm/emcee/issues/209

def next_pow_two(n):
    i = 1
    while i < n:
        i = i << 1
    return i

def autocorr_func_1d(x, norm=True):
    x = np.atleast_1d(x)
    if len(x.shape) != 1:
        raise ValueError("invalid dimensions for 1D autocorrelation function")
    n = next_pow_two(len(x))

    # Compute the FFT and then (from that) the auto-correlation function
    f = np.fft.fft(x - np.mean(x), n=2*n)
    acf = np.fft.ifft(f * np.conjugate(f))[:len(x)].real
    acf /= 4*n

    # Optionally normalize
    if norm:
        acf /= acf[0]

    return acf

# Automated windowing procedure following Sokal (1989)
def auto_window(taus, c):
    m = np.arange(len(taus)) < c * taus
    if np.any(m):
        return np.argmin(m)
    return len(taus) - 1

# Following the suggestion from Goodman & Weare (2010)
def autocorr_gw2010(y, c=5.0):
    f = autocorr_func_1d(np.mean(y, axis=0))
    taus = 2.0*np.cumsum(f)-1.0
    window = auto_window(taus, c)
    return taus[window]

def autocorr_new(y, c=5.0):
    f = np.zeros(y.shape[1])
    for yy in y:
        f += autocorr_func_1d(yy)
    f /= len(y)
    taus = 2.0*np.cumsum(f)-1.0
    window = auto_window(taus, c)
    return taus[window]

# Wrapper, allowing two choices, for data given as an array of chains
def get_autocor(data, method='autocor_new'):
    if method=='autocor_new':
        return autocorr_new(data)
    elif method=='acor':
        return np.mean([acor.acor(data[k])[0] for k in range(len(data))])
    else:
        raise ValueError('Autocorrelation method %s not recognized.' % (method))

################################################################################
# Constrained Gaussian draws
# Recursively draw from Gaussian until within the prior bounds

# Using infer_params to identify angular params, first map to 2pi or pi-range
# Necessary as Fisher errors for e.g. phi, psi can be very large
# TODO: a bit clumsy, but this is used at initialization essentially
def enforce_range_angles(x, infer_params):
    # Handle both 1d and 2d arrays, y is always 2d
    if x.ndim==1:
        y = np.array([x])
    else:
        y = x.copy()
    if 'inc' in infer_params:
        iinc = infer_params.index('inc')
        y[:,iinc] = pytools.modpi(y[:,iinc])
    if 'phi' in infer_params:
        iphi = infer_params.index('phi')
        y[:,iphi] = pytools.mod2pi(y[:,iphi])
    if 'lambda' in infer_params:
        ilambda = infer_params.index('lambda')
        y[:,ilambda] = pytools.mod2pi(y[:,ilambda])
    if 'beta' in infer_params:
        ibeta = infer_params.index('beta')
        y[:,ibeta] = pytools.modpi2(y[:,ibeta])
    if 'psi' in infer_params:
        ipsi = infer_params.index('psi')
        y[:,ipsi] = pytools.modpi(y[:,ipsi])
    if x.ndim==1:
        return y[0]
    else:
        return y

def draw_multivariate_normal_constrained(mean, cov, prior_bounds, infer_params):
    x = np.random.multivariate_normal(mean, cov)
    x = enforce_range_angles(x, infer_params)
    if prior_check(x, prior_bounds):
        return x
    else:
        return draw_multivariate_normal_constrained(mean, cov, prior_bounds, infer_params)

################################################################################
# Interface for json

def waveform_params_json2py(waveform_params):
    waveform_params_py = copy.deepcopy(waveform_params)
    if ('modes' in waveform_params.keys()) and isinstance(waveform_params_py['modes'], list):
        waveform_params_py['modes'] = [tuple(lm) for lm in waveform_params['modes']]
    if 'waveform_params_update_for_template' in waveform_params.keys():
        if ('modes' in waveform_params['waveform_params_update_for_template'].keys()) and isinstance(waveform_params['waveform_params_update_for_template']['modes'], list):
            waveform_params_py['waveform_params_update_for_template']['modes'] = [tuple(lm) for lm in waveform_params['waveform_params_update_for_template']['modes']]
    if 'gridfreq' in waveform_params.keys():
        waveform_params_py['gridfreq'] = np.array(waveform_params['gridfreq'])
    return waveform_params_py

################################################################################
# Functions for multimodal jumps, see Marsat&al arXiv:2003.00357

def map_skymode(angle_params, skymode_index0, skymode_index1):
    inc = angle_params['inc']
    lambdaL = angle_params['lambda']
    betaL = angle_params['beta']
    psiL = angle_params['psi']
    jump_params = {}
    jump_params['inc'] = pytools.modpi(np.pi/2 - (skymode_index0 *(np.pi/2 - inc)))
    jump_params['lambda'] = pytools.mod2pi(lambdaL + skymode_index1 * np.pi/2)
    jump_params['beta'] = skymode_index0 * betaL
    jump_params['psi'] = pytools.modpi(np.pi/2 - (skymode_index0 *(np.pi/2 - psiL)) + skymode_index1 * np.pi/2)
    return jump_params

# Used e.g. for the simple22 map: transform sky and indexpsi
# In the inverse map, indexpsi=[0,1] decides of the branch psi \in [0,pi/2] or [pi/2,pi]
def map_skymode_simple22map(angle_params, skymode_index0, skymode_index1, skymode_index2):
    lambdaL = angle_params['lambda']
    sbetaL = angle_params['sbeta']
    indexpsi = angle_params['indexpsi']
    jump_params = {}
    jump_params['lambda'] = pytools.mod2pi(lambdaL + skymode_index1 * np.pi/2)
    jump_params['sbeta'] = skymode_index0 * sbetaL
    jump_params['indexpsi'] = skymode_index2
    return jump_params

def proposal_skymode(size=None, pattern='8modes', random_state=np.random):
    if pattern=='8modes':
        return np.array([2 * (np.random.binomial(1, 0.5, size=size) - 1./2), np.random.randint(0, 4, size=size)]).T
    elif pattern=='2modes':
        return np.array([2 * (np.random.binomial(1, 0.5, size=size) - 1./2), np.zeros(size, dtype=int)]).T
    else:
        raise ValueError('pattern %s not recognized.' % (pattern))

# Used e.g. for the simple22 map: transform sky and indexpsi
# In the inverse map, indexpsi=[0,1] decides of the branch psi \in [0,pi/2] or [pi/2,pi]
def proposal_skymode_simple22map(size=None, pattern='8modes', random_state=np.random):
    if pattern=='8modes':
        return np.array([2 * (np.random.binomial(1, 0.5, size=size) - 1./2), np.random.randint(0, 4, size=size), np.random.randint(0, 2, size=size)]).T
    elif pattern=='2modes':
        return np.array([2 * (np.random.binomial(1, 0.5, size=size) - 1./2), np.zeros(size, dtype=int), np.random.randint(0, 2, size=size)]).T
    else:
        raise ValueError('pattern %s not recognized.' % (pattern))

################################################################################
# Functions for a parameter map adapted to the simple likelihood with 22 mode
# see Marsat&al arXiv:2003.00357

# def func_extrparams(params, injparams):
#     params_extr = {}
#     for p in ['inc', 'phi', 'lambda', 'beta', 'psi']:
#         params_extr[p] = params[p]
#     params_extr['d'] = params['dist'] / injparams['dist']
#     params_extr['phi'] = pytools.modpi(params_extr['phi'])
#     return params_extr

# def func_restoreparams(params, injparams):
#     params_restore = {}
#     for p in ['inc', 'phi', 'lambda', 'beta', 'psi']:
#         params_restore[p] = params[p]
#     params_restore['dist'] = params['d'] * injparams['dist']
#     params_restore['phi'] = pytools.modpi(params['phi'])
#     for p in pytools.list_mass_params:
#         params_restore[p] = injparams[p]
#     for p in pytools.list_spin_params:
#         params_restore[p] = injparams[p]
#     params_restore['Deltat'] = injparams['Deltat']
#     params_restore['Lframe'] = injparams['Lframe']
#     return params_restore

def map_params_simple_response_22(params, injdist):
    dist = params['dist']
    inc = params['inc']
    phi = params['phi']
    lambda_a = params['lambda'] - np.pi/6
    beta = params['beta']
    psi = params['psi']

    if (np.any(dist<=0.) or np.any(inc<0.) or np.any(inc>np.pi) or np.any(beta<-np.pi/2) or np.any(beta>np.pi/2)):
        raise ValueError('params are outside physical range.')

    d = dist / injdist
    tiota = np.tan(inc/2)
    ttheta = np.tan(1./2 * (np.pi/2 - beta))
    rho = 1./(4*d) * np.sqrt(5/np.pi) * 1./(1+tiota**2)**2 * 1./(1+ttheta**2)**2

    sigma_plus = rho*np.exp(2*1j*phi) * (ttheta**4 * np.exp(-2*1j*psi) + tiota**4 * np.exp(2*1j*psi)) * np.exp(-2*1j*lambda_a)
    sigma_minus = rho*np.exp(2*1j*phi) * (np.exp(-2*1j*psi) + ttheta**4 * tiota**4 * np.exp(2*1j*psi)) * np.exp(2*1j*lambda_a)

    if isinstance(psi, np.ndarray):
        indexpsi = np.zeros(psi.shape, dtype=int)
        indexpsi[pytools.modpi(psi) > np.pi/2] = 1
    else:
        if pytools.modpi(psi) <= np.pi/2:
            indexpsi = 0
        else:
            indexpsi = 1

    params_map = {}
    params_map['Aplus'] = np.abs(sigma_plus)
    params_map['Aminus'] = np.abs(sigma_minus)
    params_map['Phiplus'] = np.angle(sigma_plus)
    params_map['Phiminus'] = np.angle(sigma_minus)
    params_map['lambda'] = lambda_a + np.pi/6
    params_map['sbeta'] = np.sin(beta)
    params_map['indexpsi'] = indexpsi

    return params_map

def physical_check_simple_response_22(params_map):

    Aplus = params_map['Aplus']
    Aminus = params_map['Aminus']
    sbeta = params_map['sbeta']
    indexpsi = params_map['indexpsi']

    return (not (np.any(Aplus<=0.) or np.any(Aminus<=0.) or np.any(sbeta<-1.) or np.any(sbeta>1.) or not np.all((indexpsi==0) | (indexpsi==1))))

def invmap_params_simple_response_22(params_map, injdist):

    Aplus = params_map['Aplus']
    Aminus = params_map['Aminus']
    Phiplus = params_map['Phiplus']
    Phiminus = params_map['Phiminus']
    lambd = params_map['lambda']
    sbeta = params_map['sbeta']
    indexpsi = params_map['indexpsi']

    if (np.any(Aplus<=0.) or np.any(Aminus<=0.) or np.any(sbeta<-1.) or np.any(sbeta>1.) or not np.all((indexpsi==0) | (indexpsi==1))):
        raise ValueError('params_map are outside physical range.')

    lambda_a = lambd - np.pi/6
    sigma_plus = Aplus * np.exp(1j*Phiplus)
    sigma_minus = Aminus * np.exp(1j*Phiminus)
    rtilde = sigma_plus / sigma_minus * np.exp(4*1j*lambda_a)

    ctheta = sbeta
    a = ((ctheta-1) / (ctheta+1))**2
    bz = (a - rtilde) / (a*rtilde - 1)
    b = np.abs(bz)
    tiota2 = np.sqrt(b)
    ciota = (1 - tiota2) / (1 + tiota2)
    fourpsi = np.angle(bz)
    # Ambiguity in psi: psi0 in [0, pi/2], psi1=psi0+pi/2 in [pi/2, pi]
    # We use indexpsi=[0,1] to represent this degeneracy
    psi0 = pytools.mod_interval(1./4*fourpsi, interval=[0, np.pi/2])
    psi = psi0 + indexpsi*np.pi/2

    # Get a,b,z
    a = ((ctheta-1) / (ctheta+1))**2
    b = ((ciota-1) / (ciota+1))**2
    z = np.exp(1j*4*psi)

    # No ambiguity in phi, since for 22-mode only we can restrict it mod pi
    phi = 1./2 * np.angle(sigma_minus / (np.exp(-2*1j*psi) * (1+ a*b*z) * np.exp(1j*2*lambda_a)))
    phi = pytools.modpi(phi)

    # Amplitude, unambiguous
    rho = np.abs(sigma_minus / (np.exp(-2*1j*psi) * (1+ a*b*z) * np.exp(1j*2*lambda_a)))
    ttheta2 = np.sqrt(a)
    d = 1/(4*rho) * np.sqrt(5/np.pi) * 1./((1+ttheta2)**2 * (1+tiota2)**2)
    beta = np.arcsin(sbeta)
    inc = np.arccos(ciota)

    params = {}
    params['dist'] = d * injdist
    params['inc'] = inc
    params['phi'] = phi
    params['lambda'] = lambd
    params['beta'] = beta
    params['psi'] = psi

    return params

def jacobian_map_simple_response_22(params, params_map, injdist):

    d = params['dist'] / injdist
    inc = params['inc']
    beta = params['beta']

    Aplus = params_map['Aplus']
    Aminus = params_map['Aminus']

    ttheta2 = np.tan(1./2 * (np.pi/2-beta))**2
    tiota2 = np.tan(1./2 * inc)**2

    return (5/np.pi)**2 * 1./(32*d**3) * 1./(Aplus*Aminus) * (1+ttheta2**2)**2 * (1-ttheta2)**2 * tiota2**3 / (1+ttheta2)**6 / (1+tiota2)**6

def complete_params_degen_response_22(params, injdist):

    params_map = map_params_simple_response_22(params, injdist)

    params_complete = copy.deepcopy(params)
    for p in ['Aplus', 'Aminus', 'Phiplus', 'Phiminus', 'indexpsi']:
        params_complete[p] = params_map[p]
    params_complete['Phis'] = pytools.mod_interval(1./2 * (params_complete['Phiplus'] + params_complete['Phiminus']), [-np.pi/2, np.pi/2])
    params_complete['Phia'] = pytools.mod_interval(1./2 * (params_complete['Phiplus'] - params_complete['Phiminus']), [-np.pi/2, np.pi/2])

    return params_complete
