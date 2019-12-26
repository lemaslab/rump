# 2018.12.19. ask
rm(list=ls(all=TRUE))

# 20 Digits Precision Representation
options(scipen=20)

# Setting the correct working directory.
# NOTE!!! -> Can be linked differently on different computers.
# setwd("/Users/xinsongdu/mnt/projects/beach01/secimtools")
# Extra check
getwd()

library(xcms)
library(optparse) # add this library to enable argparse arguments
options(warn=-1)

## Define input and output arguments
option_list = list(
  make_option(c("-c", "--input_pos_data"), type="character", default="Lemas_POS_mzmine_ht_17DEC18_data.csv", 
              help="input POS data file", metavar="character"),
  make_option(c("-d", "--input_neg_data"), type="character", default="Lemas_NEG_mzmine_ht_17DEC18_data.csv", 
              help="input NEG data file", metavar="character")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

# Reading Data files Into R.
# pos
files_pos = dir(opt$input_pos_data, full.names = TRUE, recursive = TRUE)
# neg
files_neg = dir(opt$input_neg_data, full.names = TRUE, recursive = TRUE)

# Checking The Input
dim(milk_data_pos_ph_raw)
dim(milk_data_neg_ph_raw)