import tomopy
import dxchange
import numpy as np

h5file = "/nvme/h/jo21gi1/data_p029/test_00_/test_00_.h5"
path_recon = "/nvme/h/jo21gi1/data_p029/test_00_/recon/"
path_recon = "/nvme/h/jo21gi1/data_p029/test_00_/recon_phase/"

# read projections, darks, flats and angles
projs, flats, darks, theta = dxchange.read_aps_32id(h5file, exchange_rank=0)

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

# rescale GV range to uint8
# uint8 GV range as MIN and MAX of 3D data
range_min = np.min(recon)
range_max = np.max(recon)
range_max = range_max - range_min

recon_uint8Range = 255*((recon - range_min)/range_max)
recon_uint8Range[recon_uint8Range < 0] = 0
recon_uint8Range[recon_uint8Range > 255] = 255

# apply again circ mask
recon_uint8Range = tomopy.circ_mask(recon_uint8Range, axis=0, ratio=0.95)

# write output stack of TIFFs as uint8
fileout = path_recon+'data.tiff'
dxchange.writer.write_tiff_stack(recon_uint8Range, fname=fileout, dtype='uint8', axis=0, digit=5, start=0, overwrite=True)