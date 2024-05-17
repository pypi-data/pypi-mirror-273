/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#include "LISAresponse.h"

/******************************************************************************/
/* Response function and TDI combinations */
/******************************************************************************/

/* Function evaluating the orbital delay phase */
/* NOTE: this is simply the leading-order formula */
double EvaluatephaseRdelay(
  const double f,                          /* Frequency (Hz) */
  const double t,                          /* Time (s) */
  LISAGeometricCoefficients* coeffs,       /* Struct for precomputed coeffs */
  const LISAconstellation *LISAconst,      /* LISA orbital constants */
  const ResponseApproxtag responseapprox)  /* Approximation level in response */
{
  double phaseRdelay = 0.;

  double phase = LISAconst->OrbitOmega*(t - LISAconst->Orbitt0)
                 + LISAconst->OrbitPhi0;
  double cosphase = cos(phase);
  double sinphase = sin(phase);
  double prefactorR = 2*PI * f * LISAconst->OrbitR/C_SI;
  double kR = coeffs->coeffkRconst;
  kR += cosphase * coeffs->coeffkRcos[0]
        + sinphase * coeffs->coeffkRsin[0];
  phaseRdelay = prefactorR * kR;

  /* Take into account level of approximation in for low-f response */
  /* Choices are full, lowfL, lowf, ignoreRdelay */
  if ((responseapprox==lowf) || (responseapprox==ignoreRdelay)) {
    phaseRdelay = 0.;
  }

  return phaseRdelay;
}

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
  const ResponseApproxtag responseapprox)  /* Approximation level in response */
{
  double phase = LISAconst->OrbitOmega*(t - LISAconst->Orbitt0)
                 + LISAconst->OrbitPhi0;

  /* Precompute array of sine/cosine */
  double cosarray[4] = {0., 0., 0., 0.};
  double sinarray[4] = {0., 0., 0., 0.};
  for(int j=0; j<4; j++) {
    cosarray[j] = cos((j+1) * phase);
    sinarray[j] = sin((j+1) * phase);
  }
  /* Scalar products with k */
  double n1Pn1plus = coeffs->coeffn1Hn1plusconst;
  double n1Pn1cross = coeffs->coeffn1Hn1crossconst;
  double n2Pn2plus = coeffs->coeffn2Hn2plusconst;
  double n2Pn2cross = coeffs->coeffn2Hn2crossconst;
  double n3Pn3plus = coeffs->coeffn3Hn3plusconst;
  double n3Pn3cross = coeffs->coeffn3Hn3crossconst;
  for(int j=0; j<4; j++) {
    n1Pn1plus += cosarray[j] * coeffs->coeffn1Hn1pluscos[j]
                 + sinarray[j] * coeffs->coeffn1Hn1plussin[j];
    n1Pn1cross += cosarray[j] * coeffs->coeffn1Hn1crosscos[j]
                 + sinarray[j] * coeffs->coeffn1Hn1crosssin[j];
    n2Pn2plus += cosarray[j] * coeffs->coeffn2Hn2pluscos[j]
                 + sinarray[j] * coeffs->coeffn2Hn2plussin[j];
    n2Pn2cross += cosarray[j] * coeffs->coeffn2Hn2crosscos[j]
                  + sinarray[j] * coeffs->coeffn2Hn2crosssin[j];
    n3Pn3plus += cosarray[j] * coeffs->coeffn3Hn3pluscos[j]
                 + sinarray[j] * coeffs->coeffn3Hn3plussin[j];
    n3Pn3cross += cosarray[j] * coeffs->coeffn3Hn3crosscos[j]
                  + sinarray[j] * coeffs->coeffn3Hn3crosssin[j];
  }
  /* Scalar products with k */
  double kn1 = coeffs->coeffkn1const;
  double kn2 = coeffs->coeffkn2const;
  double kn3 = coeffs->coeffkn3const;
  double kp1plusp2 = coeffs->coeffkp1plusp2const;
  double kp2plusp3 = coeffs->coeffkp2plusp3const;
  double kp3plusp1 = coeffs->coeffkp3plusp1const;
  double kR = coeffs->coeffkRconst;
  for(int j=0; j<2; j++) {
    kn1 += cosarray[j] * coeffs->coeffkn1cos[j]
           + sinarray[j] * coeffs->coeffkn1sin[j];
    kn2 += cosarray[j] * coeffs->coeffkn2cos[j]
          + sinarray[j] * coeffs->coeffkn2sin[j];
    kn3 += cosarray[j] * coeffs->coeffkn3cos[j]
           + sinarray[j] * coeffs->coeffkn3sin[j];
    kp1plusp2 += cosarray[j] * coeffs->coeffkp1plusp2cos[j]
                + sinarray[j] * coeffs->coeffkp1plusp2sin[j];
    kp2plusp3 += cosarray[j] * coeffs->coeffkp2plusp3cos[j]
                + sinarray[j] * coeffs->coeffkp2plusp3sin[j];
    kp3plusp1 += cosarray[j] * coeffs->coeffkp3plusp1cos[j]
                 + sinarray[j] * coeffs->coeffkp3plusp1sin[j];
  }
  for(int j=0; j<1; j++) {
    kR += cosarray[j] * coeffs->coeffkRcos[j]
          + sinarray[j] * coeffs->coeffkRsin[j];
  }
  /* Common factors */
  double complex factn1Pn1 = n1Pn1plus*Yfactorplus + n1Pn1cross*Yfactorcross;
  double complex factn2Pn2 = n2Pn2plus*Yfactorplus + n2Pn2cross*Yfactorcross;
  double complex factn3Pn3 = n3Pn3plus*Yfactorplus + n3Pn3cross*Yfactorcross;
  double prefactor = PI * f * LISAconst->OrbitL/C_SI;
  double prefactorR = 2*PI * f * LISAconst->OrbitR/C_SI;
  double complex factorcexp12 = cexp(I*prefactor * (1.+kp1plusp2));
  double complex factorcexp23 = cexp(I*prefactor * (1.+kp2plusp3));
  double complex factorcexp31 = cexp(I*prefactor * (1.+kp3plusp1));
  double factorsinc12 = sinc( prefactor * (1.-kn3));
  double factorsinc21 = sinc( prefactor * (1.+kn3));
  double factorsinc23 = sinc( prefactor * (1.-kn1));
  double factorsinc32 = sinc( prefactor * (1.+kn1));
  double factorsinc31 = sinc( prefactor * (1.-kn2));
  double factorsinc13 = sinc( prefactor * (1.+kn2));
  /* R-delay phase term (here leading order) */
  double complex factorcexpkR = cexp(I*prefactorR * kR);

  /* Take into account level of approximation in for low-f response */
  /* Choices are full, lowfL, lowf, ignoreRdelay */
  if ((responseapprox==lowf) || (responseapprox==ignoreRdelay)) {
    factorcexpkR = 1.;
  }
  if ((responseapprox==lowfL) || (responseapprox==lowf) || (responseapprox==lowfL_highfsens)) {
    factorsinc12 = 1.;
    factorsinc21 = 1.;
    factorsinc23 = 1.;
    factorsinc32 = 1.;
    factorsinc31 = 1.;
    factorsinc13 = 1.;
    factorcexp12 = 1.;
    factorcexp23 = 1.;
    factorcexp31 = 1.;
  }
  /* Introduce high-f degradation inspired from sky-averaged sensitivity */
  /* Attempts to reproduce what other groups use as a low-f SOBH response */
  /* See (9) in Cornish-Robson 1803.01944 -- factor deviating from constant */
  if (responseapprox==lowfL_highfsens) {
    prefactor = prefactor * 1./sqrt(1. + 0.6*pow(2*PI*f*LISAconst->OrbitL/C_SI, 2));
  }

  /* Output result */
  *G12 = I*prefactor * factorcexpkR * factn3Pn3 * factorsinc12 * factorcexp12;
  *G21 = I*prefactor * factorcexpkR * factn3Pn3 * factorsinc21 * factorcexp12;
  *G23 = I*prefactor * factorcexpkR * factn1Pn1 * factorsinc23 * factorcexp23;
  *G32 = I*prefactor * factorcexpkR * factn1Pn1 * factorsinc32 * factorcexp23;
  *G31 = I*prefactor * factorcexpkR * factn2Pn2 * factorsinc31 * factorcexp31;
  *G13 = I*prefactor * factorcexpkR * factn2Pn2 * factorsinc13 * factorcexp31;

  return SUCCESS;
}

