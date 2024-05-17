/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#include "spline.h"

/******************************************************************************/

/* Implementation of the Thomas algorithm to solve a tridiagonal system */
/* Note: assumes numerical stability (e.g. diagonal-dominated matrix) */
static void SolveTridiagThomas(
  real_vector* vectx,        /* Output: solution vector, length n - allocated */
  real_vector* vecta,        /* Diagonal of the matrix, length n */
  real_vector* vectb,        /* Lower diagonal, length n-1 */
  real_vector* vectc,        /* Upper diagonal, length n-1 */
  real_vector* vecty,        /* Right-hand-side vector, length n */
  size_t size)                  /* Length of vectx, vecty */
{
  /* Check lengths */
  if(!(vectx->size==size && vecty->size==size && vecta->size==size
       && vectb->size==size-1 && vectc->size==size-1)) {
    ERROR(ERROR_EINVAL, "Incompatible vector lengths.\n");
  }
  int n = size;

  /* Note: we modify the vectors c, y in place */
  double* chat = vectc->data;
  double* yhat = vecty->data;
  double* x = vectx->data;
  double* a = vecta->data;
  double* b = vectb->data;

  /* Sweep forward, computing the chat and yhat values */
  chat[0] = chat[0] / a[0];
  yhat[0] = yhat[0] / a[0];
  double factor;
  for(int i=1; i<=n-2; i++) {
    factor = 1./(a[i] - b[i-1]*chat[i-1]);
    chat[i] = chat[i] * factor;
    yhat[i] = (yhat[i] - b[i-1]*yhat[i-1]) * factor;
  }
  factor = 1./(a[n-1] - b[n-2]*chat[n-2]);
  yhat[n-1] = (yhat[n-1] - b[n-2]*yhat[n-2]) * factor;

  /* Solve for x going backward */
  x[n-1] = yhat[n-1];
  for(int i=n-2; i>=0; i--) {
    x[i] = yhat[i] - chat[i] * x[i+1];
  }
}

/******************************************************************************/

