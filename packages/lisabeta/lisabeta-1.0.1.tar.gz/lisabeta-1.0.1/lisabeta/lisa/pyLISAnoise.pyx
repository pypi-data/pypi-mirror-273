#
#  Copyright (C) 2019 Sylvain Marsat.
#


"""
    Cython wrapping of LISA noise

    The underlying C functions work on one value of f at a time.
    Interface for a numpy array of freq values is provided as a python loop.
"""

# from lisabeta.pyconstants cimport *
# from lisabeta.struct.pystruct cimport *
cimport numpy as np
import numpy as np
from enum import Enum
import lisabeta.pyconstants as pyconstants
import lisabeta.tools.pyspline as pyspline
from pyLISAnoise cimport *
import lisabeta.lisa.pyresponse as pyresponse
from pyresponse cimport *
from pyresponse import LISAconst2010, LISAconstProposal, TDIEnum
#cimport lisabeta.struct.pystruct as pystruct

class LISANoiseEnum(Enum):
    LISASciRDv1noise  = 0
    LISAProposalnoise = 1
    LISA2010noise     = 2
    LISA2017noise     = 3

LISAnoiseDict = {
  'SciRDv1': LISANoiseEnum.LISASciRDv1noise.value,
  'Proposal': LISANoiseEnum.LISAProposalnoise.value,
  '2010': LISANoiseEnum.LISA2010noise.value,
  '2017': LISANoiseEnum.LISA2017noise.value
}

LISAnoiseSciRDv1 = {
  'InstrumentalNoise' : LISANoiseEnum.LISASciRDv1noise.value,
  'WDbackground' : True,
  'WDduration' : 3.,
  'lowf_add_pm_noise_f0': 0.,
  'lowf_add_pm_noise_alpha': 2.
}

LISAnoiseProposal = {
  'InstrumentalNoise' : LISANoiseEnum.LISAProposalnoise.value,
  'WDbackground' : True,
  'WDduration' : 3.,
  'lowf_add_pm_noise_f0': 0.,
  'lowf_add_pm_noise_alpha': 2.
}

LISAnoise2017 = {
  'InstrumentalNoise' : LISANoiseEnum.LISA2017noise.value,
  'WDbackground' : False,
  'WDduration' : 3.,
  'lowf_add_pm_noise_f0': 0.,
  'lowf_add_pm_noise_alpha': 2.
}

cdef class LISANoisePSDFunction(py_object_function):

    def __init__(self, LISAnoise, int nchan,
                 basestring TDI='TDIAET', TDIrescaled=True,
                 LISAconst=LISAconstProposal):
        """Constructor
        Args:
          LISAnoise           # Choice of noise model
          nchan               # Choice of TDI channel id (1,2,3)
        Keyword args:
          TDI                 # Choice of TDI variables
          LISAconst           # Choice of LISA constellation
          TDIrescaled         # Flag to apply rescaling to TDI variables
        """

        # Set up orbital constants from dictionary
        self.CLISAconst.OrbitOmega = LISAconst['OrbitOmega']
        self.CLISAconst.OrbitPhi0 = LISAconst['OrbitPhi0']
        self.CLISAconst.Orbitt0 = LISAconst['Orbitt0']
        self.CLISAconst.OrbitR = LISAconst['OrbitR']
        self.CLISAconst.OrbitL = LISAconst['OrbitL']

        # Set up noise model from dictionary
        instrumentalnoise = LISAnoise['InstrumentalNoise']
        if isinstance(instrumentalnoise, basestring):
            self.CLISAnoise.noise = LISAnoiseDict[instrumentalnoise]
        else:
            self.CLISAnoise.noise = instrumentalnoise
        self.CLISAnoise.WDbackground = int(LISAnoise['WDbackground'])
        self.CLISAnoise.WDduration = LISAnoise['WDduration']
        self.CLISAnoise.lowf_add_pm_noise_f0 = LISAnoise['lowf_add_pm_noise_f0']
        self.CLISAnoise.lowf_add_pm_noise_alpha = LISAnoise['lowf_add_pm_noise_alpha']

        # Set up noise function
        self.fn = NULL
        self.CLISAdata = LISA_noise_func_data(&self.CLISAnoise, &self.CLISAconst)
        CTDI = TDIEnum[TDI].value
        if (CTDI==TDIEnum['TDIAET'].value):
            if TDIrescaled:
                if nchan==1: self.fn = SnA
                elif nchan==2: self.fn = SnE
                elif nchan==3: self.fn = SnT
                else: raise ValueError("No such channel: "+str(nchan))
            else:
                if nchan==1: self.fn = SnANoRescaling
                elif nchan==2: self.fn = SnENoRescaling
                elif nchan==3: self.fn = SnTNoRescaling
                else: raise ValueError("No such channel: "+str(nchan))
        elif (CTDI==TDIEnum['TDIXYZ'].value):
            if TDIrescaled:
                self.fn = SnXYZ
            else:
                self.fn = SnXYZNoRescaling
        elif (CTDI==TDIEnum['TDI2AET'].value):
            if TDIrescaled:
                if nchan==1: self.fn = SnA
                elif nchan==2: self.fn = SnE
                elif nchan==3: self.fn = SnT
                else: raise ValueError("No such channel: "+str(nchan))
            else:
                if nchan==1: self.fn = SnA2NoRescaling
                elif nchan==2: self.fn = SnE2NoRescaling
                elif nchan==3: self.fn = SnT2NoRescaling
                else: raise ValueError("No such channel: "+str(nchan))
        elif (CTDI==TDIEnum['TDI2XYZ'].value):
            if TDIrescaled:
                self.fn = SnXYZ
            else:
                self.fn = SnXYZ2NoRescaling
        else: raise ValueError("No support for TDI = '"+str(nchan)+"'")

        self.obfn.object = <void*> &self.CLISAdata
        self.obfn.function = self.fn

    # cpdef double call(self, double f):
    #     return self.fn(&self.CLISAdata, f)
    #
    # cpdef np.ndarray[np.float_t, ndim=1] apply(self,
    #                                        np.ndarray[np.float_t, ndim=1] freq):
    #     cdef np.ndarray[np.float_t, ndim=1] psd = np.zeros_like(freq)
    #     for i in range(len(freq)):
    #         psd[i] = self.fn(&self.CLISAdata, freq[i])
    #     return psd


