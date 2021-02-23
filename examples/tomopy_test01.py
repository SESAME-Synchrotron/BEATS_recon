#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TomoPy test run.

For more information, call this script with the help option::
    tomopy_test01.py -h

"""

"""
2DO:
- test full recon from script
- test GPU recon
- test ASTRA recon
- separate scripts for:
    - data read and sino generation
    - COR
    - recon

"""

__author__ = 'Gianluca Iori'
__date_created__ = '2020-11-15'
__copyright__ = 'Copyright (c) 2021, SESAME|BEATS'
__docformat__ = 'restructuredtext en'
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = 'Gianluca Iori'
__email__ = "gianluca.iori@sesame.org.jo"


import logging
import os
import dxchange
import tomopy
import numpy as np
import h5py
import matplotlib
import matplotlib.pyplot as plt
import argparse
import tifffile

# parameters #####################################################################
# path_recon = "/home/gianthk/Data/StefanFly_test/test_00_/recon/"
COR_ind = 500 # index of the slice to be used for recon
COR_tol = 0.5 # Sub-pixel accuracy

def read_tiff_stack(filename):
    # Read a stack of tiffs from single slice filename.
    # Searches all files in parent folder and opens them as a stack of images.
    # TO DO:
    #     - check that folder contains only .TIFF files; skip the rest

    # search all files in parent folder; create filenames list
    tifffiles = [os.path.join(os.path.dirname(filename), f) for f in os.listdir(os.path.dirname(filename))
                     if os.path.isfile(os.path.join(os.path.dirname(filename), f))]
    tifffiles.sort()

    # load stack using tifffile
    return tifffile.imread(tifffiles)


def read_tiff_DXchange(filename):
    print('not implemented..')
    # print('Loading file: {}'.format(filename))
    # the dxchange TIFF reader requires list of slice indexes
    # data = dxchange.reader.read_tiff_stack(args.filein, ind=[560, 561, 562, 563, 564])


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--filein', type=str, help='Input HDF5 file.')
    parser.add_argument('-o', '--fileout', type=str, default=None, help='Output filename (.TIFF stack).')
    parser.add_argument('-a', '--algorithm', type=str, default='gridrec', help='Reconstruction algorithm.')
    parser.add_argument('--accelerated', type=bool, default=False, help='GPU accelerated recon (only valid with sirt and mlem algorithms)')
    # parser.add_argument('-vs', '--voxelsize', type=float, nargs='+', default=[1.0, 1.0, 1.0], help='Data voxel size [X, Y, Z].')
    parser.add_argument('-v', '--verbose', type=bool, default=False, help='Verbose output')

    args = parser.parse_args()

    # check inputs
    # filename_in, ext = os.path.split(args.filein)
    filename_in = args.filein
    if args.verbose is True:
        logging.basicConfig(level=logging.INFO)

    # read projections
    projs, flats, darks, theta = dxchange.read_aps_32id(filename_in, exchange_rank=0)

    # read one projection every 10
    # projs, flats, darks, theta = dxchange.read_aps_32id(filename_in, exchange_rank=0, proj=[1, 1000, 10])

    data_shape = projs.shape
    logging.info('Projection data loaded with size {size[0]} x {size[0]} x {size[0]}'.format(size=data_shape))

    if args.verbose is True:
        # display one projection
        plt.imshow(projs[200, :, :])
        plt.show()

    # create angles array
    if theta is None:
        theta = tomopy.angles(projs.shape[0])

    # flat field correction
    projs = tomopy.normalize(projs, flats, darks)

    # find Center Of Rotation (COR)
    COR = tomopy.find_center(projs, theta, init=projs.shape[2] / 2, ind=COR_ind, tol=COR_tol)

    # recon
    if args.algorithm == 'sirt' or args.algorithm == 'mlem':
        recon = tomopy.recon(projs, theta, center=COR + 15, algorithm=args.algorithm, sinogram_order=False, accelerated=args.accelerated)
    else:
        recon = tomopy.recon(projs, theta, center=COR + 15, algorithm=args.algorithm, sinogram_order=False)

    # apply circular mask
    recon = tomopy.circ_mask(recon, axis=0, ratio=0.95)

    if args.verbose is True:
        # display one reconstructed slice
        plt.imshow(recon[100, :, :], cmap='gray')
        plt.show()

    if args.fileout is not None:
        # write output slices
        dxchange.writer.write_tiff_stack(recon, fname=args.fileout, dtype=None, axis=0, digit=5, start=0, overwrite=True)
        logging.info('TIFF data written to file {}'.format(args.fileout))
    return

if __name__ == '__main__':
    main()
