from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy
from distutils.sysconfig import get_python_lib
import sys


gsl_prefix="/usr"
lisabeta_include="../.."

argv_replace = []
for arg in sys.argv:
    if arg.startswith('--gsl-prefix='):
        gsl_prefix = arg.split('=', 1)[1]
    else:
        argv_replace.append(arg)
sys.argv = argv_replace

gsl_lib = gsl_prefix+"/lib"
gsl_include = gsl_prefix+"/include"

extensions=[
    Extension("pyIMRPhenomD",
              sources=["pyIMRPhenomD.c", "IMRPhenomD.c", "IMRPhenomD_internals.c"],
              include_dirs = [numpy.get_include(),lisabeta_include,gsl_include],
              language="c",
              extra_compile_args = ["-std=c99", "-O3"],
              libraries=["gsl", "gslcblas"],
              library_dirs=[gsl_lib],
    )
]
setup(
    ext_modules = extensions
)

setup(
    ext_modules = cythonize("pyIMRPhenomD.pyx")
)

