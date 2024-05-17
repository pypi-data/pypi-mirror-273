/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#ifndef _WAVEFORM_TOOLS_H
#define _WAVEFORM_TOOLS_H

#define _XOPEN_SOURCE 500

#ifdef __GNUC__
#define UNUSED __attribute__ ((unused))
#else
#define UNUSED
#endif

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#include <time.h>
#include <unistd.h>
#include <getopt.h>
#include <stdbool.h>
#include <string.h>

#include <gsl/gsl_errno.h>
#include <gsl/gsl_bspline.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_min.h>
#include <gsl/gsl_spline.h>
#include <gsl/gsl_complex.h>

#include "struct.h"
#include "constants.h"
#include "spline.h"


#if defined(__cplusplus)
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif
/******************************************************************************/
/* Numerical functions */
/******************************************************************************/

#ifndef min
#define min(a,b)            (((a) < (b)) ? (a) : (b))
#endif

#ifndef max
#define max(a,b)            (((a) < (b)) ? (b) : (a))
#endif

/* Function cardinal sine */
inline double sinc(const double x) {
  if (x==0)
    return 1;
  else return sin(x)/x;
}

/* Function for getting a phase mod 2pi (between -pi and pi) */
inline double mod2pi(double phase) {
  return phase - floor((phase + PI) / (2*PI)) * (2*PI);
}
/* Function for getting a phase mod pi (between 0 and pi, e.g. polarization) */
inline double modpi(double phase) {
  return phase - floor(phase / PI) * PI;
}

/******************************************************************************/
/* Functions for frequency grids */
/******************************************************************************/

/* Build geom frequency grid suitable for waveform amp/phase interpolation */
int BuildWaveformGeomFrequencyGrid(
  real_vector** Mfreq,   /* Output: pointer to real vector */
  const double Mfmin,    /* Starting geometric frequency */
  const double Mfmax,    /* Ending geometric frequency */
  const double eta,      /* Symmetric mass ratio */
  const double acc);     /* Desired phase interpolation error for inspiral */

/* Build frequency grid suitable for representing the LISA response */
int BuildResponseFrequencyGrid(
  real_vector** freq,       /* Output: pointer to real vector */
  real_matrix* tfspline,    /* Spline matrix for tf */
  const double f_min,       /* Minimal frequency */
  const double f_max,       /* Maximal frequency */
  const double Deltat_max,  /* Maximal time step, in years */
  const double Deltaf_max,  /* Maximal frequency step, in Hz */
  const int nptlogmin);     /* Minimal number of points with log-spacing */

/* Build frequency grid suitable for both the waveform and the response */
int BuildFrequencyGrid(
  real_vector** freq,          /* Output: pointer to real vector */
  const double f_min,          /* Minimal frequency (Hz) */
  const double f_max,          /* Maximal frequency (Hz) */
  const double M,              /* Total mass (solar masses) */
  const double q,              /* Symmetric mass ratio */
  const double Deltat_max,     /* Maximal time step, in years */
  const double Deltaf_max,     /* Maximal frequency step, in Hz */
  const double DeltalnMf_max,  /* Maximal ln(Mf) step */
  const double acc,            /* Target phase interpolation error (inspiral) */
  const int nptlogmin);        /* Minimal number of points with log-spacing */

/******************************************************************************/
/* Function for merging two monotonously increasing grids */
/******************************************************************************/

/* Merge two grids with increasing values (e.g. two frequency grids) */
/* Discards duplicate values */
/* Allows for safeguarding: can ignore points that are almost identical */
/* Two criterion available: absolute deltax or relative deltalnx */
/* NOTE: deltalnx criterion only allowed for positive values of x */
int BuildMergedGrid(
    real_vector** grid,      /* Output: merged grid */
    real_vector* grid1,      /* Input: grid1 */
    real_vector* grid2,      /* Input: grid2 */
    const int usedeltaxmin,        /* Flag to use a minimal deltax criterion */
    const double deltaxmin,        /* Value of minimal deltax criterion */
    const int usedeltalnxmin,      /* Flag to use a minimal deltalnx criterion */
    const double deltalnxmin       /* Value of minimal deltalnx criterion */
);

/******************************************************************************/
/* Helper function for residuals likelihood */
/******************************************************************************/

double LinearInterpMultiMode3ChannelsResidualNorm(
  complex_array_3d* alpha0,
  complex_array_3d* alpha1,
  complex_array_3d* w0,
  complex_array_3d* w1,
  complex_array_3d* w2);

/******************************************************************************/
/* Functions for Spin weighted spherical harmonics */
/******************************************************************************/

/* Function reproducing XLALSpinWeightedSphericalHarmonic */
/* Currently only supports s=-2, l=2,3,4,5 modes */
double complex SpinWeightedSphericalHarmonic(
  double theta,
  double phi,
  int s,
  int l,
  int m);

#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _WAVEFORM_TOOLS_H */
