/**
 * \author Sylvain Marsat, University of Maryland - NASA GSFC
 *
 * \brief C code for the implementation of the Fourier-domain overlaps, likelihoods.
 *
 */


#define _XOPEN_SOURCE 500

#ifdef __GNUC__
#define UNUSED __attribute__ ((unused))
#else
#define UNUSED
#endif

#include "overlap.h"


/******************************************************************************/
/* Utilities */
/******************************************************************************/

/* Quadratic Legendre approximation to compute values at minf and maxf when they do not fall on the grid of a freqseries, using the two first/last intervals */
static double LegendreQuad(
  real_vector* vectx,   /**/
  real_vector* vecty,   /**/
  int j,               /**/
  double xvalue)       /**/
{
  double x0 = real_vector_get(vectx, j);
  double x1 = real_vector_get(vectx, j+1);
  double x2 = real_vector_get(vectx, j+2);
  double x = xvalue;
  double y0 = real_vector_get(vecty, j);
  double y1 = real_vector_get(vecty, j+1);
  double y2 = real_vector_get(vecty, j+2);
  if ( !(x>=x0 && x<=x2) ) {
    printf("%.16e %.16e %.16e %.16e\n", x0, x1, x2, x);
    ERROR(ERROR_EINVAL, "Value out of bounds.");
  }
  return y0*(x-x1)*(x-x2)/(x0-x1)/(x0-x2) + y1*(x-x0)*(x-x2)/(x1-x0)/(x1-x2)
         + y2*(x-x0)*(x-x1)/(x2-x0)/(x2-x1);
}

/******************************************************************************/
/* Functions to compute integrand values in preparation for amp/phase overlap */
/******************************************************************************/

