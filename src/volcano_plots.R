# 2019.07.14. ask
rm(list=ls(all=TRUE))

# Code reference: https://www.biostars.org/p/214100/

# 20 Digits Precision Representation
options(scipen=20)

# Setting the correct working directory.
# NOTE!!! -> Can be linked differently on different computers.
setwd("/Users/xinsongdu/mnt/projects/milk_analysis")
# Extra check
getwd()


# loading library for rows standard deviations
suppressPackageStartupMessages(library("plotly"))
library(optparse) # add this library to enable argparse arguments
options(warn=-1)

## Define input and output arguments
option_list = list(
  make_option(c("-i", "--input_file"), type="character", default="./data/milk_data_pos_ph_summaries_filter_allgroups_threshold_100_modified.csv", 
              help="input csv file", metavar="character"),
  make_option(c("-o", "--output_file"), type="character", default="./results/figs/volcano_plot", 
              help="output plot file", metavar="character")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

# Read dataframe
df <- read.delim(file = opt$input_file,header = TRUE,sep = ',')
# Display column names of the dataframe
colnames(df)

# for our plot, we want to highlight 
# p-value < 0.001 (significance level)
# Fold Change > 1.5

# add a grouping column; default value is "not significant"
df["group1"] <- "NotSignificant"

# comparison of skim and whole
# change the grouping for the entries with significance but not a large enough Fold change
df[which(df['p_value_whole_skim_anova'] < 0.001 & abs(df['foldchange_skim_whole']) < 1.5 ),"group1"] <- "Significant"
# change the grouping for the entries a large enough Fold change but not a low enough p value
df[which(df['p_value_whole_skim_anova'] > 0.001 & abs(df['foldchange_skim_whole']) > 1.5 ),"group1"] <- "FoldChange"
# change the grouping for the entries with both significance and large enough fold change
df[which(df['p_value_whole_skim_anova'] < 0.001 & abs(df['foldchange_skim_whole']) > 1.5 ),"group1"] <- "Significant&FoldChange"

# Find and label the top peaks..
top_peaks <- df[with(df, order(foldchange_skim_whole, p_value_whole_skim_anova)),][1:5,]
top_peaks <- rbind(top_peaks, df[with(df, order(-foldchange_skim_whole, p_value_whole_skim_anova)),][1:5,])

# Add labels for all of the top metabolites we found
# here we are creating an empty list, and filling it with entries for each row in the dataframe
# each list entry is another list with named items that will be used by Plot.ly
a <- list()
for (i in seq_len(nrow(top_peaks))) {
  m <- top_peaks[i, ]
  a[[i]] <- list(
    x = m[["foldchange_skim_whole"]],
    y = -log10(m[["p_value_whole_skim_anova"]]),
    text = m[["label"]],
    xref = "x",
    yref = "y",
    showarrow = TRUE,
    arrowhead = 0.5,
    ax = 20,
    ay = -40
  )
}

# make the Plot.ly plot
p <- plot_ly(data = df, x = ~foldchange_skim_whole, y = ~logpvalue_whole_skim, text = ~label, mode = "markers", color = ~group1) %>% 
  layout(title ="Volcano Plot") %>%
  layout(annotations = a)

# add a grouping column; default value is "not significant"
df["group"] <- "NotSignificant"

# comparison of fat and whole
# change the grouping for the entries with significance but not a large enough Fold change
df[which(df['p_value_whole_fat_anova'] < 0.001 & abs(df['foldchange_fat_whole']) < 1.5 ),"group"] <- "Significant"
# change the grouping for the entries a large enough Fold change but not a low enough p value
df[which(df['p_value_whole_fat_anova'] > 0.001 & abs(df['foldchange_fat_whole']) > 1.5 ),"group"] <- "FoldChange"
# change the grouping for the entries with both significance and large enough fold change
df[which(df['p_value_whole_fat_anova'] < 0.001 & abs(df['foldchange_fat_whole']) > 1.5 ),"group"] <- "Significant&FoldChange"

# Find and label the top peaks..
top_peaks <- df[with(df, order(logfoldchange_fat_whole, logp_value_whole_fat_anova)),][1:5,]
top_peaks <- rbind(top_peaks, df[with(df, order(-logfoldchange_fat_whole, logp_value_whole_fat_anova)),][1:5,])

# Add labels for all of the top metabolites we found
# here we are creating an empty list, and filling it with entries for each row in the dataframe
# each list entry is another list with named items that will be used by Plot.ly
a <- list()
for (i in seq_len(nrow(top_peaks))) {
  m <- top_peaks[i, ]
  a[[i]] <- list(
    x = m[["logfoldchange_fat_whole"]],
    y = m[["logp_value_whole_fat_anova"]],
    text = m[["label"]],
    xref = "x",
    yref = "y",
    showarrow = TRUE,
    arrowhead = 0.5,
    ax = 20,
    ay = -40
  )
}

# make the Plot.ly plot
p <- plot_ly(data = df, x = ~logfoldchange_fat_whole, y = ~logpvalue_whole_fat, text = ~label, mode = "markers", color = ~group) %>% 
  layout(title ="Volcano Plot") %>%
  layout(annotations = a)
