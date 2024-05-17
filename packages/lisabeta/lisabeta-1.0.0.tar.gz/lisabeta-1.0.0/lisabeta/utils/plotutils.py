#
# Copyright (C) 2019 Sylvain Marsat
#


"""
    Python plotting tools.
"""

from __future__ import absolute_import, division, print_function
import sys
if sys.version_info[0] == 2:
    from future_builtins import map, filter


import copy
import json
import h5py
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import lisabeta.tools.pytools as pytools
import lisabeta.lisa.pyresponse as pyresponse
import lisabeta.lisa.lisatools as lisatools
import lisabeta.lisa.lisa_fisher as lisa_fisher
import lisabeta.utils.corner_covar as corner_covar


################################################################################
# Plotting functions and options
################################################################################

################################################################################
# Functions to plot arrays
# Input format :
# ax axes object (for subplot use)
# arg data sequence [data1, [colx1, coly1]], ...
# kwargs options : domain (figsize now at the level of subplot)
# allow for two data formats, distinguished by wether the 2nd arg in the list is a numpy array or not :
# i) [nparray d, cols [i,j]] : datax = d[:,i], datay = d[:,j]
# ii) [nparray datax, nparray datay] directly
# typical usage for continuous color map: [cm, cmb] = ['inferno', [0.,0.9]] lplot(...,  colormap=cm, colormapbounds=cmb)
# Color palette stolen from seaborn package (deep, with reshuffled ordering)
# SEABORN_PALETTES = dict(
#     deep=["#4C72B0", "#55A868", "#C44E52",
#           "#8172B2", "#CCB974", "#64B5CD"],
#     muted=["#4878CF", "#6ACC65", "#D65F5F",
#            "#B47CC7", "#C4AD66", "#77BEDB"],
#     pastel=["#92C6FF", "#97F0AA", "#FF9F9A",
#             "#D0BBFF", "#FFFEA3", "#B0E0E6"],
#     bright=["#003FFF", "#03ED3A", "#E8000B",
#             "#8A2BE2", "#FFC400", "#00D7FF"],
#     dark=["#001C7F", "#017517", "#8C0900",
#           "#7600A1", "#B8860B", "#006374"],
#     colorblind=["#0072B2", "#009E73", "#D55E00",
#                 "#CC79A7", "#F0E442", "#56B4E9"]
#)
# Added colors by hand:
# import matplotlib._color_data as mcd
# mcd.CSS4_COLORS['orange']
# '#FFA500'
# mcd.CSS4_COLORS['sienna']
# '#A0522D'
rc_params = {'backend': 'ps',
            'font.family': 'Times New Roman',
            'font.sans-serif': ['Bitstream Vera Sans'],
            'axes.unicode_minus':False,
            'text.usetex':True,
            'axes.grid':True,
            'grid.linestyle':':',
            'grid.linewidth':1.,
            'hist.bins':50,
            'axes.labelsize':16,
            'axes.titlesize':16,
            'xtick.labelsize':16,
            'ytick.labelsize':16,
            'legend.fontsize':16,
            'savefig.bbox':'tight',
            'savefig.transparent':True,
            'figure.dpi':300}
plt.rcParams.update(rc_params)

