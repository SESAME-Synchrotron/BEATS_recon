#!/bin/sh
#SBATCH --mem-per-cpu=8000

export SINGULARITY_HOME=$HOME:/home
export SINGULARITY_BINDPATH="/home/gianthk/Data/StefanFly_test:/data,/home/gianthk/PycharmProjects/BEATS/tomopy_tests/scripts/Rum:/code,/home/gianthk/Desktop/pippo:/scratch"

singularity exec /home/gianthk/singularity_containers/tomopy.sif python /code/recon_test.py