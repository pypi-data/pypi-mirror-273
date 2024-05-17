/**
 * \author Sylvain Marsat, University of Maryland - NASA GSFC
 *
 * \brief C header for the instrumental noise for LISA-type detectors.
 *
 * Formulas taken from Królak&al gr-qc/0401108 (c.f. section III).
 *
 */

#ifndef _LISANOISE_H
#define _LISANOISE_H

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
#include "LISAgeometry.h"


#if defined(__cplusplus)
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif

/************************************************************************/
/****** Global variables storing min and max f for the noise PSD  *******/

//TODO
/* Defines bounds in frequency beyond which we don't trust the instrument model anymore - all waveforms will be cut to this range */
/* Here extended range - allows for instance to taper the FD signal for f>1Hz */
#define __LISASimFD_Noise_fLow 1.e-6
#define __LISASimFD_Noise_fHigh 5.
/* Original, more conservative bounds */
//#define __LISASimFD_Noise_fLow 1.e-5
//#define __LISASimFD_Noise_fHigh 1.

typedef enum LISAInstrumentalNoise {
  LISASciRDv1noise  = 0,
  LISAProposalnoise = 1,
  LISA2010noise     = 2,
  LISA2017noise     = 3
} LISAInstrumentalNoise;

typedef struct tagLISANoiseModel {
  LISAInstrumentalNoise noise;        /* Noise level */
  int WDbackground;            /* Flag for including WD background */
  double WDduration;           /* Duration of observation for subtracting WD background (in years) */
  double lowf_add_pm_noise_f0;     /* Charac. freq. f0 of low-f degradation of pm noise (1 + (f0/f)^alpha) */
  double lowf_add_pm_noise_alpha;  /* Power alpha of low-f degradation of pm noise (1 + (f0/f)^alpha) */
} LISANoiseModel;

/******************************************************************************/
/* Prototypes: functions evaluating the noise PSD */
/******************************************************************************/

/* Function returning the relevant noise function, given a set of TDI observables and a channel */
//ObjectFunction NoiseFunction(const LISAconstellation *variant, const TDItag tditag, const int nchan);

/* Noise Sn for TDI observables - factors have been scaled out both in the response and the noise */
// double SnXYZ(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
// double SnA(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
// double SnE(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
// double SnT(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
double SnXYZ(const void* object, double f);
double SnA(const void* object, double f);
double SnE(const void* object, double f);
double SnT(const void* object, double f);

/* Noise functions without rescaling */
// double SnXYZNoRescaling(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
// double SnANoRescaling(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
// double SnENoRescaling(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
// double SnTNoRescaling(const LISANoiseModel *LISAnoise, const LISAconstellation *LISAconst, double f);
double SnXYZNoRescaling(const void* object, double f);
double SnANoRescaling(const void* object, double f);
double SnENoRescaling(const void* object, double f);
double SnTNoRescaling(const void* object, double f);

/* Noise functions without rescaling for TDI 2 */
double SnXYZ2NoRescaling(const void* object, double f);
double SnA2NoRescaling(const void* object, double f);
double SnE2NoRescaling(const void* object, double f);
double SnT2NoRescaling(const void* object, double f);

/* Combined data structure and versions of these function with void pointers (to allow generalization beyond LISA) */
typedef struct {
  const LISANoiseModel *LISAnoise;
  const LISAconstellation *LISAconst;
} LISA_noise_func_data;

/******************************************************************************/
/* Noise functions for 3 channels */
/******************************************************************************/

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

/******************************************************************************/
/* Galactic noise functions from LDC */
/******************************************************************************/

/* Function to compute the WD galactic confusion noise for a given duration */
/* Copied from ldc.lisa.noise, assumes 6 links, SNR=7, L=2.5e9, SciRDv1 */
double LDCGalaxyShape(
  double f,
  double WDduration);
/* Rescaled to represent additive contribution in SnA,SnE rescaled: */
/* represents 3*(2pifL)^2*GalNoise(...) */
double LDCGalaxyNoiseAERescaled(
  double f,
  double twopifL,
  double WDduration);
/* Rescaled to represent additive contribution in SnXYZ rescaled: */
/* represents 2*(2pifL)^2*GalNoise(...) */
double LDCGalaxyNoiseXYZRescaled(
  double f,
  double twopifL,
  double WDduration);


#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _LISANOISE_H */
