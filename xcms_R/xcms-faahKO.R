# LCMS data preprocessing and analysis with xcms

# 26 June 2018
# Package
# xcms 3.3.2
# 
# Package: xcms
# Authors: Johannes Rainer
# Modified: 2018-05-28 16:46:20
# Compiled: Tue Jun 26 18:48:06 2018

# Notes: https://www.ebi.ac.uk/training/online/course/lcms-data-analysis-xcms-and-metfrag-phenomenal

# Data
# https://bioconductor.org/packages/release/data/experiment/html/faahKO.html

# BOOT into docker container
# docker run -ti bioconductor/release_metabolomics2 R

library(xcms)
library(faahKO)
library(RColorBrewer)
library(pander)
library(magrittr)
library(optparse) # add this library to enable argparse arguments

## Define input and output arguments
option_list = list(
    make_option(c("-i", "--input"), type="character", default="/Users/xinsongdu/Library/R/3.5/library/faahKO/cdf", 
              help="input folder location", metavar="character"),
    make_option(c("-p", "--plot1"), type="character", default="chromatograms_1_mqc.jpeg", 
              help="the file name and location of the first chromatograms plot", metavar="character"),
    make_option(c("-q", "--plot2"), type="character", default="ion_current_mqc.jpeg", 
              help="the file name and location of the box plot", metavar="character"),
    make_option(c("-r", "--plot3"), type="character", default="chromatograms_2_mqc.jpeg", 
              help="the file name and location of the second chromatograms plot", metavar="character")
); 
 
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

## Data Import
## ------------

## Get the full path to the CDF files
files <- dir(opt$input, full.names = TRUE,
            recursive = TRUE)

# add flaxibility to sample_group and sample_name to the original file
sg = c()
sn = c()
for (name in strsplit(files, "/")){
    sg = append(sg, name[length(name) - 1])
    sn = append(sn, name[length(name)])
}

## Create a phenodata data.frame
    # modified sample_name and sample_group of the original file
pd <- data.frame(sample_name = sn,
                 sample_group = sg,
                 stringsAsFactors = FALSE) 


## load the raw data as an OnDiskMSnExp object using the readMSData method 
## from the MSnbase package.
raw_data <- readMSData(files = files, pdata = new("NAnnotatedDataFrame", pd),
                       mode = "onDisk") 
  # The OnDiskMSnExp object contains general information about the number of spectra, 
  # retention times, the measured total ion current etc, but does not contain the 
  # full raw data (i.e. the m/z and intensity values from each measured spectrum).

## Initial data inspection
## -----------------------

# extract the retention time values from the object.
head(rtime(raw_data)) 

# returns a numeric vector that provides the mapping of the values to 
# the originating file
mzs <- mz(raw_data)

## Split the list by file
mzs_by_file <- split(mzs, f = fromFile(raw_data))
length(mzs_by_file) 

## Get the base peak chromatograms. This reads data from the files.
bpis <- chromatogram(raw_data, aggregationFun = "max")
## Define colors for the two groups
group_colors <- brewer.pal(3, "Set1")[1:2]
names(group_colors) <- unique(sg) # Change the exact name to unique values of sample_group to improve the flexibility

## Plot all chromatograms.
jpeg(opt$plot1)    # add code to plot the figure then save it to file
plot(bpis, col = group_colors[raw_data$sample_group])
dev.off() # close file
## note: create a total ion chromatogram we could set aggregationFun to sum.

# The chromatogram method returned a Chromatograms object that organizes individual
# Chromatogram objects (which in fact contain the chromatographic data) in a 
# two-dimensional array: columns represent samples and rows (optionally) m/z 
# and/or retention time ranges. Below we extract the chromatogram of the first 
# sample and access its retention time and intensity values.

bpi_1 <- bpis[1, 1]
head(rtime(bpi_1))
head(intensity(bpi_1)) 

# Below we create boxplots representing the distribution of total ion 
# currents per file. Such plots can be very useful to spot problematic or 
# failing MS runs.

## Get the total ion current by file
tc <- split(tic(raw_data), f = fromFile(raw_data))
jpeg(opt$plot2)    # add code to plot the figure then save it to file
boxplot(tc, col = group_colors[raw_data$sample_group],
        ylab = "intensity", main = "Total ion current")
dev.off() # close file

## Chromatographic peak detection

#To evaluate the typical chromatographic peak width we plot the EIC for one peak.

## Define the rt and m/z range of the peak area
rtr <- c(2700, 2900)
mzr <- c(334.9, 335.1)
## extract the chromatogram
chr_raw <- chromatogram(raw_data, mz = mzr, rt = rtr)
jpeg(opt$plot3)    # add code to plot the figure then save it to file
plot(chr_raw, col = group_colors[chr_raw$sample_group]) 

raw_data %>%
  filterRt(rt = rtr) %>%
  filterMz(mz = mzr) %>%
  plot(type = "XIC") 
dev.off() # close file
## Below we perform the chromatographic peak detection using the 
## findChromPeaks method. The submitted parameter object defines which 
## algorithm will be used and allows to define the settings for this algorithm. 
## Note that we set the argument noise to 1000 to slightly speed up the analysis
## by considering only signals with a value larger than 1000 in the peak 
## detection step.

cwp <- CentWaveParam(peakwidth = c(30, 80), noise = 1000)
xdata <- findChromPeaks(raw_data, param = cwp) 

# print(xdata)