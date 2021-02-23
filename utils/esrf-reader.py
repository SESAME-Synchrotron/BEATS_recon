import numpy as np
import h5py
from enum import Enum
import time


def read_esrf_data(filepath):
	class ImageKeys(Enum):
		Projection = 0
		Flat = 1
		Dark = 2
		Invalid = 3

	datafile = h5py.File(filepath,'r')

	image_key = np.array(datafile["/entry/instrument/detector/image_key"])
	data      = datafile["/entry/instrument/detector/data"]
	nFrames = data.shape[0]
	ang = datafile["/entry/sample/rotation_angle"]

	views = [[],[],[],[]]
	angles = [[],[],[],[]]

	proj_idx    = np.where(image_key ==ImageKeys.Projection.value)
	flat_idx    = np.where(image_key ==ImageKeys.Flat.value)
	dark_idx    = np.where(image_key ==ImageKeys.Dark.value)
	invalid_idx = np.where(image_key ==ImageKeys.Invalid.value)

	for frame in range(nFrames):
		dataview    = data[frame:frame+1].view()
		key         = image_key[frame]
		#print("Frame: #{} | key: {}".format(frame,key))
		views[key].append(dataview)
		angles[key].append(ang[frame])
	
	datafile.close()
	projViews ,flatViews, darkViews, invalidViews = views
	projAngles ,flatAngles, darkAngles, invalidAngles = angles

	print("Number of projection frames: {}".format(len(projViews)))
	print("Number of flat-field frames: {}".format(len(flatViews)))
	print("Number of dark-current frames: {}".format(len(darkViews)))
	print("Number of invalid frames: {}".format(len(invalidViews)))

	print("Number of projection angles: {}".format(len(projAngles)))
	print("Number of flat-field angles: {}".format(len(flatAngles)))
	print("Number of dark-current angles: {}".format(len(darkAngles)))
	print("Number of invalid angles: {}".format(len(invalidAngles)))
	return projViews ,flatViews, darkViews, invalidViews, projAngles ,flatAngles, darkAngles, invalidAngles 

proj, flat, dark, invalid, projang, flatang, darkang, invalidang  = read_esrf_data("/home/Tomodata/bamboo/bamboo.h5")