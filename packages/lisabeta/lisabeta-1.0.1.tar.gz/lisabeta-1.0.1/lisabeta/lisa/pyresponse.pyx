#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython wrapping of C LISA FD response.
"""

import numpy as np
cimport numpy as np
from enum import Enum

import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pytools as pytools
import lisabeta.tools.pyspline as pyspline


################################################################################
# Structures and defaults
################################################################################

class TDIEnum(Enum):
    TDIAET = 0
    TDIXYZ = 1
    TDI2AET = 2
    TDI2XYZ = 3

class ResponseApproxEnum(Enum):
    full         = 0
    lowfL        = 1
    lowf         = 2
    ignoreRdelay = 3
    lowfL_highfsens = 4

LISAconst2010 = {
  'OrbitOmega' : _EarthOrbitOmega_SI,
  'OrbitPhi0' : 0.,
  'Orbitt0' : 0.,
  'OrbitR' : _AU_SI,
  'OrbitL' : 5e9
}

LISAconstProposal = {
  'OrbitOmega' : _EarthOrbitOmega_SI,
  'OrbitPhi0' : 0.,
  'Orbitt0' : 0.,
  'OrbitR' : _AU_SI,
  'OrbitL' : 2.5e9
}

LISAconstDict = {
  '2010': LISAconst2010,
  'Proposal': LISAconstProposal
}

################################################################################
# LISA TDI response
################################################################################

cdef class LISAFDresponseTDI3Chan:
    """ Transfer functions for the LISA response.
    """

    cdef real_vector* CphaseRdelay  # pointer to C vector, orbital delay phase
    cdef complex_vector* Ctransfer1 # pointer to C vector, channel 1 transfer
    cdef complex_vector* Ctransfer2 # pointer to C vector, channel 2 transfer
    cdef complex_vector* Ctransfer3 # pointer to C vector, channel 3 transfer

    cdef freq                       # input numpy array for frequencies
    cdef tf                         # input numpy array for tf spline

    cdef real_vector* Cfreq         # pointer to C frequency vector
    cdef real_vector* Ctf           # pointer to C vector for tf

    cdef double t0                  # Reference orbital time (yr)
    cdef int l                      # Mode number l
    cdef int m                      # Mode number m
    cdef double inc                 # Inclination in source-frame
    cdef double phi                 # Azimuthal phase in source-frame
    cdef double lambd               # Ecliptic longitude, SSB-frame
    cdef double beta                # Ecliptic latitude, SSB-frame
    cdef double psi                 # Polarization angle, SSB-frame

    cdef LISAconst                  # dict for LISA orbital constants
    cdef responseapprox             # tag for approximation in LISA response
    cdef TDI                        # choice of TDI observables
    cdef frozenLISA                 # tag to treat LISA as motionless
    cdef TDIrescaled                # Flag to rescale TDI variables

    cdef phaseRdelay                # numpy array, orbital delay phase
    cdef transfer1                  # numpy array, channel 1 transfer
    cdef transfer2                  # numpy array, channel 2 transfer
    cdef transfer3                  # numpy array, channel 3 transfer


    def __init__(self,
                 np.ndarray[np.float_t, ndim=1] freq,
                 np.ndarray[np.float_t, ndim=1] tf,
                 t0, l, m, inc, phi, lambd, beta, psi,
                 TDI='TDIAET', LISAconst=LISAconstProposal,
                 responseapprox='full', frozenLISA=False, TDIrescaled=False):
        """Constructor
        Args:
          freq                       # input numpy array for frequencies
          tf                         # input numpy array for tf

          t0                  # Reference orbital time (yr)
          l                   # Mode number l
          m                   # Mode number m
          inc                 # Inclination in source-frame
          phi                 # Azimuthal phase in source-frame
          lambd               # Ecliptic longitude, SSB-frame
          beta                # Ecliptic latitude, SSB-frame
          psi                 # Polarization angle, SSB-frame
        Keyword args:
          TDI                 # Choice of TDI variables
          LISAconst           # Choice of LISA constellation
          responseapprox      # Choice of low-f approximation in the response
          frozenLISA          # Flag to freeze LISA motion
          TDIrescaled         # Flag to apply rescaling to TDI variables
        """

        self.freq = freq
        self.tf = tf

        self.t0 = t0
        self.l = l
        self.m = m
        self.inc = inc
        self.phi = phi
        self.lambd = lambd
        self.beta = beta
        self.psi = psi

        self.TDI = TDI
        self.responseapprox = responseapprox
        self.frozenLISA = frozenLISA
        self.TDIrescaled = TDIrescaled
        if isinstance(LISAconst, basestring):
            self.LISAconst = LISAconstDict[LISAconst]
        else:
            self.LISAconst = LISAconst

        self.Cfreq = NULL
        self.Ctf = NULL
        self.CphaseRdelay = NULL
        self.Ctransfer1 = NULL
        self.Ctransfer2 = NULL
        self.Ctransfer3 = NULL

        # If the input is an empty array, init to empty arrays and stop there
        # NOTE: __init__ is required to return nothing
        if len(freq)==0 or len(tf)==0:
            self.phaseRdelay = np.empty(0, dtype=float)
            self.transfer1 = np.empty(0, dtype=float)
            self.transfer2 = np.empty(0, dtype=float)
            self.transfer3 = np.empty(0, dtype=float)
            return

        # Build a real_vector representation of the input numpy arrays
        if not freq.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array freq is not C_CONTIGUOUS')
        if not tf.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array tf is not C_CONTIGUOUS')
        cdef double* freq_data = <double *> &freq[0]
        self.Cfreq = real_vector_view(freq_data, freq.shape[0])

        cdef double* tf_data = <double *> &tf[0]
        self.Ctf = real_vector_view(tf_data, tf.shape[0])

        cdef CTDI = TDIEnum[self.TDI].value
        cdef Cresponseapprox = ResponseApproxEnum[self.responseapprox].value
        cdef int CfrozenLISA = <int> self.frozenLISA
        cdef int Crescaled = <int> self.TDIrescaled

        cdef LISAconstellation CLISAconst
        CLISAconst.OrbitOmega = self.LISAconst['OrbitOmega']
        CLISAconst.OrbitPhi0 = self.LISAconst['OrbitPhi0']
        CLISAconst.Orbitt0 = self.LISAconst['Orbitt0']
        CLISAconst.OrbitR = self.LISAconst['OrbitR']
        CLISAconst.OrbitL = self.LISAconst['OrbitL']

        ret = EvalLISAFDresponseTDI3Chan(
            &self.CphaseRdelay,
            &self.Ctransfer1,
            &self.Ctransfer2,
            &self.Ctransfer3,
            self.Cfreq,
            self.Ctf,
            self.t0,
            self.l,
            self.m,
            self.inc,
            self.phi,
            self.lambd,
            self.beta,
            self.psi,
            CTDI,
            &CLISAconst,
            Cresponseapprox,
            CfrozenLISA,
            Crescaled
        );
        if ret == _FAILURE:
            raise ValueError("Call to EvalLISAFDresponseTDI3Chan() failed.")

        # Cast C double array to numpy via a MemoryView
        cdef double[::1] view_phaseRdelay = \
          <(double)[:self.CphaseRdelay.size]> self.CphaseRdelay.data
        self.phaseRdelay = np.asarray(view_phaseRdelay)
        cdef double complex[::1] view_transfer1 = \
          <(double complex)[:self.Ctransfer1.size]> self.Ctransfer1.data
        self.transfer1 = np.asarray(view_transfer1)
        cdef double complex[::1] view_transfer2 = \
          <(double complex)[:self.Ctransfer2.size]> self.Ctransfer2.data
        self.transfer2 = np.asarray(view_transfer2)
        cdef double complex[::1] view_transfer3 = \
          <(double complex)[:self.Ctransfer3.size]> self.Ctransfer3.data
        self.transfer3 = np.asarray(view_transfer3)
        #self.Mfreq = real_vector_to_np_array(self.CMfreq)

    def __dealloc__(self):
        """Destructor
        """
        if self.CphaseRdelay != NULL:
            real_vector_free(self.CphaseRdelay)
        if self.Ctransfer1 != NULL:
            complex_vector_free(self.Ctransfer1)
        if self.Ctransfer2 != NULL:
            complex_vector_free(self.Ctransfer2)
        if self.Ctransfer3 != NULL:
            complex_vector_free(self.Ctransfer3)
        if self.Cfreq != NULL:
            real_vector_view_free(self.Cfreq)
        if self.Ctf != NULL:
            real_vector_view_free(self.Ctf)

    def get_response(self):
        return np.copy(self.phaseRdelay), np.copy(self.transfer1), \
                 np.copy(self.transfer2), np.copy(self.transfer3),

################################################################################
# Signal modulations from orbit around AGN
################################################################################

def chirp_bands(t, phi, fdot_exclude_mono=2e-12):
    spline_phi = pyspline.CubicSpline(t, phi)
    phiddot = spline_phi.get_spline_dd()[:,1]
    # We put a minus sign here so as to give the + sign to chirping domains
    # Indeed, \ddot{phi_{22}} is negative since phi_{22} = -2 phi_{orb}
    # The 2pi is just to convert to frequency f instead of omega
    x, y = t, -phiddot / (2*np.pi)
    interval = [-fdot_exclude_mono, fdot_exclude_mono]
    t_bands = pytools.func_domain_decomp_linear(x, y, interval)
    return t_bands

def chirping_signal_decomp(signal_td, t_bands, window_fraction=0.25, npt_min=20):
    signals = []
    # TODO: building splines probably done outside this function already ?
    spline_ampClass = pyspline.CubicSpline(signal_td[:,0], signal_td[:,1])
    spline_phiClass = pyspline.CubicSpline(signal_td[:,0], signal_td[:,2])
    spline_amp = spline_ampClass.get_spline()
    spline_phi = spline_phiClass.get_spline()
    for i, band in enumerate(t_bands):
        if band[2]==0:
            deltat = (band[1] - band[0]) * window_fraction
            deltatf = deltat
            deltati = deltat
            ti = band[0] + deltat
            tf = band[1] - deltat
        else:
            if i>0:
                deltati = window_fraction * (t_bands[i-1][1] - t_bands[i-1][0])
                ti = band[0] - deltati
            else:
                deltati = 0.
                ti = band[0]
            if i<len(t_bands)-1:
                deltatf = window_fraction * (t_bands[i+1][1] - t_bands[i+1][0])
                tf = band[1] + deltatf
            else:
                deltatf = 0.
                tf = band[1]
        s_r = pytools.restrict_data_bycol(signal_td, [ti, tf], col=0)
        if len(s_r)<npt_min:
            times = np.linspace(ti, tf, npt_min)
            s_r = np.zeros((npt_min, 3), dtype=float)
            s_r[:,0] = times
            s_r[:,1] = pyspline.spline_eval_vector(spline_amp, times)
            s_r[:,2] = pyspline.spline_eval_vector(spline_phi, times)
        w = pytools.window_planck_vec(s_r[:,0], ti, tf, deltati, deltatf)
        s_w = np.array([s_r[:,0], s_r[:,1]*w, s_r[:,2]]).T
        signals += [s_w]
    return signals

# NOTE: convention tr = te + d(te)
# NOTE: by convention, d(t0) = 0 (t0 in s)
# NOTE: R_AGN in units of M_AGN (e.g. R=700M), M_AGN in solar masses
def doppler_modulated_signal_td(signal_td, t0=0., **AGNparams):
    t, amp, phase = signal_td.T
    shapiro_delay = AGNparams.get('shapiro_delay', False)
    M_AGN = AGNparams['M_AGN']
    R_AGN = AGNparams['R_AGN']
    theta_AGN = AGNparams['theta_AGN']
    phi_AGN = AGNparams['phi_AGN']
    M_AGN_s = M_AGN * pyconstants.MTSUN_SI
    Omega_AGN = 1./(M_AGN_s) * (R_AGN**(-3/2.))
    # Leading order geometric propagation delay
    d = -R_AGN * M_AGN_s * np.sin(theta_AGN) * np.cos(Omega_AGN*t - phi_AGN)
    d0 = -R_AGN * M_AGN_s * np.sin(theta_AGN) * np.cos(Omega_AGN*t0 - phi_AGN)
    # Shapiro time delay if included, with a constant scaled out by convention
    d_shapiro = np.zeros_like(d0)
    d0_shapiro = np.zeros_like(d0)
    if shapiro_delay:
        d_shapiro = -2*M_AGN_s * np.log(1 + np.sin(theta_AGN) * np.cos(Omega_AGN*t - phi_AGN))
        d0_shapiro = -2*M_AGN_s * np.log(1 + np.sin(theta_AGN) * np.cos(Omega_AGN*t0 - phi_AGN))
    td = t + d - d0 + d_shapiro - d0_shapiro
    return np.array([td, amp, phase]).T
