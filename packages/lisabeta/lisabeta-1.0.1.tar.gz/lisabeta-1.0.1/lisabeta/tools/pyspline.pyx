#
# Copyright (C) 2019 Sylvain Marsat.
#
#


"""
    Cython wrapping of C spline interpolation tools.
"""

import numpy as np
cimport numpy as np

from lisabeta.pyconstants cimport *
from lisabeta.struct.pystruct cimport *


cdef class CubicSpline:
    """ Cubic spline with the not-a-knot boundary condition, as a matrix.
    """

    cdef real_matrix* Cspline   # pointer to C spline matrix
    cdef real_matrix* Cspline_d # pointer to C spline derivative matrix
    cdef real_matrix* Cspline_dd # pointer to C spline double derivative matrix
    cdef real_matrix* Cspline_int # pointer to C spline integral matrix
    cdef real_vector* Cx        # pointer to C x vector
    cdef real_vector* Cy        # pointer to C y vector
    cdef x, y                   # input numpy arrays
    cdef spline                 # numpy array for spline matrix
    cdef spline_d               # numpy array for spline derivative matrix
    cdef spline_dd              # numpy array for spline double derivative matrix
    cdef spline_int             # numpy array for spline integral matrix (4th order)


    def __init__(self,
                 np.ndarray[np.float_t, ndim=1] x,
                 np.ndarray[np.float_t, ndim=1] y):
        """Constructor
        Args:
          x                     # Input 1D numpy array with x values
          y                     # Input 1D numpy array with y values
        Keyword args:
          None
        """
        self.x = x
        self.y = y

        self.Cspline = NULL
        self.Cspline_d = NULL
        self.Cspline_dd = NULL
        self.Cspline_int = NULL
        cdef double val

        # If the input is an empty array, init to empty array and stop there
        # NOTE: __init__ is required to return nothing
        if len(x)==0 or len(y)==0:
            self.spline = np.empty((0,0), dtype=float)
            return

        # Build a real_vector representation of the input numpy arrays
        if not x.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array x is not C_CONTIGUOUS')
        if not y.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array y is not C_CONTIGUOUS')
        cdef double* x_data = <double *> &x[0]
        cdef double* y_data = <double *> &y[0]
        self.Cx = real_vector_view(x_data, x.shape[0])
        self.Cy = real_vector_view(y_data, y.shape[0])

        if len(x)>3:
            ret = BuildNotAKnotSpline(
                &self.Cspline,
                self.Cx,
                self.Cy,
            );
            if ret == _FAILURE:
                raise ValueError("Call to BuildNotAKnotSpline() failed.")
        else:
            #Cannot BuildNotAKnotSpline for n<4
            #Instead we build a QuadSpline and use its coefficients
            quadspline=QuadSpline(x,y).get_spline()

            self.Cspline=real_matrix_alloc(len(x),5)
            for i in range(len(x)): #Not very optimized, but <16 array elems
                for j in range(5):
                    if j<4:
                        val=quadspline[i,j]
                    else:val=0
                    self.Cspline.data[i * 5 + j] = val

        # Cast C double array to numpy via a MemoryView
        cdef int m = self.Cspline.size1
        cdef int n = self.Cspline.size2
        cdef double[::1] view_Cspline = \
          <(double)[:(m * n)]> self.Cspline.data
        self.spline = np.reshape(np.asarray(view_Cspline), (m, n))
        #self.spline = real_matrix_to_np_array(self.Cspline)

    def __dealloc__(self):
        """Destructor
        """
        if self.Cspline != NULL:
            real_matrix_free(self.Cspline)
        if self.Cspline_d != NULL:
            real_matrix_free(self.Cspline_d)
        if self.Cspline_dd != NULL:
            real_matrix_free(self.Cspline_dd)
        if self.Cspline_int != NULL:
            real_matrix_free(self.Cspline_int)
        if self.Cx != NULL:
            real_vector_view_free(self.Cx)
        if self.Cy != NULL:
            real_vector_view_free(self.Cy)

    def get_spline(self):
        return np.copy(self.spline)

    def get_spline_d(self):

        # If the spline is an empty array (or len=1 where deriv is undefined), return empty array and stop there
        # NOTE: __init__ is required to return nothing
        if len(self.spline)==0 or len(self.x)<2:
            return np.empty((0,0), dtype=float)

        if self.Cspline_d == NULL:
            ret = CubicSplineDerivative(
                &self.Cspline_d,
                self.Cspline
            );
            if ret == _FAILURE:
                raise ValueError("Call to CubicSplineDerivative() failed.")

        # Cast C double array to numpy via a MemoryView
        #self.spline_d = real_matrix_to_np_array(self.Cspline_d)
        cdef int m = self.Cspline_d.size1
        cdef int n = self.Cspline_d.size2
        cdef double[::1] view_Cspline_d = \
          <(double)[:(m * n)]> self.Cspline_d.data
        self.spline_d = np.reshape(np.asarray(view_Cspline_d), (m, n))

        return np.copy(self.spline_d)

    def get_spline_dd(self):

        # If the spline is an empty array, return empty array and stop there
        # NOTE: __init__ is required to return nothing
        if len(self.spline)==0:
            return np.empty((0,0), dtype=float)

        if self.Cspline_dd == NULL:
            ret = CubicSplineDoubleDerivative(
                &self.Cspline_dd,
                self.Cspline
            );
            if ret == _FAILURE:
                raise ValueError("Call to CubicSplineDerivative() failed.")

        # Cast C double array to numpy via a MemoryView
        #self.spline_d = real_matrix_to_np_array(self.Cspline_d)
        cdef int m = self.Cspline_dd.size1
        cdef int n = self.Cspline_dd.size2
        cdef double[::1] view_Cspline_dd = \
          <(double)[:(m * n)]> self.Cspline_dd.data
        self.spline_dd = np.reshape(np.asarray(view_Cspline_dd), (m, n))

        return np.copy(self.spline_dd)

    def get_spline_int(self):

        # If the spline is an empty array, return empty array and stop there
        # NOTE: __init__ is required to return nothing
        if len(self.spline)==0:
            return np.empty((0,0), dtype=float)

        if self.Cspline_int == NULL:
            ret = CubicSplineIntegral(
                &self.Cspline_int,
                self.Cspline
            );
            if ret == _FAILURE:
                raise ValueError("Call to CubicSplineDerivative() failed.")

        # Cast C double array to numpy via a MemoryView
        #self.spline_int = real_matrix_to_np_array(self.Cspline_int)
        cdef int m = self.Cspline_int.size1
        cdef int n = self.Cspline_int.size2
        cdef double[::1] view_Cspline_int = \
          <(double)[:(m * n)]> self.Cspline_int.data
        self.spline_int = np.reshape(np.asarray(view_Cspline_int), (m, n))

        return np.copy(self.spline_int)

