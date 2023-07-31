# 30.07.2023 - investigating slurm crash on Rum nodes

# python call for BL-BEATS-WS01
python /home/beats/PycharmProjects/BEATS_recon/scripts/rum/BEATS_recon.py /mnt/PETRA/SED/BEATS/IH/fiber_wet_below_kink_HR-20230726T171211/fiber_wet_below_kink_HR-20230726T171211.h5 -s 1000 1200 --recon_dir /home/beats/Data/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/recon_phase_alpha0.0002/ --work_dir /home/beats/Data/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/ --cor 718.5 --ncore 36 --phase --no-phase_pad --alpha 0.0002 --pixelsize 0.00065 --sdd 20
# this call is successful for both '--phase_pad' and '--no-phase_pad'. executed in < 1 min

# python call for Rum
# Modules section:
ml load anaconda/tomopy

# Variables section:
export NUMEXPR_MAX_THREADS=96

# Standard reconstruction
python /PETRA/SED/BEATS/IH/scratch/scripts/BEATS_recon.py /PETRA/SED/BEATS/IH/fiber_wet_below_kink_HR-20230726T171211/fiber_wet_below_kink_HR-20230726T171211.h5 -s 1000 1200 --recon_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/recon_test/ --work_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/ --cor 718.5 --ncore 36
# this call is successful on cpunode. executed in < 2 sec

# Phase-reconstruction
python /PETRA/SED/BEATS/IH/scratch/scripts/BEATS_recon.py /PETRA/SED/BEATS/IH/fiber_wet_below_kink_HR-20230726T171211/fiber_wet_below_kink_HR-20230726T171211.h5 -s 1000 1200 --recon_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/recon_phase_alpha0.0002/ --work_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/ --cor 718.5 --ncore 36 --phase --no-phase_pad --alpha 0.0002 --pixelsize 0.00065 --sdd 20
# with `--phase_pad` this call is successful on cpunode. executed in < 2 sec
# with `--no-phase_pad` this call is stuck infinitely on cpunode. Even killing python processes one by one does not help

# Notes:
# - !!!!!! Any python call on gpunode1 returns "Bus error (core dumped)"

test