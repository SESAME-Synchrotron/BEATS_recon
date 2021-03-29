# TomoPy recon on Cyclone: compare different algorithms

import tomopy
import dxchange
import numpy as np
import os
import logging
from time import time

def touint8(data, quantiles=None):
    # scale data to uint8
    # if quantiles is empty data is scaled based on its min and max values
    if quantiles == None:
        data_min = np.min(data)
        data_max = np.max(data)
        data_max = data_max - data_min
        data = 255 * ((data - data_min) / data_max)
        return np.uint8(data)
    else:
        [q0, q1] = np.quantile(np.ravel(data), quantiles)
        q1 = q1 - q0
        data = 255 * ((data - q0) / q1)
        return np.uint8(data)


def writemidplanesDxchange(data, filename_out):
    if data.ndim == 3:
        filename, ext = os.path.splitext(filename_out)
        dxchange.writer.write_tiff(touint8(data[int(data.shape[0] / 2), :, :]), fname=filename+'_XY.tiff', dtype='uint8')
        dxchange.writer.write_tiff(touint8(data[:, int(data.shape[1] / 2), :]), fname=filename + '_XZ.tiff', dtype='uint8')
        dxchange.writer.write_tiff(touint8(data[:, :, int(data.shape[2] / 2)]), fname=filename + '_YZ.tiff', dtype='uint8')

h5file = "/tmp/tomoData/8671_8_B_01_/8671_8_B_01_.h5"
path_recon = "/scratch/recon/algorithm_test/"

# path_recon = "/nvme/h/jo21gi1/data_p029/test_00_/recon_phase/"
logging.basicConfig(filename=path_recon+'recon_algorithm_test.log', level=logging.DEBUG)


CPU_algorithms = ['gridrec', 'fbp', 'mlem', 'sirt', 'art']

# read projections, darks, flats and angles
projs, flats, darks, theta = dxchange.read_aps_32id(h5file, exchange_rank=0)

# If the angular information is not available from the raw data you need to set the data collection angles.
# In this case, theta is set as equally spaced between 0-180 degrees.
if theta is None:
    theta = tomopy.angles(projs.shape[0])

# flat-field correction
logging.info("Flat-field correct.")
projs = tomopy.normalize(projs, flats, darks)

# - log transform
logging.info("- log transform.")
projs = tomopy.minus_log(projs)

# COR was found with Vo method + manual inspection
COR = 1303

for alg in CPU_algorithms:
    time_start = time()
    # CPU recon
    recon = tomopy.recon(projs, theta, center=COR, algorithm=alg, sinogram_order=False)
    time_end = time()
    execution_time = time_end - time_start
    logging.info("{} reconstructed in {} s".format(alg, str(execution_time)))

    # apply circular mask
    recon = tomopy.circ_mask(recon, axis=0, ratio=0.95)

    # rescale GV range to uint8 from MIN and MAX of 3D data
    recon_uint8Range = touint8(recon)
    del recon

    # apply again circ mask
    recon_uint8Range = tomopy.circ_mask(recon_uint8Range, axis=0, ratio=0.95)

    # write output stack of TIFFs as uint8
    fileout = path_recon+alg
    # dxchange.writer.write_tiff_stack(recon_uint8Range, fname=fileout, dtype='uint8', axis=0, digit=5, start=0, overwrite=True)
    writemidplanesDxchange(recon_uint8Range, fileout)