/* Build a cubic not-a-knot spline, represented as a matrix */
int BuildNotAKnotSpline(
  real_matrix** splinecoeffs,  /* Output: matrix of spline coeffs */
  real_vector* vectx,          /* Input: vector x*/
  real_vector* vecty)          /* Input: vector y */
{
  /* Check input */
  if (!(*splinecoeffs==NULL))
    ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (vectx==NULL || vecty==NULL)
    ERROR(ERROR_EFAULT, "Input pointer is NULL.");
  /* Lengths */
  int n = (int) vectx->size;
  if (n<4) {
    printf("n=%i\n",n);
    ERROR(ERROR_EINVAL, "Vector lengths must exceed 3. \n");
  }
  if (!( (int) vecty->size==n)) {
    ERROR(ERROR_EINVAL, "Incompatible vector lengths.\n");
  }

  double* x = vectx->data;
  double* y = vecty->data;

  /* Computing vecth and vectDeltay */
  real_vector* vecth = real_vector_alloc(n-1);
  real_vector* vectDeltay = real_vector_alloc(n-1);
  real_vector* vectDeltayoverh = real_vector_alloc(n-1);
  double* h = vecth->data;
  double* Deltay = vectDeltay->data;
  double* Deltayoverh = vectDeltayoverh->data;
  for(int i=0; i<n-1; i++) {
    h[i] = x[i+1] - x[i];
    Deltay[i] = y[i+1] - y[i];
    Deltayoverh[i] = Deltay[i] / h[i];
  }

  /* Structures for the tridiagonal system */
  real_vector* vectY = real_vector_alloc(n-2);
  real_vector* vecta = real_vector_alloc(n-2);
  real_vector* vectb = real_vector_alloc(n-3);
  real_vector* vectc = real_vector_alloc(n-3);
  double* Y = vectY->data;
  double* a = vecta->data;
  double* b = vectb->data;
  double* c = vectc->data;
  for(int i=0; i<=n-3; i++) {
    Y[i] = 3.*(Deltayoverh[i+1] - Deltayoverh[i]);
    a[i] = 2.*(h[i+1] + h[i]);
  }
  for(int i=0; i<=n-4; i++) {
    b[i] = h[i+1];
    c[i] = h[i+1];
  }
  /* Adjusting for the not-a-knot condition */
  a[0] += h[0] + h[0]*h[0]/h[1];
  c[0] += -h[0]*h[0]/h[1];
  a[n-3] += h[n-2] + h[n-2]*h[n-2]/h[n-3];
  b[n-4] += -h[n-2]*h[n-2]/h[n-3];

  /* Solving the tridiagonal system */
  real_vector* vectp2 = real_vector_alloc(n);
  real_vector* vectp2trunc_view = real_vector_view_subvector(vectp2, 1, n-2);
  SolveTridiagThomas(vectp2trunc_view, vecta, vectb, vectc, vectY, n-2);
  double* p2 = vectp2->data;
  p2[0] = p2[1] - h[0]/h[1] * (p2[2] - p2[1]);
  p2[n-1] = p2[n-2] + h[n-2]/h[n-3] * (p2[n-2] - p2[n-3]);

  /* Deducing the p1's and the p3's */
  real_vector* vectp1 = real_vector_alloc(n);
  real_vector* vectp3 = real_vector_alloc(n);
  double* p1 = vectp1->data;
  double* p3 = vectp3->data;
  for(int i=0; i<=n-2; i++) {
    p1[i] = Deltayoverh[i] - h[i]/3. * (p2[i+1] + 2.*p2[i]);
    p3[i] = (p2[i+1] - p2[i]) / (3*h[i]);
  }
  /* Note: p1[n-1], p2[n-1], p3[n-1] are set to values coherent with the
   * derivatives of the spline at the last point, but they are not stricly
   * speaking coefficients of the spline. */
  p1[n-1] = p1[n-2] + 2.*p2[n-2]*h[n-2] + 3.*p3[n-2]*h[n-2]*h[n-2];
  p3[n-1] = p3[n-2];

  /* Allocate output */
  *splinecoeffs = real_matrix_alloc(n, 5);

  /* Copying the results in the output matrix -  without gsl views, by hand ! */
  for(int i=0; i<n; i++) {
    real_matrix_set(*splinecoeffs, i, 0, x[i]);
    real_matrix_set(*splinecoeffs, i, 1, y[i]);
    real_matrix_set(*splinecoeffs, i, 2, p1[i]);
    real_matrix_set(*splinecoeffs, i, 3, p2[i]);
    real_matrix_set(*splinecoeffs, i, 4, p3[i]);
  }

  /* Cleanup*/
  real_vector_free(vecth);
  real_vector_free(vectDeltay);
  real_vector_free(vectDeltayoverh);
  real_vector_free(vectY);
  real_vector_free(vecta);
  real_vector_free(vectb);
  real_vector_free(vectc);
  real_vector_free(vectp1);
  real_vector_free(vectp2);
  real_vector_free(vectp3);
  real_vector_view_free(vectp2trunc_view);

  return SUCCESS;
}

/******************************************************************************/

