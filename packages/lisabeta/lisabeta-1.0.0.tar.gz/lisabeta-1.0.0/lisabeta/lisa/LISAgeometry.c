/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#include "LISAgeometry.h"

/******************************************************************************/
/* Structures */
/******************************************************************************/

// LISAconstellation LISAProposal = {
//   EarthOrbitOmega_SI,
//   0.,
//   0.,
//   AU_SI,
//   2.5e9,
//   LISA2017noise
// };
//
// LISAconstellation LISA2017 = {
//   EarthOrbitOmega_SI,
//   0,
//   AU_SI,
//   EarthOrbitOmega_SI,
//   0,
//   2.5e9,
//   LISA2017noise
// };
//
// LISAconstellation LISA2010 = {
//   EarthOrbitOmega_SI,
//   0,
//   AU_SI,
//   EarthOrbitOmega_SI,
//   0,
//   5e9,
//   LISA2010noise
// };
//
// LISAconstellation slowOrbitLISA = {
//   EarthOrbitOmega_SI/100.0,
//   0,
//   AU_SI,
//   EarthOrbitOmega_SI/100.0,
//   0,
//   2.5e9,
//   LISA2017noise
// };
//
// LISAconstellation tinyOrbitLISA = {
//   EarthOrbitOmega_SI,
//   0,
//   AU_SI/100,
//   EarthOrbitOmega_SI,
//   0,
//   2.5e9,
//   LISA2017noise
// };
//
// LISAconstellation fastOrbitLISA = {
//   EarthOrbitOmega_SI*10.0,
//   0,
//   AU_SI,
//   EarthOrbitOmega_SI*10.0,
//   0,
//   2.5e9,
//   LISA2017noise
// };
//
// LISAconstellation bigOrbitLISA = {
//   EarthOrbitOmega_SI/10.0,
//   0,
//   AU_SI,
//   EarthOrbitOmega_SI/10.0,
//   0,
//   2.5e9,
//   LISA2017noise
// };


/*************************************************************/
/********* Functions for the geometric response **************/

// /* Function to convert string input TDI string to TDItag */
// TDItag ParseTDItag(char* string) {
//   TDItag tag;
//   if(strcmp(string, "delayO")==0) tag = delayO;
//   else if(strcmp(string, "y12L")==0) tag = y12L;
//   else if(strcmp(string, "y12")==0) tag = y12;
//   else if(strcmp(string, "TDIXYZ")==0) tag = TDIXYZ;
//   else if(strcmp(string, "TDIalphabetagamma")==0) tag = TDIalphabetagamma;
//   else if(strcmp(string, "TDIAETXYZ")==0) tag = TDIAETXYZ;
//   else if(strcmp(string, "TDIAETalphabetagamma")==0) tag = TDIAETalphabetagamma;
//   else if(strcmp(string, "TDIX")==0) tag = TDIX;
//   else if(strcmp(string, "TDIalpha")==0) tag = TDIalpha;
//   else if(strcmp(string, "TDIAXYZ")==0) tag = TDIAXYZ;
//   else if(strcmp(string, "TDIEXYZ")==0) tag = TDIEXYZ;
//   else if(strcmp(string, "TDITXYZ")==0) tag = TDITXYZ;
//   else if(strcmp(string, "TDIAalphabetagamma")==0) tag = TDIAalphabetagamma;
//   else if(strcmp(string, "TDIEalphabetagamma")==0) tag = TDIEalphabetagamma;
//   else if(strcmp(string, "TDITalphabetagamma")==0) tag = TDITalphabetagamma;
//   else {
//     printf("Error in ParseTDItag: string not recognized.\n");
//     exit(1);
//   }
//   return tag;
// }

// /* Function to convert string input ResponseApprox to tag */
// ResponseApproxtag ParseResponseApproxtag(char* string) {
//   ResponseApproxtag tag;
//   if(strcmp(string, "full")==0) tag = full;
//   else if(strcmp(string, "lowfL")==0) tag = lowfL;
//   else if(strcmp(string, "lowf")==0) tag = lowf;
//   else {
//     printf("Error in ParseResponseApproxtag: string not recognized.\n");
//     exit(1);
//   }
//   return tag;
// }

