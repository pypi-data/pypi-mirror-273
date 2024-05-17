/*
 * Copyright (C) 2019 Sylvain Marsat
 *
 */

#include "tools.h"
#include "spline.h"


/******************************************************************************/
/*  Utility functions */
/******************************************************************************/

/* Convert between mass ratio and symmetric mass ratio */
static UNUSED double qofeta(const double eta)
{
    return (1.0 + sqrt(1.0 - 4.0*eta) - 2.0*eta) / (2.0*eta);
}
static double etaofq(const double q)
{
    return q / ((1.0 + q)*(1.0 + q));
}

/* NOTE: interface changes with respect to similar python functions */
/* Newtonian estimate of the relation between frequency and time */
/* Geometric frequency for a given mass ratio and time to coalescence (t/M) */
static double NewtonianMfoftM(const double q, const double deltatM)
{
  double eta = etaofq(q);
  return 1./PI * pow(256*eta/5.*deltatM, -3./8);
}
/* Frequency (Hz) for a given mass (solar masses), mass ratio */
/* and time to coalescence deltat (in s) */
static double Newtonianfoft(const double M, const double q, const double deltat)
{
  double Ms = M * MTSUN_SI;
  double Mf = NewtonianMfoftM(q, deltat/Ms);
  return Mf / Ms;
}
/* Time to merger (deltat/M) for a given mass ratio */
/* and geometric frequency Mf */
static double NewtoniantMofMf(const double q, const double Mf)
{
  double eta = etaofq(q);
  return 5./256/eta*pow(PI*Mf, -8./3);
}
/* Time to merger (s) for a given mass (solar masses), mass ratio */
/* and frequency f (Hz) */
static double Newtoniantoff(const double M, const double q, const double f)
{
  double Ms = M * MTSUN_SI;
  double deltatM = NewtoniantMofMf(q, Ms*f);
  return deltatM * Ms;
}

/******************************************************************************/
/* Functions for frequency grids */
/******************************************************************************/

/* Build geom frequency grid suitable for waveform amp/phase interpolation */
int BuildWaveformGeomFrequencyGrid(
  real_vector** Mfreq,   /* Output: pointer to real vector */
  const double Mfmin,    /* Starting geometric frequency */
  const double Mfmax,    /* Ending geometric frequency */
  const double eta,      /* Symmetric mass ratio */
  const double acc)      /* Desired phase interpolation error for inspiral */
{
  if (!(Mfmin < Mfmax))
    ERROR(ERROR_EINVAL, "Input Mf limits do not verify Mfmin < Mfmax.");

  /* Inspiral sampling */
  /* Dimensionless number so that DeltaMf = Lambda * Mf^(17/12) */
  /* Factor 3.8 tuned empirically */
  double Lambda = 3.8 * pow(acc * eta, 1./4) * pow(PI, 5./12);

  /* Log sampling */
  /* nptlogmin arbitrary safety, deltalnMfmax tuned empirically */
  int Nptlogmin = 100;
  double DeltalnMfmax = 0.025;
  double DeltalnMf = fmin(DeltalnMfmax, log(Mfmax/Mfmin)/(Nptlogmin - 1));

  /* Transition frequency between the two samplings */
  double Mfstar = pow(DeltalnMf / Lambda, 12./5);
  Mfstar = fmax(fmin(Mfstar, Mfmax), Mfmin);

  /* Number of samples with inspiral sampling */
  int Ninsp = 0;
  double Lambdatilde = 0.;
  if (Mfstar==Mfmin) Ninsp = 1; /* will actually belong to the log part */
  else {
    Ninsp = 1 + ceil(12./5/Lambda * (pow(Mfmin, -5./12) - pow(Mfstar, -5./12)));
    /* Adjust a bit Lambda so that the last point at N_insp-1 is Mfstar */
    Lambdatilde = 12./5/(Ninsp-1) * (pow(Mfmin, -5./12) - pow(Mfstar, -5./12));
  }

  /* Number of samples with log sampling */
  int Nlog = 0;
  double DeltalnMftilde = 0.;
  if (Mfstar==Mfmax) Nlog = 1;
  else {
    Nlog = 1 + ceil(log(Mfmax/Mfstar) / DeltalnMf);
    /* Adjust a bit DeltalnMf so that the number of points is Nlog */
    DeltalnMftilde = log(Mfmax/Mfstar) / (Nlog - 1);
  }

  /* Allocate output */
  /* We will not repeat Mfstar, we set it to belong to the log sampling */
  int Ntot = Ninsp - 1 + Nlog;
  *Mfreq = real_vector_alloc(Ntot);

  /* Fill in values */
  double Mfmin_m512 = pow(Mfmin, -5./12);
  for (int i=0; i<Ninsp-1; i++) { /* exclude Mfstar */
    (*Mfreq)->data[i] = pow(Mfmin_m512 - 5./12*Lambdatilde*i, -12./5);
  }
  (*Mfreq)->data[Ninsp-1] = Mfstar; /* include Mfstar */
  double ratio = exp(DeltalnMftilde);
  for (int i=Ninsp; i<Ntot; i++) {
    (*Mfreq)->data[i] = ratio * (*Mfreq)->data[i-1];
  }

  /* Eliminate rounding errors at both ends */
  (*Mfreq)->data[0] = Mfmin;
  (*Mfreq)->data[Ntot-1] = Mfmax;

  return SUCCESS;
}

