#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Watch for .H5 file generation.
Run this watchdog with the command:
    wdog_h5_cor.py /folder/to/watch/

"""
import os.path
import time
import sys
import dxchange
import tomopy
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        if event.src_path.endswith('.h5'):
            print("Got event for .H5 file %s" % event.src_path)
            filesize = os.path.getsize(event.src_path)
            time.sleep(1)
            # wait until file size does not grow anymore
            while os.path.getsize(event.src_path) > filesize:
                filesize = os.path.getsize(event.src_path)
                time.sleep(1)
            try:
                dimension_y = dxchange.read_hdf5(event.src_path, '/measurement/instrument/camera/dimension_y')[0]
                print("Sinogram size: %s" % dimension_y)
                print("Guessing the COR...")

                projs, flats, darks, _ = dxchange.read_aps_32id(event.src_path, exchange_rank=0, sino=(int(dimension_y/2), int(dimension_y/2)+1))
                theta = np.radians(dxchange.read_hdf5(event.src_path, 'exchange/theta'))

                COR = tomopy.find_center(projs, theta, tol=1)[0]
                print("COR guess: %s" % COR)

            except:
                print("Cannot read sinogram size")


if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    observer = Observer()
    event_handler = ExampleHandler() # create event handler
    # set observer to use created handler in directory
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    # sleep until keyboard interrupt, then stop + rejoin the observer
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()