cdef class QuadSpline:
    """ Quadratic spline, as a matrix.
    """

    cdef real_matrix* Cspline   # pointer to C spline matrix
    cdef real_matrix* Cspline_d # pointer to C spline derivative matrix
    # cdef real_matrix* Cspline_int # pointer to C spline integral matrix
    cdef real_vector* Cx        # pointer to C x vector
    cdef real_vector* Cy        # pointer to C y vector
    cdef x, y                   # input numpy arrays
    cdef spline                 # numpy array for spline matrix
    cdef spline_d               # numpy array for spline derivative matrix
    cdef spline_int             # numpy array for spline integral matrix (4th order)


    def __init__(self,
                 np.ndarray[np.float_t, ndim=1] x,
                 np.ndarray[np.float_t, ndim=1] y):
        """Constructor
        Args:
          x                     # Input 1D numpy array with x values
          y                     # Input 1D numpy array with y values
        Keyword args:
          None
        """
        self.x = x
        self.y = y

        self.Cspline = NULL
        self.Cspline_d = NULL
        cdef double slope

        # self.Cspline_int = NULL

        # If the input is an empty array, init to empty array and stop there
        # NOTE: __init__ is required to return nothing
        if len(x)==0 or len(y)==0:
            self.spline = np.empty((0,0), dtype=float)
            return

        # Build a real_vector representation of the input numpy arrays
        if not x.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array x is not C_CONTIGUOUS')
        if not y.flags['C_CONTIGUOUS']:
            raise ValueError('Input numpy array y is not C_CONTIGUOUS')
        cdef double* x_data = <double *> &x[0]
        cdef double* y_data = <double *> &y[0]
        self.Cx = real_vector_view(x_data, x.shape[0])
        self.Cy = real_vector_view(y_data, y.shape[0])

        if len(x)>2:
            ret = BuildQuadSpline(
                &self.Cspline,
                self.Cx,
                self.Cy,
            );
            if ret == _FAILURE:
                raise ValueError("Call to BuildNotAKnotSpline() failed.")
        else:
            #Cannot QuadSpline for n<3
            #Instead we set coefficients for linear interpolation, or constant
            slope=0;
            if len(x)>1: slope=(y_data[1]-y_data[0])/(x_data[1]-x_data[0])
            self.Cspline=real_matrix_alloc(len(x),4)
            for i in range(len(x)): #Not very optimized, but <16 array elems
                self.Cspline.data[i * 4 + 0] = x_data[i]
                self.Cspline.data[i * 4 + 1] = y_data[i]
                self.Cspline.data[i * 4 + 2] = slope
                self.Cspline.data[i * 4 + 3] = 0

        # Cast C double array to numpy via a MemoryView
        cdef int m = self.Cspline.size1
        cdef int n = self.Cspline.size2
        cdef double[::1] view_Cspline = \
          <(double)[:(m * n)]> self.Cspline.data
        self.spline = np.reshape(np.asarray(view_Cspline), (m, n))
        #self.spline = real_matrix_to_np_array(self.Cspline)

    def __dealloc__(self):
        """Destructor
        """
        if self.Cspline != NULL:
            real_matrix_free(self.Cspline)
        if self.Cspline_d != NULL:
            real_matrix_free(self.Cspline_d)
        # if self.Cspline_int != NULL:
        #     real_matrix_free(self.Cspline_int)
        if self.Cx != NULL:
            real_vector_view_free(self.Cx)
        if self.Cy != NULL:
            real_vector_view_free(self.Cy)

    def get_spline(self):
        return np.copy(self.spline)

    def get_spline_d(self):

        # If the spline is an empty array (or len=1 where deriv is undefined), return empty array and stop there
        # NOTE: __init__ is required to return nothing
        if len(self.spline)==0 or len(self.x)<2:
            return np.empty((0,0), dtype=float)

        if self.Cspline_d == NULL:
            ret = QuadSplineDerivative(
                &self.Cspline_d,
                self.Cspline
            );
            if ret == _FAILURE:
                raise ValueError("Call to CubicSplineDerivative() failed.")

        # Cast C double array to numpy via a MemoryView
        #self.spline_d = real_matrix_to_np_array(self.Cspline_d)
        cdef int m = self.Cspline_d.size1
        cdef int n = self.Cspline_d.size2
        cdef double[::1] view_Cspline_d = \
          <(double)[:(m * n)]> self.Cspline_d.data
        self.spline_d = np.reshape(np.asarray(view_Cspline_d), (m, n))

        return np.copy(self.spline_d)

    # def get_spline_int(self):
    #
    #     if self.Cspline_int == NULL:
    #         ret = CubicSplineIntegral(
    #             &self.Cspline_int,
    #             self.Cspline
    #         );
    #         if ret == _FAILURE:
    #             raise ValueError("Call to CubicSplineDerivative() failed.")
    #
    #     # Cast C double array to numpy via a MemoryView
    #     #self.spline_int = real_matrix_to_np_array(self.Cspline_int)
    #     cdef int m = self.Cspline_int.size1
    #     cdef int n = self.Cspline_int.size2
    #     cdef double[::1] view_Cspline_int = \
    #       <(double)[:(m * n)]> self.Cspline_int.data
    #     self.spline_int = np.reshape(np.asarray(view_Cspline_int), (m, n))
    #
    #     return np.copy(self.spline_int)