/******************************************************************************/

/* Build frequency grid suitable for representing the LISA response */
/* Default in pyFDresponse : */
/* nptlogmin=150, Deltat_max=0.02083335, Deltaf_max=0.001 */
int BuildResponseFrequencyGrid(
  real_vector** freq,       /* Output: pointer to real vector */
  real_matrix* tfspline,    /* Spline matrix for tf */
  const double f_min,       /* Minimal frequency */
  const double f_max,       /* Maximal frequency */
  const double Deltat_max,  /* Maximal time step, in years */
  const double Deltaf_max,  /* Maximal frequency step, in Hz */
  const int nptlogmin)      /* Minimal number of points with log-spacing */
{
  /* Check frequency bounds */
  if (!(f_min < f_max))
      ERROR(ERROR_EINVAL, "Input freq limits do not verify f_min < f_max.");

  /* Check input pointers */
  if (*freq != NULL)
      ERROR(ERROR_EFAULT, "Input pointer for frequencies is not NULL.");
  if (tfspline == NULL)
      ERROR(ERROR_EFAULT, "Input pointer for spline is NULL.");

  /* Frequency limits in the input spline for tf */
  int n = (int) tfspline->size1;
  double f_min_tf = real_matrix_get(tfspline, 0, 0);
  double f_max_tf = real_matrix_get(tfspline, n-1, 0);

  /* Combining with input frequency limits */
  double f_min_r = fmax(f_min, f_min_tf);
  double f_max_r = fmin(f_max, f_max_tf);

  /* Sampling target for log, defined by a minimal number of samples */
  double Deltalnf_max = log(f_max_r/f_min_r)/(nptlogmin - 1.);

  /* Keep monotonous part of tf and build reciprocal spline for f(t) */
  int index_cuttf = 0;
  while (index_cuttf<n-1 && real_matrix_get(tfspline, index_cuttf+1, 1)
         - real_matrix_get(tfspline, index_cuttf, 1)>0) index_cuttf++;
  int n_foft = index_cuttf+1;
  real_vector* tdata = real_vector_alloc(n_foft);
  real_vector* fdata = real_vector_alloc(n_foft);
  for (int i=0; i<n_foft; i++) {
    real_vector_set(fdata, i, real_matrix_get(tfspline, i, 0));
    real_vector_set(tdata, i, real_matrix_get(tfspline, i, 1));
  }
  real_matrix* foftspline = NULL;
  BuildNotAKnotSpline(&foftspline, tdata, fdata);

  /* Initialize temporary working space with upper bound on number of points */
  size_t i_slide = 0;
  double tf_fmin = 0.;
  double tf_fmax = 0.;
  EvalCubicSplineSlide(&tf_fmin, tfspline, &i_slide, f_min_r);
  EvalCubicSplineSlide(&tf_fmax, tfspline, &i_slide, f_max_r);
  size_t n_f_bound = (size_t) (nptlogmin
                          + ceil((tf_fmax - tf_fmin) / (Deltat_max * YRSID_SI))
                          + ceil((f_max_r-f_min_r) / Deltaf_max));
  real_vector* freq_v = real_vector_alloc(n_f_bound);

  /* Will be used to ensure the last point is not too close to fmax */
  /* which poses problems for splines (derivatives become meaningless) */
  double minsteptofmax = 1e-5 * f_max_r;

  /* Iteratively appending frequencies for combined criteria */
  double* freq_data = freq_v->data;
  double f = 0.;
  double f_append = 0.;
  double tf_new = 0.;
  double tf_min = real_vector_get(tdata, 0);
  double tf_max = real_vector_get(tdata, n_foft-1);
  size_t i_f = 0;
  size_t i_slide_foft = 0;
  i_slide = 0;
  double Deltaf_time = 0.;
  double Deltaf = 0.;
  freq_data[0] = f_min_r;
  while (i_f<n_f_bound && freq_data[i_f]<f_max_r) {
    f = freq_data[i_f];
    EvalCubicSplineSlide(&tf_new, tfspline, &i_slide, f) + Deltat_max*YRSID_SI;
    if (tf_min<=tf_new && tf_new<=tf_max) {
      EvalCubicSplineSlide(&Deltaf_time, foftspline, &i_slide_foft, tf_new);
    }
    else {
      Deltaf_time = f_max_r - f;
    }
    Deltaf = fmin(fmin(Deltaf_max, f * Deltalnf_max), Deltaf_time);
    if (f+Deltaf<f_max_r && f+Deltaf>f_max_r-minsteptofmax) {
      f_append = f_max_r;
    }
    else {
      f_append = fmin(f_max_r, f+Deltaf);
    }

    i_f++;
    if (i_f>=n_f_bound)
        ERROR(ERROR_EINVAL, "Index exceeds n_f_bound.\n");
    freq_data[i_f] = f_append;
  }

  /* Resize output */
  *freq = real_vector_resize(freq_v, 0, i_f);

  /* Cleanup */
  real_vector_free(freq_v);
  real_vector_free(fdata);
  real_vector_free(tdata);
  real_matrix_free(foftspline);

  return SUCCESS;
}