/******************************************************************************/

/* Function evaluating the Fourier-domain combinations of Gslr's for TDI */
/* NOTE: factors have been scaled out, in parallel to the noise function */
/* NOTE: here we follow the LDC definition of A,E,T, differs from flare */
/* (A,E,T)_LDC = 2 * (A,E,T)_flare */
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
  const int rescaled)                     /* Apply rescaling to response */
{
  /* Notation: x=pifL, z=e^2ix*/
  double x = PI * f * LISAconst->OrbitL/C_SI;
  double complex z = cexp(2*I*x);

  /* In both lowf and lowf-L approximations, ignore z factors */
  /* and keep leading-order in x=pifL */
  double complex factor_rescaling_AE = 1.;
  double complex factor_rescaling_T = 1.;
  double complex factor_rescaling_XYZ = 1.;
  double complex factor_TDI2 = 1.;
  switch(tditag) {
  /* First-generation rescaled TDI aet from X,Y,Z */
  /* With x=pifL, factor scaled out A,E: I*sqrt2*sin2x*e2ix */
  /* factor scaled out T: 2*sqrt2*sin2x*sinx*e3ix */
  case TDIAET:
    if (!rescaled) {
      if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) {
        factor_rescaling_AE = I*SQRT2*2.*x;
        factor_rescaling_T = 2.*SQRT2*2.*x*x;
      }
      else {
        factor_rescaling_AE = I*SQRT2*sin(2.*x)*z;
        factor_rescaling_T = 2.*SQRT2*sin(2.*x)*sin(x)*cexp(I*3.*x);
      }
    }
    else {
      factor_rescaling_AE = 1.;
      factor_rescaling_T = 1.;
    }
    if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) z = 1.;
    *transfer1 = factor_rescaling_AE *
        ( (1.+z)*(G31+G13) - G23 - z*G32 - G21 - z*G12 );
    *transfer2 = factor_rescaling_AE *
        INVSQRT3 * ( (1.-z)*(G13-G31) + (2.+z)*(G12-G32) + (1.+2*z)*(G21-G23) );
    *transfer3 = factor_rescaling_T *
        2.*INVSQRT6 * ( G21-G12 + G32-G23 + G13-G31);
    break;
  /* First-generation TDI XYZ */
  /* With x=pifL, factor scaled out: 2I*sin2x*e2ix */
  case TDIXYZ:
    if (!rescaled) {
      if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) {
        factor_rescaling_XYZ = 2*I*2.*x;
      }
      else {
        factor_rescaling_XYZ = 2*I*sin(2.*x)*z;
      }
    }
    else {
      factor_rescaling_XYZ = 1.;
    }
    if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) z = 1.;
    *transfer1 = factor_rescaling_XYZ * (G21 + z*G12 - G31 - z*G13);
    *transfer2 = factor_rescaling_XYZ * (G32 + z*G23 - G12 - z*G21);
    *transfer3 = factor_rescaling_XYZ * (G13 + z*G31 - G23 - z*G32);
    break;
  /* Second-generation rescaled TDI aet from X,Y,Z */
  /* With x=pifL, factor scaled out A,E: I*sqrt2*sin2x*e2ix */
  /* factor scaled out T: 2*sqrt2*sin2x*sinx*e3ix */
  /* Factor going from TDI 1st-gen to TDI 2nd-gen: -2I*sin4x*e4ix */
  case TDI2AET:
    if (!rescaled) {
      if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) {
        factor_rescaling_AE = I*SQRT2*2.*x;
        factor_rescaling_T = 2.*SQRT2*2.*x*x;
        factor_TDI2 = -2*I * 4*x * 4*I*x;
      }
      else {
        factor_rescaling_AE = I*SQRT2*sin(2.*x)*z;
        factor_rescaling_T = 2.*SQRT2*sin(2.*x)*sin(x)*cexp(I*3.*x);
        factor_TDI2 = -2*I * sin(4.*x) * cexp(I*4.*x);
      }
    }
    else {
      factor_rescaling_AE = 1.;
      factor_rescaling_T = 1.;
      factor_TDI2 = 1.;
    }
    if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) z = 1.;
    *transfer1 = factor_TDI2 * factor_rescaling_AE *
        ( (1.+z)*(G31+G13) - G23 - z*G32 - G21 - z*G12 );
    *transfer2 = factor_TDI2 * factor_rescaling_AE *
        INVSQRT3 * ( (1.-z)*(G13-G31) + (2.+z)*(G12-G32) + (1.+2*z)*(G21-G23) );
    *transfer3 = factor_TDI2 * factor_rescaling_T *
        2.*INVSQRT6 * ( G21-G12 + G32-G23 + G13-G31);
    break;
  /* Second-generation TDI XYZ */
  /* With x=pifL, factor scaled out: 2I*sin2x*e2ix */
  /* Factor going from TDI 1st-gen to TDI 2nd-gen: -2I*sin4x*e4ix */
  case TDI2XYZ:
    if (!rescaled) {
      if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) {
        factor_rescaling_XYZ = 2*I*2.*x;
        factor_TDI2 = -2*I * 4*x * 4*I*x;
      }
      else {
        factor_rescaling_XYZ = 2*I*sin(2.*x)*z;
        factor_TDI2 = -2*I * sin(4.*x) * cexp(I*4.*x);
      }
    }
    else {
      factor_rescaling_XYZ = 1.;
      factor_TDI2 = 1.;
    }
    if ((responseapprox==lowf) || (responseapprox==lowfL) || (responseapprox==lowfL_highfsens)) z = 1.;
    *transfer1 = factor_TDI2 * factor_rescaling_XYZ * (G21 + z*G12 - G31 - z*G13);
    *transfer2 = factor_TDI2 * factor_rescaling_XYZ * (G32 + z*G23 - G12 - z*G21);
    *transfer3 = factor_TDI2 * factor_rescaling_XYZ * (G13 + z*G31 - G23 - z*G32);
    break;
  default:
    ERROR(ERROR_EINVAL, "TDItag not recognized.");
  }
  return SUCCESS;
}

