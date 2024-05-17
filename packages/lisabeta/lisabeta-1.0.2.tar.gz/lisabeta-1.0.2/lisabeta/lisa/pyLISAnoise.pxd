#
#  Copyright (C) 2019 Sylvain Marsat.
#


"""
    Cython declarations for LISA noise
"""

cimport numpy as np

# from lisabeta.pyconstants cimport *
# from lisabeta.struct.pystruct cimport *
from pyresponse cimport *

cdef extern from "LISAnoise.h":
    #double SnXYZ(const LISANoiseModel *LISAnoise,
    #             const LISAconstellation *LISAconst,
    #             double f);
    #double SnA(const LISANoiseModel *LISAnoise,
    #              const LISAconstellation *LISAconst,
    #              double f);
    #double SnE(const LISANoiseModel *LISAnoise,
    #              const LISAconstellation *LISAconst,
    #              double f);
    #double SnT(const LISANoiseModel *LISAnoise,
    #              const LISAconstellation *LISAconst,
    #              double f);
    #double SnXYZNoRescaling(const LISANoiseModel *LISAnoise,
    #                         const LISAconstellation *LISAconst,
    #                         double f);
    #double SnANoRescaling(const LISANoiseModel *LISAnoise,
    #                         const LISAconstellation *LISAconst,
    #                         double f);
    #double SnENoRescaling(const LISANoiseModel *LISAnoise,
    #                         const LISAconstellation *LISAconst,
    #                         double f);
    #double SnTNoRescaling(const LISANoiseModel *LISAnoise,
    #                         const LISAconstellation *LISAconst,
    #                         double f);

    double SnXYZ(const void* variant, double f);
    double SnA(const void* variant, double f);
    double SnE(const void* variant, double f);
    double SnT(const void* variant, double f);
    double SnXYZNoRescaling(const void* variant, double f);
    double SnANoRescaling(const void* variant, double f);
    double SnENoRescaling(const void* variant, double f);
    double SnTNoRescaling(const void* variant, double f);
    double SnXYZ2NoRescaling(const void* variant, double f);
    double SnA2NoRescaling(const void* variant, double f);
    double SnE2NoRescaling(const void* variant, double f);
    double SnT2NoRescaling(const void* variant, double f);

    void Sn3ChanXYZ(double* SnX,
                    double* SnY,
                    double* SnZ,
                    const void* object,
                    double f);

    void Sn3ChanXYZNoRescaling(double* SnX,
                               double* SnY,
                               double* SnZ,
                               const void* object,
                               double f);

    void Sn3ChanXYZ2NoRescaling(double* SnX,
                               double* SnY,
                               double* SnZ,
                               const void* object,
                               double f);

    void Sn3ChanAET(double* SnA,
                    double* SnE,
                    double* SnT,
                    const void* object,
                    double f);

    void Sn3ChanAETNoRescaling(double* SnA,
                               double* SnE,
                               double* SnT,
                               const void* object,
                               double f);

    void Sn3ChanAET2NoRescaling(double* SnA,
                               double* SnE,
                               double* SnT,
                               const void* object,
                               double f);

    enum LISAInstrumentalNoise:
        LISASciRDv1noise  = 0
        LISAProposalnoise = 1
        LISA2010noise     = 2
        LISA2017noise     = 3

    ctypedef struct LISANoiseModel:
        LISAInstrumentalNoise noise;
        int WDbackground;
        double WDduration;
        double lowf_add_pm_noise_f0;
        double lowf_add_pm_noise_alpha;

    ctypedef struct LISA_noise_func_data:
        const LISANoiseModel *LISAnoise;
        const LISAconstellation *LISAconst;



#ctypedef double (*CLISANoisePSDFunc)(const LISANoiseModel *LISAnoise,
#                                     const LISAconstellation *LISAconst,
#                                     double f)
ctypedef double (*CLISANoisePSDFunc)(const void* variant, double f)
ctypedef void (*CLISANoisePSDFunc3Chan)(double* Snval1, double* Snval2, double* Snval3, const void* variant, double f)
ctypedef int (*CLISANoisePSDFuncVec)(real_vector** Snvals, const void* variant, real_vector* freq)

cdef class LISANoisePSDFunction(py_object_function):
    cdef LISAconstellation CLISAconst
    cdef LISANoiseModel CLISAnoise
    cdef LISA_noise_func_data CLISAdata
    cdef CLISANoisePSDFunc fn
    #cdef ... fn_vec
    #cdef object_function obfn
    #cpdef double call(self, double f)
    #cpdef np.ndarray[np.float_t, ndim=1] apply(self, np.ndarray[np.float_t, ndim=1] freq)
    #cpdef np.ndarray[np.float_t, ndim=1] apply_vec(self, np.ndarray[np.float_t, ndim=1] freq)

cdef class LISANoisePSDFunction3Chan:
    cdef LISAconstellation CLISAconst
    cdef LISANoiseModel CLISAnoise
    cdef LISA_noise_func_data CLISAdata
    cdef CLISANoisePSDFunc3Chan fn

    cpdef np.ndarray[np.float_t, ndim=2] apply(self, np.ndarray[np.float_t, ndim=1] freqs)
