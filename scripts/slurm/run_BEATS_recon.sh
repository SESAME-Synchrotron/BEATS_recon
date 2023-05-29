#!/bin/bash
#SBATCH --job-name=BEATS_rec_%j
#SBATCH --output=BEATS_rec_%j.out
#SBATCH --error=BEATS_rec_%j.err
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=2
#SBATCH --time=00:30:00
#SBATCH --partition=cpu
#SBATCH --mem-per-cpu=2

# Modules section: 
ml load anaconda/tomopy

# Variables section: 
export NUMEXPR_MAX_THREADS=96

python BEATS_recon.py /mnt/PETRA/SED/BEATS/IH/dead_sea_coral_PCO-20230519T164542/dead_sea_coral_PCO-20230519T164542.h5 --recon_dir ~/Data/tmp/recon --work_dir ~/Data/tmp --cor 1204