/* Build a quadratic spline, represented as a matrix */
int BuildQuadSpline(
  real_matrix** splinecoeffs,  /* Output: matrix of spline coeffs */
  real_vector* vectx,          /* Input: vector x */
  real_vector* vecty)          /* Input: vector y */
{
  /* Check input */
  if (!(*splinecoeffs==NULL))
    ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (vectx==NULL || vecty==NULL)
    ERROR(ERROR_EFAULT, "Input pointer is NULL.");
  /* Lengths */
  int n = (int) vectx->size;
  if (!( (int) vecty->size==n)) {
    ERROR(ERROR_EINVAL, "Incompatible vector lengths.\n");
  }

  double* x = vectx->data;
  double* y = vecty->data;

  /* Computing vecth and vectDeltay */
  real_vector* vecth = real_vector_alloc(n-1);
  real_vector* vectDeltay = real_vector_alloc(n-1);
  real_vector* vectDeltayoverh = real_vector_alloc(n-1);
  double* h = vecth->data;
  double* Deltay = vectDeltay->data;
  double* Deltayoverh = vectDeltayoverh->data;
  for(int i=0; i<n-1; i++) {
    h[i] = x[i+1] - x[i];
    Deltay[i] = y[i+1] - y[i];
    Deltayoverh[i] = Deltay[i] / h[i];
  }

  /* Solving for p1 */
  real_vector* vectp1 = real_vector_alloc(n);
  double* p1 = vectp1->data;
  double ratio = h[n-2] / h[n-3];
  p1[n-3] = ((2. + ratio)*Deltayoverh[n-3] - Deltayoverh[n-2]) / (1. + ratio);
  p1[n-2] = -p1[n-3] + 2.*Deltayoverh[n-3];
  for(int i=n-4; i>=0; i--) {
    p1[i] = -p1[i+1] + 2.*Deltayoverh[i];
  }
  p1[n-1] = (1. + ratio)*p1[n-2] - ratio*p1[n-3];

  /* Deducing the p2's */
  real_vector* vectp2 = real_vector_alloc(n);
  double* p2 = vectp2->data;
  for(int i=0; i<=n-2; i++) {
    p2[i] = (p1[i+1] - p1[i]) / (2.*h[i]);
  }
  /* Note: p2[n-1] is set to values coherent with the derivatives of the spline
   * at the last point, but not stricly speaking a coefficient of the spline. */
  p2[n-1] = p2[n-2];

  /* Allocate output */
  *splinecoeffs = real_matrix_alloc(n, 4);

  /* Copying the results in the output matrix -  without gsl views, by hand ! */
  for(int i=0; i<n; i++) {
    real_matrix_set(*splinecoeffs, i, 0, x[i]);
    real_matrix_set(*splinecoeffs, i, 1, y[i]);
    real_matrix_set(*splinecoeffs, i, 2, p1[i]);
    real_matrix_set(*splinecoeffs, i, 3, p2[i]);
  }

  /* Cleanup*/
  real_vector_free(vecth);
  real_vector_free(vectDeltay);
  real_vector_free(vectDeltayoverh);
  real_vector_free(vectp1);
  real_vector_free(vectp2);

  return SUCCESS;
}

/* Function to compute the derivative of a cubic spline */
/* Returns a spline matrix of the same dimension, with zero cubic coeffs */
int CubicSplineDerivative(
  real_matrix** spline_deriv,  /* Output: matrix for derivative cubic spline */
  real_matrix* spline)         /* Input: matrix for cubic spline */
{
  /* Check input */
  if (!(*spline_deriv==NULL))
    ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (spline==NULL)
    ERROR(ERROR_EFAULT, "Input pointer is NULL.");

  int n = spline->size1;

  /* Allocate */
  *spline_deriv = real_matrix_alloc(n, 5);

  /* Set values */
  double* line = NULL;
  double* line_deriv = NULL;
  for(int i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line_deriv = real_matrix_line(*spline_deriv, i);
    line_deriv[0] = line[0];
    line_deriv[1] = line[2];
    line_deriv[2] = 2*line[3];
    line_deriv[3] = 3*line[4];
    line_deriv[4] = 0.;
  }

  return SUCCESS;
}

/* Function to compute the double derivative of a cubic spline */
/* Returns a spline matrix of the same dimension, with zero quadratic, cubic coeffs */
int CubicSplineDoubleDerivative(
  real_matrix** spline_dderiv, /* Output: matrix for double derivative cubic spline */
  real_matrix* spline)         /* Input: matrix for cubic spline */
{
  /* Check input */
  if (!(*spline_dderiv==NULL))
    ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (spline==NULL)
    ERROR(ERROR_EFAULT, "Input pointer is NULL.");

  int n = spline->size1;

  /* Allocate */
  *spline_dderiv = real_matrix_alloc(n, 5);

  /* Set values */
  double* line = NULL;
  double* line_dderiv = NULL;
  for(int i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line_dderiv = real_matrix_line(*spline_dderiv, i);
    line_dderiv[0] = line[0];
    line_dderiv[1] = 2*line[3];
    line_dderiv[2] = 6*line[4];
    line_dderiv[3] = 0.;
    line_dderiv[4] = 0.;
  }

  return SUCCESS;
}