/******************************************************************************/

/* Build frequency grid suitable for both the waveform and the response */
/* Combines criteria: */
/* Max deltat (using approximate leading-order Newtonian tN(f) */
/* Max deltaf */
/* Max deltalnf */
/* Max deltalnMf */
/* Adapted sampling for inspiral regime */
/* Default in pyFDresponse : */
/* nptlogmin=150, Deltat_max=0.02083335, Deltaf_max=0.001 */
int BuildFrequencyGrid(
  real_vector** freq,          /* Output: pointer to real vector */
  const double f_min,          /* Minimal frequency (Hz) */
  const double f_max,          /* Maximal frequency (Hz) */
  const double M,              /* Total mass (solar masses) */
  const double q,              /* Symmetric mass ratio */
  const double Deltat_max,     /* Maximal time step, in years */
  const double Deltaf_max,     /* Maximal frequency step, in Hz */
  const double DeltalnMf_max,  /* Maximal ln(Mf) step */
  const double acc,            /* Target phase interpolation error (inspiral) */
  const int nptlogmin)         /* Minimal number of points with log-spacing */
{

  /* Check frequency bounds */
  if (!(f_min < f_max))
      ERROR(ERROR_EINVAL, "Input freq limits do not verify f_min < f_max.");

  /* Check input pointer */
  if (*freq != NULL)
      ERROR(ERROR_EFAULT, "Input pointer for frequencies is not NULL.");

  /* Geometric frequency bounds, time step in seconds */
  double eta = etaofq(q);
  double Ms = M * MTSUN_SI;
  double Mfmin = Ms * f_min;
  double Mfmax = Ms * f_max;
  double Deltat_max_s = Deltat_max * YRSID_SI;

  /* Inspiral sampling */
  /* Dimensionless number so that DeltaMf = Lambda * Mf^(17/12) */
  /* Factor 3.8 tuned empirically */
  double Lambda = 3.8 * pow(acc * eta, 1./4) * pow(PI, 5./12);
  size_t N_sampling_inspiral = (size_t)
           ceil(1 + 12/5./Lambda * (pow(Mfmin, -5./12) - pow(Mfmax, -5./12)));

  /* Log sampling */
  /* nptlogmin arbitrary safety, deltalnMfmax tuned empirically */
  double DeltalnMf = fmin(DeltalnMf_max, log(Mfmax/Mfmin)/(nptlogmin - 1));

  /* Initialize temporary working space with upper bound on number of points */
  /* NOTE: mind the minus sign in tN, Newtoniantoff is the time to merger > 0 */
  double tfN_fmin = -Newtoniantoff(M, q, f_min);
  double tfN_fmax = -Newtoniantoff(M, q, f_max);
  size_t N_f_bound = (size_t) (N_sampling_inspiral
                       + ceil(log(Mfmax/Mfmin) / DeltalnMf)
                       + ceil((tfN_fmax - tfN_fmin) / Deltat_max_s)
                       + ceil((f_max - f_min) / Deltaf_max));
  real_vector* freq_v = real_vector_alloc(N_f_bound);

  /* Will be used to ensure the last point is not too close to fmax */
  /* which poses problems for splines (derivatives become meaningless) */
  double minsteptofmax = 1e-5 * f_max;

  /* Loop to file in values based on the smallest Deltaf */
  /* NOTE: mind the minus sign in tN, Newtoniantoff is the time to merger > 0 */
  size_t i_f = 0;
  double* freq_data = freq_v->data;
  freq_data[0] = f_min;
  double tN = 0., f = 0., Deltaf = 0., f_append = 0.;
  double Deltaf_time = 0., Deltaf_inspiral = 0.;
  while (i_f<N_f_bound && freq_data[i_f]<f_max) {
    f = freq_data[i_f];
    tN = -Newtoniantoff(M, q, f);
    Deltaf_time = Newtonianfoft(M, q, -(tN + Deltat_max_s)) - f;
    Deltaf_inspiral = 1./Ms * Lambda * pow(Ms * f, 17./12);
    Deltaf = fmin(fmin(fmin(Deltaf_max, f * DeltalnMf), Deltaf_time),
                  Deltaf_inspiral);
    if (f+Deltaf<f_max && f+Deltaf>f_max-minsteptofmax) {
      f_append = f_max;
    }
    else {
      f_append = fmin(f_max, f+Deltaf);
    }

    i_f++;
    if (i_f>=N_f_bound)
        ERROR(ERROR_EINVAL, "Index exceeds N_f_bound.\n");
    freq_data[i_f] = f_append;
  }

  /* Resize output */
  *freq = real_vector_resize(freq_v, 0, i_f);

  /* Cleanup */
  real_vector_free(freq_v);

  return SUCCESS;
}