plotpalette = ["#4C72B0", "#C44E52", "#CCB974", "#55A868", "#8172B2", "#64B5CD", '#FFA500', '#A0522D']
def lplot(ax, *args, **kwargs):
    rangex = kwargs.pop('rangex', [])
    rangey = kwargs.pop('rangey', [])
    ds = kwargs.pop('downsample', 1)
    size = kwargs.pop('figsize', (8, 4))
    grid = kwargs.pop('grid', True)
    colormap = kwargs.pop('colormap', None)
    colormapbounds = kwargs.pop('colormapbounds', [0.,1.])
    colors = kwargs.pop('colors', None)
    linestyles = kwargs.pop('linestyles', None)
    linewidths = kwargs.pop('linewidths', None)
    markers = kwargs.pop('markers', None)
    labels = kwargs.pop('labels', None)
    log_xscale = kwargs.pop('log_xscale', False)
    log_yscale = kwargs.pop('log_yscale', False)
    n = len(args)
    if colors is None: # colors option supersedes colormap
        if colormap is not None:
            colorm = cm.get_cmap(colormap)
            colors = [colorm(x) for x in np.linspace(colormapbounds[0],
                                                     colormapbounds[1], n)]
        else:
            #defaultcolorlist = plt.rcParams['axes.prop_cycle'].by_key()['color']
            defaultcolorlist = plotpalette
            colors = pytools.fold_list(defaultcolorlist, n)
    if linestyles is None:
        linestyles = ['-']*n
    if linewidths is None:
        linewidths = [1]*n
    if markers is None:
        markers = [None]*n
    if labels is None:
        labels = [None]*n
    f = plt.figure(0, figsize=size)
    minxvals = np.zeros(n)
    maxxvals = np.zeros(n)
    minyvals = np.zeros(n)
    maxyvals = np.zeros(n)
    avyvals = np.zeros(n)
    for i, x in enumerate(args):
        if type(x[1]) is np.ndarray:
            data = pytools.restrict_data_soft(np.array([x[0][::ds], x[1][::ds]]).T, rangex)
            col1, col2 = [0, 1]
        else:
            data = pytools.restrict_data_soft(x[0][::ds], rangex)
            col1, col2 = x[1]
        if not (log_xscale and log_yscale):
            minxvals[i] = data[0, col1]
        else: # Restrict to the first non-zero value of y - convenient for log-x plots (also always exclude x=0)
            datax = data[:, col1]
            datay = data[:, col2]
            if datax[0]==0.:
                datax = datax[1:]
                datay = datay[1:]
            minxvals[i] = datax[(datay > 0)][0]
        maxxvals[i] = data[-1, col1]
        minyvals[i] = min(data[:, col2])
        maxyvals[i] = max(data[:, col2])
        avyvals[i] = np.average(data[:, col2])
        ax.plot(data[:,col1], data[:,col2], color=colors[i], linestyle=linestyles[i], linewidth=linewidths[i], marker=markers[i], label=labels[i], **kwargs)
    if rangex:
        ax.set_xlim(rangex[0], rangex[1])
    else:
        ax.set_xlim(min(minxvals), max(maxxvals))
    if rangey:
        ax.set_ylim(rangey[0], rangey[1])
    else:
        if log_yscale:
            minyvalplot = max(min(minyvals), 1e-8*np.average(avyvals))
            ax.set_ylim(1./2*minyvalplot, 2*max(maxyvals))
        else:
            if max(maxyvals)==min(minyvals): # Collapsed case: plot a constant, scale is arbitrary, just plot +-1.
                ax.set_ylim(min(minyvals) - 1., max(maxyvals) + 1.)
            else:
                margin = 0.1 * (max(maxyvals) - np.average(avyvals))
                ax.set_ylim(min(minyvals) - margin, max(maxyvals) + margin)
    if log_xscale:
        ax.set_xscale('log')
    if log_yscale:
        ax.set_yscale('log')
    if grid:
        ax.grid('on', linestyle=':')
def llogplot(ax, *arg, **kwargs):
    args = (ax,) + arg
    return lplot(*args, log_yscale=True, **kwargs)
def lloglinearplot(ax, *arg, **kwargs):
    args = (ax,) + arg
    return lplot(*args, log_xscale=True, **kwargs)
def lloglogplot(ax, *arg, **kwargs):
    args = (ax,) + arg
    return lplot(*args, log_xscale=True, log_yscale=True, **kwargs)

################################################################################
# Functions to parse and manipulate parameter files and posterior files
################################################################################

