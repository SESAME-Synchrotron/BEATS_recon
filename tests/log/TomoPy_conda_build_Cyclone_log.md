## 14.03.21 - TomoPy conda build on Cyclone - log
#### Load modules
`module load CUDA/10.1.243`
TomoPy requires CMake 3.9+, which has support for CUDA as a first-class language – meaning that the CUDA compiler only needs to be in the PATH. On Unix, this is easily checked with the command: which nvcc. If the command returns a path to the compiler, build TomoPy normally. If not, locate the CUDA compiler and place the path to the compiler in PATH, remove the build directory (rm -r _skbuild or python setup.py clean) and rebuild.
`module load CMake/3.18.4-GCCcore-10.2.0`
`which nvcc`
`/nvme/h/buildsets/eb200211/software/CUDA/10.1.243/bin/nvcc`
`module load Anaconda3`

#### Create conda env
`conda create --name tomopy --channel conda-forge tomopy`
! Solving environment is stuck..
`conda create --prefix ./envs --channel conda-forge tomopy`
! Solving environment is stuck..