/* Function to compute the integral of a cubic spline */
/* Returns a spline matrix of dimension+1 (4th order polynomials) */
int CubicSplineIntegral(
  real_matrix** spline_int,    /* Output: matrix for integral cubic spline */
  real_matrix* spline)         /* Input: matrix for cubic spline */
{
  /* Check input */
  if (!(*spline_int==NULL))
    ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (spline==NULL)
    ERROR(ERROR_EFAULT, "Input pointer is NULL.");

  int n = spline->size1;

  /* Allocate */
  /* NOTE: one more column than a cubic spline */
  *spline_int = real_matrix_alloc(n, 6);

  /* Set values */
  double* line = NULL;
  double* line_int = NULL;
  double val = 0.;
  double eps = 0.;
  for(int i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line_int = real_matrix_line(*spline_int, i);
    line_int[0] = line[0];
    line_int[1] = val;
    line_int[2] = line[1];
    line_int[3] = 1./2*line[2];
    line_int[4] = 1./3*line[3];
    line_int[5] = 1./4*line[4];
    eps = real_matrix_get(spline, i+1, 0) - line[0];
    val += eps * (line_int[2] + eps * (line_int[3]
                                    + eps * (line_int[4] + eps * line_int[5])));
  }
  /* Note: at the last point, the last increment of val is simply discarded */
  /* Coeff values at the last line of the quartic spline are meaningless */
  /* They are simply copies of the previous line */

  return SUCCESS;
}

/* Function to compute the derivative of a quad spline */
/* Returns a spline matrix of the same dimension, with zero quad coeffs */
int QuadSplineDerivative(
  real_matrix** spline_deriv,  /* Output: matrix for derivative quad spline */
  real_matrix* spline)         /* Input: matrix for quad spline */
{
  /* Check input */
  if (!(*spline_deriv==NULL))
    ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (spline_deriv==NULL)
    ERROR(ERROR_EFAULT, "Input pointer is NULL.");

  int n = spline->size1;

  /* Allocate */
  *spline_deriv = real_matrix_alloc(n, 4);

  /* Set values */
  double* line = NULL;
  double* line_deriv = NULL;
  for(int i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line_deriv = real_matrix_line(*spline_deriv, i);
    line_deriv[0] = line[0];
    line_deriv[1] = line[2];
    line_deriv[2] = 2*line[3];
    line_deriv[3] = 0.;
  }

  return SUCCESS;
}

/* Functions to multiply/add to the y data of a spline matrix by a constant */
/* IN PLACE, no copy */
int CubicSplineScaley(
  real_matrix* spline,   /* Input/Output (in place): matrix for cubic spline */
  double s)             /* Multiplication constant */
{
  size_t n = spline->size1;
  double* line;
  for (size_t i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line[1] *= s;
    line[2] *= s;
    line[3] *= s;
    line[4] *= s;
  }
  return SUCCESS;
}
int QuadSplineScaley(
  real_matrix* spline,   /* Input/Output (in place): matrix for quad spline */
  double s)             /* Multiplication constant */
{
  size_t n = spline->size1;
  double* line;
  for (size_t i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line[1] *= s;
    line[2] *= s;
    line[3] *= s;
  }
  return SUCCESS;
}
int CubicSplineAddy(
  real_matrix* spline,   /* Input/Output (in place): matrix for cubic spline */
  double a)             /* Addition constant */
{
  size_t n = spline->size1;
  double* line;
  for (size_t i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line[1] += a;
  }
  return SUCCESS;
}
int QuadSplineAddy(
  real_matrix* spline,   /* Input/Output (in place): matrix for quad spline */
  double a)             /* Addition constant */
{
  size_t n = spline->size1;
  double* line;
  for (size_t i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line[1] += a;
  }
  return SUCCESS;
}
int CubicSplineScalex(
  real_matrix* spline,   /* Input/Output (in place): matrix for cubic spline */
  double s)             /* Multiplication constant */
{
  size_t n = spline->size1;
  double invs = 1./s;
  double invs2 = invs*invs;
  double invs3 = invs2*invs;
  double* line;
  for (size_t i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line[0] *= s;
    line[2] *= invs;
    line[3] *= invs2;
    line[4] *= invs3;
  }
  return SUCCESS;
}
int QuadSplineScalex(
  real_matrix* spline,   /* Input/Output (in place): matrix for quad spline */
  double s)             /* Multiplication constant */
{
  size_t n = spline->size1;
  double invs = 1./s;
  double invs2 = invs*invs;
  double* line;
  for (size_t i=0; i<n; i++) {
    line = real_matrix_line(spline, i);
    line[0] *= s;
    line[2] *= invs;
    line[3] *= invs2;
  }
  return SUCCESS;
}

