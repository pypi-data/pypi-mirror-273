/**
 * \author Sylvain Marsat, University of Maryland - NASA GSFC
 *
 * \brief C header for the computation of the Fourier-domain overlaps, likelihoods.
 *
 *
 */

#ifndef _OVERLAP_H
#define _OVERLAP_H

#define _XOPEN_SOURCE 500

#ifdef __GNUC__
#define UNUSED __attribute__ ((unused))
#else
#define UNUSED
#endif

#include "constants.h"
#include "struct.h"
#include "spline.h"
#include "fresnel.h"


#if defined(__cplusplus)
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif



/******************************************************************************/
/* Functions to compute integrand values in preparation for amp/phase overlap */
/******************************************************************************/

/* Function computing the integrand values */
int ComputeIntegrandValues(
  CAmpPhaseFDData** integrand,   /* Output: integrand on the (cut) freqs of 1 */
  CAmpPhaseFDData* freqseries1,  /* Input: wf 1, camp/phase */
  CAmpPhaseFDSpline* splines2,   /* Input: wf 2, camp/phase splines */
  const double fLow,             /* Lower bound frequency - 0 to ignore */
  const double fHigh);           /* Upper bound frequency - 0 to ignore */
/* Function computing the integrand values, combining three channels */
/* NOTE: assumes phase is the same across channels */
int ComputeIntegrandValues3Chan(
  CAmpPhaseFDData** integrand,   /* Output: integrand on the (cut) freqs of 1 */
  CAmpPhaseFDData* freqseries1chan1, /* Input: wf 1, camp/phase, channel 1 */
  CAmpPhaseFDData* freqseries1chan2, /* Input: wf 1, camp/phase, channel 2 */
  CAmpPhaseFDData* freqseries1chan3, /* Input: wf 1, camp/phase, channel 3 */
  CAmpPhaseFDSpline* splines2chan1,  /* Input: wf 2, camp/phase splines, channel 1 */
  CAmpPhaseFDSpline* splines2chan2,  /* Input: wf 2, camp/phase splines, channel 2 */
  CAmpPhaseFDSpline* splines2chan3,  /* Input: wf 2, camp/phase splines, channel 3 */
  const double fLow,                 /* Lower bound frequency - 0 to ignore */
  const double fHigh);               /* Upper bound frequency - 0 to ignore */

/******************************************************************************/
/* Functions to compute amp/phase overlap */
/******************************************************************************/

/* Compute (h1|h2) = 4Re \int (h1 h2* / Sn)  */
/* Integrand represents camp/phase data for (h1 h2* / Sn) */
/* Does a cubic spline interpolation for the complex amplitude */
/* and a quadratic spline interplolation for the phase */
/* NOTE: we return the complex overlap, no Re() */
double complex ComputeFresnelIntegral(CAmpPhaseFDData* integrand);

/* Function computing the overlap (h1|h2) between two amplitude/phase signals */
/* Signal 1 is in amplitude/phase form */
/* Signal 2 is already interpolated, and already has weighting by the noise */
/* NOTE: we return the complex overlap, no Re() */
double complex FDSinglemodeFresnelOverlap(
  CAmpPhaseFDData* freqseries1, /* First mode h1, in camp/phase form */
  CAmpPhaseFDSpline* splines2,  /* Second mode h2, splines, noise-weighted */
  double fLow,                  /* Lower bound frequency - 0 to ignore */
  double fHigh);                /* Upper bound frequency - 0 to ignore */

/* Function computing the overlap (h1|h2) between two amplitude/phase signals */
/* Signal 1 is in amplitude/phase form */
/* Signal 2 is already interpolated, and already has weighting by the noise */
/* NOTE: frequencies and phases are assumed the same across channels */
/* NOTE: we return the complex overlap, no Re() */
double complex FDSinglemodeFresnelOverlap3Chan(
  CAmpPhaseFDData* freqseries1chan1, /* First wf h1, camp/phase, channel 1 */
  CAmpPhaseFDData* freqseries1chan2, /* First wf h1, camp/phase, channel 2 */
  CAmpPhaseFDData* freqseries1chan3, /* First wf h1, camp/phase, channel 3 */
  CAmpPhaseFDSpline* splines2chan1,  /* Second wf h2, splines, noise-weighted, channel 1 */
  CAmpPhaseFDSpline* splines2chan2,  /* Second wf h2, splines, noise-weighted, channel 2 */
  CAmpPhaseFDSpline* splines2chan3,  /* Second wf h2, splines, noise-weighted, channel 3 */
  double fLow,                       /* Lower bound frequency - 0 to ignore */
  double fHigh);                     /* Upper bound frequency - 0 to ignore */


#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _OVERLAP_H */
