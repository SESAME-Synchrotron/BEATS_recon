import os
import dxchange
import tomopy
import numpy as np
import h5py
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['figure.dpi'] = 150

import logging
logging.basicConfig(level=logging.INFO)

h5file = "data/test_00_.h5"
# path_recon = "data/recon/"
path_recon = "data/recon_phase/"
fout = "data/tiffs/reco.tiff"


# read the full proj
projs, flats, darks, theta = dxchange.read_aps_32id(h5file, exchange_rank=0)


if theta is None:
    theta = tomopy.angles(projs.shape[0])


projs = tomopy.normalize(projs, flats, darks)
projs = tomopy.minus_log(projs)


COR = tomopy.find_center(projs, theta, init=projs.shape[2]/2, ind=200, tol=0.5)



extra_options = {'MinConstraint': 0}
options = {
    'proj_type': 'cuda',
    'method': 'SIRT_CUDA',
    'num_iter': 100,
    'extra_options': extra_options
}

# options = {'proj_type': 'cuda', 'method': 'FBP_CUDA'}


recon = tomopy.recon(projs,
                     theta,
                     center=COR,
                     algorithm=tomopy.astra,
                     options=options,
                     ncore=1)
recon = tomopy.circ_mask(recon, axis=0, ratio=0.95)

#recon = tomopy.recon(projs, theta, center=COR, algorithm='gridrec', sinogram_order=False)
#recon = tomopy.circ_mask(recon, axis=0, ratio=0.95)

print(recon.shape)
reco_plot = recon[200].reshape(recon.shape[1], recon.shape[2])

import tifffile as tif

# from PIL import Image

# # recon = np.array(recon, dtype='float32')
# def write_tiffs(recon):
	

# 	xd = recon.shape[1]
# 	yd = recon.shape[2]

# 	for r in range(len(recon)):

# 		recon2 = recon[r].reshape(xd, yd)
# 		recon2 = Image.fromarray(recon2, mode='F') # float32
# 		recon2.save(fout+'reconstruction_'+str(r)+'.tiff',"TIFF")
# 		# imsave(fout+'reconstruction_'+str(r)+'.tiff',recon2[r].reshape(recon2.shape[1], recon2.shape[2]))


# write_tiffs(recon)

recon = recon.astype('float32')
tif.imsave('reco.tif', recon, bigtiff=True)


# dxchange.write_tiff_stack(recon, fname=fout,overwrite=True)
logging.info('TIFF data written to file {}'.format(fout))



plt.imshow(reco_plot, cmap='gray')
plt.show()