/******************************************************************************/
/* Function for merging two monotonously increasing grids */
/******************************************************************************/

/* Merge two grids with increasing values (e.g. two frequency grids) */
/* Discards duplicate values */
/* Allows for safeguarding: can ignore points that are almost identical */
/* Two criterion available: absolute deltax or relative deltalnx */
/* NOTE: deltalnx criterion only allowed for positive values of x */
int BuildMergedGrid(
    real_vector** grid,      /* Output: merged grid */
    real_vector* grid1,      /* Input: grid1 */
    real_vector* grid2,      /* Input: grid2 */
    const int usedeltaxmin,        /* Flag to use a minimal deltax criterion */
    const double deltaxmin,        /* Value of minimal deltax criterion */
    const int usedeltalnxmin,      /* Flag to use a minimal deltalnx criterion */
    const double deltalnxmin       /* Value of minimal deltalnx criterion */
)
{
  /* Check pointers */
  if (*grid != NULL)
      ERROR(ERROR_EFAULT, "Output pointer is not NULL.");
  if (grid1 == NULL || grid2 == NULL)
      ERROR(ERROR_EFAULT, "Input pointer for grid1 or grid2 is NULL.");

  /* Length, alloc temporary vector to the max possible needed size */
  size_t n1 = grid1->size;
  size_t n2 = grid2->size;
  real_vector* tempgrid = real_vector_alloc(n1 + n2);

  /* Min x values */
  double minx1 = real_vector_get(grid1, 0);
  double minx2 = real_vector_get(grid2, 0);
  double minx = fmin(minx1, minx2);

  /* For the relative step criterion */
  double ratioxmin = 0.;
  if (usedeltalnxmin) ratioxmin = exp(deltalnxmin);

  /* Loop to fill output frequencies */
  /* At this stage, allow duplicates and do not apply spacing requirements */
  /* All the n1+n2 values will be filled */
  size_t i1 = 0;
  size_t i2 = 0;
  double* data = tempgrid->data;
  double* data1 = grid1->data;
  double* data2 = grid2->data;
  double x1 = data1[i1];
  double x2 = data2[i2];
  data[0] = minx;
  for (size_t i=1; i<n1+n2; i++) {
    if (i1 > n1-1 && i2 > n2-1) break;
    else if (i1 > n1-1) {
      data[i] = x2;
      i2++;
      if (i2 < n2) x2 = data2[i2];
    }
    else if (i2 > n2-1) {
      data[i] = x1;
      i1++;
      if (i1 < n1) x1 = data1[i1];
    }
    else {
      if (x1 < x2) {
        data[i] = x1;
        i1++;
        if (i1 < n1) x1 = data1[i1];
      }
      else { /* NOTE: at this stage, we allow duplicates */
        data[i] = x2;
        i2++;
        if (i2 < n2) x2 = data2[i2];
      }
    }
  }

  /* Eliminate duplicates and apply spacing requirements -- done in-place */
  int* mask = malloc((n1+n2) * sizeof(int));
  memset(mask, 0, (n1+n2) * sizeof(int));
  double x = 0.;
  int passduplicate = 0;
  int passdeltax = 0;
  int passdeltalnx = 0;
  mask[0] = 1;
  size_t nout = 1;
  double oldx = data[0];
  for (size_t i=1; i<n1+n2; i++) {
    oldx = data[i-1];
    x = data[i];
    if ( x < oldx )
      ERROR(ERROR_EINVAL, "Found strictly decreasing value of x");
    if ( usedeltaxmin && x<0 )
      ERROR(ERROR_EINVAL, "Cannot do usedeltalnxmin with negative values of x");
    passduplicate = ( x > oldx );
    passdeltax = (!usedeltaxmin || (usedeltaxmin && (x>=oldx+deltaxmin)));
    passdeltalnx = (!usedeltalnxmin ||
                    (usedeltalnxmin && (x>=oldx*(1.+ratioxmin))));
    if (passduplicate && passdeltax && passdeltalnx) {
      mask[i] = 1;
      nout++;
    }
  }

  /* Allocate output and copy data */
  *grid = real_vector_alloc(nout);
  size_t iout = 0;
  double* griddata = (*grid)->data;
  for (size_t i=0; i<n1+n2; i++) {
    if ( mask[i] ) {
      griddata[iout] = data[i];
      iout++;
    }
  }

  /* Cleanup */
  free(tempgrid);
  free(mask);

  return SUCCESS;
}