// void BuildSplineCoeffs(
//   CAmpPhaseSpline** splines,                  /*  */
//   CAmpPhaseFrequencySeries* freqseries)       /*  */
// {
//   /* Initialize output structure */
//   int n = (int) freqseries->freq->size;
//   CAmpPhaseSpline_Init(splines, n);
//
//   /* Build the splines */
//   BuildNotAKnotSpline((*splines)->spline_amp_real, freqseries->freq, freqseries->amp_real, n);
//   BuildNotAKnotSpline((*splines)->spline_amp_imag, freqseries->freq, freqseries->amp_imag, n);
//   BuildQuadSpline((*splines)->quadspline_phase, freqseries->freq, freqseries->phase, n);
// }
//
// void BuildListmodesCAmpPhaseSpline(
//   ListmodesCAmpPhaseSpline** listspline,              /* Output: list of modes of splines in matrix form */
//   ListmodesCAmpPhaseFrequencySeries* listh)           /* Input: list of modes in amplitude/phase form */
// {
//     if(*listspline){ /* We don't allow for the case where listspline already points to something */
//       printf("Error: Tried to add a mode to an already existing ListmodesCAmpPhaseSpline ");
//       exit(1);
//     }
//     else {
//       ListmodesCAmpPhaseFrequencySeries* listelementh = listh;
//       while(listelementh) {
// 	int l = listelementh->l;
// 	int m = listelementh->m;
// 	CAmpPhaseSpline* splines = NULL;
// 	BuildSplineCoeffs(&splines, listelementh->freqseries);
// 	*listspline = ListmodesCAmpPhaseSpline_AddModeNoCopy(*listspline, splines, l, m);
// 	listelementh = listelementh->next;
//       }
//     }
// }

/* Evaluate cubic spline on a vector of increasing values */
/* NOTE: assumes xvec is sorted, only range-checks the two ends */
int EvalCubicSplineOnVector(
  real_vector** yvec,     /* Output: pointer to spline-evaluated y values */
  real_vector* xvec,      /* Input: x values to evluate on */
  real_matrix* spline,    /* Input: spline matrix */
  int extrapol_zero)      /* Allow values of x outside of spline range, return 0 there */
{
  /* Check input/output pointers */
  if (xvec == NULL)
      ERROR(ERROR_EFAULT, "Input pointer to xvec is NULL.");
  if (spline == NULL)
      ERROR(ERROR_EFAULT, "Input pointer to spline is NULL.");
  if (*yvec != NULL)
      ERROR(ERROR_EFAULT, "Output pointer to yvec is not NULL.");

  size_t N = xvec->size;
  size_t n = spline->size1;

  /* Allocate output */
  *yvec = real_vector_alloc(N);

  /* Basic range checking, we assume xvec is sorted */
  double xmin_spline = real_matrix_get(spline, 0, 0);
  double xmax_spline = real_matrix_get(spline, n-1, 0);
  double xmin = real_vector_get(xvec, 0);
  double xmax = real_vector_get(xvec, N-1);
  /* If we do not extrapolate with zeros, check bounds */
  if (!extrapol_zero) {
    if ((xmin<xmin_spline) || (xmax_spline<xmax)) {
        real_vector_free(*yvec);
        ERRORCODE(ERROR_EINVAL, "Bounds of xvec exceed bounds of spline.");
      }
  }

  /* Evaluation by sliding along the spline, again assuming xvec is sorted */
  double x = 0., y = 0.;
  double* line;
  size_t i_spline = 0;
  double x_spline_up = real_matrix_get(spline, 1, 0);
  for (size_t i=0; i<N; i++) {
    x = real_vector_get(xvec, i);
    if ((x<xmin_spline) || (xmax_spline<x)) y = 0.;
    else {
      if (x_spline_up < x) {
        while (real_matrix_get(spline, i_spline+1, 0) < x) i_spline++;
        x_spline_up = real_matrix_get(spline, i_spline+1, 0);
      }
      line = real_matrix_line(spline, i_spline);
      y = EvalCubic(line, x);
    }
    real_vector_set(*yvec, i, y);
  }

  return SUCCESS;
}

