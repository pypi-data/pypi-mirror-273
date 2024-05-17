#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython definitions for LISA FD response.
"""

import numpy as np
cimport numpy as np
from enum import Enum

from lisabeta.pyconstants cimport *
from lisabeta.struct.pystruct cimport *


cdef extern from "LISAgeometry.h":

    enum TDItag:
        TDIAET = 0
        TDIXYZ = 1
        TDI2AET = 2
        TDI2XYZ = 3

    enum ResponseApproxtag:
        full         = 0
        lowfL        = 1
        lowf         = 2
        ignoreRdelay = 3

    ctypedef struct LISAconstellation:
        double OrbitOmega;
        double OrbitPhi0;
        double Orbitt0;
        double OrbitR;
        double OrbitL;

cdef extern from "LISAresponse.h":

    int EvalLISAFDresponseTDI3Chan (
        real_vector** phaseRdelay,
        complex_vector** transfer1,
        complex_vector** transfer2,
        complex_vector** transfer3,
        real_vector* freq,
        real_vector* tf,
        const double t0,
        const int l,
        const int m,
        const double inc,
        const double phi,
        const double lambd,
        const double beta,
        const double psi,
        const TDItag tditag,
        const LISAconstellation *LISAconst,
        const ResponseApproxtag responseapprox,
        const int tagfrozenLISA,
        const int rescaled
    );
