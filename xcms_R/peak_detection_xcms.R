# LCMS data preprocessing and analysis with xcms

library(xcms)
library(optparse) # add this library to enable argparse arguments
options(warn=-1)

packageVersion("xcms")
## Define input and output arguments
option_list = list(
    make_option(c("-i", "--input"), type="character", default="./data/DCSM/DCSM.mzXML", 
              help="input folder location", metavar="character"),
    make_option(c("-a", "--mzTolerance"), type="double", default=0.01, 
              help="mz tolerance for peak detection", metavar="character"),
    make_option(c("-b", "--peakwidth_low"), type="double", default=0.6, 
              help="lower bound of peakwidth", metavar="character"),
    make_option(c("-c", "--peakwidth_high"), type="double", default=30.0, 
              help="higher bound of peakwidth", metavar="character"),
    make_option(c("-d", "--noise"), type="integer", default=100, 
              help="noise value", metavar="character"),
    make_option(c("-e", "--prefilter_low"), type="integer", default=1, 
              help="lower bound of prefilter", metavar="character"),
    make_option(c("-f", "--prefilter_high"), type="integer", default=1000, 
              help="higher bound of prefilter", metavar="character"),
    make_option(c("-g", "--integrate"), type="integer", default=2, 
              help="integrate value", metavar="character"),
    make_option(c("-j", "--outfile"), type="character", default="/Users/xinsongdu/mnt/projects/metabolomics_data_processing/results/xcms_dcsm_peaks.csv", 
              help="name of output peak table file", metavar="character"),
    make_option(c("-k", "--ppm"), type="integer", default=25, 
              help="part per million of m/z tolerance for peak detection", metavar="character"),
    make_option(c("-o", "--outdir"), type="character", default="/Users/xinsongdu/mnt/projects/metabolomics_data_processing/reports/xcms_mod_out", 
              help="output folder including output information", metavar="character")
); 
 
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

## Data Import
## ------------

## Get the full path to the CDF files
files <- opt$input

xr<-xcmsRaw(files)

xdata <- findPeaks.centWave(xr, ppm = opt$ppm, peakwidth = c(opt$peakwidth_low, opt$peakwidth_high), noise = opt$noise, prefilter = c(opt$prefilter_low,opt$prefilter_high), integrate = opt$integrate) #, out_dir = opt$outdir)
write.csv(xdata@.Data, opt$outfile)