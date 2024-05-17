/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#ifndef _SPLINE_H
#define _SPLINE_H

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


#if defined(__cplusplus)
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif

/* Build a cubic not-a-knot spline, represented as a matrix */
int BuildNotAKnotSpline(
  real_matrix** splinecoeffs,  /* Output: matrix of spline coeffs */
  real_vector* vectx,          /* Input: vector x */
  real_vector* vecty);         /* Input: vector y */

/* Build a quadratic spline, represented as a matrix */
int BuildQuadSpline(
  real_matrix** splinecoeffs,  /* Output: matrix of spline coeffs */
  real_vector* vectx,          /* Input: vector x */
  real_vector* vecty);         /* Input: vector y */

/* Function to compute the derivative of a cubic spline */
/* Returns a spline matrix of the same dimension, with zero cubic coeffs */
int CubicSplineDerivative(
  real_matrix** spline_deriv,  /* Output: matrix for derivative cubic spline */
  real_matrix* spline);        /* Input: matrix for cubic spline */

/* Function to compute the double derivative of a cubic spline */
/* Returns a spline matrix of the same dimension, with zero quadratic, cubic coeffs */
int CubicSplineDoubleDerivative(
  real_matrix** spline_dderiv, /* Output: matrix for double derivative cubic spline */
  real_matrix* spline);        /* Input: matrix for cubic spline */

/* Function to compute the integral of a cubic spline */
/* Returns a spline matrix of dimension+1 (4th order polynomials) */
int CubicSplineIntegral(
  real_matrix** spline_int,    /* Output: matrix for integral cubic spline */
  real_matrix* spline);        /* Input: matrix for cubic spline */

/* Function to compute the derivative of a quad spline */
/* Returns a spline matrix of the same dimension, with zero quad coeffs */
int QuadSplineDerivative(
  real_matrix** spline_deriv,  /* Output: matrix for derivative quad spline */
  real_matrix* spline);        /* Input: matrix for quad spline */

/* Functions to multiply/add to the x/y data of a spline matrix by a constant */
/* IN PLACE, no copy */
int CubicSplineScaley(
  real_matrix* spline,   /* Input/Output (in place): matrix for cubic spline */
  double s);             /* Multiplication constant */
int QuadSplineScaley(
  real_matrix* spline,   /* Input/Output (in place): matrix for quad spline */
  double s);             /* Multiplication constant */
int CubicSplineAddy(
  real_matrix* spline,   /* Input/Output (in place): matrix for cubic spline */
  double a);             /* Addition constant */
int QuadSplineAddy(
  real_matrix* spline,   /* Input/Output (in place): matrix for quad spline */
  double a);             /* Addition constant */
int CubicSplineScalex(
  real_matrix* spline,   /* Input/Output (in place): matrix for cubic spline */
  double s);             /* Multiplication constant */
int QuadSplineScalex(
  real_matrix* spline,   /* Input/Output (in place): matrix for quad spline */
  double s);             /* Multiplication constant */

// int BuildSplineCoeffs(
//   CAmpPhaseSpline** splines,                  /*  */
//   CAmpPhaseFrequencySeries* freqseries);      /*  */
//
// int BuildListmodesCAmpPhaseSpline(
//   ListmodesCAmpPhaseSpline** listspline,              /* Output: list of modes of splines in matrix form */
//   ListmodesCAmpPhaseFrequencySeries* listh);          /* Input: list of modes in amplitude/phase form */

/* Evaluate cubic spline on a vector of increasing values */
/* NOTE: assumes xvec is sorted, only range-checks the two ends */
int EvalCubicSplineOnVector(
  real_vector** yvec,     /* Output: pointer to spline-evaluated y values */
  real_vector* xvec,      /* Input: x values to evluate on */
  real_matrix* spline,    /* Input: spline matrix */
  int extrapol_zero);     /* Allow values of x outside of spline range, return 0 there */

/* Evaluate quad spline on a vector of increasing values */
/* NOTE: assumes xvec is sorted, only range-checks the two ends */
int EvalQuadSplineOnVector(
  real_vector** yvec,     /* Output: pointer to spline-evaluated y values */
  real_vector* xvec,      /* Input: x values to evluate on */
  real_matrix* spline,    /* Input: spline matrix */
  int extrapol_zero);     /* Allow values of x outside of spline range, return 0 there */

/* Evaluate cubic spline at input value */
/* Uses a slide index that is updated with the evaluation */
/* Keeps track of last interval, requires increasing values of x */
int EvalCubicSplineSlide(
  double* res,            /* Output: pointer to the result */
  real_matrix* spline,    /* Pointer to line in spline matrix */
  size_t* i_slide,        /* Pointer to persistent index for slide eval */
  double x);              /* x value to evaluate */

/* Evaluate quadratic spline at input value */
/* Uses a slide index that is updated with the evaluation */
/* Keeps track of last interval, requires increasing values of x */
int EvalQuadSplineSlide(
  double* res,            /* Output: pointer to the result */
  real_matrix* spline,    /* Pointer to line in spline matrix */
  size_t* i_slide,        /* Pointer to persistent index for slide eval */
  double x);              /* x value to evaluate */

/* Evaluate cubic polynomial of spline */
/* Note: for splines in matrix form, the first column contains the x values */
/* So the coeffs start at 1 */
inline double EvalCubic(
  double* coeffs,        /* Pointer to line in spline matrix */
  double x)              /* x value to evaluate, no range checking */
{
  double eps = x - coeffs[0];
  return coeffs[1] + eps * (coeffs[2] + eps * (coeffs[3] + eps * coeffs[4]));
}

/* Evaluate quadratic polynomial of spline */
/* Note: for splines in matrix form, the first column contains the x values */
/* So the coeffs start at 1 */
inline double EvalQuad(
  double* coeffs,       /* Pointer to line in spline matrix */
  double x)             /* x value to evaluate, no range checking */
{
  double eps = x - coeffs[0];
  return coeffs[1] + eps * (coeffs[2] + eps * coeffs[3]);
}

// UNFINISHED
// REQUIRES DEBUGGING
// /* Evaluate complex exponential of cubic phase spline */
// int EvalCubicSplineCExpOnConstDeltaxVector(
//   complex_vector** cexpvec,   /* Output: pointer to spline-evaluated y values */
//   real_vector* xvec,          /* Input: evenly spaced x values to evaluate on */
//   real_matrix* phase_spline); /* Input: cubic spline matrix */
// int EvalCubicCExpOnConstDeltaxInterval(
//   complex_vector* cexpvec,
//   double* coeffs,
//   double Deltax_spline,
//   double Deltax,
//   int ix_start,
//   int ix_end);

// void EvalCAmpPhaseSpline(
//   CAmpPhaseSpline* splines,                     //input
//   CAmpPhaseFrequencySeries* freqseries);  //in/out defines CAmpPhase from defined freqs

#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _SPLINE_H */
