/**
 * \author Sylvain Marsat, University of Maryland - NASA GSFC
 *
 * \brief C code for the instrumental noise for LISA-type detectors.
 *
 * Formulas taken from Królak&al gr-qc/0401108 (c.f. section III).
 */


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
#include "LISAnoise.h"
#include "LISAgeometry.h"

#include <stdio.h>


/* static double tflight_SI = L_SI/C_SI; */
/* static double twopitflight_SI = 2.*PI*L_SI/C_SI; */
static double fzero=1e-15; //Cut away from f=0 to avoid NaNs in that case.

/* Proof mass and optic noises - f in Hz */
/* WARNING: Taken from (4) in McWilliams&al_0911, but there was a typo there */
/* WARNING: the term (1. + 1e-8*invf2) in Spm should not come with a sqrt */
static double SpmLISA2010(const double f) {
  double invf2 = 1./(f*f);
  //return 2.5e-48 * invf2 * sqrt(1. + 1e-8*invf2);
  //const double Daccel=3.0e-15; //acceleration noise in m/s^2/sqrt(Hz)
  const double Daccel=3.0e-15; //scaled off L3LISA-v1 to for equal-SNR PE experiment
  const double SaccelFF=Daccel*Daccel/4.0/PI/PI/C_SI/C_SI; //f^-2 coeff for fractional-freq noise PSD from accel noise; yields 2.54e-48 from 3e-15;
  double invf8=invf2*invf2*invf2*invf2;
  //Here we add an eyeball approximation based on 4yrs integration with L3LISAReferenceMission looking at a private comm from Neil Cornish 2016.11.12
  double WDWDnoise=5000.0/sqrt(1e-21*invf8 + invf2 + 3e28/invf8)*SaccelFF*invf2;
  return SaccelFF * invf2 * (1. + 1e-8*invf2) + WDWDnoise;
}
static double SopLISA2010(const double f) {
  const double Dop=2.0e-11; //Optical path noise in m/rtHz (Standard LISA)
  const double SopFF=Dop*Dop*4.0*PI*PI/C_SI/C_SI; //f^2 coeff for OP frac-freq noise PSD.  Yields 1.76e-37 for Dop=2e-11.
  return SopFF * f * f;
}

/* Proof mass and optical noises - f in Hz */
/* L3 Reference Mission, from Petiteau LISA-CST-TN-0001 */
static double SpmLISA2017(const double f) {
  double invf2 = 1./(f*f);
  //double invf4=invf2*invf2;
  //double invf8=invf4*invf4;
  //double invf10=invf8*invf2;
  const double twopi2=4.0*PI*PI;
  double ddtsq=twopi2/invf2; //time derivative factor
  const double C2=1.0*C_SI*C_SI; //veloc to doppler
  const double Daccel_white=3.0e-15; //acceleration noise in m/s^2/sqrt(Hz)
  const double Daccel_white2=Daccel_white*Daccel_white;
  const double Dloc=1.7e-12; //local IFO noise in m/sqrt(Hz)
  const double Dloc2=Dloc*Dloc;
  double Saccel_white=Daccel_white2/ddtsq; //PM vel noise PSD (white accel part)
  //double Saccel_red=Saccel_white*(1.0 + 2.12576e-44*invf10 + 3.6e-7*invf2); //reddening factor from Petiteau Eq 1
  double Saccel_red=Saccel_white*(1.0 + 36.0*(pow(3e-5/f,10) + 1e-8*invf2)); //reddening factor from Petiteau Eq 1
  //Saccel_red*=4.0;//Hack to decrease low-freq sens by fac of 2.
  double Sloc=Dloc2*ddtsq/4.0;//Factor of 1/4.0 is in Petiteau eq 2
  double S4yrWDWD=5.16e-27*exp(-pow(f,1.2)*2.9e3)*pow(f,(-7./3.))*0.5*(1.0 + tanh(-(f-2.0e-3)*1.9e3))*ddtsq;//Stas' fit for 4yr noise (converted from Sens curve to position noise by multipyling by 3*L^2/80) which looks comparable to my fit), then converted to velocity noise
  double Spm_vel = ( Saccel_red + Sloc + S4yrWDWD );
  return Spm_vel / C2;//finally convert from velocity noise to fractional-frequency doppler noise.
}
static double SopLISA2017(const double f) {
  //double invf2 = 1./(f*f);
  const double twopi2=4.0*PI*PI;
  double ddtsq=twopi2*f*f; //time derivative factor
  const double C2=C_SI*C_SI; //veloc to doppler
  const double Dloc=1.7e-12; //local IFO noise in m/sqrt(Hz)
  const double Dsci=8.9e-12; //science IFO noise in m/sqrt(Hz)
  const double Dmisc=2.0e-12; //misc. optical path noise in m/sqrt(Hz)
  const double Dop2=Dsci*Dsci+Dloc*Dloc+Dmisc*Dmisc;
  double Sop=Dop2*ddtsq/C2; //f^2 coeff for OP frac-freq noise PSD.  Yields 1.76e-37 for Dop=2e-11.
  return Sop;
}

