# lisabeta

Copyright (C) 2019 Sylvain Marsat, John G. Baker. 
All rights reserved.

## Installation

`lisabeta` has the GSL library as a dependency. If already installed on the system, it can be located by
```
gsl-config --prefix
```

You can add the location of the GSL library in `setup.cfg` and then run
```
python setup.py install
```

Alternatively, you can specify the location of GSL on the command line as
```
python setup.py --with-gsl=... install
```

Physical constants can be tuned to:
- LAL (default)
- LDC
- LISA (in that case, path to `pdbParam.h` should be defined in `setup.cfg`)

```
python setup.py --with-constants=LDC install
```

If you want to use `lisabeta/inference/ptemcee_smbh.py`, also install ptemcee from the following fork:
```
https://github.com/SylvainMarsat/ptemcee
```

## conda

An example conda environment is given in the file `lisabeta-py36.yml`. You can create and activate the conda environment as
```
conda env create -f lisabeta-py36.yml
conda activate lisabeta-py36
```

### MPI with conda

NOTE: in order to use MPI in the inference modules like `lisabeta/inference/ptemcee_smbh.py`, you need to also install `mpi4py`. This is left out of the example environment since on a cluster it is necessary to build from source to ensure with the right version of MPI compilers.

Check that we have no `mpi4py` installed yet:
```
conda list mpi
> no mpi-related package
```

Assume there is no system-wide mpi compilers loaded yet:
```
which mpicc
> none
```

Find the mpi module and load it (this is cluster-specific -- not all clusters work with modules)
```
module load openmpi/3.1.1
which mpicc
>/softs/rh7/openmpi/3.1.1/bin/mpicc
```

Finally, install mpi4py using pip inside conda, forcing to build from source with these compilers:
```
conda install -c conda-forge pip
CC=mpicc MPICC=mpicc pip install mpi4py --no-binary mpi4py
```

## ptemcee sampler

To run Bayesian parameter estimation scripts with `ptemcee`, you will need to install our fork (in another directory):
```
git clone https://github.com/SylvainMarsat/ptemcee
python setup.py install
```
