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

cdef extern from "spline.h":

    int BuildNotAKnotSpline(
        real_matrix** splinecoeffs,
        real_vector* vectx,
        real_vector* vecty
    );

    int BuildQuadSpline(
        real_matrix** splinecoeffs,
        real_vector* vectx,
        real_vector* vecty
    );

    int CubicSplineDerivative(
        real_matrix** spline_deriv,
        real_matrix* spline
    );

    int CubicSplineDoubleDerivative(
        real_matrix** spline_dderiv,
        real_matrix* spline
    );

    int CubicSplineIntegral(
        real_matrix** spline_int,
        real_matrix* spline
    );

    int QuadSplineDerivative(
        real_matrix** spline_deriv,
        real_matrix* spline
    );

    int EvalCubicSplineOnVector(
        real_vector** yvec,
        real_vector* xvec,
        real_matrix* spline,
        int extrapol_zero
    );

    int EvalQuadSplineOnVector(
        real_vector** yvec,
        real_vector* xvec,
        real_matrix* spline,
        int extrapol_zero
    );

    # UNFINISHED
    # REQUIRES DEBUGGING
    # int EvalCubicSplineCExpOnConstDeltaxVector(
    #     complex_vector** cexpvec,
    #     real_vector* xvec,
    #     real_matrix* phase_spline
    # );
