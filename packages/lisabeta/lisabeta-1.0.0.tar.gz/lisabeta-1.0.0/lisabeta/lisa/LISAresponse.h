/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#ifndef _LISAFDRESPONSE_H
#define _LISAFDRESPONSE_H

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

#include "constants.h"
#include "struct.h"
#include "tools.h"
#include "LISAgeometry.h"


#if defined(__cplusplus)
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif

/******************************************************************************/
/* Response function and TDI combinations */
/******************************************************************************/

/* Function evaluating the G^lm_slr kernels */
/* NOTE: higher-order response not yet implemented */
int EvaluateGlmslr(
  double complex* G12,                     /* Output for G12 */
  double complex* G21,                     /* Output for G21 */
  double complex* G23,                     /* Output for G23 */
  double complex* G32,                     /* Output for G32 */
  double complex* G31,                     /* Output for G31 */
  double complex* G13,                     /* Output for G13 */
  const double f,                          /* Frequency (Hz) */
  const double t,                          /* Time (s) */
  const double complex Yfactorplus,        /* sYlm combined prefactor: plus */
  const double complex Yfactorcross,       /* sYlm combined prefactor: cross */
  LISAGeometricCoefficients* coeffs,       /* Struct for precomputed coeffs */
  const LISAconstellation *LISAconst,      /* LISA orbital constants */
  const ResponseApproxtag responseapprox); /* Approximation level in response */

/* Function evaluating the Fourier-domain combinations of Gslr's for TDI */
/* NOTE: factors have been scaled out, in parallel to the noise function */
int EvaluateTDIfactor3Chan(
  double complex* transfer1,              /* Output: transfer for TDI chan. 1 */
  double complex* transfer2,              /* Output: transfer for TDI chan. 2 */
  double complex* transfer3,              /* Output: transfer for TDI chan. 3 */
  const double complex G12,               /* Input for G12 */
  const double complex G21,               /* Input for G21 */
  const double complex G23,               /* Input for G23 */
  const double complex G32,               /* Input for G32 */
  const double complex G31,               /* Input for G31 */
  const double complex G13,               /* Input for G13 */
  const double f,                         /* Frequency (Hz) */
  const TDItag tditag,                    /* Choice of TDI observable */
  const LISAconstellation *LISAconst,     /* LISA orbital constants */
  const ResponseApproxtag responseapprox, /* Approximation in FD response */
  const int rescaled);                    /* Apply rescaling to response */

/******************************************************************************/
/* TDI rescalings */
/******************************************************************************/

/* Function for the Fourier-domain factors scaled out of TDI observables */
/* The factors scaled out, parallel what is done for the noise functions */
int ScaledTDIfactor3Chan(
  double complex* factor1,             /* Output: factor for TDI factor 1 */
  double complex* factor2,             /* Output: factor for TDI factor 2 */
  double complex* factor3,             /* Output: factor for TDI factor 3 */
  const double f,                      /* Frequency (Hz)*/
  const TDItag tditag,                 /* Selector for the TDI observables */
  const LISAconstellation *LISAconst); /* LISA orbital constants */

// /* Function restoring the factor scaled out of the TDI observables */
// /* NOTE: the operation is made in-place, and the input is overwritten */
// int RestoreInPlaceScaledFactorTDI(
//   const LISAconstellation *variant,    /* Description of LISA variant */
//   ListmodesCAmpPhaseFrequencySeries* listtdi,     /* Output/Input: list of mode contributions to TDI observable */
//   TDItag tditag,                                  /* Tag selecting the TDI observable */
//   int nchannel);                                  /* TDI channel number */

/******************************************************************************/
/* TDI response function */
/******************************************************************************/

/* TDI response function for a single mode hlm */
/* tf gives t-t0, t0 (in yrs) locates the waveform in SSB time */
/* NOTE: phaseRdelay kept separately and factored out from TDI transfers */
int EvalLISAFDresponseTDI3Chan(
  real_vector** phaseRdelay,           /* Output: orbital delay phase */
  complex_vector** transfer1,          /* Output: transfer for TDI channel 1 */
  complex_vector** transfer2,          /* Output: transfer for TDI channel 2 */
  complex_vector** transfer3,          /* Output: transfer for TDI channel 3 */
  real_vector* freq,                   /* Frequencies to evaluate on (Hz) */
  real_vector* tf,                     /* Input tf (s) */
  const double t0,                     /* Reference orbital time (yr) */
  const int l,                         /* Mode number l */
  const int m,                         /* Mode number m */
  const double inc,                    /* Inclination in source-frame */
  const double phi,                    /* Azimuthal phase in source-frame */
  const double lambd,                  /* Ecliptic longitude, SSB-frame */
  const double beta,                   /* Ecliptic latitude, SSB-frame */
  const double psi,                    /* Polarization angle, SSB-frame */
  const TDItag tditag,                 /* Choice of TDI observable */
  const LISAconstellation *LISAconst,  /* LISA orbital constants */
  const ResponseApproxtag responseapprox, /* Approximation in FD response */
  const int tagfrozenLISA,             /* Tag to treat LISA as motionless */
  const int rescaled);                 /* Apply rescaling to response */


#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _LISAFDRESPONSE_H */