/******************************************************************************/
/* Helper function for residuals likelihood */
/******************************************************************************/

double LinearInterpMultiMode3ChannelsResidualNorm(
  complex_array_3d* alpha0,
  complex_array_3d* alpha1,
  complex_array_3d* w0,
  complex_array_3d* w1,
  complex_array_3d* w2)
{
  /* TODO: check dimensions are consistent ? */
  int ngrid = (int) alpha0->size1;
  int nmodes = (int) alpha0->size2;
  int nchan = (int) alpha0->size3;

  double complex wijk = 0.;
  double complex alphaik = 0.;
  double complex alphajk = 0.;
  double complex alpha_fac = 0.;

  double complex res = 0.;

  /* Term u^0 */
  for (int k=0; k<ngrid; k++) {
    for (int i=0; i<nmodes; i++) {
      for (int j=0; j<nmodes; j++) {
        wijk = complex_array_3d_get(w0, k, i, j);
        alpha_fac = 0.;
        for (int chan=0; chan<nchan; chan++) {
          alphaik = complex_array_3d_get(alpha0, k, i, chan);
          alphajk = complex_array_3d_get(alpha0, k, j, chan);
          alpha_fac += alphaik * conj(alphajk);
        }
        res += alpha_fac * wijk;
      }
    }
  }

  /* Term u^1 */
  /* factor 2 coming from alpha0*alpha1 + alpha1*alpha0 -> 2Re(alpha0*alpha1) */
  for (int k=0; k<ngrid; k++) {
    for (int i=0; i<nmodes; i++) {
      for (int j=0; j<nmodes; j++) {
        wijk = complex_array_3d_get(w1, k, i, j);
        alpha_fac = 0.;
        for (int chan=0; chan<nchan; chan++) {
          alphaik = complex_array_3d_get(alpha0, k, i, chan);
          alphajk = complex_array_3d_get(alpha1, k, j, chan);
          alpha_fac += alphaik * conj(alphajk);
        }
        res += 2 * alpha_fac * wijk;
      }
    }
  }

  /* Term u^2 */
  for (int k=0; k<ngrid; k++) {
    for (int i=0; i<nmodes; i++) {
      for (int j=0; j<nmodes; j++) {
        wijk = complex_array_3d_get(w2, k, i, j);
        alpha_fac = 0.;
        for (int chan=0; chan<nchan; chan++) {
          alphaik = complex_array_3d_get(alpha1, k, i, chan);
          alphajk = complex_array_3d_get(alpha1, k, j, chan);
          alpha_fac += alphaik * conj(alphajk);
        }
        res += alpha_fac * wijk;
      }
    }
  }

  /* Return real part, include factor 4 */
  return creal(4*res);
}

