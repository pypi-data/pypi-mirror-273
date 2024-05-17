/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#ifndef _CONSTANTS_H
#define _CONSTANTS_H

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

//#include <gsl/gsl_errno.h>
//#include <gsl/gsl_bspline.h>
//#include <gsl/gsl_blas.h>
//#include <gsl/gsl_min.h>
//#include <gsl/gsl_spline.h>

#if defined(__cplusplus)
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif


/******************************************************************************/
/* Return codes */
/******************************************************************************/

#define SUCCESS 0
#define FAILURE -1

/******************************************************************************/
/* Mathematical constants */
/******************************************************************************/

/* Mathematica 11.3.0.0 */
#define PI           3.141592653589793238462643383279502884
#define PI_2         1.570796326794896619231321691639751442
#define PI_3         1.047197551196597746154214461093167628
#define PI_4         0.785398163397448309615660845819875721
#define SQRTPI       1.772453850905516027298167483341145183
#define SQRTTWOPI    2.506628274631000502415765284811045253
#define INVSQRTPI    0.564189583547756286948079451560772585
#define INVSQRTTWOPI 0.398942280401432677939946059934381868
#define GAMMA        0.577215664901532860606512090082402431
#define SQRT2        1.414213562373095048801688724209698079
#define SQRT3        1.732050807568877293527446341505872367
#define SQRT6        2.449489742783178098197284074705891392
#define INVSQRT2     0.707106781186547524400844362104849039
#define INVSQRT3     0.577350269189625764509148780501957455
#define INVSQRT6     0.408248290463863016366214012450981898


/******************************************************************************/
/* Physical constants in SI units */
/******************************************************************************/

#ifdef LDCCONSTANTS
  /* From LDC LISAConstants.py */
  /* NOTE: in python some constants are indirect: e.g. MsunKG = GMsun/G */
  #define C_SI 299792458.0
  #define G_SI 6.67408e-11
  //#define MSUN_SI 1.9884754467881714e+30
  #define MTSUN_SI 4.925491025543576e-06
  #define MRSUN_SI 1476.6250614046494 /* Absent in python, GMsun/c**2 */
  #define PC_SI 3.08567758149136727e+16
  #define AU_SI 149597870700.
  #define YRSID_SI 31558149.763545600
#elif LISACONSTANTS
  #include "pdbParam.h" // LISA constants
  #define MSUN_SI (double)Nature_SUN_MASS
  #define YRSID_SI = (double)Nature_SIDEREALYEAR_J2000DAY*24*60*60
  #define AU_SI = (double)Nature_ASTRONOMICALUNIT_METER
  #define C_SI = (double)Nature_VELOCITYOFLIGHT_CONSTEXPRANT_VACUUM
  #define G_SI = (double)Nature_NEWTON_CONSTANT
  #define GMSUN = (double)Nature_SUN_GM
  #define MTSUN_SI = GMSUN/(C_SI*C_SI*C_SI)
  #define MRSUN_SI = GMSUN/(C_SI*C_SI)
  #define PC_SI = (double)Nature_PARSEC_METER
#else
  /* From LALConstants.h */
  #define C_SI 299792458.
  #define G_SI 6.67384e-11
  #define MSUN_SI 1.988546954961461467461011951140572744e30
  #define MTSUN_SI 4.925491025543575903411922162094833998e-6
  #define MRSUN_SI 1.476625061404649406193430731479084713e3
  #define PC_SI 3.085677581491367278913937957796471611e16
  #define AU_SI 1.49597870700e11
  #define YRSID_SI 3.1558149763545600e7
#endif

/* NOTE: YRSID_SI is the same in pyFDresponse as here */
/* from EarthOrbitOmega_SI = 2pi/YRSID_SI with the same YRSID_SI */
//#define Omega_SI 1.99098659277e-6 /* Orbital pulsation: 20pi/year for "fast-orbit-LISA2017 "*/
//#define Omega_SI 6e-7 /* Orbital pulsation: ~6pi/year for "fast-orbit-LISA2017 "*/
//#define Omega_SI 1.99098659277e-7 /* Orbital pulsation: 2pi/year - use sidereal year as found on http://hpiers.obspm.fr/eop-pc/models/constants.html */
#define EarthOrbitOmega_SI 1.9909865927683785e-07 /* Orbital pulsation: 2pi/year - use sidereal year as found on http://hpiers.obspm.fr/eop-pc/models/constants.html */
//#define Omega_SI 1.99098659277e-9 /* Orbital pulsation: 2pi/century - alternative model to test the impact of a non-moving LISA*/
//#define Omega_SI 1.99098659277e-11 /* Orbital pulsation: 2pi/century - alternative model to test the impact of a non-moving LISA*/
//#define f0_SI 3.168753575e-8 /* Orbital frequency: 1/year */   //not used?
//#define L_SI 5.0e9 /* Arm length of the detector (in m): (Standard LISA) */
//#define L_SI 2.5e9 /* Arm length of the detector (in m): (L3 reference LISA) */
//#define R_SI 1.4959787066e11 /* Radius of the orbit around the sun: 1AU */
//#define AU_SI 1.4959787066e11 /* Radius of the orbit around the sun: 1AU */
//#define R_SI 1.4959787066e8 /* Radius of the orbit around the sun: 0.001 AU for hacked LISA test*/


/******************************************************************************/
/* Constants used to relate time scales */
/******************************************************************************/

#define EPOCH_J2000_0_TAI_UTC 32           /* Leap seconds (TAI-UTC) on the J2000.0 epoch (2000 JAN 1 12h UTC) */
#define EPOCH_J2000_0_GPS 630763213        /* GPS seconds of the J2000.0 epoch (2000 JAN 1 12h UTC) */

// TODO: arbitrary J2000 + 34*365.25*86400
#define EPOCH_LISA_0_GPS 1703721613        /* GPS seconds of the LISA epoch (approx. 34 yrs after J2000) */

/******************************************************************************/
/* NaN */
/******************************************************************************/

#ifndef NAN
# define NAN (INFINITY-INFINITY)
#endif

#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _CONSTANTS_H */
