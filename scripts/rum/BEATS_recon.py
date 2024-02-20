#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tomographic reconstruction script for the SESAME BEATS beamline.
For more information, call this script with the help option:
	BEATS_recon.py -h

"""

__author__ = ['Gianluca Iori']
__date_created__ = '2023-05-15'
__date__ = '2023-11-10'
__copyright__ = 'Copyright (c) 2023, SESAME'
__docformat__ = 'restructuredtext en'
__license__ = "MIT"
__maintainer__ = 'Gianluca Iori'
__email__ = "gianthk.iori@gmail.com"

import tomopy
import dxchange
import argparse
import textwrap
import logging
import numpy as np
import os
from time import time
import recon_utils as ru
from datetime import datetime

#################################################################################

def read_phase_retrieval_params(h5file):
	pixel_size = dxchange.read_hdf5(h5file, '/measurement/instrument/camera/pixel_size')[0]
	magnification = dxchange.read_hdf5(h5file, '/measurement/instrument/detection_system/objective/magnification')[0]
	dist = dxchange.read_hdf5(h5file, '/measurement/instrument/detector_motor_stack/detector_z')[0]
	energy = dxchange.read_hdf5(h5file, '/measurement/instrument/monochromator/energy')[0]

	return pixel_size, magnification, dist, energy


def main():
	description = textwrap.dedent('''\
	TomoPy reconstruction script for the BEATS beamline of SESAME.
	''')

	epilog = textwrap.dedent('''\
				EXAMPLES:

				* Standard (180 degrees, absorption contrast) reconstruction call. Output folder and bitformat are specified:
					BEATS_recon.py dataset.h5 -dtype uint8
					
				* Reconstruct subset of the sinograms using phase retrieval; attempt 8bit conversion from data histogram quantiles:
					BEATS_recon.py dataset.h5 --recon_dir ./recon_test -s 200 400 1 --phase --phase_pad -en 22 -sdd 300 --pixelsize 0.0045 -dtype uint8 -dq 0.05 0.095
				''')
	onemoreexample = textwrap.dedent('''
				* 360 degrees reconstruction:
					BEATS_recon.py dataset.h5 --360 --overlap 300
					''')

	parser = argparse.ArgumentParser(description=description, epilog=epilog,
									formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('h5file', type=str, help='<Required> Input HDF5 filename (projection data).')
	parser.add_argument('-p', '--proj', type=int, default=None, nargs='+', help='Specify projections to read. (start, end, step)')
	parser.add_argument('-s', '--sino', type=int, default=None, nargs='+', help='Specify sinograms to read. (start, end, step)')
	parser.add_argument('--work_dir', type=str, default=None, help='Work folder.')
	parser.add_argument('--recon_dir', type=str, default=None, help='Output reconstruction folder.')
	parser.add_argument('--phase', dest='phase', action='store_true',
						help='Perform single-step phase retrieval from phase-contrast measurements.')
	parser.add_argument('--alpha', type=float, default=0.001, help='Phase retrieval regularization parameter.')
	parser.add_argument('--pixelsize', type=float, default=None,
						help='Scan pixel size [mm]. Used for phase retrieval.')
	parser.add_argument('--energy', type=float, default=None,
						help='Scan energy [keV]. Used for phase retrieval.')
	parser.add_argument('--sdd', type=float, default=None,
						help='Sample Detector Distance [mm]. Used for phase retrieval.')
	parser.add_argument('--phase_pad', dest='phase_pad', action='store_true',
						help='Extend the size of the projections by padding with zeros.')
	parser.add_argument('--no-phase_pad', dest='phase_pad', action='store_false')
	# parser.add_argument('--phase_pad', type=bool, default=True,
	#                     help='Extend the size of the projections by padding with zeros.')
	parser.add_argument('--360', dest='fullturn', action='store_true', help='360 degrees scan.')
	parser.add_argument('--overlap', type=int, default=0, help='Overlap parameter for 360 degrees scan.')
	parser.add_argument('--rotside', type=str, default='left', help='Rotation axis side for 360 degrees scan.')
	parser.add_argument('--cor', type=float, default=None, help='Center Of Rotation.')
	parser.add_argument('--cor_method', type=str, default='Vo',
						help='Method for automatic finding of the rotation axis location.')
	parser.add_argument('--ncore', type=int, default=36, help='Number of cores that will be assigned to jobs.')
	parser.add_argument('--algorithm', type=str, default='gridrec',
						help='Reconstruction algorithm. Options are: gridrec, fbp, fbp_astra, fbp_cuda_astra, sirt, sirt_cuda, sirt_cuda_astra, sart_cuda_astra, cgls_cuda_astra, mlem, art.'
							' Visit https://tomopy.readthedocs.io/en/latest/api/tomopy.recon.algorithm.html for more info.')
	parser.add_argument('--num_iter', type=int, default=50, help='Number of iterations for iterative reconstruction.')
	parser.add_argument('--stripe_method', type=str, default='None',
						help='Stripe removal method. Available options are: remove_dead_stripe, remove_large_stripe, remove_stripe_based_sorting, and remove_all_stripe')
	parser.add_argument('--snr', type=float, default=3.0, help='Ratio used to locate of large stripes. Greater is less sensitive.')
	parser.add_argument('--size', type=int, default=51, help='Window size of the median filter.')
	parser.add_argument('--drop_ratio', type=float, default=0.1, help='Ratio of pixels to be dropped, which is used to reduce the false detection of stripes.')
	parser.add_argument('--norm', dest='norm', action='store_true',
						help='Apply sinogram normalization before stripe removal.')
	parser.add_argument('--no-norm', dest='norm', action='store_false',
						help='Do not apply sinogram normalization before stripe removal.')
	parser.add_argument('--dim', type=int, default=1, help='({1, 2}, optional) – Dimension of the window for stripe removal.')
	parser.add_argument('--la_size', type=int, default=61, help='Window size of the median filter to remove large stripes.')
	parser.add_argument('--sm_size', type=int, default=21, help='Window size of the median filter to remove small-to-medium stripes.')
	parser.add_argument('--circ_mask', dest='circ_mask', action='store_true',
						help='If True, apply circular mask to the Z-axis of reconstructed volume.')
	parser.add_argument('--circ_mask_ratio', type=float, default=1.0,
						help='Ratio of the mask’s diameter in pixels to the smallest slice size.')
	parser.add_argument('--circ_mask_val', type=float, default=0.0, help='Value for the masked region.')
	parser.add_argument('--midplanes', dest='write_midplanes', action='store_true',
						help='Write midplane images through the reconstructed volume.')
	parser.add_argument('--dtype', type=str, default='float32',
						help='Data type for output reconstructed TIFF slices.')
	parser.add_argument('--data_range', type=float, default=None, nargs='+',
						help='Range [min, max] for integer conversion. Used if an integer dtype is specified.')
	parser.add_argument('--data_quantiles', type=float, default=None, nargs='+',
						help='Quantiles [min, max] for integer conversion. Used if an integer dtype is specified.')
	parser.add_argument('--flip', type=int, default=None, nargs='+',
	                    help='Flip reconstruction volume along given axis. --flip 1 2 rotates the reconstruction by 180 degrees around Z-axis.')
	parser.add_argument('--crop', type=int, default=None, nargs='+',
	                    help='Crop reconstruction volume with parameters: [X_start, X_size, Y_start, Y_size, Z_start, Z_size]. If argument is negative the corresponding axis is not cropped.')
	parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Verbose output.')
	parser.set_defaults(fullturn=False, phase=False, phase_pad=True, circ_mask=False, write_midplanes=False, verbose=False, norm=True)

	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.INFO)

	if args.work_dir is None:
		work_dir = os.path.dirname(args.h5file)
	else:
		work_dir = args.work_dir

	time_start = time()
	logging.basicConfig(filename=work_dir + '/' + os.path.splitext(os.path.basename(args.h5file))[0] + '_recon.log', level=logging.DEBUG)
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	logging.info('\n')
	logging.info("==================================================================================================================")
	logging.info("BEATS reconstruction - {}.".format(dt_string))
	logging.info("==================================================================================================================\n\n")

	# output reconstruction directory
	if args.recon_dir is None:
		recon_dir = work_dir + "/recon"
	else:
		recon_dir = args.recon_dir

	if not os.path.isdir(recon_dir):
		logging.warning('Reconstruction directory does not exist. Will create it: {}'.format(recon_dir))
		os.mkdir(recon_dir)

	# read projections, darks, flats and angles
	projs, flats, darks, _ = dxchange.read_aps_32id(args.h5file, exchange_rank=0, proj=args.proj, sino=args.sino)
	theta = np.radians(dxchange.read_hdf5(args.h5file, 'exchange/theta', slc=(args.proj,)))

	# If the angular information is not available from the raw data, we need to set the data collection angles.
	# In this case, theta is set as equally spaced between 0-180 degrees.
	if theta is None:
		theta = tomopy.angles(projs.shape[0])
		logging.info("Theta not found.. generated by TomoPy.")
	logging.info("Theta min: {0}, max: {1}.\n".format(np.min(theta), np.max(theta)))

	# flat-field correction
	logging.info("Flat-field correct.\n")
	projs = tomopy.normalize(projs, flats, darks, ncore=args.ncore)

	if args.stripe_method is not 'None':
		if 'dead' in args.stripe_method:
			# Remove unresponsive and fluctuating stripe artifacts from sinogram using Nghia Vo’s approach [B23] (algorithm 6).
			logging.info("Remove unresponsive and fluctuating stripe artifacts from sinogram using TomoPy Nghia Vo’s approach...\n")
			projs = tomopy.prep.stripe.remove_dead_stripe(projs, snr=args.snr, size=args.size, ncore=args.ncore)
		elif 'large' in args.stripe_method:
			# Remove large stripe artifacts from sinogram using Nghia Vo’s approach [B23] (algorithm 5).
			logging.info("Remove large stripe artifacts from sinogram using Nghia Vo’s approach...\n")
			projs = tomopy.prep.stripe.remove_dead_stripe(projs, snr=args.snr, size=args.size, drop_ratio=args.drop_ratio, norm=args.norm, ncore=args.ncore)
		elif 'sorting' in args.stripe_method:
			# Remove full and partial stripe artifacts from sinogram using Nghia Vo’s approach [B23] (algorithm 3). Suitable for removing partial stripes.
			logging.info("Remove full and partial stripe artifacts from sinogram using Nghia Vo’s approach. Suitable for removing partial stripes...\n")
			projs = tomopy.prep.stripe.remove_stripe_based_sorting(projs, size=args.size, dim=args.dim, ncore=args.ncore)
		elif 'all' in args.stripe_method:
			# Remove all types of stripe artifacts from sinogram using Nghia Vo’s approach [B23] (combination of algorithm 3,4,5, and 6).
			logging.info("Remove all types of stripe artifacts from sinogram using Nghia Vo’s approach...\n")
			projs = tomopy.prep.stripe.remove_all_stripe(projs, snr=args.snr, la_size=args.la_size, sm_size=args.sm_size, dim=args.dim, ncore=args.ncore)
		else:
			logging.error("Stripe removal method not implemented.")

	# Convert from 360 to 180 degree sinograms
	if args.fullturn:
		logging.info("Convert 360 to 180 degrees sinograms. Rotation axis: {0}; Overlap: {1}.\n".format(args.rotside, args.overlap))
		projs = tomopy.sino_360_to_180(projs, args.overlap, args.rotside)

	# Phase retrieval
	if args.phase:
		# Try to get phase retrieval parameters from HDF5 file
		logging.info("Attempting to read phase retrieval parameters from HDF5 file...\n")
		det_pixel_size, magnification, dist, energy = read_phase_retrieval_params(args.h5file)
		if args.pixelsize is not None:
			pixel_size = args.pixelsize
		else:
			pixel_size = det_pixel_size / magnification

		if args.energy is not None:
			energy = args.energy

		if args.sdd is not None:
			dist = args.sdd

		logging.info("Retrieving phase with parameters:")
		logging.info("	- Detector pixel size: {0} micron".format(det_pixel_size * 1e3))
		logging.info("	- Object pixel size: {0} micron".format(pixel_size * 1e3))
		logging.info("	- Magnification: {0}X".format(magnification))
		logging.info("	- Sample Detector Distance: {0} mm".format(dist))
		logging.info("	- Energy: {0} KeV".format(energy))
		logging.info("	- Alpha: {0}".format(args.alpha))
		logging.info("	- Padding: {0}".format(args.phase_pad))
		logging.info("	- Number of cores: {0}\n".format(args.ncore))

		phase_start_time = time()
		# Retrieve phase
		projs = tomopy.retrieve_phase(projs, pixel_size=0.1*pixel_size, dist=0.1*dist, energy=energy, alpha=args.alpha, pad=args.phase_pad, ncore=args.ncore, nchunk=args.nchunk)
		phase_end_time = time()
		phase_time = phase_end_time - phase_start_time
		logging.info("Phase retrieval time: {} s\n".format(str(phase_time)))
		# Perform - log transform
		logging.info("Applying - log transform.\n")
		projs = tomopy.minus_log(projs, ncore=args.ncore)
	else:
		# Perform - log transform
		logging.info("Applying - log transform.\n")
		projs = tomopy.minus_log(projs, ncore=args.ncore)

	# Center Of Rotation (COR)
	if args.fullturn:
		logging.info("Center Of Rotation for 360 degrees scan.\n")
		COR = projs.shape[2]/2
	else:
		if args.cor is None:
			logging.info("Automatic find of Center Of Rotation (COR):")
			if args.cor_method == 'Vo':
				# auto detect Center Of Rotation (COR) witn Vo method
				logging.info("tomopy.find_center_vo..\n")
				COR = tomopy.find_center_vo(projs)
			else:
				logging.info("tomopy.find_center..\n")
				COR = tomopy.find_center(projs, theta, init=projs.shape[2] / 2, tol=1)
		else:
			logging.info("Center Of Rotation given by user.")
			COR = args.cor
	logging.info("COR: {}\n".format(COR))

	# Reconstruction
	logging.info("Start reconstruction with algorithm: " + args.algorithm)
	recon_start_time = time()
	if 'cuda_astra' in args.algorithm:
		if 'fbp' in args.algorithm:
			options = {'proj_type': 'cuda', 'method': 'FBP_CUDA'}
		elif 'sirt' in args.algorithm:
			options = {'proj_type': 'cuda', 'method': 'SIRT_CUDA', 'num_iter': args.num_iter}
		elif 'sart' in args.algorithm:
			options = {'proj_type': 'cuda', 'method': 'SART_CUDA', 'num_iter': args.num_iter}
		elif 'cgls' in args.algorithm:
			options = {'proj_type': 'cuda', 'method': 'CGLS_CUDA', 'num_iter': args.num_iter}
		else:
			logging.warning("Algorithm option not recognized. Will reconstruct with ASTRA FBP CUDA.")
			options = {'proj_type': 'cuda', 'method': 'FBP_CUDA'}
		recon = tomopy.recon(projs, theta, center=COR, algorithm=tomopy.astra, options=options, ncore=1)
	else:
		recon = tomopy.recon(projs, theta, center=COR, algorithm=args.algorithm, sinogram_order=False, ncore=args.ncore)

	recon_end_time = time()
	recon_time = recon_end_time - recon_start_time
	logging.info("Reconstruction time: {} s\n".format(str(recon_time)))
	recon_shape = recon.shape
	logging.info("Reconstructed volume size: {2} x {1} x {0} [X x Y x Z]".format(recon_shape[0], recon_shape[1], recon_shape[2]))

	if args.circ_mask:
		# apply circular mask
		recon = tomopy.circ_mask(recon, axis=0, ratio=args.circ_mask_ratio, val=args.circ_mask_val)

	if 'uint' in args.dtype:
		logging.info("Rescale dataset to {}.\n".format(args.dtype))
		if args.data_range:
			logging.info("Data range for rescale given by user: {}.\n".format(args.data_range))
		recon = ru.touint(recon, args.dtype, args.data_range, args.data_quantiles)

	if args.flip:
		logging.info("Flip reconstruction around axis: {}.\n".format(args.flip))
		recon = np.flip(recon, args.flip)

	if args.crop:
		X_end = recon_shape[2]
		Y_end = recon_shape[1]
		Z_end = recon_shape[0]

		X_start = args.crop[0]
		if args.crop[1] > 0:
			X_size = args.crop[1]
			X_end = X_start + X_size

		Y_start = args.crop[2]
		if args.crop[3] > 0:
			Y_size = args.crop[3]
			Y_end = Y_start + Y_size

		Z_start = args.crop[4]
		if args.crop[5] > 0:
			Z_size = args.crop[5]
			Z_end = Z_start + Z_size

		# check crop parameters
		if X_start < 0:
			X_start = 0

		if Y_start < 0:
			Y_start = 0

		if Z_start < 0:
			Z_start = 0

		if X_end > recon_shape[2]:
			X_end = recon_shape[2]

		if Y_end > recon_shape[1]:
			Y_end = recon_shape[1]

		if Z_end > recon_shape[0]:
			Z_end = recon_shape[0]

		logging.info("Crop reconstruction with parameters:")
		logging.info("	X_start: {0};   X_size: {1}".format(X_start, X_end-X_start))
		logging.info("	Y_start: {0};   Y_size: {1}".format(Y_start, Y_end-Y_start))
		logging.info("	Z_start: {0};   Z_size: {1}\n".format(Z_start, Z_end-Z_start))
		recon = recon[Z_start:Z_end, Y_start:Y_end, X_start:X_end]

	logging.info('Writing reconstructed dataset.\n')
	logging.info('converted dtype: {}.\n'.format(str(recon.dtype)))
	dxchange.writer.write_tiff_stack(recon, fname=recon_dir + '/slice.tiff', dtype=args.dtype, axis=0, digit=4, start=0, overwrite=True)
	os.chmod(recon_dir, 0o0777)
	
	if args.write_midplanes:
		ru.writemidplanesDxchange(recon, work_dir + '/slice.tiff')

	time_end = time()
	execution_time = time_end - time_start
	logging.info("Reconstruction job completed in {} s\n".format(str(execution_time)))

	return

if __name__ == '__main__':
	main()
