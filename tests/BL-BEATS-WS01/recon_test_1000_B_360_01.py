# TomoPy recon test on SESAME Rum

import tomopy
import dxchange
import numpy as np
# from scipy import ndimage
import numexpr as ne
import os
import logging
from time import time

def convert8bit(rec, data_min, data_max, numexpr=True):
    rec = rec.astype(np.float32, copy=False)
    df = np.float32(data_max-data_min)
    mn = np.float32(data_min)

    if numexpr:
        scl = ne.evaluate('0.5+255*(rec-mn)/df', truediv=True)
        ne.evaluate('where(scl<0,0,scl)', out=scl)
        ne.evaluate('where(scl>255,255,scl)', out=scl)
        return scl.astype(np.uint8)
    else:
        rec = 0.5+255*(rec-mn)/df
        rec[rec<0]=0
        rec[rec>255]=255
        return np.uint8(rec)

def touint8(data, range=None, quantiles=None, numexpr=True):
    """Normalize and convert data to uint8.

        Parameters
        ----------
        data
            Input data.
        range : [float, float]
            Control range for data normalization.
        quantiles : [float, float]
            Define range for data normalization through input data quantiles. If range is given this input is ignored.
        numexpr : bool
            Use fast numerical expression evaluator for NumPy (memory expensive).

        Returns
        -------
        output : uint8
            Normalized data.
        """

    if range == None:

        # if quantiles is empty data is scaled based on its min and max values
        if quantiles == None:
            data_min = np.nanmin(data)
            data_max = np.nanmax(data)
            data_max = data_max - data_min
            return convert8bit(data, data_min, data_max, numexpr)
        else:
            [q0, q1] = np.quantile(np.ravel(data), quantiles)
            return convert8bit(data, q0, q1, numexpr)

    else:
        # ignore quantiles input if given
        if quantiles is not None:
            print('quantiles input ignored.')

        return convert8bit(data, range[0], range[1], numexpr)

def writemidplanesDxchange(data, filename_out):
    if data.ndim == 3:
        filename, ext = os.path.splitext(filename_out)
        dxchange.writer.write_tiff(touint8(data[int(data.shape[0] / 2), :, :]), fname=filename + '_XY.tiff', dtype='uint8')
        dxchange.writer.write_tiff(touint8(data[:, int(data.shape[1] / 2), :]), fname=filename + '_XZ.tiff', dtype='uint8')
        dxchange.writer.write_tiff(touint8(data[:, :, int(data.shape[2] / 2)]), fname=filename + '_YZ.tiff', dtype='uint8')

# settings ####################################################################################################
algorithm = 'gridrec'
# algorithm = 'fbp'
# algorithm = 'fbp_astra'
# algorithm = 'fbp_cuda_astra'
# algorithm = 'sirt_cuda'
# algorithm = 'sirt_cuda_astra'
# algorithm = 'sart_cuda_astra'
# algorithm = 'cgls_cuda_astra'
# algorithm = 'mlem'
# algorithm = 'sirt'
# algorithm = 'art'

ncore = 36
reconstruction_type = 'full' # 'slice' # 'full'
recon_slice = 500 

# input data file
# h5file = "/data/test_00_/test_00_.h5"
h5file = "1000_B_360_01_.h5"

# output reconstruction path (make sure this exists)
path_test = "scratch/"
path_recon = "scratch/recon/"

# start test ##################################################################################################
time_start = time()
logging.basicConfig(filename=path_test+'recon_'+algorithm+'.log', level=logging.DEBUG)

# read projections, darks, flats and angles
projs, flats, darks, theta = dxchange.read_aps_32id(h5file, exchange_rank=0)

# If the angular information is not available from the raw data you need to set the data collection angles.
# In this case, theta is set as equally spaced between 0-180 degrees.
if theta is None:
    theta = tomopy.angles(projs.shape[0])

# crop
# projs = projs[:, 0:1000, :]
# flats = flats[:, 0:1000, :]
# darks = darks[:, 0:1000, :]

# flat-field correction
logging.info("Flat-field correct.")
projs = tomopy.normalize(projs, flats, darks, ncore=ncore)

# - log transform
logging.info("- log transform.")
projs = tomopy.minus_log(projs, ncore=ncore)

# 360 deg sinogram to 180
overlap = 991 # 495
logging.info("Convert 360deg sinogram to 180deg:")
logging.info("Input data shape: " + str(projs.shape[0]) + " x " + str(projs.shape[1]) + " x " + str(projs.shape[2]))
projs = tomopy.sino_360_to_180(projs, overlap, 'left')
logging.info("New data shape: " + str(projs.shape[0]) + " x " + str(projs.shape[1]) + " x " + str(projs.shape[2]))