/* Evaluate quad spline on a vector of increasing values */
/* NOTE: assumes xvec is sorted, only range-checks the two ends */
int EvalQuadSplineOnVector(
  real_vector** yvec,     /* Output: pointer to spline-evaluated y values */
  real_vector* xvec,      /* Input: x values to evluate on */
  real_matrix* spline,    /* Input: spline matrix */
  int extrapol_zero)      /* Allow values of x outside of spline range, return 0 there */
{
  /* Check input/output pointers */
  if (xvec == NULL)
      ERROR(ERROR_EFAULT, "Input pointer to xvec is NULL.");
  if (spline == NULL)
      ERROR(ERROR_EFAULT, "Input pointer to spline is NULL.");
  if (*yvec != NULL)
      ERROR(ERROR_EFAULT, "Output pointer to yvec is not NULL.");

  size_t N = xvec->size;
  size_t n = spline->size1;

  /* Allocate output */
  *yvec = real_vector_alloc(N);

  /* Basic range checking, we assume xvec is sorted */
  double xmin_spline = real_matrix_get(spline, 0, 0);
  double xmax_spline = real_matrix_get(spline, n-1, 0);
  double xmin = real_vector_get(xvec, 0);
  double xmax = real_vector_get(xvec, N-1);
  /* If we do not extrapolate with zeros, check bounds */
  if (!extrapol_zero) {
    if ((xmin<xmin_spline) || (xmax_spline<xmax)) {
        real_vector_free(*yvec);
        ERRORCODE(ERROR_EINVAL, "Bounds of xvec exceed bounds of spline.");
      }
  }

  /* Evaluation by sliding along the spline, again assuming xvec is sorted */
  double x = 0., y = 0.;
  double* line;
  size_t i_spline = 0;
  double x_spline_up = real_matrix_get(spline, 1, 0);
  for (size_t i=0; i<N; i++) {
    x = real_vector_get(xvec, i);
    if (x_spline_up < x) {
      while (real_matrix_get(spline, i_spline+1, 0) < x) i_spline++;
      x_spline_up = real_matrix_get(spline, i_spline+1, 0);
    }
    line = real_matrix_line(spline, i_spline);
    y = EvalQuad(line, x);
    real_vector_set(*yvec, i, y);
  }

  return SUCCESS;
}

// /* Evaluate quad spline on a vector of increasing values */
// /* NOTE: assumes xvec is sorted, only range-checks the two ends */
// double EvalQuadSplineVector(
//   real_vector** yvec,     /* Output: pointer to spline-evaluated y values */
//   real_vector* xvec,      /* Input: x values to evluate on */
//   real_matrix* spline);   /* Input: spline matrix */

/* Evaluate cubic spline at input value */
/* Uses a slide index that is updated with the evaluation */
/* Keeps track of last interval, requires increasing values of x */
int EvalCubicSplineSlide(
  double* res,            /* Output: pointer to the result */
  real_matrix* spline,    /* Pointer to line in spline matrix */
  size_t* i_slide,        /* Pointer to persistent index for slide eval */
  double x)               /* x value to evaluate */
{
  size_t i_slide_val = (*i_slide);
  size_t i_slide_data = 5 * i_slide_val;
  double* coeffs = &(spline->data[i_slide_data]);
  if (x<coeffs[0])
      ERRORCODE(ERROR_EINVAL, "Input value x is less than x of slide eval.\n");
  while (i_slide_val<(spline->size1-2) && spline->data[i_slide_data + 5]<x) {
    i_slide_val++;
    i_slide_data += 5;
  }

  if (x>spline->data[i_slide_data + 5])
      ERRORCODE(ERROR_EINVAL, "Input value x exceeds maximal value of spline.\n");

  /* Update persistent index for future evaluations */
  *i_slide = i_slide_val;

  /* Evaluate */
  coeffs = &(spline->data[i_slide_data]);

  *res = EvalCubic(coeffs, x);

  return SUCCESS;
}