/******************************************************************************/
/* Utilities */
/******************************************************************************/

/* Conversion between Solar System Barycenter time tSSB */
/* and retarded time at the center of the LISA constellation tL */
double tSSBfromtL(
  const double tL,                       /* Lisa-frame time */
  const double lambdaSSB,                /* Ecliptic longitude, SSB-frame */
  const double betaSSB,                  /* Ecliptic latitude, SSB-frame */
  const LISAconstellation *LISAconst)    /* LISA orbital constants */
{
  double phase = LISAconst->OrbitOmega*(tL - LISAconst->Orbitt0)
                  + LISAconst->OrbitPhi0 - lambdaSSB;
  double RoC = LISAconst->OrbitR/C_SI;
 return tL + RoC*cos(betaSSB)*cos(phase)
        - 1./2*LISAconst->OrbitOmega*pow(RoC*cos(betaSSB), 2)*sin(2.*phase);
}
double tLfromtSSB(
  const double tSSB,                     /* SSB-frame time */
  const double lambdaSSB,                /* Ecliptic longitude, SSB-frame */
  const double betaSSB,                  /* Ecliptic latitude, SSB-frame */
  const LISAconstellation *LISAconst)    /* LISA orbital constants */
{
  double phase = LISAconst->OrbitOmega*(tSSB - LISAconst->Orbitt0)
                  + LISAconst->OrbitPhi0 - lambdaSSB;
  double RoC = LISAconst->OrbitR/C_SI;
  return tSSB - RoC*cos(betaSSB)*cos(phase);
}

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
  const LISAconstellation *LISAconst)   /* LISA orbital constants */
{
  double alpha = 0., cosalpha = 0., sinalpha = 0.;
  double coslambdaL = 0., sinlambdaL = 0., cosbetaL = 0., sinbetaL = 0.;
  double cospsiL = 0., sinpsiL = 0.;
  double coszeta = cos(PI/3.);
  double sinzeta = sin(PI/3.);
  coslambdaL = cos(lambdaL);
  sinlambdaL = sin(lambdaL);
  cosbetaL = cos(betaL);
  sinbetaL = sin(betaL);
  cospsiL = cos(psiL);
  sinpsiL = sin(psiL);
  double lambdaSSB_approx = 0.;
  double betaSSB_approx = 0.;
  /* Initially, approximate alpha using tL instead of tSSB - then iterate */
  double tSSB_approx = tL;
  for(int k=0; k<3; k++) {
    alpha = LISAconst->OrbitOmega * (tSSB_approx) + LISAconst->OrbitPhi0;
    cosalpha = cos(alpha);
    sinalpha = sin(alpha);
    lambdaSSB_approx = atan2(cosalpha*cosalpha*cosbetaL*sinlambdaL -sinalpha*sinbetaL*sinzeta + cosbetaL*coszeta*sinalpha*sinalpha*sinlambdaL -cosalpha*cosbetaL*coslambdaL*sinalpha + cosalpha*cosbetaL*coszeta*coslambdaL*sinalpha, cosbetaL*coslambdaL*sinalpha*sinalpha -cosalpha*sinbetaL*sinzeta + cosalpha*cosalpha*cosbetaL*coszeta*coslambdaL -cosalpha*cosbetaL*sinalpha*sinlambdaL + cosalpha*cosbetaL*coszeta*sinalpha*sinlambdaL);
    betaSSB_approx = asin(coszeta*sinbetaL + cosalpha*cosbetaL*coslambdaL*sinzeta + cosbetaL*sinalpha*sinzeta*sinlambdaL);
    tSSB_approx = tSSBfromtL(tL, lambdaSSB_approx, betaSSB_approx, LISAconst);
  }
  *tSSB = tSSB_approx;
  *lambdaSSB = lambdaSSB_approx;
  *betaSSB = betaSSB_approx;
  /* Polarization */
  *psiSSB = modpi(psiL + atan2(cosalpha*sinzeta*sinlambdaL -coslambdaL*sinalpha*sinzeta, cosbetaL*coszeta -cosalpha*coslambdaL*sinbetaL*sinzeta -sinalpha*sinbetaL*sinzeta*sinlambdaL));

  return SUCCESS;
}

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
  const LISAconstellation *LISAconst)   /* LISA orbital constants */
{
  double alpha = 0., cosalpha = 0., sinalpha = 0.;
  double coslambda = 0., sinlambda = 0.;
  double cosbeta = 0., sinbeta = 0., cospsi = 0., sinpsi = 0.;
  double coszeta = cos(PI/3.);
  double sinzeta = sin(PI/3.);
  coslambda = cos(lambdaSSB);
  sinlambda = sin(lambdaSSB);
  cosbeta = cos(betaSSB);
  sinbeta = sin(betaSSB);
  cospsi = cos(psiSSB);
  sinpsi = sin(psiSSB);
  alpha = LISAconst->OrbitOmega * (tSSB) + LISAconst->OrbitPhi0;
  cosalpha = cos(alpha);
  sinalpha = sin(alpha);
  *tL = tLfromtSSB(tSSB, lambdaSSB, betaSSB, LISAconst);
  *lambdaL = atan2(cosalpha*cosalpha*cosbeta*sinlambda + sinalpha*sinbeta*sinzeta + cosbeta*coszeta*sinalpha*sinalpha*sinlambda -cosalpha*cosbeta*coslambda*sinalpha + cosalpha*cosbeta*coszeta*coslambda*sinalpha, cosalpha*sinbeta*sinzeta + cosbeta*coslambda*sinalpha*sinalpha + cosalpha*cosalpha*cosbeta*coszeta*coslambda -cosalpha*cosbeta*sinalpha*sinlambda + cosalpha*cosbeta*coszeta*sinalpha*sinlambda);
  *betaL = asin(coszeta*sinbeta -cosalpha*cosbeta*coslambda*sinzeta -cosbeta*sinalpha*sinzeta*sinlambda);
  *psiL = modpi(psiSSB + atan2(coslambda*sinalpha*sinzeta -cosalpha*sinzeta*sinlambda, cosbeta*coszeta + cosalpha*coslambda*sinbeta*sinzeta + sinalpha*sinbeta*sinzeta*sinlambda));

  return SUCCESS;
}

