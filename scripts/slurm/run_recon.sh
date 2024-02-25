#!/bin/bash
#SBATCH --job-name=BEATS_rec_%j
#SBATCH --output=BEATS_rec_%j.out
#SBATCH --error=BEATS_rec_%j.err
#SBATCH --ntasks=11
#SBATCH --cpus-per-task=8
#SBATCH --time=00:40:00
#SBATCH --partition=gpu
#SBATCH --nodelist=gpunode1
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2G

# Modules section: 
ml load anaconda/tomopy

# Variables section: 
export NUMEXPR_MAX_THREADS=10

# python /PETRA/SED/BEATS/IH/scratch/scripts/BEATS_recon.py /PETRA/SED/BEATS/SEM_6/20235163/ExpData/T2_diaphysis-20240221T153352/T2_diaphysis-20240221T153352.h5 --recon_dir /PETRA/SED/BEATS/SEM_6_recon/20235163/T2_diaphysis-20240221T153352/recon_phase_alpha0.0001/ --work_dir /PETRA/SED/BEATS/SEM_6_recon/20235163/ --cor 1403 --ncore 8 --phase --sdd 330 --pixelsize 0.0045 --energy 36 --alpha 0.0001 --algorithm gridrec --circ_mask --circ_mask_ratio 0.95 --nchunk 100 --dtype uint8 --data_range -0.0002 0.0013 --midplanes 