/* Proof mass and optical noises - f in Hz */
/* LISA Proposal, copied from the LISA Data Challenge pipeline */
static double SpmLISAProposal(const double f) {
  /* Acceleration noise */
  double noise_Sa_a = 9.e-30; /* m^2/sec^4 /Hz */
  /* In acceleration */
  double Sa_a = noise_Sa_a * (1.0 + pow(0.4e-3/f, 2)) * (1.0 + pow((f/8e-3), 4));
  /* In displacement */
  double Sa_d = Sa_a * pow(2.*PI*f, -4);
  /* In relative frequency unit */
  double Sa_nu = Sa_d * pow(2.*PI*f/C_SI, 2);
  double Spm = Sa_nu;
  return Spm;
}
static double SopLISAProposal(const double f) {
  /* Optical Metrology System noise */
  double noise_Soms_d = pow((10e-12), 2); /* m^2/Hz */
  /* In displacement */
  double Soms_d = noise_Soms_d * (1. + pow(2.e-3/f, 4));
  /* In relative frequency unit */
  double Soms_nu = Soms_d * pow(2.*PI*f/C_SI, 2);
  double Sop = Soms_nu;
  return Sop;
}

/* Proof mass and optical noises - f in Hz */
/* LISA SciRDv1, copied from the LISA Data Challenge pipeline */
/* 'SciRDv1': Science Requirement Document: ESA-L3-EST-SCI-RS-001 14/05/2018 */
/* (https://atrium.in2p3.fr/f5a78d3e-9e19-47a5-aa11-51c81d370f5f) */
static double SpmLISASciRDv1(const double f) {
  /* Acceleration noise */
  double noise_Sa_a = 9.e-30; /* m^2/sec^4 /Hz */
  /* In acceleration */
  double Sa_a = noise_Sa_a * (1.0 + pow(0.4e-3/f, 2)) * (1.0 + pow((f/8e-3), 4));
  /* In displacement */
  double Sa_d = Sa_a * pow(2.*PI*f, -4);
  /* In relative frequency unit */
  double Sa_nu = Sa_d * pow(2.*PI*f/C_SI, 2);
  double Spm = Sa_nu;
  return Spm;
}
static double SopLISASciRDv1(const double f) {
  /* Optical Metrology System noise */
  double noise_Soms_d = pow((15e-12), 2); /* m^2/Hz */
  /* In displacement */
  double Soms_d = noise_Soms_d * (1. + pow(2.e-3/f, 4));
  /* In relative frequency unit */
  double Soms_nu = Soms_d * pow(2.*PI*f/C_SI, 2);
  double Sop = Soms_nu;
  return Sop;
}

/* Compute proof mass and optical noises, for a given choice of noise - f in Hz */
/* Allows a degradation of Spm as (1+(f0/f)^alpha) */
/* No modification for f0 = 0. */
/* BEWARE: keep alpha > 0 ! */
static void ComputeLISASpmSop(double* Spm, double* Sop, double f,
                              const LISANoiseModel* noisemodel) {
  LISAInstrumentalNoise noise = noisemodel->noise;
  if(noise==LISASciRDv1noise) {
    *Spm = SpmLISASciRDv1(f);
    *Sop = SopLISASciRDv1(f);
  }
  else if(noise==LISAProposalnoise) {
    *Spm = SpmLISAProposal(f);
    *Sop = SopLISAProposal(f);
  }
  else if(noise==LISA2017noise) {
    *Spm = SpmLISA2017(f);
    *Sop = SopLISA2017(f);
  }
  else if(noise==LISA2010noise) {
    *Spm = SpmLISA2010(f);
    *Sop = SopLISA2010(f);
  }
  else {
    ERROR(ERROR_EINVAL, "LISAInstrumentalNoise=%i not recognized.\n",noise);
  }
  /* Introduce a low-frequency degradation of Spm */
  /* Silent if f0 = 0., alpha != 0 */
  double f0 = noisemodel->lowf_add_pm_noise_f0;
  double alpha = noisemodel->lowf_add_pm_noise_alpha;
  if (alpha==0.) {
    ERROR(ERROR_EINVAL, "Power alpha=0 not allowed in (1+(f0/f)^alpha) \
                                              (can create 0^0 situations).\n");
  }
  *Spm = *Spm * (1. + pow(f0/f, alpha));
}

