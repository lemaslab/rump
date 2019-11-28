#!/bin/bash
#SBATCH --job-name=nf_aftermzmine
#SBATCH --mail-type=ALL #Changed ALL to NONE
#SBATCH --mail-user=xinsongdu@ufl.edu
#SBATCH --ntasks=10
#SBATCH --mem=20gb
#SBATCH --account=djlemas
#SBATCH --qos=djlemas-b
#SBATCH --time=10:00:00
#SBATCH --output=./logs/nf_aftermzmine_%j.log
pwd; hostname; date

# load modules
ml R
ml nextflow/18.10.1
ml singularity
SINGULARITYENV_TMPDIR=$(pwd)/tmp
export SINGULARITYENV_TMPDIR
TMPDIR=$(pwd)/tmp
# XDG_RUNTIME_DIR=$(pwd)/singularity_cache
export TMPDIR

nextflow run_R_postprocessing.nf -with-singularity docker://galaxydream/mzmine_oldversion
date
