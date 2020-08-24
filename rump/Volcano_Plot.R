#Library your packages
library(ggplot2)
library(gridExtra)
library(plotly)
library(dplyr)
library(psych)
library(processx)
library(optparse)
library(cmmr)

# 20 Digits Precision Representation
options(scipen = 20)
# If shows every warning
options(warn = -1)

setwd("/Users/xu.ke/Dropbox (UFL)/Research/Active/20200707_RUMP/DATA0")

# Define input and output arguments
option_list <- list(
  make_option(c("-i", "--input"), type = "character",
              default = "pos_data_after_blank_subtraction.csv",
              help = "input data file"),
  make_option(c("-c", "--fc_col"), type = "character",
              default = "fold_change.group1.versus.group2.",
              help = "column name indicating fold change values"),
  make_option(c("-p", "--padjust_col"), type = "character",
              default = "adjusted_p_value",
              help = "column name indicating padjusted values"),
  make_option(c("-l", "--label_col"), type = "character",
              default = "label",
              help = "sample identifier"),
  make_option(c("-r", "--outliers"), type = "character",
              default = "yes",
              help = "if ignore outliers"),
  make_option(c("-b", "--boxplot"), type = "character",
              default = "outliers_boxplot.png",
              help = "output outliers boxplot path and plot file name"),
  make_option(c("-s", "--outliers_tb"), type = "character",
              default = "outliers.csv",
              help = "output outliers table path and plot file name"),
  make_option(c("-o", "--volcano_plot"), type = "character",
              default = "volcano_plot.html",
              help = "output volcano path and plot file name")
);

opt_parser <- OptionParser(option_list = option_list);
opt <- parse_args(opt_parser);

#####################
# read data
sample_data <- read.csv(file = opt$input)
sample_data$Fold <- sample_data[, opt$fc_col]
#adjusted p.value
sample_data$FDR <- sample_data[, opt$padjust_col]
sample_data$external_gene_name <- sample_data[, opt$label_col]
sample_data[, "value_name"] <- "Fold"


# Check outliers for Fold value and deleted outliers
p <- ggplot(data = sample_data) +
  aes(x = value_name, y = abs(Fold)) +
  geom_boxplot(outlier.colour = "red", outlier.shape = 8, outlier.size = 4) +
  geom_jitter(shape = 16, position = position_jitter(0.2)) +
  ggtitle("Boxplot of abs(Fold), outliers highlighted") +
  theme_classic()
png(opt$boxplot)
p
dev.off()

#Outliers table
is_outlier <- function(x) {
  return(x < quantile(x, 0.25) - 1.5 * IQR(x) |
           x > quantile(x, 0.75) + 1.5 * IQR(x))
}
outliers_table <- sample_data[is_outlier(sample_data$Fold), ]

write.csv(outliers_table, opt$outliers_tb)

# if deleted fold's outliers
outliers<-outliers_table$Fold
if (opt$outliers == "yes") {
  sample_data <- sample_data[-which(sample_data$Fold %in% outliers), ]
}

# add a grouping column; default value is "not significant"
sample_data["group"] <- "NonSignificant"

# for our plot, we want to highlight
# FDR < 0.05 (significance level)
# Fold Change > 1.5

# change the grouping for the entries with significance but not a large enough Fold change
sample_data[which(sample_data["FDR"] < 0.01 & abs(sample_data["Fold"]) < 1.5), "group"] <- "Significant"

# change the grouping for the entries a large enough Fold change but not a low enough p value
sample_data[which(sample_data["FDR"] > 0.01 & abs(sample_data["Fold"]) > 1.5), "group"] <- "FoldChange"

# change the grouping for the entries with both significance and large enough fold change
sample_data[which(sample_data["FDR"] < 0.01 & abs(sample_data["Fold"]) > 1.5), "group"] <- "Significant&FoldChange"


# Find and label the top peaks..
top_peaks <- sample_data[with(sample_data, order(Fold, FDR)), ][1:5, ]
top_peaks <- rbind(top_peaks, sample_data[with(sample_data, order(-Fold, FDR)), ][1:5, ])

# Add gene labels for all of the top genes we found
# here we are creating an empty list, and filling it with entries for each row in the dataframe
# each list entry is another list with named items that will be used by Plot.ly
a <- list()
for (i in seq_len(nrow(top_peaks))) {
  m <- top_peaks[i, ]
  a[[i]] <- list(
    x = m[["Fold"]],
    y = -log10(m[["FDR"]]),
    text = m[["external_gene_name"]],
    xref = "x",
    yref = "y",
    showarrow = TRUE,
    arrowhead = 0.5,
    ax = 20,
    ay = -40
  )
}

# make the Plot.ly plot
p <- plot_ly(data = sample_data, x = ~Fold, y = ~-log10(FDR),
             mode = "markers", color = ~group) %>%
  layout(title = "Volcano Plot") %>%
  layout(annotations = a)
htmlwidgets::saveWidget(p, file = opt$volcano_plot)