## 14.03.21 - TomoPy source build on Cyclone - log
#### Cloning the repo
From inside /code/
`git clone https://github.com/tomopy/tomopy.git`
#### Load modules
`module load CUDA/10.1.243`
TomoPy requires CMake 3.9+, which has support for CUDA as a first-class language – meaning that the CUDA compiler only needs to be in the PATH. On Unix, this is easily checked with the command: which nvcc. If the command returns a path to the compiler, build TomoPy normally. If not, locate the CUDA compiler and place the path to the compiler in PATH, remove the build directory (rm -r _skbuild or python setup.py clean) and rebuild.
`module load CMake/3.18.4-GCCcore-10.2.0`
`which nvcc`
`/nvme/h/buildsets/eb200211/software/CUDA/10.1.243/bin/nvcc`
`module load Anaconda3`
`module load OpenBLAS/0.3.12-GCC-10.2.0`
`module load fosscuda`
Description:
      GCC based compiler toolchain __with CUDA support__, and including OpenMPI for MPI support,
      OpenBLAS (BLAS and LAPACK support), FFTW and ScaLAPACK.

#### Installing dependencies
`more envs/linux-37.yml` 
name: tomopy
channels:
  - conda-forge
  - jrmadsen
  - defaults
dependencies:
  - coverage!=5.0.2
  - dxchange
  - gcc_linux-64<=8
  - git
  - gxx_linux-64<=8
  - h5py
  - libstdcxx-ng
  - libgcc-ng
  - mkl ["blas=*=openblas"]
  - mkl-devel ["blas=*=openblas"]
  - mkl_fft
  - nose
  - numexpr
  - numpy ["blas=*=openblas"]
  - opencv>=3.4 ["blas=*=openblas"]
  - pyctest>0.0.10
  - python=3.7
  - pywavelets
  - scikit-build
  - scikit-image>=0.17
  - scipy
  - setuptools_scm
  - setuptools_scm_git_archive
  - timemory

`conda env create -f envs/linux-37.yml --prefix ./envs`

