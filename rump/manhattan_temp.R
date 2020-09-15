---
  title: "Manhattan Plot"
author: "Yasmine Gillespie"
date: "6/6/2020"
output: html_document
---
  
  

install.packages("cmmr")
devtools::install_github("lzyacht/cmmr")



library(shiny)
library(ggplot2)
library(dplyr)
library(grid)
library(plotly)
library(manhattanly)
library(forcats)
library(readr)
library(ggrepel)
library(RColorBrewer)
library(tidyr)
library(qqman)
library(argparser)
library(optparse) # add this library to enable argparse arguments
library(cmmr)
library(lintr)


tempdir()
# [1] "C:\Users\XYZ~1\AppData\Local\Temp\Rtmp86bEoJ\Rtxt32dcef24de2"
dir.create(tempdir())




options(warn = -1)

## Define input and output arguments
option_list <- list(
  make_option(c("-i", "--input"),
              type = "character",
              default = "bovine_enriched_unknown.csv",
              help = "input data file"),
  make_option(c("-c", "--mz_col"), type = "character", default = "row.m.z",
              help = "column name indicating m/z values"),
  make_option(c("-n", "--ion"),
              type = "character",
              default = "positive",
              help = "ion mode"),
  make_option(c("-o", "--output"),
              type = "character",
              default = "searched_unknown_pos_after_blank_subtraction.csv",
              help = "output csv file name")
);
opt_parser <- OptionParser(option_list = option_list);
opt <- parse_args(opt_parser);

# read data
data <- rio::import(
  "C:\\Users\\Yasmine\\Documents\\pos_data_after_blank_subtraction.csv")


# extract mz values from data
mzs <- as.vector(data[["row.m.z"]])


if (opt$ion == "negative") {
  adduct <- '["M-H"]'
} else {
  adduct <- '["M+H"]'
}

# batch search
batch_df <- batch_search("http://ceumass.eps.uspceu.es/mediator/api/v3/batch",
                         "all-except-peptides",
                         "['all-except-mine']",
                         "mz",
                         opt$ion,
                         adduct,
                         5,
                         "ppm",
                         mzs)
if (typeof(batch_df) == "character") {
  data_merge <- data.frame(Empty = character())
} else {
  data_merge <- merge(data, batch_df,
                      by.x = "row.m.z", by.y = "experimental_mass")
}

write.csv(data_merge, opt$output, row.names = FALSE)

      
new_data <- data %>%
  select("row", "time", "p_value", "adjusted_p_value")


       
mz_data <- data %>%
  select("row", "p_value", "adjusted_p_value")


        
time_data <- data %>%
  select("time", "p_value", "adjusted_p_value")


# Basic dot plot MZ data
metabolite_data <- mz_data$row
yval <- -log10(mz_data$p_value)
plot(Metabolite, yval)
abline(h = -log10(0.050000877), col = "blue")
abline(h = -log10(0.005508435), col = "blue")

      
# Basic dot plot MZ data
time_s <- time_data$time
yval <- -log10(time_data$p_value)
plot(Time, yval)
abline(h = -log10(0.050000877), col = "blue")
abline(h = -log10(0.005508435), col = "blue")

       
# check code quality
library(lintr)
# replace your path of .R file
lint("C:\\Users\\Yasmine\\Documents\\R\\Manhattan_Plot.rmd")