/******************************************************************************/
/* Functions for Spin weighted spherical harmonics */
/******************************************************************************/

/* Function reproducing XLALSpinWeightedSphericalHarmonic */
/* Currently only supports s=-2, l=2,3,4,5 modes */
double complex SpinWeightedSphericalHarmonic(
  double theta,
  double phi,
  int s,
  int l,
  int m)
{
  double fac;
  double complex ans;

  /* sanity checks ... */
  if ( l < abs(s) )
      ERROR(ERROR_EINVAL, "Invalid mode s=%d, l=%d, m=%d - require |s| <= l",
            s, l, m);
  if ( l < abs(m) )
      ERROR(ERROR_EINVAL, "Invalid mode s=%d, l=%d, m=%d - require |m| <= l",
            s, l, m);


  if ( s != -2 )
      ERROR(ERROR_EINVAL, "Unsupported mode s=%d (only s=-2 implemented)", s);

  /* l = 2 */
  if ( l == 2 ) {
      switch ( m ) {
      case -2:
	fac = sqrt( 5.0 / ( 64.0 * PI ) ) * ( 1.0 - cos( theta ))*( 1.0 - cos( theta ));
	break;
      case -1:
	fac = sqrt( 5.0 / ( 16.0 * PI ) ) * sin( theta )*( 1.0 - cos( theta ));
	break;

      case 0:
	fac = sqrt( 15.0 / ( 32.0 * PI ) ) * sin( theta )*sin( theta );
	break;

      case 1:
	fac = sqrt( 5.0 / ( 16.0 * PI ) ) * sin( theta )*( 1.0 + cos( theta ));
	break;

      case 2:
	fac = sqrt( 5.0 / ( 64.0 * PI ) ) * ( 1.0 + cos( theta ))*( 1.0 + cos( theta ));
	break;
      default:
  ERROR(ERROR_EINVAL, "Invalid mode s=%d, l=%d, m=%d - require |m| <= l",
        s, l, m);
	break;
      }
  }
  /* l = 3 */
  else if ( l == 3 ) {
      switch ( m ) {
      case -3:
	fac = sqrt(21.0/(2.0*PI))*cos(theta/2.0)*pow(sin(theta/2.0),5.0);
	break;
      case -2:
	fac = sqrt(7.0/(4.0*PI))*(2.0 + 3.0*cos(theta))*pow(sin(theta/2.0),4.0);
	break;
      case -1:
	fac = sqrt(35.0/(2.0*PI))*(sin(theta) + 4.0*sin(2.0*theta) - 3.0*sin(3.0*theta))/32.0;
	break;
      case 0:
	fac = (sqrt(105.0/(2.0*PI))*cos(theta)*pow(sin(theta),2.0))/4.0;
	break;
      case 1:
	fac = -sqrt(35.0/(2.0*PI))*(sin(theta) - 4.0*sin(2.0*theta) - 3.0*sin(3.0*theta))/32.0;
	break;

      case 2:
	fac = sqrt(7.0/PI)*pow(cos(theta/2.0),4.0)*(-2.0 + 3.0*cos(theta))/2.0;
	break;

      case 3:
	fac = -sqrt(21.0/(2.0*PI))*pow(cos(theta/2.0),5.0)*sin(theta/2.0);
	break;

      default:
	ERROR(ERROR_EINVAL, "Invalid mode s=%d, l=%d, m=%d - require |m| <= l",
        s, l, m);
	break;
      }
  }
  /* l = 4 */
  else if ( l == 4 ) {
      switch ( m ) {
      case -4:
	fac = 3.0*sqrt(7.0/PI)*pow(cos(theta/2.0),2.0)*pow(sin(theta/2.0),6.0);
	break;
      case -3:
	fac = 3.0*sqrt(7.0/(2.0*PI))*cos(theta/2.0)*(1.0 + 2.0*cos(theta))*pow(sin(theta/2.0),5.0);
	break;

      case -2:
	fac = (3.0*(9.0 + 14.0*cos(theta) + 7.0*cos(2.0*theta))*pow(sin(theta/2.0),4.0))/(4.0*sqrt(PI));
	break;
      case -1:
	fac = (3.0*(3.0*sin(theta) + 2.0*sin(2.0*theta) + 7.0*sin(3.0*theta) - 7.0*sin(4.0*theta)))/(32.0*sqrt(2.0*PI));
	break;
      case 0:
	fac = (3.0*sqrt(5.0/(2.0*PI))*(5.0 + 7.0*cos(2.0*theta))*pow(sin(theta),2.0))/16.0;
	break;
      case 1:
	fac = (3.0*(3.0*sin(theta) - 2.0*sin(2.0*theta) + 7.0*sin(3.0*theta) + 7.0*sin(4.0*theta)))/(32.0*sqrt(2.0*PI));
	break;
      case 2:
	fac = (3.0*pow(cos(theta/2.0),4.0)*(9.0 - 14.0*cos(theta) + 7.0*cos(2.0*theta)))/(4.0*sqrt(PI));
	break;
      case 3:
	fac = -3.0*sqrt(7.0/(2.0*PI))*pow(cos(theta/2.0),5.0)*(-1.0 + 2.0*cos(theta))*sin(theta/2.0);
	break;
      case 4:
	fac = 3.0*sqrt(7.0/PI)*pow(cos(theta/2.0),6.0)*pow(sin(theta/2.0),2.0);
	break;
      default:
	ERROR(ERROR_EINVAL, "Invalid mode s=%d, l=%d, m=%d - require |m| <= l",
        s, l, m);
	break;
      }
  }
  /* l==5 */
  else if ( l == 5 ) {
      switch ( m ) {
      case -5:
	fac = sqrt(330.0/PI)*pow(cos(theta/2.0),3.0)*pow(sin(theta/2.0),7.0);
	break;
      case -4:
	fac = sqrt(33.0/PI)*pow(cos(theta/2.0),2.0)*(2.0 + 5.0*cos(theta))*pow(sin(theta/2.0),6.0);
	break;
      case -3:
	fac = (sqrt(33.0/(2.0*PI))*cos(theta/2.0)*(17.0 + 24.0*cos(theta) + 15.0*cos(2.0*theta))*pow(sin(theta/2.0),5.0))/4.0;
	break;
      case -2:
	fac = (sqrt(11.0/PI)*(32.0 + 57.0*cos(theta) + 36.0*cos(2.0*theta) + 15.0*cos(3.0*theta))*pow(sin(theta/2.0),4.0))/8.0;
	break;
      case -1:
	fac = (sqrt(77.0/PI)*(2.0*sin(theta) + 8.0*sin(2.0*theta) + 3.0*sin(3.0*theta) + 12.0*sin(4.0*theta) - 15.0*sin(5.0*theta)))/256.0;
	break;
      case 0:
	fac = (sqrt(1155.0/(2.0*PI))*(5.0*cos(theta) + 3.0*cos(3.0*theta))*pow(sin(theta),2.0))/32.0;
	break;
      case 1:
	fac = sqrt(77.0/PI)*(-2.0*sin(theta) + 8.0*sin(2.0*theta) - 3.0*sin(3.0*theta) + 12.0*sin(4.0*theta) + 15.0*sin(5.0*theta))/256.0;
	break;
      case 2:
	fac = sqrt(11.0/PI)*pow(cos(theta/2.0),4.0)*(-32.0 + 57.0*cos(theta) - 36.0*cos(2.0*theta) + 15.0*cos(3.0*theta))/8.0;
	break;
      case 3:
	fac = -sqrt(33.0/(2.0*PI))*pow(cos(theta/2.0),5.0)*(17.0 - 24.0*cos(theta) + 15.0*cos(2.0*theta))*sin(theta/2.0)/4.0;
	break;
      case 4:
	fac = sqrt(33.0/PI)*pow(cos(theta/2.0),6.0)*(-2.0 + 5.0*cos(theta))*pow(sin(theta/2.0),2.0);
	break;
      case 5:
	fac = -sqrt(330.0/PI)*pow(cos(theta/2.0),7.0)*pow(sin(theta/2.0),3.0);
	break;
      default:
	ERROR(ERROR_EINVAL, "Invalid mode s=%d, l=%d, m=%d - require |m| <= l",
        s, l, m);
	break;
      }
  }
  else
      ERROR(ERROR_EINVAL, "Unsupported mode l=%d (only l in [2,5] implemented)",
            l);

  if (m)
    ans = fac*cexp(I*m*phi);
  else
    ans = fac;
  return ans;
}