def spline_eval_vector(np.ndarray[np.float_t, ndim=2] spline,
                       np.ndarray[np.float_t, ndim=1] xvec,
                       extrapol_zero=False):

    # If the input is an empty array, return empty array and stop there
    # NOTE: __init__ is required to return nothing
    if len(spline)==0 or len(xvec)==0:
        return np.empty(0, dtype=float)

    # Build real_vector representation of input numpy array for x
    cdef double* xvec_data = <double *> &xvec[0]
    Cxvec = real_vector_view(xvec_data, xvec.shape[0])

    # Build real_matrix representation of input numpy array for spline
    if not spline.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array spline is not C_CONTIGUOUS.')
    if not spline.shape[1] == 5:
        raise ValueError(
        'Input array for spline has dimensions (%d, %d) instead of (n,5)',
        spline.shape[0], spline.shape[1])
    if not xvec.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array xvec is not C_CONTIGUOUS')
    cdef real_matrix* Cspline = NULL
    cdef double* spline_data = <double *> &spline[0,0]
    Cspline = real_matrix_view(spline_data,
                               spline.shape[0], spline.shape[1])

    cdef real_vector* Cyvec = NULL
    ret = EvalCubicSplineOnVector(
        &Cyvec,
        Cxvec,
        Cspline,
        extrapol_zero
    );
    if ret == _FAILURE:
        raise ValueError("Call to EvalCubicSplineOnVector() failed.")

    # Cast C double array to numpy via a MemoryView
    # NOTE: np.copy to return an array independent of C allocated memory
    cdef int n = Cyvec.size
    cdef double[::1] view_Cyvec = <(double)[:n]> Cyvec.data
    yvec = np.copy(np.asarray(view_Cyvec))

    # Cleanup
    if Cyvec != NULL:
        real_vector_free(Cyvec)
    if Cxvec != NULL:
        real_vector_view_free(Cxvec)
    if Cspline != NULL:
        real_matrix_view_free(Cspline)

    return yvec