/* Function for the Fourier-domain factors scaled out of TDI observables */
/* The factors scaled out, parallel what is done for the noise functions */
int ScaledTDIfactor3Chan(
  double complex* factor1,             /* Output: factor for TDI factor 1 */
  double complex* factor2,             /* Output: factor for TDI factor 2 */
  double complex* factor3,             /* Output: factor for TDI factor 3 */
  const double f,                      /* Frequency (Hz)*/
  const TDItag tditag,                 /* Selector for the TDI observables */
  const LISAconstellation *LISAconst)  /* LISA orbital constants */
{
  /* Notation: x=pifL */
  double x = PI*f*LISAconst->OrbitL/C_SI;
  switch(tditag) {
  /* First-generation rescaled TDI aet from X,Y,Z */
  case TDIAET:
    *factor1 = I*SQRT2*sin(2*x)*cexp(2*I*x);
    *factor2 = I*SQRT2*sin(2*x)*cexp(2*I*x);
    *factor3 = 2*SQRT2*sin(x)*sin(2*x)*cexp(3*I*x);
    break;
  /* First-generation TDI XYZ */
  case TDIXYZ:
    *factor1 = 2*I*sin(2*x)*cexp(2*I*x);
    *factor2 = 2*I*sin(2*x)*cexp(2*I*x);
    *factor3 = 2*I*sin(2*x)*cexp(2*I*x);
    break;
  /* Second-generation rescaled TDI aet from X,Y,Z */
  case TDI2AET:
    *factor1 = -2*I*sin(4*x)*cexp(4*I*x) * I*SQRT2*sin(2*x)*cexp(2*I*x);
    *factor2 = -2*I*sin(4*x)*cexp(4*I*x) * I*SQRT2*sin(2*x)*cexp(2*I*x);
    *factor3 = -2*I*sin(4*x)*cexp(4*I*x) * 2*SQRT2*sin(x)*sin(2*x)*cexp(3*I*x);
    break;
  /* Second-generation TDI XYZ */
  case TDI2XYZ:
    *factor1 = -2*I*sin(4*x)*cexp(4*I*x) * 2*I*sin(2*x)*cexp(2*I*x);
    *factor2 = -2*I*sin(4*x)*cexp(4*I*x) * 2*I*sin(2*x)*cexp(2*I*x);
    *factor3 = -2*I*sin(4*x)*cexp(4*I*x) * 2*I*sin(2*x)*cexp(2*I*x);
    break;
  default:
    ERROR(ERROR_EINVAL, "ScaledTDIfactor3Chan: tditag not recognized.");
  }
  return SUCCESS;
}

