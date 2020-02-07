#!/bin/bash
#SBATCH --job-name=nf_humanbovine
#SBATCH --mail-type=ALL #Changed ALL to NONE
#SBATCH --mail-user=xinsongdu@ufl.edu
#SBATCH --ntasks=20
#SBATCH --mem=200gb
#SBATCH --account=djlemas
#SBATCH --qos=djlemas-b
#SBATCH --time=20:00:00
#SBATCH --output=./logs/nf_humanbovine%j.log
pwd; hostname; date

# load modules
ml R
ml nextflow/18.10.1
ml singularity
SINGULARITYENV_TMPDIR=$(pwd)/tmp
export SINGULARITYENV_TMPDIR
TMPDIR=$(pwd)/tmp
export TMPDIR
unset XDG_RUNTIME_DIR

nextflow run_all.nf --pos_mzmine_peak_output pos_data.csv --neg_mzmine_peak_output neg_data.csv --input_dir_pos /ufrc/djlemas/xinsongdu/jupyter_notebook/data/metabolomics/Human_Bovine/mzXML/POS_HumanVSBovine --input_dir_neg /ufrc/djlemas/xinsongdu/jupyter_notebook/data/metabolomics/Human_Bovine/mzXML/NEG_HumanVSBovine --POS_design_path ./data/pos_design_HumanVSBovine.csv --NEG_design_path ./data/neg_design_HumanVSBovine.csv -with-singularity docker://galaxydream/metabolomics_pipeline
date
