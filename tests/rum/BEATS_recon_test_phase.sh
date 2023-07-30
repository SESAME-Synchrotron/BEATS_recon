# 30.07.2023 - investigating slurm crash on Rum nodes

# python call for BL-BEATS-WS01
# OK python /home/beats/PycharmProjects/BEATS_recon/scripts/rum/BEATS_recon.py /mnt/PETRA/SED/BEATS/IH/fiber_wet_below_kink_HR-20230726T171211/fiber_wet_below_kink_HR-20230726T171211.h5 -s 1000 1200 --recon_dir /home/beats/Data/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/recon_phase_alpha0.0002/ --work_dir /home/beats/Data/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/ --cor 718.5 --ncore 36 --phase --alpha 0.0002 --pixelsize 0.00065 --sdd 20

# python call for Rum
# Modules section:
ml load anaconda/tomopy

# Variables section:
export NUMEXPR_MAX_THREADS=96

python /PETRA/SED/BEATS/IH/scratch/scripts/BEATS_recon.py /PETRA/SED/BEATS/IH/fiber_wet_below_kink_HR-20230726T171211/fiber_wet_below_kink_HR-20230726T171211.h5 -s 1000 1200 --recon_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/recon_phase_alpha0.0002/ --work_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/ --cor 718.5 --ncore 36 --phase --alpha 0.0002 --pixelsize 0.00065 --sdd 20
# !!!!!! Bus error (core dumped)