#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython definitions for generic waveform tools.
"""

import numpy as np
cimport numpy as np

from lisabeta.pyconstants cimport *
from lisabeta.struct.pystruct cimport *

cdef extern from "tools.h":

    double complex SpinWeightedSphericalHarmonic (
        double theta,
        double phi,
        int s,
        int l,
        int m
    );

    int BuildWaveformGeomFrequencyGrid (
        real_vector** Mfreq,
        const double Mfmin,
        const double Mfmax,
        const double eta,
        const double acc
    );

    int BuildResponseFrequencyGrid (
      real_vector** freq,
      real_matrix* tfspline,
      const double f_min,
      const double f_max,
      const double Deltat_max,
      const double Deltaf_max,
      const int nptlogmin
    );

    int BuildFrequencyGrid (
      real_vector** freq,
      const double f_min,
      const double f_max,
      const double M,
      const double q,
      const double Deltat_max,
      const double Deltaf_max,
      const double DeltalnMf_max,
      const double acc,
      const int nptlogmin
    );

    int BuildMergedGrid (
      real_vector** grid,
      real_vector* grid1,
      real_vector* grid2,
      const int usedeltaxmin,
      const double deltaxmin,
      const int usedeltalnxmin,
      const double deltalnxmin
    );

    double LinearInterpMultiMode3ChannelsResidualNorm(
      complex_array_3d* alpha0,
      complex_array_3d* alpha1,
      complex_array_3d* w0,
      complex_array_3d* w1,
      complex_array_3d* w2
    );