/******************************************************************************/
/* Geometric coefficients */
/******************************************************************************/

/* Function to compute, given a value of a sky position,
 * all the time-independent trigonometric coeffs entering the response */
int SetGeometricCoeffs(
  LISAGeometricCoefficients* coeffs, /* Output: struct for coeffs */
  const double lambda,               /* Ecliptic longitude, SSB-frame */
  const double beta)                 /* Ecliptic latitude, SSB-frame */
{
  /* Checking output pointer */
  if(!coeffs) ERROR(ERROR_EFAULT, "Output pointer is NULL.");

  /* Precomputing cosines and sines */
  double coslambda = cos(lambda);
  double sinlambda = sin(lambda);
  double cosbeta = cos(beta);
  double sinbeta = sin(beta);
  double coslambda2 = coslambda*coslambda;
  //double sinlambda2 = sinlambda*sinlambda;
  double cosbeta2 = cosbeta*cosbeta;
  //double sinbeta2 = sinbeta*sinbeta;
  double cos2lambda = 2*coslambda2 - 1.;
  double sin2lambda = 2*coslambda*sinlambda;
  double cos2beta = 2*cosbeta2 - 1.;
  double sin2beta = 2*cosbeta*sinbeta;

  /* Projection coefficients for hplus in n3.H.n3 */
  /**/
  coeffs->coeffn3Hn3plusconst = (-8*cosbeta2 + 9*(-3 + cos2beta)*(cos2lambda - sin2lambda*SQRT3))/128.;
  /**/
  coeffs->coeffn3Hn3pluscos[0] = (sin2beta*(-9*sinlambda + 7*coslambda*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3pluscos[1] = (3*(-((-3 + cos2beta)*cos2lambda) - 3*cosbeta2))/32.;
  /**/
  coeffs->coeffn3Hn3pluscos[2] = -(sin2beta*(3*sinlambda + coslambda*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3pluscos[3] = ((-3 + cos2beta)*(cos2lambda + sin2lambda*SQRT3))/128.;
  /**/
  coeffs->coeffn3Hn3plussin[0] = (sin2beta*(-9*coslambda + sinlambda*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3plussin[1] = (3*(-((-3 + cos2beta)*sin2lambda) + 3*cosbeta2*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3plussin[2] = -(sin2beta*(-3*coslambda + sinlambda*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3plussin[3] = -((-3 + cos2beta)*(-sin2lambda + cos2lambda*SQRT3))/128.;

  /* Projection coefficients for hcross in n3.H.n3 */
  /**/
  coeffs->coeffn3Hn3crossconst = (-9*sinbeta*(sin2lambda + cos2lambda*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3crosscos[0] = (cosbeta*(9*coslambda + 7*sinlambda*SQRT3))/16.;
  /**/
  coeffs->coeffn3Hn3crosscos[1] = (3*coslambda*sinbeta*sinlambda)/4.;
  /**/
  coeffs->coeffn3Hn3crosscos[2] = -(cosbeta*(-3*coslambda + sinlambda*SQRT3))/16.;
  /**/
  coeffs->coeffn3Hn3crosscos[3] = (sinbeta*(-sin2lambda + cos2lambda*SQRT3))/32.;
  /**/
  coeffs->coeffn3Hn3crosssin[0] = -(cosbeta*(9*sinlambda + coslambda*SQRT3))/16.;
  /**/
  coeffs->coeffn3Hn3crosssin[1] = (-3*cos2lambda*sinbeta)/8.;
  /**/
  coeffs->coeffn3Hn3crosssin[2] = (cosbeta*(3*sinlambda + coslambda*SQRT3))/16.;
  /**/
  coeffs->coeffn3Hn3crosssin[3] = (sinbeta*(cos2lambda + sin2lambda*SQRT3))/32.;

  /* Projection coefficients for hplus in n2.H.n2 */
  /**/
  coeffs->coeffn2Hn2plusconst = (-8*cosbeta2 + 9*(-3 + cos2beta)*(cos2lambda + sin2lambda*SQRT3))/128.;
  /**/
  coeffs->coeffn2Hn2pluscos[0] = (sin2beta*(9*sinlambda + 7*coslambda*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2pluscos[1] = (3*(-((-3 + cos2beta)*cos2lambda) - 3*cosbeta2))/32.;
  /**/
  coeffs->coeffn2Hn2pluscos[2] = -(sin2beta*(-3*sinlambda + coslambda*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2pluscos[3] = ((-3 + cos2beta)*(cos2lambda - sin2lambda*SQRT3))/128.;
  /**/
  coeffs->coeffn2Hn2plussin[0] = (sin2beta*(9*coslambda + sinlambda*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2plussin[1] = (3*(-((-3 + cos2beta)*sin2lambda) - 3*cosbeta2*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2plussin[2] = -(sin2beta*(3*coslambda + sinlambda*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2plussin[3] = ((-3 + cos2beta)*(sin2lambda + cos2lambda*SQRT3))/128.;

  /* Projection coefficients for hcross in n2.H.n2 */
  /**/
  coeffs->coeffn2Hn2crossconst = (9*sinbeta*(-sin2lambda + cos2lambda*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2crosscos[0] = (cosbeta*(-9*coslambda + 7*sinlambda*SQRT3))/16.;
  /**/
  coeffs->coeffn2Hn2crosscos[1] = (3*coslambda*sinbeta*sinlambda)/4.;
  /**/
  coeffs->coeffn2Hn2crosscos[2] = -(cosbeta*(3*coslambda + sinlambda*SQRT3))/16.;
  /**/
  coeffs->coeffn2Hn2crosscos[3] = -(sinbeta*(sin2lambda + cos2lambda*SQRT3))/32.;
  /**/
  coeffs->coeffn2Hn2crosssin[0] = -(cosbeta*(-9*sinlambda + coslambda*SQRT3))/16.;
  /**/
  coeffs->coeffn2Hn2crosssin[1] = (-3*cos2lambda*sinbeta)/8.;
  /**/
  coeffs->coeffn2Hn2crosssin[2] = (cosbeta*(-3*sinlambda + coslambda*SQRT3))/16.;
  /**/
  coeffs->coeffn2Hn2crosssin[3] = (sinbeta*(cos2lambda - sin2lambda*SQRT3))/32.;

  /* Projection coefficients for hplus in n1.H.n1 */
  /**/
  coeffs->coeffn1Hn1plusconst = (-9*(-3 + cos2beta)*cos2lambda - 4*cosbeta2)/64.;
  /**/
  coeffs->coeffn1Hn1pluscos[0] = -(cosbeta*coslambda*sinbeta*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1pluscos[1] = (-6*(-3 + cos2beta)*cos2lambda + 36*cosbeta2)/64.;
  /**/
  coeffs->coeffn1Hn1pluscos[2] = (cosbeta*coslambda*sinbeta*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1pluscos[3] = -((-3 + cos2beta)*cos2lambda)/64.;
  /**/
  coeffs->coeffn1Hn1plussin[0] = (5*cosbeta*sinbeta*sinlambda*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1plussin[1] = (-3*(-3 + cos2beta)*sin2lambda)/32.;
  /**/
  coeffs->coeffn1Hn1plussin[2] = (cosbeta*sinbeta*sinlambda*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1plussin[3] = -((-3 + cos2beta)*sin2lambda)/64.;

  /* Projection coefficients for hcross in n1.H.n1 */
  /**/
  coeffs->coeffn1Hn1crossconst = (9*coslambda*sinbeta*sinlambda)/8.;
  /**/
  coeffs->coeffn1Hn1crosscos[0] = -(cosbeta*sinlambda*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1crosscos[1] = (3*coslambda*sinbeta*sinlambda)/4.;
  /**/
  coeffs->coeffn1Hn1crosscos[2] = (cosbeta*sinlambda*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1crosscos[3] = (coslambda*sinbeta*sinlambda)/8.;
  /**/
  coeffs->coeffn1Hn1crosssin[0] = (-5*cosbeta*coslambda*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1crosssin[1] = (-3*cos2lambda*sinbeta)/8.;
  /**/
  coeffs->coeffn1Hn1crosssin[2] = -(cosbeta*coslambda*SQRT3)/8.;
  /**/
  coeffs->coeffn1Hn1crosssin[3] = -(cos2lambda*sinbeta)/16.;

  /* Coefficients in k.n3 */
  /**/
  coeffs->coeffkn3const = (3*cosbeta*(sinlambda - coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkn3cos[0] = (-3*sinbeta)/4.;
  /**/
  coeffs->coeffkn3cos[1] = (cosbeta*(sinlambda + coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkn3sin[0] = (sinbeta*SQRT3)/4.;
  /**/
  coeffs->coeffkn3sin[1] = (cosbeta*(-coslambda + sinlambda*SQRT3))/8.;

  /* Coefficients in k.n2 */
  /**/
  coeffs->coeffkn2const = (3*cosbeta*(sinlambda + coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkn2cos[0] = (3*sinbeta)/4.;
  /**/
  coeffs->coeffkn2cos[1] = (cosbeta*(sinlambda - coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkn2sin[0] = (sinbeta*SQRT3)/4.;
  /**/
  coeffs->coeffkn2sin[1] = -(cosbeta*(coslambda + sinlambda*SQRT3))/8.;

  /* Coefficients in k.n1 */
  /**/
  coeffs->coeffkn1const = (-3*cosbeta*sinlambda)/4.;
  /**/
  coeffs->coeffkn1cos[0] = 0;
  /**/
  coeffs->coeffkn1cos[1] = -(cosbeta*sinlambda)/4.;
  /**/
  coeffs->coeffkn1sin[0] = -(sinbeta*SQRT3)/2.;
  /**/
  coeffs->coeffkn1sin[1] = (cosbeta*coslambda)/4.;

  /* Coefficients in k.(p1+p2) */
  /**/
  coeffs->coeffkp1plusp2const = (cosbeta*(3*sinlambda + coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkp1plusp2cos[0] = sinbeta/4.;
  /**/
  coeffs->coeffkp1plusp2cos[1] = -(cosbeta*(-3*sinlambda + coslambda*SQRT3))/24.;
  /**/
  coeffs->coeffkp1plusp2sin[0] = (sinbeta*SQRT3)/4.;
  /**/
  coeffs->coeffkp1plusp2sin[1] = -(cosbeta*(3*coslambda + sinlambda*SQRT3))/24.;

  /* Coefficients in k.(p2+p3) */
  /**/
  coeffs->coeffkp2plusp3const = -(cosbeta*coslambda*SQRT3)/4.;
  /**/
  coeffs->coeffkp2plusp3cos[0] = -sinbeta/2.;
  /**/
  coeffs->coeffkp2plusp3cos[1] = (cosbeta*coslambda)/(4.*SQRT3);
  /**/
  coeffs->coeffkp2plusp3sin[0] = 0;
  /**/
  coeffs->coeffkp2plusp3sin[1] = (cosbeta*sinlambda)/(4.*SQRT3);

  /* Coefficients in k.(p3+p1) */
  /**/
  coeffs->coeffkp3plusp1const = (cosbeta*(-3*sinlambda + coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkp3plusp1cos[0] = sinbeta/4.;
  /**/
  coeffs->coeffkp3plusp1cos[1] = -(cosbeta*(3*sinlambda + coslambda*SQRT3))/24.;
  /**/
  coeffs->coeffkp3plusp1sin[0] = -(sinbeta*SQRT3)/4.;
  /**/
  coeffs->coeffkp3plusp1sin[1] = -(cosbeta*(-3*coslambda + sinlambda*SQRT3))/24.;

  /* Coefficients in k.p1 */
  /**/
  coeffs->coeffkp1const = (cosbeta*coslambda*SQRT3)/4.;
  /**/
  coeffs->coeffkp1cos[0] = sinbeta/2.;
  /**/
  coeffs->coeffkp1cos[1] = -(cosbeta*coslambda)/(4.*SQRT3);
  /**/
  coeffs->coeffkp1sin[0] = 0;
  /**/
  coeffs->coeffkp1sin[1] = -(cosbeta*sinlambda)/(4.*SQRT3);

  /* Coefficients in k.p2 */
  /**/
  coeffs->coeffkp2const = -(cosbeta*(-3*sinlambda + coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkp2cos[0] = -sinbeta/4.;
  /**/
  coeffs->coeffkp2cos[1] = (cosbeta*(3*sinlambda + coslambda*SQRT3))/24.;
  /**/
  coeffs->coeffkp2sin[0] = (sinbeta*SQRT3)/4.;
  /**/
  coeffs->coeffkp2sin[1] = (cosbeta*(-3*coslambda + sinlambda*SQRT3))/24.;

  /* Coefficients in k.p3 */
  /**/
  coeffs->coeffkp3const = -(cosbeta*(3*sinlambda + coslambda*SQRT3))/8.;
  /**/
  coeffs->coeffkp3cos[0] = -sinbeta/4.;
  /**/
  coeffs->coeffkp3cos[1] = (cosbeta*(-3*sinlambda + coslambda*SQRT3))/24.;
  /**/
  coeffs->coeffkp3sin[0] = -(sinbeta*SQRT3)/4.;
  /**/
  coeffs->coeffkp3sin[1] = (cosbeta*(3*coslambda + sinlambda*SQRT3))/24.;

  /* Coefficients in k.R */
  /**/
  coeffs->coeffkRconst = 0.;
  coeffs->coeffkRcos[0] = -(cosbeta*coslambda);
  coeffs->coeffkRsin[0] = -(cosbeta*sinlambda);

  return SUCCESS;
}