// /* Function restoring the factor that have been scaled out of the TDI observables */
// /* NOTE: the operation is made in-place, and the input is overwritten */
// int RestoreInPlaceScaledFactorTDI(
//   const LISAconstellation *variant,    /* Description of LISA variant */
//   ListmodesCAmpPhaseFrequencySeries* listtdi,     /* Output/Input: list of mode contributions to TDI observable */
//   TDItag tditag,                                  /* Tag selecting the TDI observable */
//   int nchannel)                                   /* TDI channel number */
// {
//   double complex factor1 = 0;
//   double complex factor2 = 0;
//   double complex factor3 = 0;
//   double complex factor;
//   double complex camp;
//   ListmodesCAmpPhaseFrequencySeries* listelement = listtdi;
//   /* Going throug the list of modes */
//   while(listelement) {
//     gsl_vector* freq = listelement->freqseries->freq;
//     gsl_vector* ampreal = listelement->freqseries->amp_real;
//     gsl_vector* ampimag = listelement->freqseries->amp_imag;
//     for(int i=0; i<freq->size; i++) {
//       ScaledTDIfactor3Chan(variant,&factor1, &factor2, &factor3, gsl_vector_get(freq, i), tditag);
//       switch(nchannel) {
//       case 1: factor = factor1; break;
//       case 2: factor = factor2; break;
//       case 3: factor = factor3; break;
//       }
//       camp = factor * (gsl_vector_get(ampreal, i) + I*gsl_vector_get(ampimag, i));
//       gsl_vector_set(ampreal, i, creal(camp));
//       gsl_vector_set(ampimag, i, cimag(camp));
//     }
//     listelement = listelement->next;
//   }
//   return SUCCESS;
// }

