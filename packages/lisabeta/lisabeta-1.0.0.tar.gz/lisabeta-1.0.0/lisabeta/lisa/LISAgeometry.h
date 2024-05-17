/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#ifndef _LISAGEOMETRY_H
#define _LISAGEOMETRY_H

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

#if defined(__cplusplus)
#define complex _Complex
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif

/******************************************************************************/
/* Structure for geometric coefficients in the response */
/******************************************************************************/

/* Structure holding precomputed coefficients for the analytic orbit response */
typedef struct tagLISAGeometricCoefficients {
  double coeffn1Hn1crossconst, coeffn1Hn1plusconst, coeffn2Hn2crossconst,
          coeffn2Hn2plusconst, coeffn3Hn3crossconst, coeffn3Hn3plusconst;
  double coeffn1Hn1pluscos[4];
  double coeffn1Hn1plussin[4];
  double coeffn2Hn2pluscos[4];
  double coeffn2Hn2plussin[4];
  double coeffn3Hn3pluscos[4];
  double coeffn3Hn3plussin[4];
  double coeffn1Hn1crosscos[4];
  double coeffn1Hn1crosssin[4];
  double coeffn2Hn2crosscos[4];
  double coeffn2Hn2crosssin[4];
  double coeffn3Hn3crosscos[4];
  double coeffn3Hn3crosssin[4];
  double coeffkn1const, coeffkn2const, coeffkn3const, coeffkp1plusp2const,
          coeffkp2plusp3const, coeffkp3plusp1const, coeffkp1const,
          coeffkp2const, coeffkp3const, coeffkRconst;
  double coeffkn1cos[2];
  double coeffkn1sin[2];
  double coeffkn2cos[2];
  double coeffkn2sin[2];
  double coeffkn3cos[2];
  double coeffkn3sin[2];
  double coeffkp1plusp2cos[2];
  double coeffkp1plusp2sin[2];
  double coeffkp2plusp3cos[2];
  double coeffkp2plusp3sin[2];
  double coeffkp3plusp1cos[2];
  double coeffkp3plusp1sin[2];
  double coeffkp1cos[2];
  double coeffkp1sin[2];
  double coeffkp2cos[2];
  double coeffkp2sin[2];
  double coeffkp3cos[2];
  double coeffkp3sin[2];
  double coeffkRcos[1];
  double coeffkRsin[1];
} LISAGeometricCoefficients;

/******************************************************************************/
/* Structures */
/******************************************************************************/

typedef enum TDItag {
  TDIAET = 0,        /* First-generation TDI AET, LDC conventions */
  TDIXYZ = 1,        /* First-generation TDI XYZ, LDC conventions */
  TDI2AET = 2,       /* 2nd-generation TDI2 AET, LDC conventions */
  TDI2XYZ = 3        /* 2nd-generation TDI2 XYZ, LDC conventions */
} TDItag;

/* Enumerator to choose the level of approximation in the response */
typedef enum ResponseApproxtag {
  full         = 0,
  lowfL        = 1,
  lowf         = 2,
  ignoreRdelay = 3,
  lowfL_highfsens = 4
} ResponseApproxtag;

// typedef struct tagLISAconstellation {
//   double OrbitOmega;
//   double OrbitPhi0;
//   double OrbitR;
//   double ConstOmega;
//   double ConstPhi0;
//   double ConstL;
//   LISANoiseType noise;
// } LISAconstellation;
typedef struct tagLISAconstellation {
  double OrbitOmega;
  double OrbitPhi0;
  double Orbitt0;
  double OrbitR;
  double OrbitL;
} LISAconstellation;
// extern LISAconstellation LISAProposal;
// extern LISAconstellation LISA2017;
// extern LISAconstellation LISA2010;
// extern LISAconstellation slowOrbitLISA;
// extern LISAconstellation tinyOrbitLISA;
// extern LISAconstellation fastOrbitLISA;
// extern LISAconstellation bigOrbitLISA;

/* Function to convert string input TDI string to TDItag */
// TDItag ParseTDItag(char* string);

/* Function to convert string input ResponseApprox to tag */
// ResponseApproxtag ParseResponseApproxtag(char* string);

/******************************************************************************/
/* Utilities */
/******************************************************************************/

/* Conversion between Solar System Barycenter time tSSB */
/* and retarded time at the center of the LISA constellation tL */
double tSSBfromtL(
  const double tL,                       /* Lisa-frame time */
  const double lambdaSSB,                /* Ecliptic longitude, SSB-frame */
  const double betaSSB,                  /* Ecliptic latitude, SSB-frame */
  const LISAconstellation *LISAconst);   /* LISA orbital constants */
double tLfromtSSB(
  const double tSSB,                     /* SSB-frame time */
  const double lambdaSSB,                /* Ecliptic longitude, SSB-frame */
  const double betaSSB,                  /* Ecliptic latitude, SSB-frame */
  const LISAconstellation *LISAconst);   /* LISA orbital constants */

/* Convert L-frame params to SSB-frame params */
/* NOTE: no transformation of the phase -- approximant-dependence */
/* e.g. EOBNRv2HMROM setting phiRef at fRef, and freedom in definition */
int ConvertLframeParamsToSSBframe(
  double* tSSB,                         /* Time, SSB-frame */
  double* lambdaSSB,                    /* Ecliptic longitude, SSB-frame */
  double* betaSSB,                      /* Ecliptic latitude, SSB-frame */
  double* psiSSB,                       /* Polarization, SSB-frame */
  const double tL,                      /* Time, L-frame */
  const double lambdaL,                 /* Ecliptic longitude, L-frame */
  const double betaL,                   /* Ecliptic latitude, L-frame */
  const double psiL,                    /* Polarization, L-frame */
  const LISAconstellation *LISAconst);  /* LISA orbital constants */
/* Convert SSB-frame params to L-frame params */
/* NOTE: no transformation of the phase -- approximant-dependence */
/* e.g. EOBNRv2HMROM setting phiRef at fRef, and freedom in definition */
int ConvertSSBframeParamsToLframe(
  double* tL,                           /* Time, L-frame */
  double* lambdaL,                      /* Ecliptic longitude, L-frame */
  double* betaL,                        /* Ecliptic latitude, L-frame */
  double* psiL,                         /* Polarization, L-frame */
  const double tSSB,                    /* Time, SSB-frame */
  const double lambdaSSB,               /* Ecliptic longitude, SSB-frame */
  const double betaSSB,                 /* Ecliptic latitude, SSB-frame */
  const double psiSSB,                  /* Polarization, SSB-frame */
  const LISAconstellation *LISAconst);  /* LISA orbital constants */

/******************************************************************************/
/* Geometric coefficients */
/******************************************************************************/

/* Function to compute, given a value of a sky position,
 * all the time-independent trigonometric coeffs entering the response */
int SetGeometricCoeffs(
  LISAGeometricCoefficients* coeffs, /* Output: struct for coeffs */
  const double lambda,               /* Ecliptic longitude, SSB-frame */
  const double beta);                /* Ecliptic latitude, SSB-frame */


#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _LISAGEOMETRY_H */
