#
# Copyright (C) 2020 Sylvain Marsat.
#
#


"""
    Python functions for inference with emcee (ensemble sampler, stretch-move)
    with the addition of multimodal jumps in extrinsic parameters.
"""


import time
import numpy as np
import copy
import h5py

import lisabeta.inference.inference as inference

################################################################################
# emcee-like sampler, allowing for a proposal in extra dimensions (mode hopping)
# TODO: include wrapping of phase parameters
# TODO: print info in a user-friendly way
# TODO: allow for checks like m1>m2 in prior_check
# TODO: clean up notation between x_physical and x_extended
# TODO: jump proposal is wasted sometimes by staying in place (50% with 2 modes)
# TODO: have some protection against very wrong prior bounds
# TODO: prior bounds is independent of folding
# TODO: have seen errors with acor of the type:
    # File "/Users/marsat/miniconda3/envs/py36/lib/python3.6/site-packages/acor-1.1.1-py3.6-macosx-10.9-x86_64.egg/acor/acor.py", line 33, in acor
    #     return _acor.acor(np.array(data), maxlag)
    # RuntimeError: D was negative in acor. Can't calculate sigma.

# TODO: make a freely specifiable parameter
# Hardcoded a=2, law 1/sqrt(z) on [1/a, a] = [1/2, 2]
def draw_z():
    u = np.random.uniform()
    return 1./2 * (1.+u)**2

def stretch_move(x, x_ensemble):
    index = np.random.randint(len(x_ensemble))
    x0 = x_ensemble[index]
    z = draw_z()
    y = x0 + z * (x - x0)
    return y, z

def stretch_update(x, lnlike_val, lnpost_val, x_ensemble, lnlikelihood, prior, prior_bounds=None, dim_extra=0, p_extra=0, map_extra=None, proposal_extra=None):

    x_new, lnlike_new, lnpost_new, accept = x, lnlike_val, lnpost_val, False

    dim = len(x) - dim_extra

    x_prop = x.copy()
    # Update in the extra dimensions
    if dim_extra>0 and np.random.binomial(1, p_extra):
        x_prop[dim:] = proposal_extra(x[dim:])
        z = 1.
    # Normal stretch-move update for ordinary dimensions
    else:
        x_prop[:dim], z = stretch_move(x[:dim], x_ensemble[:,:dim])

    # If using extra dimensions, map back to the true point by unfolding the extra dimensions
    if dim_extra>0:
        x_prop_true = map_extra(x_prop)
    else:
        x_prop_true = x_prop

    if inference.prior_check(x_prop[:dim], prior_bounds):
        lnlike_prop = lnlikelihood(x_prop_true)
        prior_prop = prior(x_prop_true)
        lnpost_prop = lnlike_prop + np.log(prior_prop)
        # We assume we always have a sensible lnlike, lnpost
        # if post_prop==0. and post_val==0.:
        #     p = np.fmin(1., z**(dim-1))
        # elif post_val==0.:
        #     p = 1.
        # else:
        p = np.fmin(1., z**(dim-1) * np.exp(lnpost_prop - lnpost_val))
        if np.random.binomial(1, p):
            x_new = x_prop
            lnlike_new = lnlike_prop
            lnpost_new = lnpost_prop
            accept = True

    return x_new, lnlike_new, lnpost_new, accept