/******************************************************************************/
/* TDI response function */
/******************************************************************************/

/* TDI response function for a single mode hlm */
/* tf gives t-t0, t0 locates the waveform in SSB time  */
/* NOTE: phaseRdelay kept separately and factored out from TDI transfers */
int EvalLISAFDresponseTDI3Chan(
  real_vector** phaseRdelay,           /* Output: orbital delay phase */
  complex_vector** transfer1,          /* Output: transfer for TDI channel 1 */
  complex_vector** transfer2,          /* Output: transfer for TDI channel 2 */
  complex_vector** transfer3,          /* Output: transfer for TDI channel 3 */
  real_vector* freq,                   /* Frequencies to evaluate on (Hz) */
  real_vector* tf,                     /* Input t(f) (s) */
  const double t0,                     /* Reference orbital time (yr) */
  const int l,                         /* Mode number l */
  const int m,                         /* Mode number m */
  const double inc,                    /* Inclination in source-frame */
  const double phi,                    /* Azimuthal phase in source-frame */
  const double lambd,                  /* Ecliptic longitude, SSB-frame */
  const double beta,                   /* Ecliptic latitude, SSB-frame */
  const double psi,                    /* Polarization angle, SSB-frame */
  const TDItag tditag,                 /* Choice of TDI observable */
  const LISAconstellation* LISAconst,  /* LISA orbital constants */
  const ResponseApproxtag responseapprox, /* Approximation in FD response */
  const int tagfrozenLISA,             /* Tag to treat LISA as motionless */
  const int rescaled)                  /* Apply rescaling to response */
{

  /* Check input/output pointers */
  if (freq == NULL)
      ERROR(ERROR_EFAULT, "Input pointer to freq is NULL.");
  if (tf == NULL)
      ERROR(ERROR_EFAULT, "Input pointer to tf is NULL.");
  if (*phaseRdelay != NULL)
      ERROR(ERROR_EFAULT, "Output pointer to phaseRdelay is not NULL.");
  if (*transfer1 != NULL)
      ERROR(ERROR_EFAULT, "Output pointer to transfer1 is not NULL.");
  if (*transfer2 != NULL)
      ERROR(ERROR_EFAULT, "Output pointer to transfer2 is not NULL.");
  if (*transfer3 != NULL)
      ERROR(ERROR_EFAULT, "Output pointer to transfer3 is not NULL.");

  size_t n = freq->size;

  /* Orbital reference time is inupt in years, convert to seconds */
  double t0_s = t0 * YRSID_SI;

  /* Precomputing trigonometric coefficients entering the response */
  LISAGeometricCoefficients geomcoeffs;
  SetGeometricCoeffs(&geomcoeffs, lambd, beta);

  /* Computing the sYlm combined factors for plus and cross for this mode lm */
  double complex e2ipsi = cexp(2*I*psi);
  double complex em2ipsi = cexp(-2*I*psi);
  double complex sYlm;
  double complex sYlminusmstar;
  double complex Yfactorplus;
  double complex Yfactorcross;
  sYlm = SpinWeightedSphericalHarmonic(inc, phi, -2, l, m);
  sYlminusmstar = conj(SpinWeightedSphericalHarmonic(inc, phi, -2, l, -m));
  if (!(l%2)) {
    Yfactorplus = 1./2 * (sYlm*em2ipsi + sYlminusmstar*e2ipsi);
    Yfactorcross = I/2 * (sYlm*em2ipsi - sYlminusmstar*e2ipsi);
  }
  else {
    Yfactorplus = 1./2 * (sYlm*em2ipsi - sYlminusmstar*e2ipsi);
    Yfactorcross = I/2 * (sYlm*em2ipsi + sYlminusmstar*e2ipsi);
  }

  // /* Values of tf for the input frequencies */
  // real_vector* tfvals = NULL;
  // int extrapol_zero = 0;
  // EvalCubicSplineOnVector(&tfvals, freq, tfspline, extrapol_zero);

  /* Initialize output */
  *phaseRdelay = real_vector_alloc(n);
  *transfer1 = complex_vector_alloc(n);
  *transfer2 = complex_vector_alloc(n);
  *transfer3 = complex_vector_alloc(n);

  /* Main loop over freq */
  double f, t;
  double phaseRdelayval = 0.;
  double complex transfer1val = 0.;
  double complex transfer2val = 0.;
  double complex transfer3val = 0.;
  double complex G12 = 0.;
  double complex G21 = 0.;
  double complex G23 = 0.;
  double complex G32 = 0.;
  double complex G31 = 0.;
  double complex G13 = 0.;
  double complex facscaleoutphaseRdelay = 0.;
  for (size_t i =0; i<n; i++) {
    f = real_vector_get(freq, i);
    if (tagfrozenLISA) t = t0_s;
    else t = real_vector_get(tf, i) + t0_s;

    /* Orbital delay phase */
    phaseRdelayval = EvaluatephaseRdelay(f, t,
                                      &geomcoeffs, LISAconst, responseapprox);

    /* Transfer functions for individual one-arm observables */
    EvaluateGlmslr(&G12, &G21, &G23, &G32, &G31, &G13, f, t,
                   Yfactorplus, Yfactorcross, &geomcoeffs,
                   LISAconst, responseapprox);

    /* TDI combinations */
    EvaluateTDIfactor3Chan(&transfer1val, &transfer2val, &transfer3val,
                           G12, G21, G23, G32, G31, G13, f,
                           tditag, LISAconst, responseapprox, rescaled);

    /* Scale out leading order R-delay phase from transfer functions */
    facscaleoutphaseRdelay = cexp(-I*phaseRdelayval);
    transfer1val *= facscaleoutphaseRdelay;
    transfer2val *= facscaleoutphaseRdelay;
    transfer3val *= facscaleoutphaseRdelay;

    real_vector_set(*phaseRdelay, i, phaseRdelayval);
    complex_vector_set(*transfer1, i, transfer1val);
    complex_vector_set(*transfer2, i, transfer2val);
    complex_vector_set(*transfer3, i, transfer3val);
  }

  /* Cleanup */
  // real_vector_free(tfvals);

  return SUCCESS;
}
