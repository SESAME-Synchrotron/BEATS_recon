# BEATS_recon: list of features and tests
Below you find a list of tested features and project milestones.

## BEATS recon notebooks
- [ ] pipeline / narrative in single notebooks
    - [X] Minimal absorption pipeline
    - [X] Phase-contrast pipeline
    - [X] Inspect data with napari
    - [X] Convert 360 degree scan to 180
    - [X] Load separate theta array; Compare with simulated theta
    - [ ] Convert reconstruction to `uint8` or `uint16`
    - [ ] Stripe removal
    - [ ] Ring artefact correction
- [X] load HDF5
  - [ ] dxchange `read_beats`
  - [X] load range
  - [X] read theta_readout
- [X] flat field correct
- [X] 360 to 180 degree sinogram
  - [ ] inspect overlap
- [X] phase retrieval
- [X] stripe removal
- [X] log transform
- [X] Center Of Rotation (COR)
  - [X] auto (Vo, Tomopy, ...)
  - [X] save COR range; open in Imagej
- [X] CPU recon
  - [X] single slice
  - [X] view with `napari`
- [X] post-processing
  - [X] circ_mask
  - [X] ring artefact correction
  - [X] 8bit convert
- [X] write output TIFF stack
- [X] imagej launcher

## BEATS recon script
- [ ] documentation
- [X] argparse
- [X] help
- [X] flat field correct
- [X] auto COR
- [X] read phase retrieval params from hdf5 file
- [X] ring artefact correction
- [X] 8bit convert
- [X] 16bit convert
- [X] 360 to 180 degree sinogram
- [X] write output TIFF stack
- inputs:
  - [X] `--recon_dir`
  - [X] `--sino`
  - [X] `--proj`
  - [X] `--cor`
  - [x] `--cormethod`
  - [X] `--360`
  - [X] `--phase`
  - [X] `--alpha`
  - [X] `--circ_mask`
  - [X] `--recon_dtype`
  - [X] `--data_range`
  - [X] `--data_quantiles`
  - [X] `--ncore`
  - [X] `--circ_mask_ratio`
  - [X] `--circ_mask_val`
  - [X] `--midplanes`
  - [X] `--algorithm`

### ipywidgets 
> [!NOTE]  
> This milestone was deleted and moved to the new [`alrecon`](https://github.com/gianthk/alrecon/tree/master) CT reconstruction Solara app.

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
- [ ] generate slurm `bash` script from master

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
- [ ] phase retrieval with **PyPhase** (abandoned)
- [X] test different **Ring removal** algorithms
- [ ] test different **Filters**
#### LEVEL 3 - expert
- [X] TomoPy recon **GUI** `al-recon`
- [ ] print **recon report** (HTML?)
- [ ] **batch recon** from .CSV table using pandas (through config files)

## Examples:
- [TomoPy TEST 01](tests/TomoPy_test01.ipynb)
    - Complete TomoPy reconstruction pipeline on (small) TOMCAT sample data
    - Absorption reco
    - Opens Fiji for visualization of results using ImageJ macro [FolderOpener_virtual.ijm](https://gitlab.com/sesame_beats/imagej_utils/-/blob/master/macros/FolderOpener_virtual.ijm)
    - Optimization of Center Of Rotation
- [TomoPy TEST 2](tests/phase_retrieval/TomoPy_test02_PhaseRetrieval_TomoPy.ipynb)
    - Phase retrieval recon (Paganin) using TomoPy
- [TomoPy TEST 3](tests/TomoPy_test03_tomopy-cli.ipynb)
    - Instructions for recon using the TomoPy Command Line Interface (tomopy-cli)