# Load posterior file
# Assumed format: param1 param2 ... paramn lnL, parameters read from .json
# Fixed parameters completed with injected value read from .json
def load_params_posterior_lisa_smbh(params_file, posterior_file, format='multiemcee', load_fisher=True):

    params_post = {}

    # Load input params
    with open(params_file, 'r') as input_file:
        input_params = json.load(input_file)
    source_params = input_params['source_params']
    waveform_params = input_params['waveform_params']
    run_params = input_params['run_params']
    source_params_are_Lframe = source_params.get('Lframe', False)
    prior_params = input_params['prior_params']
    t0 = waveform_params.get('t0', 0.)

    # If source params are given in the Lframe, convert to SSB
    if source_params_are_Lframe:
        source_params_SSBframe = lisatools.convert_Lframe_to_SSBframe(
                                    source_params,
                                    t0=t0,
                                    frozenLISA=waveform_params['frozenLISA'])
        source_params_Lframe = source_params.copy()
    else:
        source_params_SSBframe = source_params.copy()
        source_params_Lframe = lisatools.convert_SSBframe_to_Lframe(
                                    source_params,
                                    t0=t0,
                                    frozenLISA=waveform_params['frozenLISA'])
    source_params_SSBframe['t0'] = t0
    source_params_Lframe['t0'] = t0

    # Load posterior from file
    if format=='multinest':
        post_raw = np.genfromtxt(posterior_file)
        post = {}
        for i,p in enumerate(prior_params['infer_params']):
            post[p] = post_raw[:,i]
        post['lnL'] = post_raw[:,-1]
    elif format=='multiemcee':
        with h5py.File(posterior_file, 'r') as hf:
            post = {}
            for p in prior_params['infer_params']:
                post[p] = hf[p][:]
            post['lnL'] = hf['lnlike'][:]
            post['lnpost'] = hf['lnpost'][:]
    elif format=='multifisher':
        with h5py.File(posterior_file, 'r') as hf:
            post = {}
            for p in prior_params['infer_params']:
                post[p] = hf[p][:]
            post['lnL'] = hf['lnlike'][:]
            post['lnpost'] = hf['lnpost'][:]
            post['lnweight'] = hf['lnweight'][:]
    else:
        raise ValueError('Format not recognized')

    # For multiemcee, we also load fisher
    if not format=='multinest' and load_fisher:
        with h5py.File(posterior_file, 'r') as hf:
            params_post['fishercov'] = lisa_fisher.read_h5py_fishercov(hf['/fishercov'])

    # Number of samples
    n = len(post['lnL'])

    # Complete with injected values for fixed parameters
    # NOTE: for multiemcee, post is already complete for fixed params
    # We re-do it here, not optimal
    # NOTE: fixed_params is list_params minus infer_params
    # but list_params is optional in the json; if absent, use source_params
    default_list_params = source_params.copy()
    default_list_params.pop('Lframe', False)
    list_params = prior_params.get('list_params', default_list_params.keys())
    infer_params = prior_params['infer_params']
    fixed_params = [p for p in list_params if p not in infer_params]
    for p in fixed_params:
        if run_params.get('sample_Lframe', False):
            post[p] = np.full(n, source_params_Lframe[p])
        else:
            post[p] = np.full(n, source_params_SSBframe[p])

    # Conversion of the posterior Lfame/SSBframe will happen outside for now
    post['Lframe'] = run_params.get('sample_Lframe', False)

    # Complete mass and spin parameters
    source_params_SSBframe = pytools.complete_mass_params(source_params_SSBframe)
    source_params_SSBframe = pytools.complete_spin_params(source_params_SSBframe)
    source_params_Lframe = pytools.complete_mass_params(source_params_Lframe)
    source_params_Lframe = pytools.complete_spin_params(source_params_Lframe)
    post = pytools.complete_mass_params(post)
    post = pytools.complete_spin_params(post)

    params_post['injparams_SSBframe'] = source_params_SSBframe
    params_post['injparams_Lframe'] = source_params_Lframe
    params_post['waveform_params'] = waveform_params
    params_post['prior_params'] = prior_params
    params_post['run_params'] = run_params
    params_post['post'] = post
    return params_post

