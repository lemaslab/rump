# 2018.12.19. ask
# rm(list=ls(all=TRUE))

# 20 Digits Precision Representation
options(scipen=20)

# Setting the correct working directory.
# NOTE!!! -> Can be linked differently on different computers.
# setwd("/Users/xinsongdu/mnt/projects/beach01/secimtools")

library(optparse) # add this library to enable argparse arguments
library(cmmr)
options(warn=-1)

## Define input and output arguments
option_list = list(
  make_option(c("-i", "--input"), type="character", default="bovine_enriched_unknown.csv", 
              help="input data file"),
  make_option(c("-c", "--mz_col"), type="character", default="row.m.z", 
              help="column name indicating m/z values"),
  make_option(c("-n", "--ion"), type="character", default="positive", 
              help="ion mode"),
  make_option(c("-o", "--output"), type="character", default="searched_unknown_pos_after_blank_subtraction.csv", 
              help="output csv file name")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

# read data
data <- read.csv(file=opt$input)

# extract mz values from data
mzs = as.vector(data[['row.m.z']])
# mzs = lapply(mzs,round,4)

if (opt$ion=="negative"){
  adduct <- '["M-H"]'
} else {
  adduct <- '["M+H"]'
}

# batch search
batch_df <- batch_search('http://ceumass.eps.uspceu.es/mediator/api/v3/batch',
                             'all-except-peptides',
                             '["all-except-mine"]',
                             'mz',
                             opt$ion,
                             adduct,
                             5,
                             'ppm',
                             c(0.00))
if (typeof(batch_df)=="character"){
  data_merge <- data.frame(Empty=character())
} else {
  data_merge <- merge(data, batch_df, by.x='row.m.z', by.y='experimental_mass')
}

write.csv(data_merge, opt$output, row.names=TRUE)