def quadspline_eval_vector(np.ndarray[np.float_t, ndim=2] spline,
                           np.ndarray[np.float_t, ndim=1] xvec,
                           extrapol_zero=False):

    # If the input is an empty array, return empty array and stop there
    # NOTE: __init__ is required to return nothing
    if len(spline)==0 or len(xvec)==0:
        return np.empty(0, dtype=float)

    # Build real_vector representation of input numpy array for x
    cdef double* xvec_data = <double *> &xvec[0]
    Cxvec = real_vector_view(xvec_data, xvec.shape[0])

    # Build real_matrix representation of input numpy array for spline
    if not spline.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array quad spline is not C_CONTIGUOUS.')
    if not spline.shape[1] == 4:
        raise ValueError(
        'Input array for  quad spline has dimensions (%d, %d) instead of (n,4)',
        spline.shape[0], spline.shape[1])
    if not xvec.flags['C_CONTIGUOUS']:
        raise ValueError('Input numpy array xvec is not C_CONTIGUOUS')
    cdef real_matrix* Cspline = NULL
    cdef double* spline_data = <double *> &spline[0,0]
    Cspline = real_matrix_view(spline_data,
                               spline.shape[0], spline.shape[1])

    cdef real_vector* Cyvec = NULL
    ret = EvalQuadSplineOnVector(
        &Cyvec,
        Cxvec,
        Cspline,
        extrapol_zero
    );
    if ret == _FAILURE:
        raise ValueError("Call to EvalQuadSplineOnVector() failed.")

    # Cast C double array to numpy via a MemoryView
    # NOTE: np.copy to return an array independent of C allocated memory
    cdef int n = Cyvec.size
    cdef double[::1] view_Cyvec = <(double)[:n]> Cyvec.data
    yvec = np.copy(np.asarray(view_Cyvec))

    # Cleanup
    if Cyvec != NULL:
        real_vector_free(Cyvec)
    if Cxvec != NULL:
        real_vector_view_free(Cxvec)
    if Cspline != NULL:
        real_matrix_view_free(Cspline)

    return yvec