# Load posterior file
# Assumed format: param1 param2 ... paramn lnL, parameters read from .json
# Fixed parameters completed with injected value read from .json
def load_params_posterior_lisa_sobh(params_file, posterior_file, format='multiemcee', load_fisher=True, AGN_params=False):

    params_post = {}

    # Load input params
    with open(params_file, 'r') as input_file:
        input_params = json.load(input_file)
    source_params = input_params['source_params']
    waveform_params = input_params['waveform_params']
    run_params = input_params['run_params']
    source_params_phys = source_params.copy()
    source_params_are_Lframe = source_params_phys.pop('Lframe', False)
    prior_params = input_params['prior_params']
    t0 = waveform_params.get('t0', 0.)

    # If source params are given in the Lframe, convert to SSB
    if source_params_are_Lframe:
        raise ValueError('L-frame not relevant/supported for SBHBs.')
    source_params_SSBframe = source_params.copy()

    # Load posterior from file
    if format=='multinest':
        post_raw = np.genfromtxt(posterior_file)
        post = {}
        for i,p in enumerate(prior_params['infer_params']):
            post[p] = post_raw[:,i]
        post['lnL'] = post_raw[:,-1]
    elif format=='multiemcee':
        with h5py.File(posterior_file, 'r') as hf:
            post = {}
            for p in prior_params['infer_params']:
                post[p] = hf[p][:]
            post['lnL'] = hf['lnlike'][:]
            post['lnpost'] = hf['lnpost'][:]
    elif format=='multifisher':
        with h5py.File(posterior_file, 'r') as hf:
            post = {}
            for p in prior_params['infer_params']:
                post[p] = hf[p][:]
            post['lnL'] = hf['lnlike'][:]
            post['lnpost'] = hf['lnpost'][:]
            post['lnweight'] = hf['lnweight'][:]
    else:
        raise ValueError('Format not recognized')

    # For multiemcee, we also load fisher
    if not format=='multinest' and load_fisher:
        with h5py.File(posterior_file, 'r') as hf:
            params_post['fishercov'] = lisa_fisher.read_h5py_fishercov(hf['/fishercov'])

    # Number of samples
    n = len(post['lnL'])

    # Complete with injected values for fixed parameters
    # NOTE: for multiemcee, post is already complete for fixed params
    # We re-do it here, not optimal
    infer_params = prior_params['infer_params']
    fixed_params = [p for p in source_params_phys.keys() if p not in infer_params]
    for p in fixed_params:
        if run_params.get('sample_Lframe', False):
            post[p] = np.full(n, source_params_Lframe[p])
        else:
            post[p] = np.full(n, source_params_SSBframe[p])

    # Conversion of the posterior Lfame/SSBframe will happen outside for now
    post['Lframe'] = run_params.get('sample_Lframe', False)
    if post['Lframe']:
        raise ValueError('L-frame not relevant/supported for SBHBs.')

    # Complete mass and spin parameters
    source_params_SSBframe = pytools.complete_mass_params(source_params_SSBframe)
    source_params_SSBframe = pytools.complete_spin_params(source_params_SSBframe)
    post = pytools.complete_mass_params(post)
    post = pytools.complete_spin_params(post)
    # Only relevant for SOBH_AGN case
    if AGN_params:
        source_params_SSBframe = pytools.complete_AGN_params(source_params_SSBframe)
        post = pytools.complete_AGN_params(post)

    params_post['injparams_SSBframe'] = source_params_SSBframe
    params_post['waveform_params'] = waveform_params
    params_post['prior_params'] = prior_params
    params_post['run_params'] = run_params
    params_post['post'] = post
    return params_post

# Function taken from J.Baker's corner-fisher.py
def read_covariance(file):
    pars=[]
    done=False
    trycount=0
    with open(file,'r') as f:
        line="#"
        while("#" in line): line=f.readline() #Skip comment
        for val in line.split():
            pars.append(float(val))
        Npar=len(pars)
        while(not "#Covariance" in line):line=f.readline() #Skip until the good stuff
        covar=np.zeros((Npar,Npar))
        i=0
        for par in pars:
            line=f.readline()
            covar[i]=np.array(line.split())
            i+=1
    return covar
def read_fisher(file):
    pars=[]
    done=False
    trycount=0
    with open(file,'r') as f:
        line="#"
        while("#" in line): line=f.readline() #Skip comment
        for val in line.split():
            pars.append(float(val))
        Npar=len(pars)
        while(not "#Fisher" in line):line=f.readline() #Skip until the good stuff
        covar=np.zeros((Npar,Npar))
        i=0
        for par in pars:
            line=f.readline()
            covar[i]=np.array(line.split())
            i+=1
    return covar


# Compute posterior values for individual posterior samples by multiplying with the prior
# Assumes a np array for the posterior samples, the last column being the likelihood values
# Assumes flat prior in time, phase, polarization, sphere prior in inclination and sky position
# Normalization is arbitrary
# Parameter order assumed : m1, m2, tRef, dist, phiRef, inc, lambda, beta, pol, loglikelihood
def compute_posterior(posterior, flatdistprior=False, logflatmassprior=False):
    # sort posterior samples, highest loglikelihood first
    posterior = (posterior[posterior[:,9].argsort()])[::-1]
    if flatdistprior and logflatmassprior:
        def prior(x):
            return 1./x[0] * 1./x[1] * np.sin(x[5]) * np.cos(x[7])
    elif flatdistprior and not logflatmassprior:
        def prior(x):
            return np.sin(x[5]) * np.cos(x[7])
    elif not flatdistprior and logflatmassprior:
        def prior(x):
            return 1./x[0] * 1./x[1] * x[3]**2 * np.sin(x[5]) * np.cos(x[7])
    elif not flatdistprior and not logflatmassprior:
        def prior(x):
            return  x[3]**2 * np.sin(x[5]) * np.cos(x[7])
    priorvalues = np.array(list(map(prior, posterior)))
    # normalize (arbitrarily) to the prior value of highest likelihood (injection)
    priorvalues = priorvalues / priorvalues[0]
    posteriorvalues = np.log(priorvalues) + posterior[:,9]
    return np.concatenate((posterior, np.array([posteriorvalues]).T), axis=1)



