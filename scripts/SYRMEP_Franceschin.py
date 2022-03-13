import tomopy
import dxchange
import numpy as np

# from __future__ import print_function
import dxchange
import tomopy

# fname = "/media/gianthk/My Passport/20217193_Traviglia/Test_02/Test_02/"
# fname = "/media/gianthk/My Passport/20217193_Traviglia/TDF/2_2234_crack/2_2234_crack_test180/"
# fname = "/home/gianthk/Data/BEATS/Franceschin/SYRMEP/2_2234_crack_test180/2_2234_crack_test180/2_2234_crack_flat.his"
fname = "/home/gianthk/Data/BEATS/Franceschin/SYRMEP/2_2234_crack_test180/2_2234_crack.tdf"

# proj_start = 1
# proj_end = 1801
# flat_start = 1
# flat_end = 21
# dark_start = 1
# dark_end = 21
#
# ind_tomo = range(proj_start, proj_end)
# ind_flat = range(flat_start, flat_end)
# ind_dark = range(dark_start, dark_end)

# Select the sinogram range to reconstruct.
start = 0
end = 16
sino=(start, end)

# read specific sinogram set
# proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=(start, end))

# read the whole dataset
# proj, flat, dark, theta = dxchange.read_aps_32id(fname)

exchange_base = "exchange"
tomo_grp = '/'.join([exchange_base, 'data'])
flat_grp = '/'.join([exchange_base, 'data_white'])
dark_grp = '/'.join([exchange_base, 'data_dark'])
# theta_grp = '/'.join([exchange_base, 'theta'])

tomo = dxchange.reader.read_hdf5(fname, tomo_grp, slc=(None, None, sino))
flat = dxchange.reader.read_hdf5(fname, flat_grp, slc=(None, None, sino))
dark = dxchange.reader.read_hdf5(fname, dark_grp, slc=(None, None, sino))
# theta = dxchange.reader.read_hdf5(fname, theta_grp, slc=None)

# read one H5 dataset (either data, data_white, data_dark..)
# dxchange.reader.read_hdf5(fname, "/exchange/data", slc=None, dtype=None, shared=False)


print("here")
