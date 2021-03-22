# execute on CYclone within singularity
# the following commands must be used before launching singularity script
# $ export SINGULARITY_HOME=$HOME:/home
# $ export SINGULARITY_BINDPATH="/nvme/h/jo21gi1/data_p029:/tmp,/nvme/h/jo21gi1/code:/mnt"

# to launch a singularity shell (you can then use python):
# $ singularity shell ./tomopy.sif

# launch python script within singularity
# $ singularity exec ./tomopy.sif python /mnt/tomopy_tests/tomopy_test01_script_noDXchange.py

import tomopy
import numpy as np

# h5file = "/nvme/h/jo21gi1/data_p029/test_00_/test_00_.h5"
flats_file = "/tmp/test_00_/flats.npy"
darks_file = "/tmp/test_00_/darks.npy"
projs_file = "/tmp/test_00_/projs.npy"
theta_file = "/tmp/test_00_/theta.npy"
path_recon = "/tmp/test_00_/recon/"

# read projections, darks, flats and angles
# projs, flats, darks, theta = dxchange.read_aps_32id(h5file, exchange_rank=0)
projs = np.load(projs_file)
flats = np.load(flats_file)
darks = np.load(darks_file)
theta = np.load(theta_file)

# If the angular information is not avaialable from the raw data you need to set the data collection angles.
# In this case, theta is set as equally spaced between 0-180 degrees.
if theta is None:
    theta = tomopy.angles(projs.shape[0])

# flat-field correction
projs = tomopy.normalize(projs, flats, darks)

# - log transform
projs = tomopy.minus_log(projs)

# auto detect Center Of Rotation (COR)
COR = tomopy.find_center(projs, theta, init=projs.shape[2]/2, ind=200, tol=0.5)

# CPU recon (GRIDREC)
recon = tomopy.recon(projs, theta, center=COR, algorithm='gridrec', sinogram_order=False)

# apply circular mask
recon = tomopy.circ_mask(recon, axis=0, ratio=0.95)

# write output npy file
fileout = path_recon+'recon.npy'
np.save(fileout, recon)

# write output slice as npy file
fileout = path_recon+'slice200.npy'
np.save(fileout, recon[200, :, :])
