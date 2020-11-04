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

    views = [[],[],[],[]]

    proj_idx    = np.where(image_key ==ImageKeys.Projection.value)
    flat_idx    = np.where(image_key ==ImageKeys.Flat.value)
    dark_idx    = np.where(image_key ==ImageKeys.Dark.value)
    invalid_idx = np.where(image_key ==ImageKeys.Invalid.value)

    for frame in range(nFrames):
        dataview    = data[frame:frame+1].view()
        key         = image_key[frame]
        #print("Frame: #{} | key: {}".format(frame,key))
        views[key].append(dataview)

    projViews ,flatViews, darkViews, invalidViews = views
    print("Number of projection frames: {}".format(len(projViews)))
    print("Number of flat-field frames: {}".format(len(flatViews)))
    print("Number of dark-current frames: {}".format(len(darkViews)))
    print("Number of invalid frames: {}".format(len(invalidViews)))
    return projViews ,flatViews, darkViews

proj, flat, dark = read_esrf_data("/home/Tomodata/bamboo/bamboo.h5")