################################################################################
## Automated parameter labels and scales
################################################################################

# Parameter labels
unit_M_dict = {
    '1e8':r'$(10^{8}\mathrm{M}_{\odot})$',
    '1e7':r'$(10^{7}\mathrm{M}_{\odot})$',
    '1e6':r'$(10^{6}\mathrm{M}_{\odot})$',
    '1e5':r'$(10^{5}\mathrm{M}_{\odot})$',
    '1e4':r'$(10^{4}\mathrm{M}_{\odot})$',
    '1e3':r'$(10^{3}\mathrm{M}_{\odot})$',
    '1e2':r'$(\mathrm{M}_{\odot})$',
    '1e1':r'$(\mathrm{M}_{\odot})$',
    '1':r'$(\mathrm{M}_{\odot})$'}
unit_D_dict = {
    'Gpc':r'$(\mathrm{Gpc})$',
    'Mpc':r'$(\mathrm{Mpc})$'}
unit_t_dict = {
    's':r'$(\mathrm{s})$',
    'ms':r'$(\mathrm{ms})$'}
unit_f_dict = {
    'Hz':r'$(\mathrm{Hz})$',
    'mHz':r'$(\mathrm{mHz})$'}
scale_dict_M = {'1e8':1e8, '1e7':1e7, '1e6':1e6, '1e5':1e5, '1e4':1e4, '1e3':1e3, '1e2':1e2, '1e1':10., '1':1.}
scale_dict_D = {'Gpc':1e3, 'Mpc':1.}
scale_dict_t = {'s':1., 'ms':1e-3}
scale_dict_f = {'Hz':1., 'mHz':1e-3}

# Display of parameter names
def param_label_dict(detector, scales, Lframe=False):
    unit_str_M = unit_M_dict[scales[0]]
    unit_str_D = unit_D_dict[scales[1]]
    unit_str_t = unit_t_dict[scales[2]]
    unit_str_f = unit_f_dict[scales[3]]
    res = {}
    if detector=='LISA':
        res = {
            'm1'     : r'$m_1 \;$' + unit_str_M,
            'm2'     : r'$m_2 \;$' + unit_str_M,
            'chi1'     : r'$\chi_1$',
            'chi2'     : r'$\chi_2$',
            'chis'     : r'$\chi_s$',
            'chia'     : r'$\chi_a$',
            'chip'     : r'$\chi_+$',
            'chim'     : r'$\chi_-$',
            'chiPN'    : r'$\chi_{\rm PN}$',
            'fstart' : r'$f_{\rm start} \;$' + unit_str_f,
            'dist'   : r'$D \;$' + unit_str_D,
            'phi'    : r'$\varphi \; (\mathrm{rad})$',
            'inc'    : r'$\iota \; (\mathrm{rad})$',
            'M'      : r'$M \;$' + unit_str_M,
            'q'      : r'$q$',
            'Mchirp' : r'$\mathcal{M}_c \;$' + unit_str_M,
            'eta'    : r'$\eta$',
            'Omega_AGN': r'$\Omega_{\rm AGN} \; (\mathrm{rad}.\mathrm{s}^{-1})$',
            'Rcostheta_AGN': r'$R/c \cos\theta_{\rm AGN} \; (\mathrm{s})$',
            'Rsintheta_AGN': r'$R/c \sin\theta_{\rm AGN} \; (\mathrm{s})$',
            'phi_AGN': r'$\phi_{\rm AGN} \; (\mathrm{rad})$',
            'R_AGN': r'$R_{\rm AGN} \; (M)$',
            'M_AGN': r'$M_{\rm AGN} \; (M_{\odot})$',
            'theta_AGN': r'$\theta_{\rm AGN} \; (\mathrm{rad})$',
            'Aplus': r'$A_+$',
            'Aminus': r'$A_-$',
            'Phiplus': r'$\Phi_+ \; (\mathrm{rad})$',
            'Phiminus': r'$\Phi_- \; (\mathrm{rad})$',
            'Phis': r'$\Phi_s \; (\mathrm{rad})$',
            'Phia': r'$\Phi_a \; (\mathrm{rad})$',
        }
        if not Lframe:
            res.update({
                'Deltat' : r'$\Delta t \;$' + unit_str_t,
                'lambda' : r'$\lambda \; (\mathrm{rad})$',
                'beta'   : r'$\beta \; (\mathrm{rad})$',
                'psi'    : r'$\psi \; (\mathrm{rad})$',
            })
        else:
            res.update({
                'Deltat' : r'$\Delta t_{L} \;$' + unit_str_t,
                'lambda' : r'$\lambda_{L} \; (\mathrm{rad})$',
                'beta'   : r'$\beta_{L} \; (\mathrm{rad})$',
                'psi'    : r'$\psi_{L} \; (\mathrm{rad})$',
            })
    elif detector=='LLV':
        res = {
            'm1'     : r'$m_1 \;$' + unit_str_M,
            'm2'     : r'$m_2 \;$' + unit_str_M,
            'chi1'     : r'$\chi_1$',
            'chi2'     : r'$\chi_2$',
            'chis'     : r'$\chi_s$',
            'chia'     : r'$\chi_a$',
            'chip'     : r'$\chi_+$',
            'chim'     : r'$\chi_-$',
            'chiPN'    : r'$\chi_{\rm PN}$',
            'Deltat' : r'$\Delta t \;$' + unit_str_t,
            'fstart' : r'$f_{\rm start} \;$' + unit_str_f,
            'dist'   : r'$D \;$' + unit_str_D,
            'phi'    : r'$\varphi \; (\mathrm{rad})$',
            'inc'    : r'$\iota \; (\mathrm{rad})$',
            'ra'     : r'$\mathrm{ra} \; (\mathrm{rad})$',
            'dec'    : r'$\mathrm{dec} \; (\mathrm{rad})$',
            'psi'    : r'$\psi \; (\mathrm{rad})$',
            'M'      : r'$M \;$' + unit_str_M,
            'q'      : r'$q$',
            'Mchirp' : r'$\mathcal{M}_c \;$' + unit_str_M,
            'eta'    : r'$\eta$'
        }
    return res