# Main multiemcee function
# TODO: print_info, n_iter_info very rudimentary at the moment
def multiemcee_run(lnlikelihood, prior, nwalkers, niter, xini, prior_bounds=None, dim_extra=0, p_extra=0, map_extra=None, proposal_extra=None, seed=None, print_info=False, n_iter_info=10):
    # Random seed
    np.random.seed(seed=seed)
    # Check inputs
    if not nwalkers%2==0:
        raise ValueError('Provide an even number of walkers (split in 2 groups).')
    if not nwalkers==len(xini):
        raise ValueError('nwalkers and xini differ in length.')
    # nw is the number of walkers in each group
    nw = nwalkers//2
    # Initialize walkers with the input xini
    mask = np.full(nwalkers, False, dtype=bool)
    mask[:nw] = True
    np.random.shuffle(mask)
    x_1 = xini[mask]
    x_2 = xini[np.logical_not(mask)]

    # Output arrays for the whole chain, likelihood/posterior values, acceptance
    dim_chain = xini.shape[1]
    chain_shape = (nwalkers, max(1, niter), dim_chain) # niter=0 means we do not iterate
    chain = np.zeros(chain_shape, dtype=float)
    lnlikevals = np.full((nwalkers, niter), 0., dtype=float)
    lnpostvals = np.full((nwalkers, niter), 0., dtype=float)
    acceptvals = np.full((nwalkers, niter), False, dtype=bool)

    # If n_iter=0, we don't even compute likelihoods/priors
    # Simply return the inputs as they are then, with 0s for like, prior
    if niter==0:
        for k in range(nw):
            chain[k,0] = x_1[k]
            chain[nw+k,0] = x_2[k]
        return chain, lnlikevals, lnpostvals, acceptvals

    # Structure to hold the current likelihood, posterior, acceptance
    lnlike_1 = np.zeros(nw, dtype=float)
    lnlike_2 = np.zeros(nw, dtype=float)
    lnpost_1 = np.zeros(nw, dtype=float)
    lnpost_2 = np.zeros(nw, dtype=float)
    accept_1 = np.zeros(nw, dtype=bool)
    accept_2 = np.zeros(nw, dtype=bool)
    dim = dim_chain - dim_extra
    for k in range(nw):
        lnlike_1[k] = lnlikelihood(x_1[k][:dim])
        lnlike_2[k] = lnlikelihood(x_2[k][:dim])
        lnpost_1[k] = np.log(prior(x_1[k][:dim])) + lnlike_1[k]
        lnpost_2[k] = np.log(prior(x_2[k][:dim])) + lnlike_2[k]
        # By convention, set the first acceptance to true
        accept_1[k] = True
        accept_2[k] = True

    # Main loop over iterations
    for i in range(niter):
        if print_info:
            if i%n_iter_info == 0:
                print("n_iter: %d/%d" % (i,niter))
        # Update the 1st group, given the 2nd group
        for k in range(nw):
            x_1[k], lnlike_1[k], lnpost_1[k], accept_1[k] = stretch_update(x_1[k], lnlike_1[k], lnpost_1[k], x_2, lnlikelihood, prior, prior_bounds=prior_bounds, dim_extra=dim_extra, p_extra=p_extra, map_extra=map_extra, proposal_extra=proposal_extra)
            chain[k,i] = x_1[k]
            lnlikevals[k,i] = lnlike_1[k]
            lnpostvals[k,i] = lnpost_1[k]
            acceptvals[k,i] = accept_1[k]
        # Update the 2nd group, given the 1st group
        for k in range(nw):
            x_2[k], lnlike_2[k], lnpost_2[k], accept_2[k] = stretch_update(x_2[k], lnlike_2[k], lnpost_2[k], x_1, lnlikelihood, prior, prior_bounds=prior_bounds, dim_extra=dim_extra, p_extra=p_extra, map_extra=map_extra, proposal_extra=proposal_extra)
            chain[nw+k,i] = x_2[k]
            lnlikevals[nw+k,i] = lnlike_2[k]
            lnpostvals[nw+k,i] = lnpost_2[k]
            acceptvals[nw+k,i] = accept_2[k]

    return chain, lnlikevals, lnpostvals, acceptvals

def unfold_chain(chain, dim_extra, map_extra):
    n = len(chain)
    dim = chain.shape[1] - dim_extra
    chain_unfold = np.zeros((n, dim), dtype=float)
    for i in range(n):
        chain_unfold[i] = map_extra(chain[i])
    return chain_unfold
