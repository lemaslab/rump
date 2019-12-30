#!/bin/bash
#SBATCH --job-name=nf_reproducibility_test
#SBATCH --mail-type=ALL #Changed ALL to NONE
#SBATCH --mail-user=xinsongdu@ufl.edu
#SBATCH --ntasks=20
#SBATCH --mem=200gb
#SBATCH --account=djlemas
#SBATCH --qos=djlemas-b
#SBATCH --time=20:00:00
#SBATCH --output=./logs/nf_reproducibility_test_%j.log
pwd; hostname; date

# load modules
ml R
ml nextflow/18.10.1
ml singularity
SINGULARITYENV_TMPDIR=$(pwd)/tmp
export SINGULARITYENV_TMPDIR
TMPDIR=$(pwd)/tmp
export TMPDIR

nextflow run_all.nf --pos_mzmine_peak_output DCSM.csv --mzmine_dir reproducibility_test/MZmine-2.28/ --neg_mzmine_peak_output VT001.csv --input_dir_pos /ufrc/djlemas/xinsongdu/jupyter_notebook/projects/metabolomics_data_processing/data/DCSM --input_dir_neg /ufrc/djlemas/xinsongdu/jupyter_notebook/projects/metabolomics_data_processing/data/VT001 --bs 0 --batchfile_generator ./reproducibility_test/batchfile_generator.py -with-singularity docker://galaxydream/metabolomics_pipeline
date
