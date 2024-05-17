#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Standalone EOBNRv2HMROM inspiral-merger-ringdown GW waveform model
    for binary black hole coalescences.
"""

from __future__ import print_function

import numpy as np
cimport numpy as np
from math import cos
import copy

from lisabeta.pyconstants cimport *
from lisabeta.struct.pystruct cimport *


cdef extern from "struct.h":

    ctypedef struct ListAmpPhaseFDMode:
        AmpPhaseFDMode*              hlm;
        int                          l;
        int                          m;
        ListAmpPhaseFDMode*          next;

    ListAmpPhaseFDMode* ListAmpPhaseFDMode_GetMode(
    	   ListAmpPhaseFDMode* list,  # List structure to get this mode from
    	   int l,                     # Mode number l
    	   int m);                    # Mode number m

    ListAmpPhaseFDMode* ListAmpPhaseFDMode_Destroy(
    	   ListAmpPhaseFDMode* list); # List structure to destroy

cdef extern from "EOBNRv2HMROM.h":
    int SimEOBNRv2HMROMExtTF2(
        ListAmpPhaseFDMode** listhlm, # Output: list of modes, FD amp/phase
        int nbmode,                   # Number of modes to generate
        double Mf_match,              # Match freq TF2/EOBNRv2HMROM (geom units)
        double minf,                  # Minimum frequency required (Hz)
        int tagexthm,                 # Tag for extension of the higher modes
        double deltatRef,             # Time shift (peak of h22 at deltatRef)
        double phiRef,                # Phase at reference frequency
        double fRef,                  # Ref frequency (Hz); 0 for max Mf of ROM
        double m1SI,                  # Mass of companion 1 (kg)
        double m2SI,                  # Mass of companion 2 (kg)
        double distance,              # Distance of source (m)
        int setphiRefatfRef);         # Flag: setting FD phase to phiRef at fRef

cdef class EOBNRv2HMROM:
    """ Generate EOBNRv2HMROM IMR frequency-domain waveform with higher modes.
    """

    cdef ListAmpPhaseFDMode* listhlm  # pointer to waveform structure

    cdef m1_SI                # Mass of companion 1 (kg)
    cdef m2_SI                # Mass of companion 2 (kg)
    cdef dist_SI              # Distance of source (m)
    cdef f_min                # Minimum frequency required (Hz)
    cdef deltatRef            # Time shift (peak of h22 at deltatRef)
    cdef phiRef               # Reference phase at fRef (rad)
    cdef fRef                 # Reference frequency (Hz)
    cdef public object modes  # List of modes (l,m)

    cdef hlm                  # Dictionary of modes

    #cdef modes_default
    modes_ROM = [(2,2), (2,1), (3,3), (4,4), (5,5)]

    def __init__(self,
                 m1_SI, m2_SI, dist_SI, f_min, deltatRef, phiRef, fRef,
                 modes=modes_ROM):
        """Constructor
        Arguments:
          m1_SI                 # Mass of companion 1 (kg)
          m2_SI                 # Mass of companion 2 (kg)
          dist_SI               # Distance of source (m)
          f_min                 # Minimum frequency required (Hz)
          deltatRef             # Time shift (peak of h22 at deltatRef)
          phiRef                # Reference phase at fRef (rad)
          fRef                  # Reference frequency (Hz)
        Keyword arguments:
          modes                 # List of modes to return (all are generated)
        """
        # arguments are checked in the C waveform generator
        self.m1_SI = m1_SI
        self.m2_SI = m2_SI
        self.f_min = f_min
        self.deltatRef = deltatRef
        self.phiRef = phiRef
        self.fRef = fRef
        self.dist_SI = dist_SI
        self.modes = modes

        self.listhlm = NULL

        # We generate all modes, then select user-specified modes for output
        cdef int nbmode = 5
        cdef double Mf_match = 0.
        cdef int tagexthm = 1
        cdef setphiRefatfRef = 1
        ret = SimEOBNRv2HMROMExtTF2(
            &self.listhlm,
            nbmode,
            Mf_match,
            f_min,
            tagexthm,
            deltatRef,
            phiRef,
            fRef,
            m1_SI,
            m2_SI,
            dist_SI,
            setphiRefatfRef
        );
        if ret != 0:
            raise ValueError("Call to SimEOBNRv2HMROMExtTF2() failed.")

        # Read the modes in a dictionary
        # Direct copy of C double array to numpy via a MemoryView
        cdef AmpPhaseFDMode* Chlm = NULL
        self.hlm = {}
        cdef double[::1] view_freq_amp
        cdef double[::1] view_amp_real
        cdef double[::1] view_amp_imag
        cdef double[::1] view_freq_phase
        cdef double[::1] view_phase
        for lm in self.modes:
            (l,m) = (lm[0], lm[1])
            self.hlm[lm] = {}
            if not lm in self.modes_ROM:
                raise ValueError('Mode not allowed: (%d, %d)' % (l, m))
            Chlm = ListAmpPhaseFDMode_GetMode(self.listhlm, l, m).hlm
            view_freq_amp = \
                        <(double)[:Chlm.freq_amp.size]> Chlm.freq_amp.data
            view_amp_real = \
                        <(double)[:Chlm.amp_real.size]> Chlm.amp_real.data
            view_amp_imag = \
                        <(double)[:Chlm.amp_imag.size]> Chlm.amp_imag.data
            view_freq_phase = \
                        <(double)[:Chlm.freq_phase.size]> Chlm.freq_phase.data
            view_phase = \
                        <(double)[:Chlm.phase.size]> Chlm.phase.data
            self.hlm[lm]['freq_amp'] = np.asarray(view_freq_amp)
            self.hlm[lm]['amp_real'] = np.asarray(view_amp_real)
            self.hlm[lm]['amp_imag'] = np.asarray(view_amp_imag)
            self.hlm[lm]['freq_phase'] = np.asarray(view_freq_phase)
            self.hlm[lm]['phase'] = np.asarray(view_phase)

    def __dealloc__(self):
        """Destructor
        """
        if self.listhlm != NULL:
            ListAmpPhaseFDMode_Destroy(self.listhlm)

    # NOTE: to return a copy of the modes, copy.deepcopy is noticeably slower
    def get_waveform(self):
        hlm = {}
        for lm in self.modes:
            (l,m) = (lm[0], lm[1])
            hlm[lm] = {}
            hlm[lm]['freq_amp'] = np.copy(self.hlm[lm]['freq_amp'])
            hlm[lm]['amp_real'] = np.copy(self.hlm[lm]['amp_real'])
            hlm[lm]['amp_imag'] = np.copy(self.hlm[lm]['amp_imag'])
            hlm[lm]['freq_phase'] = np.copy(self.hlm[lm]['freq_phase'])
            hlm[lm]['phase'] = np.copy(self.hlm[lm]['phase'])
        return hlm