def automatic_scales(injparams, posterior):
    M = injparams['M']
    scale_M_int = min(8, max(int(np.floor(np.log(M)/np.log(10.))), 0))
    if scale_M_int<=2:
        scale_M = '1'
    else:
        scale_M = '1e' + str(scale_M_int)
    DL = injparams['dist']
    if DL>=1e3:
        scale_D = 'Gpc'
    else:
        scale_D = 'Mpc'
    if 'Deltat' in posterior.keys():
        Deltat_mean = np.abs(np.mean(posterior['Deltat']))
        if Deltat_mean>=0.1:
            scale_t = 's'
        else:
            scale_t = 'ms'
    else:
        scale_t = 's' # Default, not used
    if 'fstart' in posterior.keys():
        scale_fstart = 'mHz'
    else:
        scale_fstart = 'Hz' # Default, not used
    return [scale_M, scale_D, scale_t, scale_fstart]
def scale_posterior(posterior, scales):
    sM, sD, st, sf = scales
    post = copy.deepcopy(posterior)
    # Masses
    post['m1'][:] /= sM
    post['m2'][:] /= sM
    post['M'][:] /= sM
    post['Mchirp'][:] /= sM
    # Distance
    post['dist'][:] /= sD
    # Time
    if 'Deltat' in post.keys():
        post['Deltat'][:] /= st
    # Starting frequency for SBHBs
    if 'fstart' in post.keys():
        post['fstart'][:] /= sf
    return post
def scale_injparams(injparams, scales):
    sM, sD, st, sf = scales
    injpar = injparams.copy()
    # Masses
    injpar['m1'] /= sM
    injpar['m2'] /= sM
    injpar['M'] /= sM
    injpar['Mchirp'] /= sM
    # Distance
    injpar['dist'] /= sD
    # Time
    if 'Deltat' in injpar.keys():
        injpar['Deltat'] /= st
    # Starting frequency for SBHBs
    if 'fstart' in injpar.keys():
        injpar['fstart'] /= sf
    return injpar
