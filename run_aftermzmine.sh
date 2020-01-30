#!/bin/bash
#SBATCH --job-name=nf_aftermzmine
#SBATCH --mail-type=ALL #Changed ALL to NONE
#SBATCH --mail-user=xinsongdu@ufl.edu
#SBATCH --ntasks=1
#SBATCH --mem=5gb
#SBATCH --account=djlemas
#SBATCH --qos=djlemas-b
#SBATCH --time=10:00:00
#SBATCH --output=./logs/nf_aftermzmine_%j.log
pwd; hostname; date

# load modules
ml R
ml nextflow
ml singularity
SINGULARITYENV_TMPDIR=$(pwd)/tmp
export SINGULARITYENV_TMPDIR
TMPDIR=$(pwd)/tmp
# XDG_RUNTIME_DIR=$(pwd)/singularity_cache
export TMPDIR

nextflow run_aftermzmine.nf --cutoff 0.000004 --input_dir_pos /ufrc/djlemas/xinsongdu/jupyter_notebook/data/metabolomics/Human_Bovine/mzXML/POS_HumanVSBovine --input_dir_neg /ufrc/djlemas/xinsongdu/jupyter_notebook/data/metabolomics/Human_Bovine/mzXML/NEG_HumanVSBovine --POS_design_path ./data/pos_design_HumanVSBovine.csv --NEG_design_path ./data/neg_design_HumanVSBovine.csv -with-singularity docker://galaxydream/metabolomics_pipeline
date
