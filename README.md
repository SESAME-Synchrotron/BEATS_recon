# TomoPy_tests

Tests of tomographic reconstruction with [TomoPy](https://tomopy.readthedocs.io/en/latest/) <br />
A dataset for running these tests can be found [here](https://sesamejo-my.sharepoint.com/:f:/g/personal/gianluca_iori_sesame_org_jo/Ei7H2BsgcgZMqiMqEzER-5oBoUlZCwY84sKT3D5i1hPc_Q?e=GgsAR6)

### 2 DO:
- [ ] normalize to uint8 using 'numexpr' (see nersc_tomopy)

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
- [ ] **HPC cluster** TomoPy build
- [ ] **MP reco**
- [ ] **GPU reco**
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