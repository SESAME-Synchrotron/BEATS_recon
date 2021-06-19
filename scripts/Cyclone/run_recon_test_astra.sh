#!/bin/sh
#SBATCH --nodes=1
#SBATCH --gpus=1


export SINGULARITY_HOME=$HOME:/home
export SINGULARITY_BINDPATH="/onyx/data/p029:/data,/nvme/h/jo21gi1/code:/code,/nvme/h/jo21gi1/scratch:/scratch"

singularity exec -nv /nvme/h/jo21gi1/tomopy.sif python /code/tomopy_tests/scripts/Cyclone/recon_test_astra.py