# auto detect Center Of Rotation (COR)
# logging.info("tomopy.find_center..")
# COR = tomopy.find_center(projs, theta, init=projs.shape[2]/2, tol=1)

# auto detect Center Of Rotation (COR) witn Vo method
# logging.info("tomopy.find_center_vo..")
# COR = tomopy.find_center_vo(projs)

# COR is the center of the image
COR = projs.shape[2]/2
logging.info("COR given by user: " + str(COR))

if reconstruction_type == 'slice':
	# projs = projs[:, [recon_slice], :]
    projs = projs[:, recon_slice-5:recon_slice+5, :]

logging.info("Reconstruct with algorithm: " + algorithm)
recon_start_time = time()
if algorithm == 'fbp_astra':
	# CPU ASTRA RECON
	options = {'proj_type': 'linear', 'method': 'FBP'}
	recon = tomopy.recon(projs, theta, center=COR, algorithm=tomopy.astra, options=options, ncore=ncore)
elif algorithm == 'fbp_cuda_astra':
	# GPU ASTRA RECON (CUDA)
	options = {'proj_type': 'cuda', 'method': 'FBP_CUDA'}
	recon = tomopy.recon(projs, theta, center=COR, algorithm=tomopy.astra, options=options, ncore=10)
elif algorithm == 'sirt_cuda':
	recon = tomopy.recon(projs, theta, center=COR, algorithm='sirt', sinogram_order=False, accelerated=True, ncore=1)
elif algorithm == 'sirt_cuda_astra':
	# GPU ASTRA RECON (CUDA)
	extra_options = {'MinConstraint': 0}
	# options = {'proj_type': 'cuda', 'method': 'SIRT_CUDA', 'num_iter': 200, 'extra_options': extra_options}
	options = {'proj_type': 'cuda', 'method': 'SIRT_CUDA', 'num_iter': 100}
	recon = tomopy.recon(projs, theta, center=COR, algorithm=tomopy.astra, options=options, ncore=10)
elif algorithm == 'sart_cuda_astra':
	options = {'proj_type': 'cuda', 'method': 'SART_CUDA', 'num_iter': 100}
	recon = tomopy.recon(projs, theta, center=COR, algorithm=tomopy.astra, options=options, ncore=10)
elif algorithm == 'cgls_cuda_astra':
	options = {'proj_type': 'cuda', 'method': 'CGLS_CUDA', 'num_iter': 100}
	recon = tomopy.recon(projs, theta, center=COR, algorithm=tomopy.astra, options=options, ncore=10)
else:
	# Launch tomopy recon (no ASTRA)
	recon = tomopy.recon(projs, theta, center=COR, algorithm=algorithm, sinogram_order=False, ncore=ncore)

recon_end_time = time()
recon_time = recon_end_time - recon_start_time
logging.info("Recon time: {} s".format(str(recon_time)))

# write outputs ################################################################################################
logging.info("Writing outputs..")

# apply circular mask
# recon = tomopy.circ_mask(recon, axis=0, ratio=0.95)

# write output stack of TIFFs as float
fileout = path_recon+'slice.tiff'
# dxchange.writer.write_tiff_stack(recon, fname=fileout, axis=0, digit=5, start=0, overwrite=True)

# rescale GV range to uint8 from MIN and MAX of 3D data
# recon_uint8Range = touint8(recon)

# apply circ mask
# recon_uint8Range = tomopy.circ_mask(recon_uint8Range, axis=0, ratio=0.95)

# write output stack of TIFFs as uint8
# dxchange.writer.write_tiff_stack(recon_uint8Range, fname=fileout, dtype='uint8', axis=0, digit=5, start=0, overwrite=True)

# write tiff midplanes (float) with dxchange
if recon.ndim == 3:
	dxchange.writer.write_tiff(recon[int(recon.shape[0] / 2), :, :], fname=path_test+algorithm+'_sliceXY.tiff')
	dxchange.writer.write_tiff(recon[:, int(recon.shape[1] / 2), :], fname=path_test+algorithm+'_sliceXZ.tiff')
	dxchange.writer.write_tiff(recon[:, :, int(recon.shape[2] / 2)], fname=path_test+algorithm+'_sliceYZ.tiff')
elif recon.ndim == 2:
	dxchange.writer.write_tiff(recon, fname=path_test+algorithm+'_slice.tiff')

# write midplanes (uint8 TIFFs)
# writemidplanesDxchange(recon_uint8Range, fileout)

time_end = time()
execution_time = time_end - time_start
logging.info("Recon test completed in {} s".format(str(execution_time)))