/* Evaluate quadratic spline at input value */
/* Uses a slide index that is updated with the evaluation */
/* Keeps track of last interval, requires increasing values of x */
int EvalQuadSplineSlide(
  double* res,            /* Output: pointer to the result */
  real_matrix* spline,    /* Pointer to line in spline matrix */
  size_t* i_slide,        /* Pointer to persistent index for slide eval */
  double x)               /* x value to evaluate */
{
  size_t i_slide_val = (*i_slide);
  size_t i_slide_data = 4 * i_slide_val;
  double* coeffs = &(spline->data[i_slide_data]);
  if (x<coeffs[0])
      ERRORCODE(ERROR_EINVAL, "Input value x is less than x of slide eval.\n");
  while (i_slide_val<(spline->size1-2) && spline->data[i_slide_data + 4]<x) {
    i_slide_val++;
    i_slide_data += 4;
  }

  if (x>spline->data[i_slide_data + 4])
      ERRORCODE(ERROR_EINVAL, "Input value x exceeds maximal value of spline.\n");

  /* Update persistent index for future evaluations */
  *i_slide = i_slide_val;

  /* Evaluate */
  coeffs = &(spline->data[i_slide_data]);

  *res = EvalQuad(coeffs, x);

  return SUCCESS;
}

// UNFINISHED
// REQUIRES DEBUGGING
// /* Evaluate complex exponential of cubic phase spline */
// int EvalCubicSplineCExpOnConstDeltaxVector(
//   complex_vector** cexpvec,   /* Output: pointer to spline-evaluated y values */
//   real_vector* xvec,          /* Input: evenly spaced x values to evaluate on */
//   real_matrix* phase_spline)  /* Input: cubic spline matrix */
// {
//   /* Check input/output pointers */
//   if (xvec == NULL)
//       ERROR(ERROR_EFAULT, "Input pointer to xvec is NULL.");
//   if (phase_spline == NULL)
//       ERROR(ERROR_EFAULT, "Input pointer to spline is NULL.");
//   if (*cexpvec != NULL)
//       ERROR(ERROR_EFAULT, "Output pointer to yvec is not NULL.");
//
//   size_t N = xvec->size;
//   size_t n = phase_spline->size1;
//
//   /* Allocate output */
//   *cexpvec = complex_vector_alloc(N);
//
//   /* Basic range checking, we assume xvec is sorted */
//   double xmin_spline = real_matrix_get(phase_spline, 0, 0);
//   double xmax_spline = real_matrix_get(phase_spline, n-1, 0);
//   double xmin = real_vector_get(xvec, 0);
//   double xmax = real_vector_get(xvec, N-1);
//   if ((xmin<xmin_spline) || (xmax_spline<xmax))
//       ERROR(ERROR_EINVAL, "Bounds of xvec exceed bounds of phase spline.");
//
//   /* We will assume that Deltax = const */
//   /* NOTE: this will not be checked */
//   double Deltax = real_vector_get(xvec, 1) - real_vector_get(xvec, 0);
//   double x0 = real_vector_get(xvec, 0);
//
//   /* Loop on spline intervals: on each interval, compute the x values covered */
//   int ix_start = 0;
//   int ix_end = 0;
//   double* coeffs;
//   double xi_spline = 0;
//   double xf_spline = 0;
//   double Deltax_spline = 0;
//   for (size_t i=0; i<n-1; i++) {
//     coeffs = real_matrix_line(phase_spline, i);
//     xi_spline = real_matrix_get(phase_spline, i, 0);
//     xf_spline = real_matrix_get(phase_spline, i+1, 0);
//     ix_start = ceil((xi_spline - x0) / Deltax);
//     ix_end = ceil((xf_spline - x0) / Deltax) - 1;
//     Deltax_spline = xi_spline - (x0 + ix_start*Deltax);
//     EvalCubicCExpOnConstDeltaxInterval(*cexpvec, coeffs, Deltax_spline, Deltax, ix_start, ix_end);
//   }
//
//   return SUCCESS;
// }
// /* Compute complex exponential of phase on a given spline interval */
// /* Notations: */
// /* x0, .., xn-1 x values evenly spaced with Deltax */
// /* a0, a1, a2, a3 polynomial coeffs of cubic spline on this interval */
// /* delta0 = Deltax_spline = x0-xi_spline, xi_spline start of spline interval */
// /* delta = Deltax constant x-spacing */
// /* ix_start, ix_end bounds for output in cexpvec */
// int EvalCubicCExpOnConstDeltaxInterval(
//   complex_vector* cexpvec,
//   double* coeffs,
//   double Deltax_spline,
//   double Deltax,
//   int ix_start,
//   int ix_end)
// {
//   /* Notations */
//   double d = Deltax;
//   double d0 = Deltax_spline;
//   double a0 = coeffs[1];
//   double a1 = coeffs[2];
//   double a2 = coeffs[3];
//   double a3 = coeffs[4];
//
//   /* Constants and their exponentials */
//   double phibar = a0 + d0 * (a1 + d0 * (a2 + d0 * (a3)));
//   double lambda = d * ((a1 + d0 * (2*a2 + d0 * 3*a3)) + d * ((a2 + 3*a3*d0) + d * a3));
//   double mu = d * (2*a2 + d * (6*a3*d0 + d * 3*a3));
//   double rho = 3*a3*d*d*d;
//   double complex eiphibar = cexp(I * phibar);
//   double complex eilambda = cexp(I * lambda);
//   double complex eimu = cexp(I * mu);
//   double complex eirho = cexp(I * rho);
//   double complex ei2rho = eirho*eirho;
//
//   /* Output indices */
//   int n = ix_end - ix_start + 1;
//   double complex* out = &(cexpvec->data[ix_start]);
//
//   /* Initial values i=0 */
//   double complex eiphi = eiphibar;
//   out[0] = eiphi;
//
//   /* Iteration for i>=1 */
//   double complex factorsigma = 0.;
//   double complex factorrho = 1.;
//   double complex factormu = 1.;
//   double complex factorlambda = eilambda;
//   for (int i=1; i<n; i++) {
//     if (i==1) factorsigma = eirho;
//     else factorsigma = ei2rho * factorsigma;
//     factorrho = factorsigma * factorrho;
//     factormu = eimu * factormu;
//     eiphi = eiphi * factorlambda * factormu * factorrho;
//     out[i] = eiphi;
//   }
//   return SUCCESS;
// }

