#!/bin/bash
#SBATCH --job-name=mzmine221_milk_fat_sample
#SBATCH --mail-type=ALL #Changed ALL to NONE
#SBATCH --mail-user=xinsongdu@ufl.edu
#SBATCH --ntasks=1
#SBATCH --mem=40gb
#SBATCH --account=djlemas
#SBATCH --qos=djlemas-b
#SBATCH --time=10:00:00
#SBATCH --output=./logs/mzmine221_milk_fat_sample_%j.log
pwd; hostname; date

# load modules
module load R

/ufrc/djlemas/share/xinsongdu/tools/MZmine-2.11/startMZmine_Linux.sh /ufrc/djlemas/share/xinsongdu/projects/milk_analysis/mzconfigs/Metabolomics_MzMine_Batch_pos_removesearch_221_ufrc.xml

date
