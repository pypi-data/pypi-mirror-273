#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython wrapping of C overlap tools.
"""

import numpy as np
cimport numpy as np

from lisabeta.pyconstants cimport *
from lisabeta.struct.pystruct cimport *
from lisabeta.tools.pyspline cimport *
import lisabeta.tools.pyspline as pyspline

def fresnel_integral(np.ndarray[np.float_t, ndim=1] freq,
                     np.ndarray[np.float_t, ndim=1] amp_real,
                     np.ndarray[np.float_t, ndim=1] amp_imag,
                     np.ndarray[np.float_t, ndim=1] phase,
                     real=True):
    """ Computes integral 4Re(\int h1 h2*/Sn) given the integrand (h1 h2*/Sn)
        Args:
          freq           # Input numpy array for the integrand frequencies
          amp_real       # Input numpy array for the integrand real amplitude
          amp_imag       # Input numpy array for the integrand imag amplitude
          phase          # Input numpy array for the integrand phase
        Keyword args:)
          real                # Return real part of integral (Default True)
    """

    # If the input is an empty array, return 0
    # Would typically happen if a mode is eliminated by time/frequency cuts
    if len(freq)==0 or len(amp_real)==0 or len(amp_imag)==0 or len(phase)==0:
        return 0.

    # Check input numpy arrays are suitable for views
    if not freq.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array freq is not C_CONTIGUOUS')
    if not amp_real.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array amp_real is not C_CONTIGUOUS')
    if not amp_imag.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array amp_imag is not C_CONTIGUOUS')
    if not phase.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array phase is not C_CONTIGUOUS')

    # Views of input numpy arrays
    cdef double* freq_data = <double *> &freq[0]
    cdef double* amp_real_data = <double *> &amp_real[0]
    cdef double* amp_imag_data = <double *> &amp_imag[0]
    cdef double* phase_data = <double *> &phase[0]
    cdef real_vector* Cfreq = real_vector_view(freq_data, freq.shape[0])
    cdef real_vector* Camp_real = real_vector_view(amp_real_data,
                                                   amp_real.shape[0])
    cdef real_vector* Camp_imag = real_vector_view(amp_imag_data,
                                                   amp_imag.shape[0])
    cdef real_vector* Cphase = real_vector_view(phase_data, phase.shape[0])

    #
    cdef CAmpPhaseFDData freqseries
    freqseries.freq = Cfreq
    freqseries.amp_real = Camp_real
    freqseries.amp_imag = Camp_imag
    freqseries.phase = Cphase

    # Compute integral
    cdef double complex integral_complex = ComputeFresnelIntegral(
        &freqseries
    );
    if real:
        integral = np.real(integral_complex)
    else:
        integral = integral_complex

    # Cleanup\
    if Cfreq != NULL:
        real_vector_view_free(Cfreq)
    if Camp_real != NULL:
        real_vector_view_free(Camp_real)
    if Camp_imag != NULL:
        real_vector_view_free(Camp_imag)
    if Cphase != NULL:
        real_vector_view_free(Cphase)

    return integral


def fresnel_overlap(dict wf1,
                    dict wf2_spline,
                    minf=None, maxf=None, real=True):

    """ Computes integral (h1|h2)
        NOTE: assumes noise-weighting has already been included in wf1 or wf2
        Args:
          wf1                 # Input dictionary for waveform 1
          - 'freq'            # Numpy array for common frequencies
          - 'phase'           # Numpy array for common phase
          - 'amp_real'        # Numpy array for amp_real
          - 'amp_imag'        # Numpy array for amp_imag
          wf2_spline          # Input dictionary for waveform 2 splines
          - 'spline_phase'    # Numpy matrix for common phase spline
          - 'spline_amp_real' # Numpy matrix for amp_real spline
          - 'spline_amp_imag' # Numpy matrix for amp_imag spline
        Keyword args:
          minf                # Minimal extra frequency cut (None to ignore)
          maxf                # Maximal extra frequency cut (None to ignore)
          real                # Return real part of integral (Default True)
    """

    # If the input is an empty array (we only test some, not all), return 0
    # Would typically happen if a mode is eliminated by time/frequency cuts
    if len(wf1['freq'])==0 or len(wf2_spline['spline_phase'])==0:
        return 0.

    # View of input data for wf1
    cdef np.ndarray[np.float_t, ndim=1] freq1 = wf1['freq']
    cdef np.ndarray[np.float_t, ndim=1] ampreal1 = wf1['amp_real']
    cdef np.ndarray[np.float_t, ndim=1] ampimag1 = wf1['amp_imag']
    cdef np.ndarray[np.float_t, ndim=1] phase1 = wf1['phase']
    cdef double* freq1_data = <double *> &freq1[0]
    cdef double* ampreal1_data = <double *> &ampreal1[0]
    cdef double* ampimag1_data = <double *> &ampimag1[0]
    cdef double* phase1_data = <double *> &phase1[0]
    cdef real_vector* Cfreq1 = real_vector_view(freq1_data, freq1.shape[0])
    cdef real_vector* Campreal1 = real_vector_view(ampreal1_data,
                                                   ampreal1.shape[0])
    cdef real_vector* Campimag1 = real_vector_view(ampimag1_data,
                                                   ampimag1.shape[0])
    cdef real_vector* Cphase1 = real_vector_view(phase1_data, phase1.shape[0])
    # Cast to C struct
    cdef CAmpPhaseFDData freqseries1
    freqseries1.freq = Cfreq1
    freqseries1.amp_real = Campreal1
    freqseries1.amp_imag = Campimag1
    freqseries1.phase = Cphase1

    # View of input data for wf2, given as splines
    cdef np.ndarray[np.float_t, ndim=2] spline_ampreal2 = \
                                                   wf2_spline['spline_amp_real']
    cdef np.ndarray[np.float_t, ndim=2] spline_ampimag2 = \
                                                   wf2_spline['spline_amp_imag']
    cdef np.ndarray[np.float_t, ndim=2] spline_phase2 = \
                                                      wf2_spline['spline_phase']
    cdef double* spline_ampreal2_data = <double *> &spline_ampreal2[0,0]
    cdef double* spline_ampimag2_data = <double *> &spline_ampimag2[0,0]
    cdef double* spline_phase2_data = <double *> &spline_phase2[0,0]
    cdef real_matrix* Cspline_ampreal2 = real_matrix_view(spline_ampreal2_data,
                             spline_ampreal2.shape[0], spline_ampreal2.shape[1])
    cdef real_matrix* Cspline_ampimag2 = real_matrix_view(spline_ampimag2_data,
                             spline_ampimag2.shape[0], spline_ampimag2.shape[1])
    cdef real_matrix* Cspline_phase2 = real_matrix_view(spline_phase2_data,
                                 spline_phase2.shape[0], spline_phase2.shape[1])
    # Cast to C struct
    cdef CAmpPhaseFDSpline splines2
    splines2.spline_amp_real = Cspline_ampreal2
    splines2.spline_amp_imag = Cspline_ampimag2
    splines2.spline_phase = Cspline_phase2

    # Optional frequency cuts
    cdef fLow, fHigh
    if minf is None:
        fLow = 0.
    else:
        fLow = minf
    if maxf is None:
        fHigh = 0.
    else:
        fHigh = maxf

    # Computation
    cdef double complex overlap_complex = 0.;
    overlap_complex = FDSinglemodeFresnelOverlap(
      &freqseries1,
      &splines2,
      fLow,
      fHigh
    );
    if real:
        overlap = np.real(overlap_complex)
    else:
        overlap = overlap_complex

    # Cleanup
    if Cfreq1 != NULL:
        real_vector_view_free(Cfreq1)
    if Campreal1 != NULL:
        real_vector_view_free(Campreal1)
    if Campimag1 != NULL:
        real_vector_view_free(Campimag1)
    if Cphase1 != NULL:
        real_vector_view_free(Cphase1)
    if Cspline_ampreal2 != NULL:
        real_matrix_view_free(Cspline_ampreal2)
    if Cspline_ampimag2 != NULL:
        real_matrix_view_free(Cspline_ampimag2)
    if Cspline_phase2 != NULL:
        real_matrix_view_free(Cspline_phase2)

    return overlap

def fresnel_overlap_3chan(dict wf1,
                          dict wf2_spline,
                          minf=None, maxf=None, real=True):

    """ Computes integral (h1|h2), summed over 3 independent channels
        Uses generalized Fresnel overlaps for amplitude/phase signals
        NOTE: assumes noise-weighting has already been included in wf1 or wf2
        Args:
          wf1                # Input dictionary for waveform 1
          - 'freq'           # Numpy array for common frequencies
          - 'phase'          # Numpy array for common phase
          - 'amp_real_chan1' # Numpy array for amp_real, channel 1
          - 'amp_imag_chan1' # Numpy array for amp_imag, channel 1
          - 'amp_real_chan2' # Numpy array for amp_real, channel 2
          - 'amp_imag_chan2' # Numpy array for amp_imag, channel 2
          - 'amp_real_chan3' # Numpy array for amp_real, channel 3
          - 'amp_imag_chan3' # Numpy array for amp_imag, channel 3
          wf2_spline         # Input dictionary for waveform 2 splines
          - 'spline_phase'   # Numpy matrix for common phase spline
          - 'spline_amp_real_chan1' # Numpy matrix for amp_real spline, chan 1
          - 'spline_amp_imag_chan1' # Numpy matrix for amp_imag spline, chan 1
          - 'spline_amp_real_chan2' # Numpy matrix for amp_real spline, chan 2
          - 'spline_amp_imag_chan2' # Numpy matrix for amp_imag spline, chan 2
          - 'spline_amp_real_chan3' # Numpy matrix for amp_real spline, chan 3
          - 'spline_amp_imag_chan3' # Numpy matrix for amp_imag spline, chan 3
        Keyword args:
          minf                # Minimal extra frequency cut (None to ignore)
          maxf                # Maximal extra frequency cut (None to ignore)
          real                # Return real part of integral (Default True)
    """

    # If the input is an empty array (we only test some, not all), return 0
    # Would typically happen if a mode is eliminated by time/frequency cuts
    if len(wf1['freq'])==0 or len(wf2_spline['spline_phase'])==0:
        return 0.

    # View of input data for wf1
    cdef np.ndarray[np.float_t, ndim=1] freq1 = wf1['freq']
    cdef np.ndarray[np.float_t, ndim=1] phase1 = wf1['phase']
    cdef np.ndarray[np.float_t, ndim=1] ampreal1chan1 = wf1['amp_real_chan1']
    cdef np.ndarray[np.float_t, ndim=1] ampimag1chan1 = wf1['amp_imag_chan1']
    cdef np.ndarray[np.float_t, ndim=1] ampreal1chan2 = wf1['amp_real_chan2']
    cdef np.ndarray[np.float_t, ndim=1] ampimag1chan2 = wf1['amp_imag_chan2']
    cdef np.ndarray[np.float_t, ndim=1] ampreal1chan3 = wf1['amp_real_chan3']
    cdef np.ndarray[np.float_t, ndim=1] ampimag1chan3 = wf1['amp_imag_chan3']
    cdef double* freq1_data = <double *> &freq1[0]
    cdef double* phase1_data = <double *> &phase1[0]
    cdef double* ampreal1chan1_data = <double *> &ampreal1chan1[0]
    cdef double* ampimag1chan1_data = <double *> &ampimag1chan1[0]
    cdef double* ampreal1chan2_data = <double *> &ampreal1chan2[0]
    cdef double* ampimag1chan2_data = <double *> &ampimag1chan2[0]
    cdef double* ampreal1chan3_data = <double *> &ampreal1chan3[0]
    cdef double* ampimag1chan3_data = <double *> &ampimag1chan3[0]
    cdef real_vector* Cfreq1 = real_vector_view(freq1_data, freq1.shape[0])
    cdef real_vector* Cphase1 = real_vector_view(phase1_data, phase1.shape[0])
    cdef real_vector* Campreal1chan1 = real_vector_view(ampreal1chan1_data,
                                                         ampreal1chan1.shape[0])
    cdef real_vector* Campimag1chan1 = real_vector_view(ampimag1chan1_data,
                                                         ampimag1chan1.shape[0])
    cdef real_vector* Campreal1chan2 = real_vector_view(ampreal1chan2_data,
                                                         ampreal1chan2.shape[0])
    cdef real_vector* Campimag1chan2 = real_vector_view(ampimag1chan2_data,
                                                         ampimag1chan2.shape[0])
    cdef real_vector* Campreal1chan3 = real_vector_view(ampreal1chan3_data,
                                                         ampreal1chan3.shape[0])
    cdef real_vector* Campimag1chan3 = real_vector_view(ampimag1chan3_data,
                                                         ampimag1chan3.shape[0])
    # Cast to C struct
    cdef CAmpPhaseFDData freqseries1chan1;
    freqseries1chan1.freq = Cfreq1
    freqseries1chan1.amp_real = Campreal1chan1
    freqseries1chan1.amp_imag = Campimag1chan1
    freqseries1chan1.phase = Cphase1
    cdef CAmpPhaseFDData freqseries1chan2;
    freqseries1chan2.freq = Cfreq1
    freqseries1chan2.amp_real = Campreal1chan2
    freqseries1chan2.amp_imag = Campimag1chan2
    freqseries1chan2.phase = Cphase1
    cdef CAmpPhaseFDData freqseries1chan3;
    freqseries1chan3.freq = Cfreq1
    freqseries1chan3.amp_real = Campreal1chan3
    freqseries1chan3.amp_imag = Campimag1chan3
    freqseries1chan3.phase = Cphase1

    # View of input data for wf2, given as splines
    cdef np.ndarray[np.float_t, ndim=2] spline_ampreal2chan1 = \
                                             wf2_spline['spline_amp_real_chan1']
    cdef np.ndarray[np.float_t, ndim=2] spline_ampimag2chan1 = \
                                             wf2_spline['spline_amp_imag_chan1']
    cdef np.ndarray[np.float_t, ndim=2] spline_ampreal2chan2 = \
                                             wf2_spline['spline_amp_real_chan2']
    cdef np.ndarray[np.float_t, ndim=2] spline_ampimag2chan2 = \
                                             wf2_spline['spline_amp_imag_chan2']
    cdef np.ndarray[np.float_t, ndim=2] spline_ampreal2chan3 = \
                                             wf2_spline['spline_amp_real_chan3']
    cdef np.ndarray[np.float_t, ndim=2] spline_ampimag2chan3 = \
                                             wf2_spline['spline_amp_imag_chan3']
    cdef np.ndarray[np.float_t, ndim=2] spline_phase2 = \
                                                wf2_spline['spline_phase']
    cdef double* spline_ampreal2chan1_data = \
                                           <double *> &spline_ampreal2chan1[0,0]
    cdef double* spline_ampimag2chan1_data = \
                                           <double *> &spline_ampimag2chan1[0,0]
    cdef double* spline_ampreal2chan2_data = \
                                           <double *> &spline_ampreal2chan2[0,0]
    cdef double* spline_ampimag2chan2_data = \
                                           <double *> &spline_ampimag2chan2[0,0]
    cdef double* spline_ampreal2chan3_data = \
                                           <double *> &spline_ampreal2chan3[0,0]
    cdef double* spline_ampimag2chan3_data = \
                                           <double *> &spline_ampimag2chan3[0,0]
    cdef double* spline_phase2_data = <double *> &spline_phase2[0,0]
    cdef real_matrix* Cspline_ampreal2chan1 = real_matrix_view(
       spline_ampreal2chan1_data,
       spline_ampreal2chan1.shape[0],
       spline_ampreal2chan1.shape[1])
    cdef real_matrix* Cspline_ampimag2chan1 = real_matrix_view(
       spline_ampimag2chan1_data,
       spline_ampimag2chan1.shape[0],
       spline_ampimag2chan1.shape[1])
    cdef real_matrix* Cspline_ampreal2chan2 = real_matrix_view(
       spline_ampreal2chan2_data,
       spline_ampreal2chan2.shape[0],
       spline_ampreal2chan2.shape[1])
    cdef real_matrix* Cspline_ampimag2chan2 = real_matrix_view(
       spline_ampimag2chan2_data,
       spline_ampimag2chan2.shape[0],
       spline_ampimag2chan2.shape[1])
    cdef real_matrix* Cspline_ampreal2chan3 = real_matrix_view(
       spline_ampreal2chan3_data,
       spline_ampreal2chan3.shape[0],
       spline_ampreal2chan3.shape[1])
    cdef real_matrix* Cspline_ampimag2chan3 = real_matrix_view(
       spline_ampimag2chan3_data,
       spline_ampimag2chan3.shape[0],
       spline_ampimag2chan3.shape[1])
    cdef real_matrix* Cspline_phase2 = real_matrix_view(
       spline_phase2_data, spline_phase2.shape[0], spline_phase2.shape[1])
    # Cast to C struct
    cdef CAmpPhaseFDSpline splines2chan1
    splines2chan1.spline_amp_real = Cspline_ampreal2chan1
    splines2chan1.spline_amp_imag = Cspline_ampimag2chan1
    splines2chan1.spline_phase = Cspline_phase2
    cdef CAmpPhaseFDSpline splines2chan2
    splines2chan2.spline_amp_real = Cspline_ampreal2chan2
    splines2chan2.spline_amp_imag = Cspline_ampimag2chan2
    splines2chan2.spline_phase = Cspline_phase2
    cdef CAmpPhaseFDSpline splines2chan3
    splines2chan3.spline_amp_real = Cspline_ampreal2chan3
    splines2chan3.spline_amp_imag = Cspline_ampimag2chan3
    splines2chan3.spline_phase = Cspline_phase2

    # Optional frequency cuts
    cdef fLow, fHigh
    if minf is None:
        fLow = 0.
    else:
        fLow = minf
    if maxf is None:
        fHigh = 0.
    else:
        fHigh = maxf

    # Computation
    cdef double complex overlap_complex = 0.;
    overlap_complex = FDSinglemodeFresnelOverlap3Chan(
      &freqseries1chan1,
      &freqseries1chan2,
      &freqseries1chan3,
      &splines2chan1,
      &splines2chan2,
      &splines2chan3,
      fLow,
      fHigh
    );
    if real:
        overlap = np.real(overlap_complex)
    else:
        overlap = overlap_complex

    # Cleanup
    if Cfreq1 != NULL:
        real_vector_view_free(Cfreq1)
    if Cphase1 != NULL:
        real_vector_view_free(Cphase1)
    if Campreal1chan1 != NULL:
        real_vector_view_free(Campreal1chan1)
    if Campimag1chan1 != NULL:
        real_vector_view_free(Campimag1chan1)
    if Campreal1chan2 != NULL:
        real_vector_view_free(Campreal1chan2)
    if Campimag1chan2 != NULL:
        real_vector_view_free(Campimag1chan2)
    if Campreal1chan3 != NULL:
        real_vector_view_free(Campreal1chan3)
    if Campimag1chan3 != NULL:
        real_vector_view_free(Campimag1chan3)
    if Cspline_ampreal2chan1 != NULL:
        real_matrix_view_free(Cspline_ampreal2chan1)
    if Cspline_ampimag2chan1 != NULL:
        real_matrix_view_free(Cspline_ampimag2chan1)
    if Cspline_ampreal2chan2 != NULL:
        real_matrix_view_free(Cspline_ampreal2chan2)
    if Cspline_ampimag2chan2 != NULL:
        real_matrix_view_free(Cspline_ampimag2chan2)
    if Cspline_ampreal2chan3 != NULL:
        real_matrix_view_free(Cspline_ampreal2chan3)
    if Cspline_ampimag2chan3 != NULL:
        real_matrix_view_free(Cspline_ampimag2chan3)
    if Cspline_phase2 != NULL:
        real_matrix_view_free(Cspline_phase2)

    return overlap

def fresnel_overlap_bands(list wf1_bands,
                          list wf2_spline_bands,
                          minf=None, maxf=None, real=True):

    """ Computes integral (h1|h2), summed over 3 independent channels
        Uses generalized Fresnel overlaps for amplitude/phase signals
        NOTE: assumes noise-weighting has already been included in wf1 or wf2
        Args:
          wf1_bands          # List of freq. band signals for waveform 1
                             # Each list element is a dictionary
                             # Same format as fresnel_overlap
          wf2_spline_bands   # List of freq. band signal splines for waveform 2
                             # Each list element is a dictionary
                             # Same format as fresnel_overlap
        Keyword args: (applied to all bands)
          minf                # Minimal extra frequency cut (None to ignore)
          maxf                # Maximal extra frequency cut (None to ignore)
          real                # Return real part of integral (Default True)
    """

    overlap = 0.
    for wf1_band in wf1_bands:
        for wf2_spline_band in wf2_spline_bands:
            overlap += fresnel_overlap(wf1_band,
                                       wf2_spline_band,
                                       minf=minf, maxf=maxf, real=real)

    return overlap

def fresnel_overlap_3chan_bands(list wf1_bands,
                                list wf2_spline_bands,
                                minf=None, maxf=None, real=True):

    """ Computes integral (h1|h2), summed over 3 independent channels
        Uses generalized Fresnel overlaps for amplitude/phase signals
        NOTE: assumes noise-weighting has already been included in wf1 or wf2
        Args:
          wf1_bands          # List of freq. band signals for waveform 1
                             # Each list element is a dictionary
                             # Same format as fresnel_overlap_3chan
          wf2_spline_bands   # List of freq. band signal splines for waveform 2
                             # Each list element is a dictionary
                             # Same format as fresnel_overlap_3chan
        Keyword args: (applied to all bands)
          minf                # Minimal extra frequency cut (None to ignore)
          maxf                # Maximal extra frequency cut (None to ignore)
          real                # Return real part of integral (Default True)
    """

    overlap = 0.
    for wf1_band in wf1_bands:
        for wf2_spline_band in wf2_spline_bands:
            overlap += fresnel_overlap_3chan(wf1_band,
                                             wf2_spline_band,
                                             minf=minf, maxf=maxf, real=real)

    return overlap

cpdef double brute_overlap(dict wf1_lm,
                           dict wf2_spline_lm,
                           deltaf,
                           minf=None, maxf=None,
                           force_include_boundaries=True,
                           brute_type='right'):

    """ Computes integral (h1|h2), summed over 3 independent channels
        Uses brute-force overlaps with a sum over freqs with deltaf-spacing
        NOTE: assumes noise-weighting has already been included in wf1 or wf2
        Args:
          wf1                # Input mode dictionary for waveform 1
          For each entry lm:
          - 'freq'           # Numpy array for common frequencies
          - 'phase'          # Numpy array for common phase
          - 'amp_real'       # Numpy array for amp_real
          - 'amp_imag'       # Numpy array for amp_imag
          wf2_spline         # Input mode dictionary for waveform 2 splines
          For each entry lm:
          - 'spline_phase'    # Numpy matrix for common phase spline
          - 'spline_amp_real' # Numpy matrix for amp_real spline
          - 'spline_amp_imag' # Numpy matrix for amp_imag spline
        Keyword args:
          - minf             # Minimal frequency cut in Hz (default None)
          - maxf             # Maximal frequency cut in Hz (default None)
          - force_include_boundaries # Boolean (default True), if set include
                             # all freq. bounds for all modes in freq. array
                             # (making it unequally spaced)
          - type             # default 'right' for bars set by data on the right
                             # 'left' for data on left, 'trapeze' for trapezes
    """

    # Sets of modes
    modes_1 = wf1_lm['modes']
    modes_2 = wf2_spline_lm['modes']

    # Frequency bounds
    minf_1 = np.min([wf1_lm[lm]['freq'][0] for lm in modes_1])
    maxf_1 = np.max([wf1_lm[lm]['freq'][-1] for lm in modes_1])
    minf_2 = np.min([wf2_spline_lm[lm]['spline_phase'][0,0] for lm in modes_2])
    maxf_2 = np.max([wf2_spline_lm[lm]['spline_phase'][-1,0] for lm in modes_2])
    fLow = np.fmax(minf_1, minf_2)
    fHigh = np.fmin(maxf_1, maxf_2)
    if minf is not None:
        fLow = np.fmax(fLow, minf)
    if maxf is not None:
        fHigh = np.fmin(fHigh, maxf)

    # Array of frequencies with fixed deltaf
    freqs_overlap = np.arange(fLow, fHigh, deltaf)
    # Force include boundaries in freq array, making it unequally spaced
    # Could be important for e.g. premerger with multiple modes
    if force_include_boundaries:
        boundaries = np.array([fLow, fHigh] + [wf1_lm[lm]['freq'][0] for lm in modes_1] + [wf1_lm[lm]['freq'][-1] for lm in modes_1] + [wf2_spline_lm[lm]['spline_phase'][0,0] for lm in modes_2] + [wf2_spline_lm[lm]['spline_phase'][-1,0] for lm in modes_2])
        boundaries = np.unique(boundaries)
        mask = (boundaries >= fLow) & (boundaries <= fHigh)
        boundaries = boundaries[mask]
        inds = np.searchsorted(freqs_overlap, boundaries)
        freqs_overlap = np.insert(freqs_overlap, inds, boundaries)
        freqs_overlap = np.unique(freqs_overlap)

    # Loop over modes to evaluate values for wf2, which is already interpolated
    wf1_vals = np.zeros_like(freqs_overlap, dtype=complex)
    for lm in modes_1:
        spline1_amp_realClass = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_real'])
        spline1_amp_imagClass = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_imag'])
        spline1_phaseClass = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['phase'])
        spline1_amp_real = spline1_amp_realClass.get_spline()
        spline1_amp_imag = spline1_amp_imagClass.get_spline()
        spline1_phase = spline1_phaseClass.get_spline()
        ampreal1 = pyspline.spline_eval_vector(spline1_amp_real, freqs_overlap, extrapol_zero=True)
        ampimag1 = pyspline.spline_eval_vector(spline1_amp_imag, freqs_overlap, extrapol_zero=True)
        phase1 = pyspline.spline_eval_vector(spline1_phase, freqs_overlap, extrapol_zero=True)
        eiphase1 = np.exp(1j*phase1)
        wf1_vals += (ampreal1 + 1j*ampimag1) * eiphase1

    # Loop over modes to evaluate values for wf2, which is already interpolated
    wf2_vals_noiseweighted = np.zeros_like(freqs_overlap, dtype=complex)
    for lm in modes_2:
        ampreal2 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_real'], freqs_overlap, extrapol_zero=True)
        ampimag2 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_imag'], freqs_overlap, extrapol_zero=True)
        phase2 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_phase'], freqs_overlap, extrapol_zero=True)
        eiphase2 = np.exp(1j*phase2)
        wf2_vals_noiseweighted += (ampreal2 + 1j*ampimag2) * eiphase2

    # Overlap
    vals = 4 * np.real(wf1_vals * np.conj(wf2_vals_noiseweighted))
    freq_diff = np.diff(freqs_overlap)
    if brute_type=='right':
        overlap = np.sum(freq_diff * vals[1:])
    elif brute_type=='left':
        overlap = np.sum(freq_diff * vals[:-1])
    elif brute_type=='trapeze':
        overlap = np.sum(freq_diff * (vals[:-1] + vals[1:])/2.)
    else:
        raise ValueError('Type of brute-force overlap not recognized.')
    return overlap

cpdef double brute_overlap_3chan(dict wf1_lm,
                                 dict wf2_spline_lm,
                                 deltaf,
                                 minf=None, maxf=None,
                                 force_include_boundaries=True,
                                 brute_type='right'
                                 ):

    """ Computes integral (h1|h2), summed over 3 independent channels
        Uses brute-force overlaps with a sum over freqs with deltaf-spacing
        NOTE: assumes noise-weighting has already been included in wf1 or wf2
        Args:
          wf1                # Input mode dictionary for waveform 1
          For each entry lm:
          - 'freq'           # Numpy array for common frequencies
          - 'phase'          # Numpy array for common phase
          - 'amp_real_chan1' # Numpy array for amp_real, channel 1
          - 'amp_imag_chan1' # Numpy array for amp_imag, channel 1
          - 'amp_real_chan2' # Numpy array for amp_real, channel 2
          - 'amp_imag_chan2' # Numpy array for amp_imag, channel 2
          - 'amp_real_chan3' # Numpy array for amp_real, channel 3
          - 'amp_imag_chan3' # Numpy array for amp_imag, channel 3
          wf2_spline         # Input mode dictionary for waveform 2 splines
          For each entry lm:
          - 'spline_phase'   # Numpy matrix for common phase spline
          - 'spline_amp_real_chan1' # Numpy matrix for amp_real spline, chan 1
          - 'spline_amp_imag_chan1' # Numpy matrix for amp_imag spline, chan 1
          - 'spline_amp_real_chan2' # Numpy matrix for amp_real spline, chan 2
          - 'spline_amp_imag_chan2' # Numpy matrix for amp_imag spline, chan 2
          - 'spline_amp_real_chan3' # Numpy matrix for amp_real spline, chan 3
          - 'spline_amp_imag_chan3' # Numpy matrix for amp_imag spline, chan 3
        Keyword args:
          - minf             # Minimal frequency cut in Hz (default None)
          - maxf             # Maximal frequency cut in Hz (default None)
          - force_include_boundaries # Boolean (default True), if set include
                             # all freq. bounds for all modes in freq. array
                             # (making it unequally spaced)
          - type             # default 'right' for bars set by data on the right
                             # 'left' for data on left, 'trapeze' for trapezes
    """

    # Sets of modes
    modes_1 = wf1_lm['modes']
    modes_2 = wf2_spline_lm['modes']

    # Frequency bounds
    minf_1 = np.min([wf1_lm[lm]['freq'][0] for lm in modes_1])
    maxf_1 = np.max([wf1_lm[lm]['freq'][-1] for lm in modes_1])
    minf_2 = np.min([wf2_spline_lm[lm]['spline_phase'][0,0] for lm in modes_2])
    maxf_2 = np.max([wf2_spline_lm[lm]['spline_phase'][-1,0] for lm in modes_2])
    fLow = np.fmax(minf_1, minf_2)
    fHigh = np.fmin(maxf_1, maxf_2)
    if minf is not None:
        fLow = np.fmax(fLow, minf)
    if maxf is not None:
        fHigh = np.fmin(fHigh, maxf)

    # Array of frequencies with fixed deltaf - NOTE: can end short of fHigh
    freqs_overlap = np.arange(fLow, fHigh, deltaf)
    # Force include boundaries in freq array, making it unequally spaced
    # Could be important for e.g. premerger with multiple modes
    if force_include_boundaries:
        boundaries = np.array([fLow, fHigh] + [wf1_lm[lm]['freq'][0] for lm in modes_1] + [wf1_lm[lm]['freq'][-1] for lm in modes_1] + [wf2_spline_lm[lm]['spline_phase'][0,0] for lm in modes_2] + [wf2_spline_lm[lm]['spline_phase'][-1,0] for lm in modes_2])
        boundaries = np.unique(boundaries)
        mask = (boundaries >= fLow) & (boundaries <= fHigh)
        boundaries = boundaries[mask]
        inds = np.searchsorted(freqs_overlap, boundaries)
        freqs_overlap = np.insert(freqs_overlap, inds, boundaries)
        freqs_overlap = np.unique(freqs_overlap)

    # Loop over modes to evaluate values for wf2, which is already interpolated
    wf1_chan1_vals = np.zeros_like(freqs_overlap, dtype=complex)
    wf1_chan2_vals = np.zeros_like(freqs_overlap, dtype=complex)
    wf1_chan3_vals = np.zeros_like(freqs_overlap, dtype=complex)
    for lm in modes_1:
        spline1_amp_real_chan1Class = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_real_chan1'])
        spline1_amp_imag_chan1Class = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_imag_chan1'])
        spline1_amp_real_chan2Class = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_real_chan2'])
        spline1_amp_imag_chan2Class = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_imag_chan2'])
        spline1_amp_real_chan3Class = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_real_chan3'])
        spline1_amp_imag_chan3Class = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['amp_imag_chan3'])
        spline1_phaseClass = pyspline.CubicSpline(wf1_lm[lm]['freq'], wf1_lm[lm]['phase'])
        spline1_amp_real_chan1 = spline1_amp_real_chan1Class.get_spline()
        spline1_amp_imag_chan1 = spline1_amp_imag_chan1Class.get_spline()
        spline1_amp_real_chan2 = spline1_amp_real_chan2Class.get_spline()
        spline1_amp_imag_chan2 = spline1_amp_imag_chan2Class.get_spline()
        spline1_amp_real_chan3 = spline1_amp_real_chan3Class.get_spline()
        spline1_amp_imag_chan3 = spline1_amp_imag_chan3Class.get_spline()
        spline1_phase = spline1_phaseClass.get_spline()
        ampreal1chan1 = pyspline.spline_eval_vector(spline1_amp_real_chan1, freqs_overlap, extrapol_zero=True)
        ampimag1chan1 = pyspline.spline_eval_vector(spline1_amp_imag_chan1, freqs_overlap, extrapol_zero=True)
        ampreal1chan2 = pyspline.spline_eval_vector(spline1_amp_real_chan2, freqs_overlap, extrapol_zero=True)
        ampimag1chan2 = pyspline.spline_eval_vector(spline1_amp_imag_chan2, freqs_overlap, extrapol_zero=True)
        ampreal1chan3 = pyspline.spline_eval_vector(spline1_amp_real_chan3, freqs_overlap, extrapol_zero=True)
        ampimag1chan3 = pyspline.spline_eval_vector(spline1_amp_imag_chan3, freqs_overlap, extrapol_zero=True)
        phase1 = pyspline.spline_eval_vector(spline1_phase, freqs_overlap, extrapol_zero=True)
        eiphase1 = np.exp(1j*phase1)
        wf1_chan1_vals += (ampreal1chan1 + 1j*ampimag1chan1) * eiphase1
        wf1_chan2_vals += (ampreal1chan2 + 1j*ampimag1chan2) * eiphase1
        wf1_chan3_vals += (ampreal1chan3 + 1j*ampimag1chan3) * eiphase1

    # Loop over modes to evaluate values for wf2, which is already interpolated
    wf2_chan1_vals_noiseweighted = np.zeros_like(freqs_overlap, dtype=complex)
    wf2_chan2_vals_noiseweighted = np.zeros_like(freqs_overlap, dtype=complex)
    wf2_chan3_vals_noiseweighted = np.zeros_like(freqs_overlap, dtype=complex)
    for lm in modes_2:
        ampreal2chan1 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_real_chan1'], freqs_overlap, extrapol_zero=True)
        ampimag2chan1 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_imag_chan1'], freqs_overlap, extrapol_zero=True)
        ampreal2chan2 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_real_chan2'], freqs_overlap, extrapol_zero=True)
        ampimag2chan2 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_imag_chan2'], freqs_overlap, extrapol_zero=True)
        ampreal2chan3 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_real_chan3'], freqs_overlap, extrapol_zero=True)
        ampimag2chan3 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_amp_imag_chan3'], freqs_overlap, extrapol_zero=True)
        phase2 = pyspline.spline_eval_vector(wf2_spline_lm[lm]['spline_phase'], freqs_overlap, extrapol_zero=True)
        eiphase2 = np.exp(1j*phase2)
        wf2_chan1_vals_noiseweighted += (ampreal2chan1 + 1j*ampimag2chan1) * eiphase2
        wf2_chan2_vals_noiseweighted += (ampreal2chan2 + 1j*ampimag2chan2) * eiphase2
        wf2_chan3_vals_noiseweighted += (ampreal2chan3 + 1j*ampimag2chan3) * eiphase2

    # Overlap
    vals = 4 * np.real(wf1_chan1_vals * np.conj(wf2_chan1_vals_noiseweighted)
                       + wf1_chan2_vals * np.conj(wf2_chan2_vals_noiseweighted)
                       + wf1_chan3_vals * np.conj(wf2_chan3_vals_noiseweighted))
    freq_diff = np.diff(freqs_overlap)
    if brute_type=='right':
        overlap = np.sum(freq_diff * vals[1:])
    elif brute_type=='left':
        overlap = np.sum(freq_diff * vals[:-1])
    elif brute_type=='trapeze':
        overlap = np.sum(freq_diff * (vals[:-1] + vals[1:])/2.)
    else:
        raise ValueError('Type of brute-force overlap not recognized.')
    return overlap
