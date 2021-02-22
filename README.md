# TomoPy_tests

Tests of tomographic reconstruction with [TomoPy](https://tomopy.readthedocs.io/en/latest/) <br />
A dataset for running these tests can be found [here](https://sesamejo-my.sharepoint.com/:f:/g/personal/gianluca_iori_sesame_org_jo/Ei7H2BsgcgZMqiMqEzER-5oBoUlZCwY84sKT3D5i1hPc_Q?e=GgsAR6)

---
### Milestones:
#### LEVEL 1 - beginner
- [x] **absorption** reco
- [x] **read HDF5**
- [ ] **phase retrieval**
- [x] **COR** optimization
- [x] write **output TIFF stack** of slices
- [ ] **360deg reco** (extended Field Of View)
- [x] circular mask
- [ ] **Ring removal** algorithms
#### LEVEL 2 - intermediate
- [ ] **HPC cluster** TomoPy build
- [ ] **MP reco**
- [ ] **GPU reco**
#### LEVEL 3 - expert
- [ ] **batch reco** from .CSV table using pandas
- [ ] print **reco report** (Latex)
- [ ] reco from **config file**

___
### Notebooks of TomoPy tests:
- [TomoPy_test01.ipynb](TomoPy_test01.ipynb)
    - Complete TomoPy reconstruction pipeline on (small) TOMCAT sample data
    - Absorption reco
    - Opens Fiji for visualization of results using ImageJ macro [FolderOpener_virtual.ijm](https://gitlab.com/sesame_beats/imagej_utils/-/blob/master/macros/FolderOpener_virtual.ijm)
    - Optimization of Center Of Rotation