/* Function computing the integrand values */
int ComputeIntegrandValues(
  CAmpPhaseFDData** integrand,   /* Output: integrand on the (cut) freqs of 1 */
  CAmpPhaseFDData* freqseries1,  /* Input: wf 1, camp/phase */
  CAmpPhaseFDSpline* splines2,   /* Input: wf 2, camp/phase splines */
  const double fLow,             /* Lower bound frequency - 0 to ignore */
  const double fHigh)            /* Upper bound frequency - 0 to ignore */
{
  /* Check input pointers */
  if (freqseries1 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1 is NULL.");
  if (splines2 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2 is NULL.");
  if (*integrand != NULL)
    ERROR(ERROR_EFAULT, "Output pointer to integrand is not NULL.");

  /* Check frequency bounds */
  double f1min = real_vector_get(freqseries1->freq, 0);
  double f1max = real_vector_get(freqseries1->freq, freqseries1->freq->size-1);
  double f2min = real_matrix_get(splines2->spline_phase, 0, 0);
  double f2max = real_matrix_get(splines2->spline_phase,
                                 splines2->spline_phase->size1-1, 0);
  double minf = fmax(f1min, f2min);
  double maxf = fmin(f1max, f2max);
  if (fLow>0) minf = fmax(minf, fLow);
  if (fHigh>0) maxf = fmin(maxf, fHigh);
  if (minf>=maxf)
    ERROR(ERROR_EINVAL, "Frequency ranges are incompatible.");

  /* Data pointers */
  real_vector* freq1 = freqseries1->freq;
  double* f1 = freqseries1->freq->data;
  double* areal1 = freqseries1->amp_real->data;
  double* aimag1 = freqseries1->amp_imag->data;
  double* phi1 = freqseries1->phase->data;

  /* Determining the boundary indices in freqseries1 */
  /* Move the ending frequencies to be just outside the final minf and maxf */
  int imin1 = 0;
  int imax1 = freq1->size - 1;
  while (f1[imin1+1]<=minf) imin1++;
  while (f1[imax1-1]>=maxf) imax1--;
  if (imax1<=imin1+3)
    ERROR(ERROR_EINVAL, "Not enough common points to build integrand.");

  /* Estimate locally values for freqseries1 at the boundaries */
  double areal1minf = LegendreQuad(freq1, freqseries1->amp_real, imin1, minf);
  double aimag1minf = LegendreQuad(freq1, freqseries1->amp_imag, imin1, minf);
  double phi1minf = LegendreQuad(freq1, freqseries1->phase, imin1, minf);
  /* Note the imax1-2 */
  double areal1maxf = LegendreQuad(freq1, freqseries1->amp_real, imax1-2, maxf);
  double aimag1maxf = LegendreQuad(freq1, freqseries1->amp_imag, imax1-2, maxf);
  double phi1maxf = LegendreQuad(freq1, freqseries1->phase, imax1-2, maxf);

  /* Initializing output structure */
  int nbpts = imax1 + 1 - imin1;
  CAmpPhaseFDData_Init(integrand, nbpts);

  /* Loop computing integrand values */
  real_vector* freq = (*integrand)->freq;
  real_vector* ampreal = (*integrand)->amp_real;
  real_vector* ampimag = (*integrand)->amp_imag;
  real_vector* phase = (*integrand)->phase;
  double f = 0., ampreal1 = 0., ampimag1 = 0., phase1 = 0., ampreal2 = 0., ampimag2 = 0., phase2 = 0.;
  double complex camp = 0.;
  real_matrix* splineAreal2 = splines2->spline_amp_real;
  real_matrix* splineAimag2 = splines2->spline_amp_imag;
  real_matrix* splinephase2 = splines2->spline_phase;
  size_t i2_ampreal = 0, i2_ampimag = 0, i2_phase = 0;
  int j = 0;
  for(int i=imin1; i<=imax1; i++) {
    /* Distinguish the case where we are at minf or maxf */
    if(i==imin1) {
      f = minf;
      ampreal1 = areal1minf;
      ampimag1 = aimag1minf;
      phase1 = phi1minf;
    }
    else if(i==imax1) {
      f = maxf;
      ampreal1 = areal1maxf;
      ampimag1 = aimag1maxf;
      phase1 = phi1maxf;
    }
    else {
      f = real_vector_get(freq1, i);
      ampreal1 = areal1[i];
      ampimag1 = aimag1[i];
      phase1 = phi1[i];
    }
    /* Adjust the index in the spline if necessary and compute */
    /* NOTE: i2_ampreal, i2_ampaimg and i2_phase are in fact the same */
    /* Slight unnecessary overhead in keeping track of them separately */
    EvalCubicSplineSlide(&ampreal2, splineAreal2, &i2_ampreal, f);
    EvalCubicSplineSlide(&ampimag2, splineAimag2, &i2_ampimag, f);
    EvalCubicSplineSlide(&phase2, splinephase2, &i2_phase, f);
    camp = (ampreal1 + I*ampimag1) * (ampreal2 - I*ampimag2);
    real_vector_set(freq, j, f);
    real_vector_set(ampreal, j, creal(camp));
    real_vector_set(ampimag, j, cimag(camp));
    real_vector_set(phase, j, phase1 - phase2);
    j++;
  }

  return SUCCESS;
}

/* Function computing the integrand values, combining three channels */
/* NOTE: assumes frequencies are the same across channels */
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
  const double fHigh)                /* Upper bound frequency - 0 to ignore */
{
  /* Check input pointers */
  if (freqseries1chan1 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1chan1 is NULL.");
  if (freqseries1chan2 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1chan2 is NULL.");
  if (freqseries1chan3 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1chan3 is NULL.");
  if (splines2chan1 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2chan1 is NULL.");
  if (splines2chan2 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2chan2 is NULL.");
  if (splines2chan3 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2chan3 is NULL.");
  if (*integrand != NULL)
    ERROR(ERROR_EFAULT, "Output pointer to integrand is not NULL.");

  /* Check frequency bounds */
  double f1min = real_vector_get(freqseries1chan1->freq, 0);
  double f1max = real_vector_get(freqseries1chan1->freq,
                                freqseries1chan1->freq->size-1);
  double f2min = real_matrix_get(splines2chan1->spline_phase, 0, 0);
  double f2max = real_matrix_get(splines2chan1->spline_phase,
                                 splines2chan1->spline_phase->size1-1, 0);
  double minf = fmax(f1min, f2min);
  double maxf = fmin(f1max, f2max);
  if (fLow>0) minf = fmax(minf, fLow);
  if (fHigh>0) maxf = fmin(maxf, fHigh);
  /* When frequency ranges are incompatible, we might want to attribute 0
     to the overlap, or treat this as an error -- so return FAILURE code */
  if (minf>=maxf) return FAILURE;

  /* Data pointers */
  real_vector* freq1 = freqseries1chan1->freq;
  double* f1 = freqseries1chan1->freq->data;
  double* areal1chan1 = freqseries1chan1->amp_real->data;
  double* areal1chan2 = freqseries1chan2->amp_real->data;
  double* areal1chan3 = freqseries1chan3->amp_real->data;
  double* aimag1chan1 = freqseries1chan1->amp_imag->data;
  double* aimag1chan2 = freqseries1chan2->amp_imag->data;
  double* aimag1chan3 = freqseries1chan3->amp_imag->data;
  double* phi1chan1 = freqseries1chan1->phase->data;

  /* Determining the boundary indices in freqseries1 */
  /* Move the ending frequencies to be just outside the final minf and maxf */
  int imin1 = 0;
  int imax1 = freq1->size - 1;
  while (f1[imin1+1]<=minf) imin1++;
  while (f1[imax1-1]>=maxf) imax1--;
  if (imax1<=imin1+3) {
    /* WARNING("Not enough common points to build integrand -- ComputeIntegrandValues3Chan will return FAILURE, which will be interpreted as a 0 overlap."); */
    return FAILURE;
  }

  /* Estimate locally values for freqseries1 at the boundaries */
  double areal1chan1minf = LegendreQuad(freq1, freqseries1chan1->amp_real, imin1, minf);
  double areal1chan2minf = LegendreQuad(freq1, freqseries1chan2->amp_real, imin1, minf);
  double areal1chan3minf = LegendreQuad(freq1, freqseries1chan3->amp_real, imin1, minf);
  double aimag1chan1minf = LegendreQuad(freq1, freqseries1chan1->amp_imag, imin1, minf);
  double aimag1chan2minf = LegendreQuad(freq1, freqseries1chan2->amp_imag, imin1, minf);
  double aimag1chan3minf = LegendreQuad(freq1, freqseries1chan3->amp_imag, imin1, minf);
  /* Assumes the same phase in the three channels */
  double phi1minf = LegendreQuad(freq1, freqseries1chan1->phase, imin1, minf);
  /* Note the imax1-2 */
  double areal1chan1maxf = LegendreQuad(freq1, freqseries1chan1->amp_real, imax1-2, maxf);
  double areal1chan2maxf = LegendreQuad(freq1, freqseries1chan2->amp_real, imax1-2, maxf);
  double areal1chan3maxf = LegendreQuad(freq1, freqseries1chan3->amp_real, imax1-2, maxf);
  double aimag1chan1maxf = LegendreQuad(freq1, freqseries1chan1->amp_imag, imax1-2, maxf);
  double aimag1chan2maxf = LegendreQuad(freq1, freqseries1chan2->amp_imag, imax1-2, maxf);
  double aimag1chan3maxf = LegendreQuad(freq1, freqseries1chan3->amp_imag, imax1-2, maxf);
  /* Assumes the same phase in the three channels */
  double phi1maxf = LegendreQuad(freq1, freqseries1chan1->phase, imax1-2, maxf);

  /* Initializing output structure */
  int nbpts = imax1 + 1 - imin1;
  CAmpPhaseFDData_Init(integrand, nbpts);

  /* Loop computing integrand values */
  real_vector* freq = (*integrand)->freq;
  real_vector* ampreal = (*integrand)->amp_real;
  real_vector* ampimag = (*integrand)->amp_imag;
  real_vector* phase = (*integrand)->phase;
  double f;
  double ampreal1chan1 = 0., ampimag1chan1 = 0.;
  double ampreal1chan2 = 0., ampimag1chan2 = 0.;
  double ampreal1chan3 = 0., ampimag1chan3 = 0.;
  double ampreal2chan1 = 0., ampimag2chan1 = 0.;
  double ampreal2chan2 = 0., ampimag2chan2 = 0.;
  double ampreal2chan3 = 0., ampimag2chan3 = 0.;
  double phase1 = 0., phase2 = 0.;
  double complex camp = 0.;
  real_matrix* splineAreal2chan1 = splines2chan1->spline_amp_real;
  real_matrix* splineAreal2chan2 = splines2chan2->spline_amp_real;
  real_matrix* splineAreal2chan3 = splines2chan3->spline_amp_real;
  real_matrix* splineAimag2chan1 = splines2chan1->spline_amp_imag;
  real_matrix* splineAimag2chan2 = splines2chan2->spline_amp_imag;
  real_matrix* splineAimag2chan3 = splines2chan3->spline_amp_imag;
  real_matrix* splinephase2chan1 = splines2chan1->spline_phase;
  size_t i2_amprealchan1 = 0, i2_ampimagchan1 = 0;
  size_t i2_amprealchan2 = 0, i2_ampimagchan2 = 0;
  size_t i2_amprealchan3 = 0, i2_ampimagchan3 = 0;
  size_t i2_phase = 0;
  int j = 0;
  for(int i=imin1; i<=imax1; i++) {
    /* Distinguish the case where we are at minf or maxf */
    if(i==imin1) {
      f = minf;
      ampreal1chan1 = areal1chan1minf;
      ampimag1chan1 = aimag1chan1minf;
      ampreal1chan2 = areal1chan2minf;
      ampimag1chan2 = aimag1chan2minf;
      ampreal1chan3 = areal1chan3minf;
      ampimag1chan3 = aimag1chan3minf;
      phase1 = phi1minf;
    }
    else if(i==imax1) {
      f = maxf;
      ampreal1chan1 = areal1chan1maxf;
      ampimag1chan1 = aimag1chan1maxf;
      ampreal1chan2 = areal1chan2maxf;
      ampimag1chan2 = aimag1chan2maxf;
      ampreal1chan3 = areal1chan3maxf;
      ampimag1chan3 = aimag1chan3maxf;
      phase1 = phi1maxf;
    }
    else {
      f = real_vector_get(freq1, i);
      ampreal1chan1 = areal1chan1[i];
      ampimag1chan1 = aimag1chan1[i];
      ampreal1chan2 = areal1chan2[i];
      ampimag1chan2 = aimag1chan2[i];
      ampreal1chan3 = areal1chan3[i];
      ampimag1chan3 = aimag1chan3[i];
      phase1 = phi1chan1[i]; /* Assumes the same phase across three channels */
    }
    /* Adjust the index in the spline if necessary and compute */
    /* NOTE: i2_ampreal, i2_ampimag and i2_phase are in fact the same */
    /* NOTE: indices are also the same across channels */
    /* Slight unnecessary overhead in keeping track of them separately */
    EvalCubicSplineSlide(&ampreal2chan1, splineAreal2chan1, &i2_amprealchan1, f);
    EvalCubicSplineSlide(&ampimag2chan1, splineAimag2chan1, &i2_ampimagchan1, f);
    EvalCubicSplineSlide(&ampreal2chan2, splineAreal2chan2, &i2_amprealchan2, f);
    EvalCubicSplineSlide(&ampimag2chan2, splineAimag2chan2, &i2_ampimagchan2, f);
    EvalCubicSplineSlide(&ampreal2chan3, splineAreal2chan3, &i2_amprealchan3, f);
    EvalCubicSplineSlide(&ampimag2chan3, splineAimag2chan3, &i2_ampimagchan3, f);
    /* Assumes the same phase across three channels */
    EvalCubicSplineSlide(&phase2, splinephase2chan1, &i2_phase, f);
    camp = (ampreal1chan1 + I*ampimag1chan1) * (ampreal2chan1 - I*ampimag2chan1)
         + (ampreal1chan2 + I*ampimag1chan2) * (ampreal2chan2 - I*ampimag2chan2)
        + (ampreal1chan3 + I*ampimag1chan3) * (ampreal2chan3 - I*ampimag2chan3);
    real_vector_set(freq, j, f);
    real_vector_set(ampreal, j, creal(camp));
    real_vector_set(ampimag, j, cimag(camp));
    real_vector_set(phase, j, phase1 - phase2);
    j++;
  }

  return SUCCESS;
}

/******************************************************************************/
/* Functions to compute amp/phase overlap */
/******************************************************************************/

/* Compute (h1|h2) = 4 \int (h1 h2* / Sn)  */
/* Integrand represents camp/phase data for (h1 h2* / Sn) */
/* Does a cubic spline interpolation for the complex amplitude */
/* and a quadratic spline interplolation for the phase */
/* NOTE: we return the complex overlap, no Re() */
double complex ComputeFresnelIntegral(CAmpPhaseFDData* integrand)
{
  /* Check pointers */
  if (integrand == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to integrand is NULL.");

  /* Interpolating the integrand */
  real_matrix* spline_amp_real = NULL;
  real_matrix* spline_amp_imag = NULL;
  real_matrix* quadspline_phase = NULL;
  BuildNotAKnotSpline(&spline_amp_real, integrand->freq, integrand->amp_real);
  BuildNotAKnotSpline(&spline_amp_imag, integrand->freq, integrand->amp_imag);
  BuildQuadSpline(&quadspline_phase, integrand->freq, integrand->phase);

  /* Computing the integral - including here the factor 4 and the real part */
  double complex overlap = 4. * ComputeInt(spline_amp_real,
                                           spline_amp_imag,
                                           quadspline_phase);

  /* Cleanup */
  real_matrix_free(spline_amp_real);
  real_matrix_free(spline_amp_imag);
  real_matrix_free(quadspline_phase);

  return overlap;
}

/* Function computing the overlap (h1|h2) between two amplitude/phase signals */
/* Signal 1 is in amplitude/phase form */
/* Signal 2 is already interpolated, and already has weighting by the noise */
/* NOTE: we return the complex overlap, no Re() */
double complex FDSinglemodeFresnelOverlap(
  CAmpPhaseFDData* freqseries1, /* First mode h1, in camp/phase form */
  CAmpPhaseFDSpline* splines2,  /* Second mode h2, splines, noise-weighted */
  double fLow,                  /* Lower bound frequency - 0 to ignore */
  double fHigh)                 /* Upper bound frequency - 0 to ignore */
{
  /* Check pointers */
  if (freqseries1 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1 is NULL.");
  if (splines2 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2 is NULL.");

  /* Computing the integrand values, on the frequency grid of h1 */
  CAmpPhaseFDData* integrand = NULL;
  ComputeIntegrandValues(&integrand, freqseries1, splines2, fLow, fHigh);

  /* Computing the integral - including here the factor 4 and the real part */
  double complex overlap = ComputeFresnelIntegral(integrand);

  /* Clean up */
  CAmpPhaseFDData_Destroy(integrand);

  return overlap;
}

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
  double fHigh)                      /* Upper bound frequency - 0 to ignore */
{
  /* Check pointers */
  if (freqseries1chan1 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1chan1 is NULL.");
  if (freqseries1chan2 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1chan2 is NULL.");
  if (freqseries1chan3 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to freqseries1chan3 is NULL.");
  if (splines2chan1 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2chan1 is NULL.");
  if (splines2chan3 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2chan2 is NULL.");
  if (splines2chan3 == NULL)
    ERROR(ERROR_EFAULT, "Input pointer to splines2chan3 is NULL.");


  /* Computing the integrand values, on the frequency grid of h1 */
  /* Here the integrand camp is summed over channels (assumes common phase) */
  CAmpPhaseFDData* integrand = NULL;
  int ret = ComputeIntegrandValues3Chan(&integrand,
                              freqseries1chan1,
                              freqseries1chan2,
                              freqseries1chan3,
                              splines2chan1,
                              splines2chan2,
                              splines2chan3,
                              fLow, fHigh);

  double complex overlap = 0.;
  /* ComputeIntegrandValues3Chan return FAILURE when frequency ranges are
     incompatible -- in this case, return 0 for the overlap */
  if (ret==FAILURE) overlap = 0.;
  else {
    /* Computing the integral - including here the factor 4 and the real part */
    overlap = ComputeFresnelIntegral(integrand);

    /* Clean up */
    CAmpPhaseFDData_Destroy(integrand);
  }

  return overlap;
}
