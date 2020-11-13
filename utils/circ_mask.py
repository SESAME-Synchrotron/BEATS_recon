#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Apply circular mask to a stack of TIFFs.
TomoPy source: https://tomopy.readthedocs.io/en/latest/api/tomopy.misc.corr.html#tomopy.misc.corr.circ_mask
"""
import os
import logging
import numpy as np
import tomopy
import dxchange
import argparse
import tifffile

def main():
    parser = argparse.ArgumentParser(description='Apply circular mask to 3D stack of TIFF images.')
    parser.add_argument('-i', '--filein', type=str, help='input filename')
    parser.add_argument('-o', '--fileout', type=str, default=None, help='output filename')
    parser.add_argument('-a', '--axis', type=int, default=0, help='Axis along which mask will be performed')
    parser.add_argument('-r', '--ratio', type=int, default=1, help='Ratio of the mask’s diameter in pixels to the smallest edge size along given axis')
    parser.add_argument('-v', '--val', type=int, default=0.0, help='Value for the masked region')

    args = parser.parse_args()

    # load file
    print('Loading file: {}'.format(args.filein))
    # the dxchange TIFF reader requires list of slice indexes
    # data = dxchange.reader.read_tiff_stack(args.filein, ind=[560, 561, 562, 563, 564])

    # load using tifffile
    tifffiles = [os.path.join(os.path.dirname(args.filein), f) for f in os.listdir(os.path.dirname(args.filein))
                     if os.path.isfile(os.path.join(os.path.dirname(args.filein), f))]
    tifffiles.sort()
    data = tifffile.imread(tifffiles)

    # apply circulcar mask
    data_masked = tomopy.circ_mask(data, axis=args.axis, ratio=args.ratio, val=args.val).astype(data.dtype)

    # write output
    if args.fileout:
        dxchange.write_tiff_stack(data_masked, fname=args.fileout)
    else:
        # compose output folder name
        stem, ext = os.path.splitext(args.filein)
        stem, stack_in = os.path.split(stem)
        stem, stack_folder_in = os.path.split(stem)
        os.mkdir(os.path.join(stem, stack_folder_in + '_CircMask'))

        # write output TIFFs stack
        dxchange.write_tiff_stack(data_masked, fname=os.path.join(stem, stack_folder_in + '_CircMask', stack_in+ext))


if __name__ == '__main__':
    main()
