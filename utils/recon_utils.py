# Reconstruction utilities

"""
2DO:
- write midplanes
- bounding box
- latex report

"""

__author__ = 'Gianluca Iori'
__date_created__ = '2021-03-28'
__date__ = '2021-03-28'
__copyright__ = 'Copyright (c) 2021, BEATS'
__docformat__ = 'restructuredtext en'
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = 'Gianluca Iori'
__email__ = "gianthk.iori@gmail.com"

import numpy as np
import png
import os
import dxchange

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


def writemidplanes(data, filename_out):
    # write orthogonal mid-planes through 3D dataset
    if data.ndim == 3:
        filename, ext = os.path.splitext(filename_out)
        with open(filename + '_XY.png', 'wb') as midplaneXY:
            pngWriter = png.Writer(data.shape[2], data.shape[1], greyscale=True, alpha=False, bitdepth=8)
            pngWriter.write(midplaneXY, touint8(data[int(data.shape[0] / 2), :, :]))

        with open(filename + '_XZ.png', 'wb') as midplaneXZ:
            pngWriter = png.Writer(data.shape[2], data.shape[0], greyscale=True, alpha=False, bitdepth=8)
            pngWriter.write(midplaneXZ, touint8(data[:, int(data.shape[1] / 2), :]))

        with open(filename + '_YZ.png', 'wb') as midplaneYZ:
            pngWriter = png.Writer(data.shape[1], data.shape[0], greyscale=True, alpha=False, bitdepth=8)
            pngWriter.write(midplaneYZ, touint8(data[:, :, int(data.shape[2] / 2)]))

def writemidplanesDxchange(data, filename_out):
    if data.ndim == 3:
        filename, ext = os.path.splitext(filename_out)
        dxchange.writer.write_tiff(touint8(data[int(data.shape[0] / 2), :, :]), fname=filename+'_XY.tiff', dtype='uint8')
        dxchange.writer.write_tiff(touint8(data[:, int(data.shape[1] / 2), :]), fname=filename + '_XZ.tiff', dtype='uint8')
        dxchange.writer.write_tiff(touint8(data[:, :, int(data.shape[2] / 2)]), fname=filename + '_YZ.tiff', dype='uint8')

