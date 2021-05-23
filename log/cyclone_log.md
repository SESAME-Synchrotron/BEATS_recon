## 19.05.21 - Cyclone log
#### ssh to Cyclone
`ssh -X jo21gi1@cyclone.hpcf.cyi.ac.cy`

#### Inspect user queue
`squeue -u jo21gi1`

#### Run batch script
`sbatch ./run_tomopy_testCyclone_recon_algorithms_comparison.sh`

#### Preliminary operations
setup home and data folders

`export SINGULARITY_HOME=$HOME:/home`

`export SINGULARITY_BINDPATH="/onyx/data/p029:/tmp,/nvme/h/jo21gi1/code:/mnt"`

#### Run .py recon script (deprecated; use tomopy-cli instead)
`singularity exec /nvme/h/jo21gi1/tomopy.sif python /mnt/tomopy_tests/scripts/tomopy_test01_script_noDXcha$`

`singularity exec --nv production_tomopy.sif python beats_recostruction.py`

#### Run shell within container
`singularity shell tomopy.sif`

With Nvidia support: `singularity shell -nv tomopy.sif`

#### Init tomopy-cli configuration file
`tomopy init --config ./tomopy_conf/test_00.conf`

Modify the conf file..
#### Run recon using tomopy-cli within singularity
`tomopy recon --config tomopy_conf/test_00.conf --reconstruction-type slice --file-name /tmp/test_00_/test_00_.h5`

#### Recon script (tomopy-cli)
`singularity exec --nv production_tomopy.sif pyt`

486.5