cpdef np.ndarray[np.float_t, ndim=1] resample(np.ndarray[np.float_t, ndim=1] xnew, np.ndarray[np.float_t, ndim=1] xold,y):
    """
    Resample the spline function on the xnew grid.  For values outside the range of the spline data fill with zeros.
    """

    #cdef np.ndarray[np.float_t, ndim=1] ynew
    cdef np.ndarray[np.float_t, ndim=2] yspline
    ynew=np.zeros(len(xnew),dtype=y.dtype)
    #Figure out the regions not to pad with zero
    cdef double xmin,xmax,newxmin,newxmax
    xmin=xold[0]
    xmax=xold[-1]
    newxmin=xnew[0]
    newxmax=xnew[-1]
    if newxmin>xmax or newxmax<xmin: return ynew
    if newxmin<xmin:imin=np.argmax(xnew>xmin)
    else: imin=0
    if newxmax>xmax:iend=imin+np.argmax(xnew[imin:]>xmax)
    else: iend=len(xnew)
    #Construct splines and fill
    if y.dtype==np.cdouble:
        yspline=CubicSpline(xold,y.real.copy()).get_spline()
        ynew[imin:iend]=spline_eval_vector(yspline,xnew[imin:iend])
        yspline=CubicSpline(xold,y.imag.copy()).get_spline()
        ynew[imin:iend]=ynew[imin:iend]+1j*spline_eval_vector(yspline,xnew[imin:iend])
    else:
        yspline=CubicSpline(xold,y).get_spline()
        ynew[imin:iend]=spline_eval_vector(yspline,xnew[imin:iend])
    return ynew

# UNFINISHED
# REQUIRES DEBUGGING
# cpdef np.ndarray[np.complex_t, ndim=1] eval_cexp_cubic_spline_constdeltax(
#                                     np.ndarray[np.float_t, ndim=2] phase_spline,
#                                     np.ndarray[np.float_t, ndim=1] xvec):
#     """
#     Evaluate exp[i*phi] on an input array of x's
#     with phi given by a cubic spline.
#     Args:
#       phi             # Input 2D (5 cols) numpy array for the cubic phase spline
#       x               # Input 1D numpy array of x values, evenly spaced
#     Keyword args:
#       None
#     """
#
#     # Build real_vector representation of input numpy array for x
#     cdef double* xvec_data = <double *> &xvec[0]
#     Cxvec = real_vector_view(xvec_data, xvec.shape[0])
#
#     # Build real_matrix representation of input numpy array for spline
#     if not phase_spline.flags['C_CONTIGUOUS']:
#         raise ValueError('Input numpy array spline is not C_CONTIGUOUS.')
#     if not phase_spline.shape[1] == 5:
#         raise ValueError(
#         'Input array for spline has dimensions (%d, %d) instead of (n,5)',
#         phase_spline.shape[0], phase_spline.shape[1])
#     if not xvec.flags['C_CONTIGUOUS']:
#         raise ValueError('Input numpy array xvec is not C_CONTIGUOUS')
#     cdef real_matrix* Cspline = NULL
#     cdef double* phase_spline_data = <double *> &phase_spline[0,0]
#     Cspline = real_matrix_view(phase_spline_data,
#                                phase_spline.shape[0], phase_spline.shape[1])
#
#     cdef complex_vector* Ccexpvec = NULL
#     ret = EvalCubicSplineCExpOnConstDeltaxVector(
#         &Ccexpvec,
#         Cxvec,
#         Cspline
#     );
#     if ret == _FAILURE:
#         raise ValueError("Call to EvalCubicSplineCExpOnVector() failed.")
#
#     # Cast C double array to numpy via a MemoryView
#     # NOTE: np.copy to return an array independent of C allocated memory
#     cdef int n = Ccexpvec.size
#     cdef double complex[::1] view_Ccexpvec = <(double complex)[:n]> Ccexpvec.data
#     cexpvec = np.copy(np.asarray(view_Ccexpvec))
#
#     # Cleanup
#     if Ccexpvec != NULL:
#         complex_vector_free(Ccexpvec)
#     if Cxvec != NULL:
#         real_vector_view_free(Cxvec)
#     if Cspline != NULL:
#         real_matrix_view_free(Cspline)
#
#     return cexpvec
