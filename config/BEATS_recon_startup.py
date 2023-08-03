# Startup configuration script for TomoPy reconstructions at SESAME BEATS
# Copy this file to the IPython startup directory (~/.ipython/profile_default/startup)

# add local path to reconstruction utilities repo
import sys
sys.path.append('/home/beats/PycharmProjects/recon_utils')

# default imports
import os
import dxchange
import tomopy
import numpy as np
import h5py
import matplotlib
import matplotlib.pyplot as plt
import logging
import recon_utils as ru

# matplotlib plotting parameters
matplotlib.rcParams['figure.dpi'] = 300
matplotlib.rc('image', cmap='gray')
plt.style.use('ggplot')

# logging settings
logging.basicConfig(level=logging.INFO)

# Fiji executable
Fiij_exe = '/opt/fiji-linux64/Fiji.app/ImageJ-linux64'
Fiji_exe_stack = Fiij_exe + ' -macro FolderOpener_virtual.ijm '

# ncore setting for BL-BEATS-WS01
ncore = 36

# Left align tables (not working)
from IPython.core.display import HTML
table_css = 'table {align:left;display:block} '
HTML('<style>{}</style>'.format(table_css))
