#!/bin/sh
# execute command on Cyclone '$ sbatch ./run_tomopy_testCyclone_find_center.sh'
export SINGULARITY_HOME=$HOME:/home
export SINGULARITY_BINDPATH="/nvme/h/jo21gi1/data_p029:/tmp,/nvme/h/jo21gi1/code:/mnt,/nvme/scratch/jo21gi1:/scratch"

singularity exec /nvme/h/jo21gi1/tomopy.sif python /mnt/tomopy_tests/scripts/Cyclone/tomopy_testCyclone_find_center.py