/* Evaluate cubic polynomial of spline */
/* Note: for splines in matrix form, the first column contains the x values */
/* So the coeffs start at 1 */
//inline double EvalCubic(
// double* coeffs,        /* Pointer to line in spline matrix */
// double x)              /* x value to evaluate, no range checking */
//{
// double eps = x - coeffs[0];
// return coeffs[1] + eps * (coeffs[2] + eps * (coeffs[3] + eps * coeffs[4]));
//}

/* Evaluate quadratic polynomial of spline */
/* Note: for splines in matrix form, the first column contains the x values */
/* So the coeffs start at 1 */
//inline double EvalQuad(
// double* coeffs,       /* Pointer to line in spline matrix */
// double x)              /* x value to evaluate, no range checking */
//{
// double eps = x - coeffs[0];
// return coeffs[1] + eps * (coeffs[2] + eps * coeffs[3]);
//}

// void EvalCAmpPhaseSpline(
//   CAmpPhaseSpline* splines,                    //input
//   CAmpPhaseFrequencySeries* freqseries)  //in/out defines CAmpPhase from defined freqs
// {
//   int ispline=0;
//   //printf("Enter: n=%i\n",freqseries->freq->size);
//   for(int i=0;i<freqseries->freq->size;i++){
//     double f=real_vector_get(freqseries->freq,i);
//
//     /* Adjust the index in the spline if necessary and compute */
//     while(gsl_matrix_get(splines->quadspline_phase, ispline+1, 0)<f)ispline++;
//
//     double eps = f - gsl_matrix_get(splines->quadspline_phase, ispline, 0);
//     double eps2 = eps*eps;
//     double eps3 = eps2*eps;
//     real_vector_view coeffsampreal = gsl_matrix_row(splines->spline_amp_real, ispline);
//     real_vector_view coeffsampimag = gsl_matrix_row(splines->spline_amp_imag, ispline);
//     real_vector_view coeffsphase = gsl_matrix_row(splines->quadspline_phase, ispline);
//     double Ar = EvalCubic(&coeffsampreal.vector, eps, eps2, eps3);
//     double Ai = EvalCubic(&coeffsampimag.vector, eps, eps2, eps3);
//     double Ph = EvalQuad(&coeffsphase.vector, eps, eps2);
//
//     real_vector_set(freqseries->amp_real,i,Ar);
//     real_vector_set(freqseries->amp_imag,i,Ai);
//     real_vector_set(freqseries->phase,i,Ph);
//   }
// };
