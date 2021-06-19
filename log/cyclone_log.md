## Cyclone recon log
Last update: 19.06.2021

COR for file `test_00_.h5`: **486.5**

COR for file `8671_8_B_01_.h5`: **1303**
______________________________________
### BASICS
#### ssh to Cyclone
`ssh -X jo21gi1@cyclone.hpcf.cyi.ac.cy`

#### Inspect user queue
`squeue -u jo21gi1`

#### Run batch script
`sbatch ./run_tomopy_testCyclone_recon_algorithms_comparison.sh`

#### Copy data from Cyclone to local computer
`scp jo21gi1@cyclone.hpcf.cyi.ac.cy://nvme/h/jo21gi1/scratch/recon/algorithm_test/sirt_XY.tiff ./`
______________________________________
### SINGULARITY
#### Preliminary operations with Singularity
setup home and data folders

`export SINGULARITY_HOME=$HOME:/home`

`export SINGULARITY_BINDPATH="/onyx/data/p029:/data,/nvme/h/jo21gi1/code:/mnt,/nvme/h/jo21gi1/scratch:/scratch"`

#### Run .py recon script (deprecated; use tomopy-cli instead)
`singularity exec /nvme/h/jo21gi1/tomopy.sif python /mnt/tomopy_tests/scripts/tomopy_test01_script_noDXchange.py`

`singularity exec --nv production_tomopy.sif python beats_recostruction.py`

#### Run shell within container
`singularity shell tomopy.sif`

With Nvidia support: `singularity shell -nv tomopy.sif`

#### Comparison of different recon algorithms
1. Login to Cyclone and export `SINGULARITY_HOME` and `INGULARITY_BINDPATH` as above.

______________________________________
### TOMOPY-CLI
#### Init tomopy-cli configuration file
`tomopy init --config ./tomopy_conf/test_00.conf`

Modify the conf file as needed..
#### Run recon using tomopy-cli within singularity
`tomopy recon --config tomopy_conf/test_00.conf --reconstruction-type slice --file-name /tmp/test_00_/test_00_.h5`

#### Recon script (tomopy-cli)
``

----
### SBATCH OPTIONS
- `#SBATCH --job-name=recon_test    # Job name`
- `#SBATCH --nodes=1`
- `#SBATCH –-ntasks-per-node=10`


