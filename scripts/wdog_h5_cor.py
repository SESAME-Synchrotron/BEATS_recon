#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Watch for .H5 file generation.
Run this watchdog with the command:
    wdog_h5_cor.py /folder/to/watch/

"""

import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        if event.src_path.endswith('.h5'):
            print("Got event for .H5 file %s" % event.src_path)

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