cdef class LISANoisePSDFunction3Chan:

    def __init__(self, LISAnoise,
                 basestring TDI='TDIAET', TDIrescaled=True,
                 LISAconst=LISAconstProposal):
        """Constructor
        Args:
          LISAnoise           # Choice of noise model
        Keyword args:
          TDI                 # Choice of TDI variables
          TDIrescaled         # Flag to apply rescaling to TDI variables
          LISAconst           # Choice of LISA constellation
        """

        # Set up orbital constants from dictionary
        if isinstance(LISAconst, basestring):
            LISAconst = pyresponse.LISAconstDict[LISAconst]
        self.CLISAconst.OrbitOmega = LISAconst['OrbitOmega']
        self.CLISAconst.OrbitPhi0 = LISAconst['OrbitPhi0']
        self.CLISAconst.Orbitt0 = LISAconst['Orbitt0']
        self.CLISAconst.OrbitR = LISAconst['OrbitR']
        self.CLISAconst.OrbitL = LISAconst['OrbitL']

        # Set up noise model from dictionary
        instrumentalnoise = LISAnoise['InstrumentalNoise']
        if isinstance(instrumentalnoise, basestring):
            self.CLISAnoise.noise = LISAnoiseDict[instrumentalnoise]
        else:
            self.CLISAnoise.noise = instrumentalnoise
        self.CLISAnoise.WDbackground = int(LISAnoise['WDbackground'])
        self.CLISAnoise.WDduration = LISAnoise['WDduration']
        self.CLISAnoise.lowf_add_pm_noise_f0 = LISAnoise['lowf_add_pm_noise_f0']
        self.CLISAnoise.lowf_add_pm_noise_alpha = LISAnoise['lowf_add_pm_noise_alpha']

        # Set up noise function
        self.fn = NULL
        self.CLISAdata = LISA_noise_func_data(&self.CLISAnoise, &self.CLISAconst)
        CTDI = TDIEnum[TDI].value
        if (CTDI==TDIEnum['TDIAET'].value):
            if TDIrescaled:
                self.fn = Sn3ChanAET
            else:
                self.fn = Sn3ChanAETNoRescaling
        elif (CTDI==TDIEnum['TDIXYZ'].value):
            if TDIrescaled:
                self.fn = Sn3ChanXYZ
            else:
                self.fn = Sn3ChanXYZNoRescaling
        elif (CTDI==TDIEnum['TDI2AET'].value):
            if TDIrescaled:
                self.fn = Sn3ChanAET
            else:
                self.fn = Sn3ChanAET2NoRescaling
        elif (CTDI==TDIEnum['TDI2XYZ'].value):
            if TDIrescaled:
                self.fn = Sn3ChanXYZ
            else:
                self.fn = Sn3ChanXYZ2NoRescaling
        else: raise ValueError("No support for TDI = " + TDI +".")
