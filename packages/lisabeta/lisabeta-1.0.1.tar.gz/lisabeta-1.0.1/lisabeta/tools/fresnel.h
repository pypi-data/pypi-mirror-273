/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#ifndef _FRESNEL_H
#define _FRESNEL_H

#define _XOPEN_SOURCE 500

#ifdef __GNUC__
#define UNUSED __attribute__ ((unused))
#else
#define UNUSED
#endif

#include "constants.h"
#include "struct.h"
#include "tools.h"


#if defined(__cplusplus)
#define complex _Complex
extern "C" {
#elif 0
} /* so that editors will match preceding brace */
#endif

double complex ComputeInt(
  real_matrix* splinecoeffsAreal,         /*  */
  real_matrix* splinecoeffsAimag,         /*  */
  real_matrix* splinecoeffsphase);        /*  */

double complex ComputeIntCase1a(
  const double complex* coeffsA,         /* */
  const double p1,                       /* */
  const double p2,                       /* */
  const double scale);                   /* */
double complex ComputeIntCase1b(
  const double complex* coeffsA,         /* */
  const double p1,                       /* */
  const double p2,                       /* */
  const double scale);                   /* */
double complex ComputeIntCase2(
  const double complex* coeffsA,         /* */
  const double p1,                       /* */
  const double p2);                      /* */
double complex ComputeIntCase3(
  const double complex* coeffsA,         /* */
  const double p1,                       /* */
  const double p2);                      /* */
double complex ComputeIntCase4(
  const double complex* coeffsA,         /* */
  const double p1,                       /* */
  const double p2);                      /* */


#if 0
{ /* so that editors will match succeeding brace */
#elif defined(__cplusplus)
}
#endif

#endif /* _FRESNEL_H */
