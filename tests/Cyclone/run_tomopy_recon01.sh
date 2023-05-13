#!/bin/sh
export SINGULARITY_HOME=$HOME:/home
export SINGULARITY_BINDPATH="/nvme/h/jo21gi1/data_p029:/tmp,/nvme/h/jo21gi1/code:/mnt"

singularity exec /nvme/h/jo21gi1/tomopy.sif python /mnt/tomopy_tests/scripts/tomopy_test01_script_noDXchange.py
