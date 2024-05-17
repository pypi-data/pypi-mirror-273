#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython definitions for spline interpolation tools.
"""

import numpy as np
cimport numpy as np

from lisabeta.struct.pystruct cimport *
from lisabeta.tools.pyspline cimport *

cdef extern from "overlap.h":

    double complex ComputeFresnelIntegral(
        CAmpPhaseFDData* integrand
    );

    double complex FDSinglemodeFresnelOverlap(
        CAmpPhaseFDData* freqseries1,
        CAmpPhaseFDSpline* splines2,
        double fLow,
        double fHigh
    );

    double complex FDSinglemodeFresnelOverlap3Chan(
        CAmpPhaseFDData* freqseries1chan1,
        CAmpPhaseFDData* freqseries1chan2,
        CAmpPhaseFDData* freqseries1chan3,
        CAmpPhaseFDSpline* splines2chan1,
        CAmpPhaseFDSpline* splines2chan2,
        CAmpPhaseFDSpline* splines2chan3,
        double fLow,
        double fHigh
    );