# Assumed format for covariance: m1 m2 Deltat D phi inc lambda beta pol
def scale_fishcov(fishcov, scales):
    list_params = fishcov['list_params']
    fishcov_scaled = {}
    fishcov_scaled['params'] = copy.deepcopy(fishcov['params'])
    fishcov_scaled['list_params'] = copy.deepcopy(fishcov['list_params'])
    sM, sD, st, sf = scales
    scale_dict = {'m1':sM, 'm2':sM, 'Mchirp':sM, 'M':sM, 'q':1., 'eta':1., 'chi1':1., 'chi2':1., 'chip':1., 'chim':1., 'chis':1., 'chia':1., 'chiPN':1., 'dist':sD, 'Deltat':st, 'fstart':sf, 'phi':1., 'inc':1., 'lambda':1., 'beta':1., 'psi':1.}
    scaling = np.diag(np.array([1./scale_dict[p] for p in list_params]))
    invscaling = np.diag(np.array([scale_dict[p] for p in list_params]))
    fishcov_scaled['fisher'] = np.dot(scaling, np.dot(fishcov['fisher'], scaling))
    fishcov_scaled['cov'] = np.dot(scaling, np.dot(fishcov['cov'], scaling))
    fishcov_scaled['scales'] = scale_dict
    return fishcov_scaled

################################################################################
## Corner plot function, based on corner_covar, modification of corner.py
################################################################################

# Default levels for contours in 2d histogram - TODO: check the correspondence with 1,2,3sigma
contour_levels_2D_default = 1.0 - np.exp(-0.5 * np.linspace(1.0, 3.0, num=3) ** 2)