#
#         # self.obfn.object = <void*> &self.CLISAdata
#         # self.obfn.function = self.fn
#

    cpdef np.ndarray[np.float_t, ndim=2] apply(self, np.ndarray[np.float_t, ndim=1] freqs):
        cdef np.ndarray[np.float_t, ndim=2] Sndata = np.zeros((len(freqs), 4))
        cdef double Snval1
        cdef double Snval2
        cdef double Snval3
        cdef double f
        for i in range(len(freqs)):
            f = freqs[i]
            self.fn(&Snval1, &Snval2, &Snval3, &self.CLISAdata, f)
            Sndata[i,0] = f
            Sndata[i,1] = Snval1
            Sndata[i,2] = Snval2
            Sndata[i,3] = Snval3
        return Sndata

# Written as a pure numpy function for now
# Only implemented for TDI AET
def rescale_tdi_noise(freq, Sn1, Sn2, Sn3, TDI='TDIAET', LISAconst=LISAconstProposal):
    if isinstance(LISAconst, basestring):
        LISAconst = pyresponse.LISAconstDict[LISAconst]
    L = LISAconst['OrbitL']
    if TDI=='TDIAET':
        pifL = np.pi * freq * L / pyconstants.C_SI
        rescalingAE = 2 * np.sin(2 * pifL)**2
        rescalingT = 8 * np.sin(2 * pifL)**2 * np.sin(pifL)**2
        return Sn1 / rescalingAE, Sn2 / rescalingAE, Sn3 / rescalingT
    elif TDI=='TDI2AET':
        pifL = np.pi * freq * L / pyconstants.C_SI
        factor_tdi2 = 4*np.sin(4 * pifL)**2
        rescalingAE = factor_tdi2 * 2 * np.sin(2 * pifL)**2
        rescalingT = factor_tdi2 * 8 * np.sin(2 * pifL)**2 * np.sin(pifL)**2
        return Sn1 / rescalingAE, Sn2 / rescalingAE, Sn3 / rescalingT
    else:
        raise ValueError('For now, only TDIAET and TDI2AET implemented.')

# Simple function to initialize noise evaluator
# Allows the normal analytical interface as well as numerical data as input
# In the latter case, we build interpolating spline here (to avoid repeating this step)
# TODO: giving a rescaled numerical input is not supported yet
def initialize_noise(LISAnoise, TDI='TDIAET',
                     TDIrescaled=True,
                     LISAconst=LISAconstProposal):
    if isinstance(LISAnoise, np.ndarray):
        freq_Sn = np.copy(LISAnoise[:,0])
        Sn1_data = np.copy(LISAnoise[:,1])
        Sn2_data = np.copy(LISAnoise[:,2])
        Sn3_data = np.copy(LISAnoise[:,3])
        Sn1_splineClass = pyspline.CubicSpline(freq_Sn, Sn1_data)
        Sn2_splineClass = pyspline.CubicSpline(freq_Sn, Sn2_data)
        Sn3_splineClass = pyspline.CubicSpline(freq_Sn, Sn3_data)
        Sn1_spline = Sn1_splineClass.get_spline()
        Sn2_spline = Sn2_splineClass.get_spline()
        Sn3_spline = Sn3_splineClass.get_spline()
        noise_evaluator = [Sn1_spline, Sn2_spline, Sn3_spline]
    else:
        SnAPSDFunc3ChanClass = LISANoisePSDFunction3Chan(
                                             LISAnoise, TDI=TDI,
                                             TDIrescaled=TDIrescaled,
                                             LISAconst=LISAconst)
        noise_evaluator = SnAPSDFunc3ChanClass
    return noise_evaluator

# Simple function to evaluate the noise
# Allows the normal analytical interface as well as numerical data as input
def evaluate_noise(LISAnoise, noise_evaluator, freq,
                   TDI='TDIAET', TDIrescaled=True, LISAconst=LISAconstProposal):
    if isinstance(LISAnoise, np.ndarray):
        Sn1_spline = noise_evaluator[0]
        Sn2_spline = noise_evaluator[1]
        Sn3_spline = noise_evaluator[2]
        Sn1_vals = pyspline.spline_eval_vector(Sn1_spline, freq)
        Sn2_vals = pyspline.spline_eval_vector(Sn2_spline, freq)
        Sn3_vals = pyspline.spline_eval_vector(Sn3_spline, freq)
        if TDIrescaled:
            Sn1_vals, Sn2_vals, Sn3_vals = rescale_tdi_noise(freq, Sn1_vals, Sn2_vals, Sn3_vals, TDI=TDI, LISAconst=LISAconst)
    else:
        Sndata = noise_evaluator.apply(freq)
        Sn1_vals = Sndata[:,1]
        Sn2_vals = Sndata[:,2]
        Sn3_vals = Sndata[:,3]

    return Sn1_vals, Sn2_vals, Sn3_vals