/* Noise Sn for TDI observables - factors have been scaled out both in the response and the noise */
/* Rescaled by 4*sin2pifL^2 */
double SnXYZ(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseXYZRescaled(f, twopifL, LISAnoise->WDduration);
  return 4*( 2*(1. + c2*c2)*Spm + Sop ) + galnoise;
}
/* Noise functions for AET(XYZ) with rescaling */
/* Rescaled by 2*sin2pifL^2 */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnA(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  return 4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise;
}
/* Rescaled by 2*sin2pifL^2 */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnE(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  return 4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise;
}
/* Rescaled by 8*sin2pifL^2*sinpifL^2 */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnT(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double pifL = PI*LISAconst->OrbitL/C_SI*f;
  double s1 = sin(pifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  /* Note: no galaxy noise available for channel T, so none added */
  double galnoise = 0.;
  return 4 * (4*s1*s1*Spm + Sop) + galnoise;
}

/* Noise functions for X,Y,Z without rescaling */
/* Scaling by 4*sin2pifL^2 put back */
double SnXYZNoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double s2 = sin(twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseXYZRescaled(f, twopifL, LISAnoise->WDduration);
  return 4*s2*s2 * (4*( 2*(1. + c2*c2)*Spm + Sop ) + galnoise);
}
/* Noise functions for AET(XYZ) without rescaling */
/* Scaling by 2*sin2pifL^2 put back */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnANoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double s2 = sin(twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  return 2*s2*s2 * (4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise);
}
/* Scaling by 2*sin2pifL^2 put back */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnENoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double s2 = sin(twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  return 2*s2*s2 * (4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise);
}
/* Scaling by 8*sin2pifL^2*sinpifL^2 put back*/
/* LDC convention - factor of 4 with respect to old flare convention */
double SnTNoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double pifL = PI*LISAconst->OrbitL/C_SI*f;
  double s1 = sin(pifL);
  double s2 = sin(2*pifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  /* Note: no galaxy noise available for channel T, so none added */
  double galnoise = 0.;
  return 8*s1*s1*s2*s2 * (4 * (4*s1*s1*Spm + Sop) + galnoise);
}

/* Noise functions for X,Y,Z without rescaling for TDI 2 */
/* Scaling by 4*sin2pifL^2 put back */
/* Additional scaling 4*sin4pifL^2 for TDI 2 */
double SnXYZ2NoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double s2 = sin(twopifL);
  double s4 = sin(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseXYZRescaled(f, twopifL, LISAnoise->WDduration);
  /* Factor to go from TDI 1st-gen to TDI 2nd-gen */
  double factor_tdi2 = 4*s4*s4;
  return factor_tdi2 * 4*s2*s2 * (4*( 2*(1. + c2*c2)*Spm + Sop ) + galnoise);
}
/* Noise functions for AET(XYZ) without rescaling for TDI 2 */
/* Scaling by 2*sin2pifL^2 put back */
/* Additional scaling 4*sin4pifL^2 for TDI 2 */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnA2NoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double s2 = sin(twopifL);
  double s4 = sin(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  /* Factor to go from TDI 1st-gen to TDI 2nd-gen */
  double factor_tdi2 = 4*s4*s4;
  return factor_tdi2 * 2*s2*s2 * (4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise);
}
/* Scaling by 2*sin2pifL^2 put back */
/* Additional scaling 4*sin4pifL^2 for TDI 2 */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnE2NoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double s2 = sin(twopifL);
  double s4 = sin(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  /* Factor to go from TDI 1st-gen to TDI 2nd-gen */
  double factor_tdi2 = 4*s4*s4;
  return factor_tdi2 * 2*s2*s2 * (4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise);
}
/* Scaling by 8*sin2pifL^2*sinpifL^2 put back */
/* Additional scaling 4*sin4pifL^2 for TDI 2 */
/* LDC convention - factor of 4 with respect to old flare convention */
double SnT2NoRescaling(const void* object, double f) {
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero)f=fzero;
  double pifL = PI*LISAconst->OrbitL/C_SI*f;
  double s1 = sin(pifL);
  double s2 = sin(2*pifL);
  double s4 = sin(4*pifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  /* Note: no galaxy noise available for channel T, so none added */
  double galnoise = 0.;
  /* Factor to go from TDI 1st-gen to TDI 2nd-gen */
  double factor_tdi2 = 4*s4*s4;
  return factor_tdi2 * 8*s1*s1*s2*s2 * (4 * (4*s1*s1*Spm + Sop) + galnoise);
}

/******************************************************************************/
/* Noise functions for 3 channels */
/******************************************************************************/

void Sn3ChanXYZ(double* SnX,
                double* SnY,
                double* SnZ,
                const void* object,
                double f)
{
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if (f<fzero) f = fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseXYZRescaled(f, twopifL, LISAnoise->WDduration);
  double SnXYZval = 4*( 2*(1. + c2*c2)*Spm + Sop ) + galnoise;
  *SnX = SnXYZval;
  *SnY = SnXYZval;
  *SnZ = SnXYZval;
}

void Sn3ChanXYZNoRescaling(double* SnX,
                           double* SnY,
                           double* SnZ,
                           const void* object,
                           double f)
{
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if (f<fzero) f = fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double s2 = sin(twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseXYZRescaled(f, twopifL, LISAnoise->WDduration);
  double SnXYZval = 4*s2*s2 * (4*( 2*(1. + c2*c2)*Spm + Sop ) + galnoise);
  *SnX = SnXYZval;
  *SnY = SnXYZval;
  *SnZ = SnXYZval;
}

void Sn3ChanXYZ2NoRescaling(double* SnX,
                            double* SnY,
                            double* SnZ,
                            const void* object,
                            double f)
{
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if (f<fzero) f = fzero;
  double twopifL = 2.*PI*LISAconst->OrbitL/C_SI*f;
  double c2 = cos(twopifL);
  double s2 = sin(twopifL);
  double s4 = sin(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseXYZRescaled(f, twopifL, LISAnoise->WDduration);
  /* Factor to go from TDI 1st-gen to TDI 2nd-gen */
  double factor_tdi2 = 4*s4*s4;
  double SnXYZval = factor_tdi2 * 4*s2*s2 * (4*( 2*(1. + c2*c2)*Spm + Sop ) + galnoise);
  *SnX = SnXYZval;
  *SnY = SnXYZval;
  *SnZ = SnXYZval;
}

void Sn3ChanAET(double* SnA,
                double* SnE,
                double* SnT,
                const void* object,
                double f)
{
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero) f = fzero;
  double pifL = PI*LISAconst->OrbitL/C_SI*f;
  double twopifL = 2*pifL;
  double s1 = sin(pifL);
  //double s2 = sin(2*pifL);
  double c2 = cos(2*pifL);
  double c4 = cos(4*pifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  /* Note: no galaxy noise available for channel T, so none added */
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  double SnAEval = 4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise;
  double SnTval = 4 * (4*s1*s1*Spm + Sop);
  *SnA = SnAEval;
  *SnE = SnAEval;
  *SnT = SnTval;
}

void Sn3ChanAETNoRescaling(double* SnA,
                           double* SnE,
                           double* SnT,
                           const void* object,
                           double f)
{
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero) f = fzero;
  double pifL = PI*LISAconst->OrbitL/C_SI*f;
  double twopifL = 2*pifL;
  double s1 = sin(pifL);
  double s2 = sin(twopifL);
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  /* Note: no galaxy noise available for channel T, so none added */
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  double SnAEval = 2*s2*s2 * (4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise);
  double SnTval = 8*s1*s1*s2*s2 * 4 * (4*s1*s1*Spm + Sop);
  *SnA = SnAEval;
  *SnE = SnAEval;
  *SnT = SnTval;
}

void Sn3ChanAET2NoRescaling(double* SnA,
                            double* SnE,
                            double* SnT,
                            const void* object,
                            double f)
{
  const LISA_noise_func_data* variant = (const LISA_noise_func_data*) object;
  const LISANoiseModel* LISAnoise = variant->LISAnoise;
  const LISAconstellation* LISAconst = variant->LISAconst;
  if(f<fzero) f = fzero;
  double pifL = PI*LISAconst->OrbitL/C_SI*f;
  double twopifL = 2*pifL;
  double s1 = sin(pifL);
  double s2 = sin(twopifL);
  double s4 = sin(2*twopifL);
  double c2 = cos(twopifL);
  double c4 = cos(2*twopifL);
  double Spm = 0., Sop = 0.;
  ComputeLISASpmSop(&Spm, &Sop, f, LISAnoise);
  /* Note: no galaxy noise available for channel T, so none added */
  double galnoise = 0.;
  if (LISAnoise->WDbackground)
    galnoise = LDCGalaxyNoiseAERescaled(f, twopifL, LISAnoise->WDduration);
  /* Factor to go from TDI 1st-gen to TDI 2nd-gen */
  double factor_tdi2 = 4*s4*s4;
  double SnAEval = factor_tdi2 * 2*s2*s2 * (4 * (2*(3. + 2*c2 + c4)*Spm + (2 + c2)*Sop) + galnoise);
  double SnTval = factor_tdi2 * 8*s1*s1*s2*s2 * 4 * (4*s1*s1*Spm + Sop);
  *SnA = SnAEval;
  *SnE = SnAEval;
  *SnT = SnTval;
}

/* Function to compute the WD galactic confusion noise for a given duration */
/* Copied from ldc.lisa.noise, assumes 6 links, SNR=7, L=2.5e9, SciRDv1 */
double LDCGalaxyShape(
  double f,
  double WDduration)
{
  double Ampl = 1.28265531e-44, alpha = 1.62966700e+00, fr2 = 4.81078093e-04, af1 = -2.23499956e-01, bf1 = -2.70408439e+00, afk = -3.60976122e-01, bfk = -2.37822436e+00;

  double Tmin = 0.25;
  double Tmax = 10.0;
  if ((WDduration<Tmin) || (WDduration>Tmax))
    ERROR(ERROR_EDOM, "Galaxy fit is valid between 3 months and 10 years\n");

  double log10WDduration = log10(WDduration);
  double fr1 = pow(10., (af1*log10WDduration + bf1));
  double fknee = pow(10., (afk*log10WDduration + bfk));
  /* This quantity is output by GalNoise.galshape in ldc */
  double galshape = Ampl * exp(-pow((f/fr1), alpha)) * (pow(f, -7./3.))*0.5*(1.0 + tanh(-(f-fknee)/fr2));
  /* Rescaling */
  return galshape;
}
/* Rescaled to represent additive contribution in SnA,SnE rescaled: */
/* represents 3*(2pifL)^2*GalNoise(...) */
double LDCGalaxyNoiseAERescaled(
  double f,
  double twopifL,
  double WDduration)
{
  /* This quantity is output by GalNoise.galshape in ldc */
  double galshape = LDCGalaxyShape(f, WDduration);

  /* Rescaling */
  return 3*twopifL*twopifL * galshape;
}
/* Rescaled to represent additive contribution in SnXYZ rescaled: */
/* represents 2*(2pifL)^2*GalNoise(...) */
double LDCGalaxyNoiseXYZRescaled(
  double f,
  double twopifL,
  double WDduration)
{
  /* This quantity is output by GalNoise.galshape in ldc */
  double galshape = LDCGalaxyShape(f, WDduration);

  /* Rescaling */
  return 2*twopifL*twopifL * galshape;
}

// /*Versions of these function with void pointers (to allow generalization beyond LISA)*/
// double SnXYZv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   return SnXYZ(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnAv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   return SnA(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnEv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   return SnE(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnTv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   return SnT(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnXYZNoRescalingv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   //printf("object=%p, noise type %i\n",object,variant->noise);
//   return SnXYZNoRescaling(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnANoRescalingv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   //printf("object=%p, noise type %i\n",object,variant->noise);
//   return SnANoRescaling(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnENoRescalingv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   return SnENoRescaling(variant->LISAnoise,variant->LISAconst,f);
// };
//
// double SnTNoRescalingv(const void *object, double f){
//   const LISA_noise_func_data *variant=(const LISA_noise_func_data*) object;
//   return SnTNoRescaling(variant->LISAnoise,variant->LISAconst,f);
// };