# Old default truth color: truth_color="#4682b4"
def corner_plot(injparams, posterior, add_posteriors=None, output=False, output_dir=None, output_file=None, histograms=True, fisher=False, fishercov=None, detector='LISA', params=['m1', 'm2', 'Deltat', 'dist', 'phi', 'inc', 'lambda', 'beta', 'psi'], params_range=None, Lframe=False, lnweight_threshold=-100., labels=None, scales=None, add_truths=None, color="k", add_colors=None, cov_color=None, show_truths=True, truth_color='k', truth_linestyle='-', add_truth_colors=None, add_truth_linestyles=None, bins=50, show_histograms=True, quantiles=[0.159, 0.5, 0.841], show_quantiles=True, levels=contour_levels_2D_default, plot_density=True, plot_contours=True, plot_datapoints=False, smooth=None, smooth1d=None, show_xtick_labels=True, show_ytick_labels=True, label_kwargs={"fontsize": 16}, show_titles=True, titles=None, plot_density_add_post=False, transparent=True, resize_fig=1.):

    # If required, transform to parameters in the L-frame or in the SSB-frame
    if Lframe:
        if not injparams.get('Lframe', False):
            injparams_plt = lisatools.convert_SSBframe_to_Lframe(injparams, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)
        else:
            injparams_plt = injparams
        if not posterior.get('Lframe', False):
            posterior_plt = lisatools.convert_SSBframe_to_Lframe(posterior, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)
        else:
            posterior_plt = posterior
        if add_posteriors is not None:
            add_posteriors_plt = []
            for add_post in add_posteriors:
                if not add_post.get('Lframe', False):
                    add_posteriors_plt += [lisatools.convert_SSBframe_to_Lframe(add_post, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)]
                else:
                    add_posteriors_plt += [add_post]
        else:
            add_posteriors_plt = None
        if add_truths is not None:
            add_truths_plt = []
            for add_truth in add_truths:
                if not add_truth.get('Lframe', False):
                    add_truths_plt += [lisatools.convert_SSBframe_to_Lframe(add_truth, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)]
                else:
                    add_truths_plt += [add_truth]
        else:
            add_truths_plt = None
    else:
        if injparams.get('Lframe', False):
            injparams_plt = lisatools.convert_Lframe_to_SSBframe(injparams, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)
        else:
            injparams_plt = injparams
        if posterior.get('Lframe', False):
            posterior_plt = lisatools.convert_Lframe_to_SSBframe(posterior, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)
        else:
            posterior_plt = posterior
        if add_posteriors is not None:
            add_posteriors_plt = []
            for add_post in add_posteriors:
                if add_post.get('Lframe', False):
                    add_posteriors_plt += [lisatools.convert_Lframe_to_SSBframe(add_post, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)]
                else:
                    add_posteriors_plt += [add_post]
        else:
            add_posteriors_plt = None
        if add_truths is not None:
            add_truths_plt = []
            for add_truth in add_truths:
                if add_truth.get('Lframe', False):
                    add_truths_plt += [lisatools.convert_Lframe_to_SSBframe(add_truth, t0=injparams['t0'], frozenLISA=False, LISAconst=pyresponse.LISAconstProposal)]
                else:
                    add_truths_plt += [add_truth]
        else:
            add_truths_plt = None

    # If not provided, determine automatically scales [M, D, t]
    if scales is None:
        scales = automatic_scales(injparams_plt, posterior_plt)
    scale_M, scale_D, scale_t, scale_f = scales
    scalefactors = scale_dict_M[scale_M], scale_dict_D[scale_D], scale_dict_t[scale_t], scale_dict_f[scale_f]
    injparams_plt = scale_injparams(injparams_plt, scalefactors)
    posterior_plt = scale_posterior(posterior_plt, scalefactors)
    if add_posteriors_plt is not None:
        add_posteriors_plt = list(map(lambda x: scale_posterior(x, scalefactors), add_posteriors))

    # Convert parameters and posteriors from dicts to numpy arrays
    injparams_plt = np.array([injparams_plt[p] for p in params])
    posterior_plt = np.array([posterior_plt[p] for p in params]).T
    if add_posteriors_plt is not None:
        add_posteriors_plt = list(map(lambda x: np.array([x[p] for p in params]).T, add_posteriors_plt))
    if add_truths is not None:
        add_truths = list(map(lambda x: np.array([x[p] for p in params]), add_truths))
    if show_truths:
        truths = injparams_plt
    else:
        truths = None

    # Process weights of individual samples if given
    weights = None
    if 'lnweight' in posterior.keys():
        mask = posterior['lnweight'] > lnweight_threshold
        posterior_plt = posterior_plt[mask]
        weights = np.exp(posterior['lnweight'][mask])
    if add_posteriors is not None:
        add_weights = [None] * len(add_posteriors)
        for i,add_post in enumerate(add_posteriors):
            if 'lnweight' in add_post.keys():
                mask = add_post['lnweight'] > lnweight_threshold
                add_posteriors_plt[i] = add_posteriors_plt[i][mask]
                add_weights[i] = [np.exp(add_post['lnweight'][mask])]

    # Covariance from the Fisher matrix
    if fisher:
        if fishercov is None:
            raise ValueError('Covariance matrix not specified.')
        if Lframe and not fishercov['Lframe']:
            raise ValueError('Covariance matrix not in the L-frame.')
        fishercov = scale_fishcov(fishercov, scalefactors)
        cov_list_params = fishercov['list_params']
        cov_cols = [cov_list_params.index(p) for p in params]
        cov_cols_cartesian = np.ix_(cov_cols, cov_cols)
        cov = fishercov['cov'][cov_cols_cartesian]
    else:
        cov = None

    # Labels
    if labels is None:
        label_dict = param_label_dict(detector, scales, Lframe)
        labels = list(map(lambda x: label_dict[x], params))

    # Main call to corner function
    fig, axes = corner_covar.corner(posterior_plt, cov=cov, bins=bins, params_range=params_range, levels=levels, weights=weights,
                                 labels=labels, label_kwargs=label_kwargs, color=color,
                                 truths=truths, add_truths=add_truths, truth_color=truth_color, truth_linestyle=truth_linestyle, add_truth_colors=add_truth_colors, add_truth_linestyles=add_truth_linestyles, plot_datapoints=plot_datapoints,
                                 smooth=smooth, smooth1d=smooth1d, show_histograms=show_histograms,
                                 quantiles=quantiles, show_quantiles=show_quantiles, plot_contours=plot_contours,
                                 show_xtick_labels=show_xtick_labels, show_ytick_labels=show_ytick_labels,
                                 show_titles=show_titles, titles=titles, plot_density=plot_density, resize_fig=resize_fig)

    # Overlay other posterior
    if add_posteriors_plt is not None:
        if add_colors is None:
            add_colors = [plotpalette[i % len(plotpalette)] for i in range(len(add_posteriors))]
        for i, add_post in enumerate(add_posteriors_plt):
            corner_covar.corner(add_post, figaxes=(fig, axes), cov=None, bins=bins, params_range=params_range, levels=levels, weights=add_weights[i],
                                     labels=labels, label_kwargs=label_kwargs, color=add_colors[i],
                                     truths=None, plot_datapoints=plot_datapoints,
                                     smooth=smooth, smooth1d=smooth1d, show_histograms=show_histograms,
                                     quantiles=quantiles, show_quantiles=show_quantiles, plot_contours=plot_contours,
                                     show_titles=False, titles=titles,
                                     show_xtick_labels=show_xtick_labels, show_ytick_labels=show_ytick_labels,
                                     plot_density=plot_density_add_post, no_fill_contours=True, resize_fig=resize_fig)

    # Output
    if output:
        if not output_dir:
            raise ValueError('output_dir not defined.')
        if not output_file:
            raise ValueError('output_file not defined.')
        fig.savefig(output_dir + output_file, bbox_inches='tight', transparent=transparent)
    else:
        return fig
