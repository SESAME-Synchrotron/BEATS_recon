#!/usr/bin/env python
import os

job_name = 'BEATS_recon_pippo'
h5file = 'pippo.h5'
recon_dir = 'pippo/recon/'
work_dir = 'pippo/'
COR = 55

def mkdir_p(dir):
    '''make a directory (dir) if it doesn't exist'''
    if not os.path.exists(dir):
        os.mkdir(dir)


# job_directory = "%s/.job" % os.getcwd()
job_directory = "%s/pippo" % os.getcwd()
# scratch = os.environ['SCRATCH']
# data_dir = os.path.join(scratch, '/project/LizardLips')

# Make top level directories
mkdir_p(job_directory)
# mkdir_p(data_dir)

job_file = os.path.join(job_directory, "%s.job" % job_name)
# job_data = os.path.join(data_dir, job_name)

# Create job directories
# mkdir_p(job_data)

# assemble python command string
py_command = ('python BEATS_recon.py {0} '
              '--recon_dir {1} '
              '--work_dir {2} '
              '--cor {3}\n'.format(h5file, recon_dir, work_dir, COR))

# write job file
with open(job_file, "x") as fh:
    fh.writelines("#!/bin/bash\n")
    fh.writelines("#SBATCH --job-name={0}%j\n".format(job_name))
    fh.writelines("#SBATCH --output=.out{0}%j.out\n".format(job_name))
    fh.writelines("#SBATCH --error=.out/{0}%j.err\n".format(job_name))
    fh.writelines("#SBATCH --ntasks=48\n")
    fh.writelines("#SBATCH --cpus-per-task=2\n")
    fh.writelines("#SBATCH --time=00:30:00\n")
    fh.writelines("#SBATCH --partition=cpu\n")
    fh.writelines("#SBATCH --mem-per-cpu=2\n\n")
    # fh.writelines("#SBATCH --qos=normal\n")
    # fh.writelines("#SBATCH --mail-type=ALL\n")
    # fh.writelines("#SBATCH --mail-user=$USER@stanford.edu\n")

    fh.writelines("# Modules section:\n")
    fh.writelines("ml load anaconda/tomopy\n\n")
    fh.writelines("# Variables section:\n")
    fh.writelines("export NUMEXPR_MAX_THREADS=96\n\n")

    fh.writelines(py_command)

# launch slurm job
# os.system("sbatch %s" % job_file)