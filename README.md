# BEATS_recon

[TomoPy](https://tomopy.readthedocs.io/en/latest/) reconstruction scripts, notebooks and examples for the [BEATS beamline](https://beats-sesame.eu/) of [SESAME](https://www.sesame.org.jo/). <br />
Datasets for running the tests can be found on the [TomoBank](https://tomobank.readthedocs.io/en/latest/)

## BEATS recon notebook
- [ ] file select: [ipyfilechooser](https://github.com/crahan/ipyfilechooser); [solara](https://solara.dev/api/file_browser)
- [ ] ipywidget COR [IntSlider](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#intslider)
- [ ] ipywidget recon write range [FloatRangeSlider](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#floatrangeslider)
- [ ] launch ImageJ
- [ ] phase contrast [Checkbox](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#checkbox)
  - [ ] get phase retrieval params from exchange
- [ ] stripe removal [Checkbox](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20List.html#checkbox)
- [ ] _add to master_ button
- [ ] recon parameter table input
- [ ] (?) visualize master ([examples](https://pbpython.com/dataframe-gui-overview.html))
- [ ] sections / narrative
- [ ] generate slurm `bash` script from master

## BEATS recon script
- [ ] argparse
- [ ] help
- [ ] phase retrieval

## Tests:
### rum@sesame:
- [X] (OK) kblt spring reconstruction (SED dataset; small)
- [X] (OK) visualization with matplotlib
- [X] (OK) import recon_utils module; visualization
- [X] (OK) imagej
- [X] (OK) ASTRA GPU reconstruction (FBP, SIRT)
- [X] (OK) tomcat 180deg CPU recon (FBP, GRIDREC)
- [X] (OK) tomcat 180deg GPU recon (FBP, SIRT)
- [X] (OK) slurm sbatch process
- [X] (OK) recon on cpunode
- [X] tomopy-cli
  - [X] (OK) `gridrec`
  - [X] (fail) `fpb` - not supported yet
  - [X] (fail) `sirt` - not supported yet
  - [X] (fail) `lprec` - `ModuleNotFoundError: No module named 'lprec'`
  - [X] (fail) `astrasirt` - `File "astra/data2d_c.pyx", line 89, in astra.data2d_c.create
ValueError: The dimensions of the data do not match those specified in the geometry: (2000, 2560) != (2001, 2560)`
- [X] (fail) tomcat 360deg recon (4001 x 2160 x 2560) (out-of-memory during flat field correct on cpunode@rum)
  - [X] (OK) complete on BL-BEATS-WS01 (recon shape: 4129 x 4129 x 2160) (tomopy gridrec; ncore=36; 172sec; 303G/503G)
- [ ] tomocupy

---
## Milestones:
#### LEVEL 1 - beginner
- [x] **absorption** reco
- [x] **read HDF5**
- [x] **COR** optimization
- [x] write **output TIFF stack** of slices
- [x] circular mask
- [x] control **bitdepth** of output slices
- [x] **phase retrieval** algorithms in TomoPy
- [x] **tomopy-cli** full recon
- [x] store and load **config files** for command line recon
- [x] **360deg recon** (extended Field Of View)
#### LEVEL 2 - intermediate
- [X] **HPC cluster** TomoPy build
- [X] **MP reco**
- [X] **GPU reco**
- [X] normalize to uint8 using 'numexpr' (see nersc_tomopy)
- [ ] phase retrieval with **PyPhase**
- [ ] test different **Ring removal** algorithms
- [ ] test different **Filters**
#### LEVEL 3 - expert
- [ ] TomoPy recon **GUI**
- [ ] print **recon report** (Latex)
- [ ] **batch recon** from .CSV table using pandas (through config files)
___

## Examples:
- [TomoPy TEST 01](examples/TomoPy_test01.ipynb)
    - Complete TomoPy reconstruction pipeline on (small) TOMCAT sample data
    - Absorption reco
    - Opens Fiji for visualization of results using ImageJ macro [FolderOpener_virtual.ijm](https://gitlab.com/sesame_beats/imagej_utils/-/blob/master/macros/FolderOpener_virtual.ijm)
    - Optimization of Center Of Rotation
- [TomoPy TEST 2](examples/phase_retrieval/TomoPy_test02_PhaseRetrieval_TomoPy.ipynb)
    - Phase retrieval recon (Paganin) using TomoPy
- [TomoPy TEST 3](examples/TomoPy_test03_tomopy-cli.ipynb)
    - Instructions for recon using the TomoPy Command Line Interface (tomopy-cli)