# TomoPy_tests

Tests of tomographic reconstruction with [TomoPy](https://tomopy.readthedocs.io/en/latest/) <br />
A dataset for running these tests can be found [here](https://sesamejo-my.sharepoint.com/:f:/g/personal/gianluca_iori_sesame_org_jo/Ei7H2BsgcgZMqiMqEzER-5oBoUlZCwY84sKT3D5i1hPc_Q?e=GgsAR6)

## SESAME RUM tests:
- [X] (OK) kblt spring reconstruction (SED dataset; small)
- [X] (OK) visualization with matplotlib
- [X] (OK) import recon_utils module; visualization
- [X] (OK) imagej
- [X] (fail) ASTRA GPU reconstruction (see error 1 below)
- [X] (fail) tomopy-cli (see error 2 below)
- [X] (fail) tomcat 180deg CPU recon (see error 3 below)
- [ ] (fail) tomcat 180deg GPU recon (see error 1 below)
- [ ] tomcat 360deg recon (check memory usage GPU node)
- [ ] tomocupy
- [ ] jupyter

### Error report:
1. error launching tomopy cuda reconstruction (with ASTRA): </br>`Error: allocateVolume: CUDA error 35: CUDA driver version is insufficient for CUDA runtime version.`
2. import error when trying to use tomopy-cli: `tomopy-cli recon -h` </br>
  `File "/PETRA/cluster_software/install/anaconda/envs/tomopy/bin/tomopy", line 33, in <module>
    sys.exit(load_entry_point('tomopy-cli==0.3', 'console_scripts', 'tomopy')())
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/bin/tomopy", line 25, in importlib_load_entry_point
    return next(matches).load()
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/lib/python3.10/importlib/metadata/__init__.py", line 171, in load
    module = import_module(match.group('module'))
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/bin/tomopycli.py", line 12, in <module>
    from tomopy_cli import config, __version__
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/lib/python3.10/site-packages/tomopy_cli/config.py", line 21, in <module>
    from tomopy_cli import recon
  File "/PETRA/cluster_software/install/anaconda/envs/tomopy/lib/python3.10/site-packages/tomopy_cli/recon.py", line 12, in <module>
    import meta
ModuleNotFoundError: No module named 'meta'`
3. less than 100GB memory available cause reconstructions to break: ![img_1.png](img_1.png)
4. get several time the following warning when using tomopy. The process nevertheless runs successfully: </br> `Error.  nthreads must be a positive integerError.  nthreads cannot be larger than environment variable "NUMEXPR_MAX_THREADS" (64)`


---
### Milestones:
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

### Examples:
- [TomoPy TEST 01](examples/TomoPy_test01.ipynb)
    - Complete TomoPy reconstruction pipeline on (small) TOMCAT sample data
    - Absorption reco
    - Opens Fiji for visualization of results using ImageJ macro [FolderOpener_virtual.ijm](https://gitlab.com/sesame_beats/imagej_utils/-/blob/master/macros/FolderOpener_virtual.ijm)
    - Optimization of Center Of Rotation
- [TomoPy TEST 2](examples/phase_retrieval/TomoPy_test02_PhaseRetrieval_TomoPy.ipynb)
    - Phase retrieval recon (Paganin) using TomoPy
- [TomoPy TEST 3](examples/TomoPy_test03_tomopy-cli.ipynb)
    - Instructions for recon using the TomoPy Command Line Interface (tomopy-cli)