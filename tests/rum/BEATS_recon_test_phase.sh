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
python /PETRA/SED/BEATS/IH/scratch/scripts/BEATS_recon.py /PETRA/SED/BEATS/IH/fiber_wet_below_kink_HR-20230726T171211/fiber_wet_below_kink_HR-20230726T171211.h5 -s 1000 1200 --recon_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/recon_phase_alpha0.0002_testscript/ --work_dir /PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_wet_below_kink_HR-20230726T171211/ --cor 718.5 --ncore 36 --phase --no-phase_pad --alpha 0.0002 --pixelsize 0.00065 --sdd 20
# with `--phase_pad` this call is successful on cpunode. executed in < 2 sec
# with `--no-phase_pad` this call is stuck infinitely on cpunode. Even killing python processes one by one does not help

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# From the python command line
projs = tomopy.retrieve_phase(projs, pixel_size=0.1*pixelsize, dist=0.1*20, energy=20, alpha=0.0002, pad=True, ncore=36, nchunk=None)
# works

projs = tomopy.retrieve_phase(projs, pixel_size=0.1*pixelsize, dist=0.1*20, energy=20, alpha=0.0002, pad=False, ncore=36, nchunk=None)
# also works

# Notes:
# - !!!!!! Any python call on gpunode1 returns "Bus error (core dumped)".

python

import dxchange
import tomopy
import numpy as np

h5file = "/PETRA/SED/BEATS/IH/fiber_drying_dynamic-20230726T110245/fiber_drying_dynamic-20230726T110245.h5"
recon_dir = "/PETRA/SED/BEATS/IH/scratch/AlHandawi/fiber_drying_dynamic-20230726T110245/phase/recon_01/"
ncore = 48
projs, flats, darks, _ = dxchange.read_aps_32id(h5file, exchange_rank=0, proj=(1,401,1), sino=(1000, 1361, 1))
theta = np.radians(dxchange.read_hdf5(h5file, 'exchange/theta', slc=((1,401,1),)))
projs = tomopy.normalize(projs, flats, darks, ncore)
projs = tomopy.retrieve_phase(projs, pixel_size=0.1*0.00065, dist=0.1*20, energy=20, alpha=0.0002, pad=False, ncore=48, nchunk=None)
# stuck here on gpunode2:
^CProcess ForkPoolWorker-95:
^CTraceback (most recent call last):
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/lib/python3.10/site-packages/tomopy/util/mproc.py", line 312, in distribute_jobs

# recon = tomopy.recon(projs, theta, center=798, algorithm="gridrec", sinogram_order=False, ncore=48)
# dxchange.writer.write_tiff_stack(recon, fname=recon_dir + '/slice.tiff', dtype="float32", axis=0, digit=4, start=0, overwrite=True)
