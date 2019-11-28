#!/bin/bash
#SBATCH --job-name=nf_r_processing_sample
#SBATCH --mail-type=ALL #Changed ALL to NONE
#SBATCH --mail-user=xinsongdu@ufl.edu
#SBATCH --ntasks=20
#SBATCH --mem=200gb
#SBATCH --account=djlemas
#SBATCH --qos=djlemas-b
#SBATCH --time=20:00:00
#SBATCH --output=./logs/nf_all_%j.log
pwd; hostname; date

# load modules
ml R
ml nextflow/18.10.1
ml singularity
SINGULARITYENV_TMPDIR=$(pwd)/tmp
export SINGULARITYENV_TMPDIR
TMPDIR=$(pwd)/tmp
export TMPDIR

nextflow run_all.nf --pos_mzmine_peak_output pos_data.csv --neg_mzmine_peak_output neg_data.csv -with-singularity docker://galaxydream/mzmine_oldversion
date
