# 2018.12.18. ask
rm(list=ls(all=TRUE))

# 20 Digits Precision Representation
options(scipen=20)

# Setting the correct working directory.
# NOTE!!! -> Can be linked differently on different computers.
# setwd("E:/Alexander/UF Research/2018 - Lemas Milk Metabolomics")
# Extra check
getwd()

# Library for matrix row standard deviations
library("matrixStats")

library(optparse) # add this library to enable argparse arguments
options(warn=-1)

## Define input and output arguments
option_list = list(
  make_option(c("--input_POS_data"), type="character", default="milk_data_pos_ph.Rdata", 
              help="input POS data file", metavar="character"),
  make_option(c("--input_NEG_data"), type="character", default="milk_data_neg_ph.Rdata", 
              help="input NEG data file", metavar="character"),
  make_option(c("--input_POS_blankbased"), type="character", default="milk_data_pos_ph_blankbased.Rdata", 
              help="input POS blankbased file", metavar="character"),
  make_option(c("--input_NEG_blankbased"), type="character", default="milk_data_neg_ph_blankbased.Rdata", 
              help="input NEG blankbased file", metavar="character"),
  make_option(c("--input_POS_anova"), type="character", default="milk_data_pos_ph_anova.Rdata", 
              help="output POS anova file", metavar="character"),
  make_option(c("--input_NEG_anova"), type="character", default="milk_data_neg_ph_anova.Rdata", 
              help="output NEG anova file", metavar="character"),
  make_option(c("--input_POS_kruskalwallis"), type="character", default="milk_data_pos_ph_kruskalwallis.Rdata", 
              help="output POS kruskalwallis file", metavar="character"),
  make_option(c("--input_NEG_kruskalwallis"), type="character", default="milk_data_neg_ph_kruskalwallis.Rdata", 
              help="output NEG kruskalwallis file", metavar="character"),
  make_option(c("--output_POS_allgroups_threshold_005"), type="character", default="milk_data_pos_ph_allgroups_threshold_005.csv", 
              help="output POS allgroups threshold 005 file", metavar="character"),
  make_option(c("--output_NEG_allgroups_threshold_005"), type="character", default="milk_data_neg_ph_allgroups_threshold_005.csv", 
              help="output NEG allgroups threshold 005 file", metavar="character"),
  make_option(c("--output_POS_allgroups_threshold_100"), type="character", default="milk_data_pos_ph_allgroups_threshold_100.csv", 
              help="output POS allgroups threshold 100 file", metavar="character"),
  make_option(c("--output_NEG_allgroups_threshold_100"), type="character", default="milk_data_neg_ph_allgroups_threshold_100.csv", 
              help="output NEG allgroups threshold 100 file", metavar="character"),
  make_option(c("--output_POS_allgroups_threshold_200"), type="character", default="milk_data_pos_ph_allgroups_threshold_200.csv", 
              help="output POS allgroups threshold 200 file", metavar="character"),
  make_option(c("--output_NEG_allgroups_threshold_200"), type="character", default="milk_data_neg_ph_allgroups_threshold_200.csv", 
              help="output NEG allgroups threshold 200 file", metavar="character"),
  make_option(c("--output_POS_raw_filtered_005"), type="character", default="milk_data_pos_filtered_005.csv", 
              help="output POS raw filtered 005 file", metavar="character"),
  make_option(c("--output_NEG_raw_filtered_005"), type="character", default="milk_data_neg_filtered_005.csv", 
              help="output NEG allgroups threshold 005 file", metavar="character"),
  make_option(c("--output_POS_raw_filtered_100"), type="character", default="milk_data_pos_filtered_100.csv", 
              help="output POS raw filtered 100 file", metavar="character"),
  make_option(c("--output_NEG_raw_filtered_100"), type="character", default="milk_data_neg_filtered_100.csv", 
              help="output NEG raw filtered 100 file file", metavar="character"),
  make_option(c("--output_POS_raw_filtered_200"), type="character", default="milk_data_pos_filtered_200.csv", 
              help="output POS raw filtered 200 file", metavar="character"),
  make_option(c("--output_NEG_raw_filtered_200"), type="character", default="milk_data_neg_filtered_200.csv", 
              help="output NEG raw filtered 200 file", metavar="character"),
  make_option(c("--output_POS_allgroups_anova"), type="character", default="milk_data_pos_ph_allgroups_anova.csv", 
              help="output POS anova file", metavar="character"),
  make_option(c("--output_POS_allgroups_kruskalwallis"), type="character", default="milk_data_pos_ph_allgroups_kruskalwallis.csv", 
              help="output POS kruskalwallis file", metavar="character"),
  make_option(c("--output_POS_allgroups_combination"), type="character", default="milk_data_pos_ph_allgroups_combination.csv", 
              help="output POS combination file", metavar="character"),
  make_option(c("--output_NEG_allgroups_anova"), type="character", default="milk_data_neg_ph_allgroups_anova.csv", 
              help="output NEG kruskalwallis file", metavar="character"),
  make_option(c("--output_NEG_allgroups_kruskalwallis"), type="character", default="milk_data_neg_ph_allgroups_kruskalwallis.csv", 
              help="output NEG kruskalwallis file", metavar="character"),
  make_option(c("--output_NEG_allgroups_combination"), type="character", default="milk_data_neg_ph_allgroups_combination.csv", 
              help="output NEG kruskalwallis file", metavar="character"),
  make_option(c("--output_POS_allgroups_combination_005"), type="character", default="milk_data_pos_ph_allgroups_combination_005.csv", 
              help="output POS allgroups combination 005 file", metavar="character"),
  make_option(c("--output_NEG_allgroups_combination_005"), type="character", default="milk_data_neg_ph_allgroups_combination_005.csv", 
              help="output NEG allgroups combination 005 file", metavar="character"),
  make_option(c("--output_POS_allgroups_combination_100"), type="character", default="milk_data_pos_ph_allgroups_combination_100.csv", 
              help="output POS allgroups combination 100 file", metavar="character"),
  make_option(c("--output_NEG_allgroups_combination_100"), type="character", default="milk_data_neg_ph_allgroups_combination_100.csv", 
              help="output NEG allgroups combination 100 file", metavar="character"),
  make_option(c("--output_POS_allgroups_combination_200"), type="character", default="milk_data_pos_ph_allgroups_combination_200.csv", 
              help="output POS allgroups combination 200 file", metavar="character"),
  make_option(c("--output_NEG_allgroups_combination_200"), type="character", default="milk_data_neg_ph_allgroups_combination_200.csv", 
              help="output NEG allgroups combination 200 file", metavar="character"),
  make_option(c("--output_POS_summaries_complete"), type="character", default="milk_data_pos_ph_summaries_complete.csv", 
              help="output POS summary file", metavar="character"),
  make_option(c("--output_NEG_summaries_complete"), type="character", default="milk_data_neg_ph_summaries_complete.csv", 
              help="output NEG summary file", metavar="character")

); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

# Loading pos ion mode summaries.
load(file = opt$input_POS_data)
load(file = opt$input_POS_blankbased)
load(file = opt$input_POS_anova)
load(file = opt$input_POS_kruskalwallis)
# Loading neg ion mode summaries.
load(file = opt$input_NEG_data)
load(file = opt$input_NEG_blankbased)
load(file = opt$input_NEG_anova)
load(file = opt$input_NEG_kruskalwallis)

# Grid of thresholds
grid_of_blankbased_thresholds <- c(1:40)* 5
which_005_threshold <- 1
which_100_threshold <- which(grid_of_blankbased_thresholds == 100)
which_200_threshold <- length(grid_of_blankbased_thresholds)

# List of treatment groups
list_of_groups_treatments_only <- c("fat", "skim", "whole")


# Performing the merger
# pos ion mode
milk_data_pos_ph_extract <- milk_data_pos_ph[, c("row_ID", "row_m_z", "row_retention_time") ]
milk_data_pos_ph_blankbased_threshold_flags_array_thresold_005 <- milk_data_pos_ph_blankbased_threshold_flags_array[which_005_threshold,,list_of_groups_treatments_only ]
milk_data_pos_ph_blankbased_threshold_flags_array_thresold_100 <- milk_data_pos_ph_blankbased_threshold_flags_array[which_100_threshold,,list_of_groups_treatments_only ]
milk_data_pos_ph_blankbased_threshold_flags_array_thresold_200 <- milk_data_pos_ph_blankbased_threshold_flags_array[which_200_threshold,,list_of_groups_treatments_only ]
# Fixing names
colnames(milk_data_pos_ph_blankbased_threshold_flags_array_thresold_005) <- paste("flag_", colnames(milk_data_pos_ph_blankbased_threshold_flags_array_thresold_005), "_threshold_005", sep ="")
colnames(milk_data_pos_ph_blankbased_threshold_flags_array_thresold_100) <- paste("flag_", colnames(milk_data_pos_ph_blankbased_threshold_flags_array_thresold_100), "_threshold_100", sep ="")
colnames(milk_data_pos_ph_blankbased_threshold_flags_array_thresold_200) <- paste("flag_", colnames(milk_data_pos_ph_blankbased_threshold_flags_array_thresold_200), "_threshold_200", sep ="")
# anova
milk_data_pos_ph_anova_summaries_array_namefix <- milk_data_pos_ph_anova_summaries_array
names(milk_data_pos_ph_anova_summaries_array_namefix) <-  paste(names(milk_data_pos_ph_anova_summaries_array_namefix), "_anova", sep ="")
# kruscalwallis
milk_data_pos_ph_kruskalwallis_summaries_array_namefix <- milk_data_pos_ph_kruskalwallis_summaries_array
names(milk_data_pos_ph_kruskalwallis_summaries_array_namefix) <-  paste(names(milk_data_pos_ph_kruskalwallis_summaries_array_namefix), "_kruskalwallis", sep ="")

# Actual merging step
milk_data_pos_ph_summaries_complete <- cbind(milk_data_pos_ph_extract, 
                                          milk_data_pos_ph_blankbased_threshold_flags_array_thresold_005, 
                                          milk_data_pos_ph_blankbased_threshold_flags_array_thresold_100,
                                          milk_data_pos_ph_blankbased_threshold_flags_array_thresold_200,
                                          milk_data_pos_ph_anova_summaries_array_namefix,
                                          milk_data_pos_ph_kruskalwallis_summaries_array_namefix )


# neg ion mode
milk_data_neg_ph_extract <- milk_data_neg_ph[, c("row_ID", "row_m_z", "row_retention_time") ]
milk_data_neg_ph_blankbased_threshold_flags_array_thresold_005 <- milk_data_neg_ph_blankbased_threshold_flags_array[which_005_threshold,,list_of_groups_treatments_only ]
milk_data_neg_ph_blankbased_threshold_flags_array_thresold_100 <- milk_data_neg_ph_blankbased_threshold_flags_array[which_100_threshold,,list_of_groups_treatments_only ]
milk_data_neg_ph_blankbased_threshold_flags_array_thresold_200 <- milk_data_neg_ph_blankbased_threshold_flags_array[which_200_threshold,,list_of_groups_treatments_only ]
# Fixing names
colnames(milk_data_neg_ph_blankbased_threshold_flags_array_thresold_005) <- paste("flag_", colnames(milk_data_neg_ph_blankbased_threshold_flags_array_thresold_005), "_threshold_005", sep ="")
colnames(milk_data_neg_ph_blankbased_threshold_flags_array_thresold_100) <- paste("flag_", colnames(milk_data_neg_ph_blankbased_threshold_flags_array_thresold_100), "_threshold_100", sep ="")
colnames(milk_data_neg_ph_blankbased_threshold_flags_array_thresold_200) <- paste("flag_", colnames(milk_data_neg_ph_blankbased_threshold_flags_array_thresold_200), "_threshold_200", sep ="")
# anova
milk_data_neg_ph_anova_summaries_array_namefix <- milk_data_neg_ph_anova_summaries_array
names(milk_data_neg_ph_anova_summaries_array_namefix) <-  paste(names(milk_data_neg_ph_anova_summaries_array_namefix), "_anova", sep ="")
# kruscalwallis
milk_data_neg_ph_kruskalwallis_summaries_array_namefix <- milk_data_neg_ph_kruskalwallis_summaries_array
names(milk_data_neg_ph_kruskalwallis_summaries_array_namefix) <-  paste(names(milk_data_neg_ph_kruskalwallis_summaries_array_namefix), "_kruskalwallis", sep ="")

# Actual merging step
milk_data_neg_ph_summaries_complete <- cbind(milk_data_neg_ph_extract, 
                                          milk_data_neg_ph_blankbased_threshold_flags_array_thresold_005, 
                                          milk_data_neg_ph_blankbased_threshold_flags_array_thresold_100,
                                          milk_data_neg_ph_blankbased_threshold_flags_array_thresold_200,
                                          milk_data_neg_ph_anova_summaries_array_namefix,
                                          milk_data_neg_ph_kruskalwallis_summaries_array_namefix )




# Saving complete datasets
# csv
write.csv(milk_data_pos_ph_summaries_complete, file = opt$output_POS_summaries_complete, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_complete, file = opt$output_NEG_summaries_complete, row.names = FALSE,  quote = FALSE )


# extracting flags dataset for simpler operations
# pos
which_flags_columns_pos_ph <- which( grepl(pattern = "flag", x = names(milk_data_pos_ph_summaries_complete) ) )
milk_data_pos_ph_summaries_flags <- milk_data_pos_ph_summaries_complete[,c(1,2,3, which_flags_columns_pos_ph)]
# neg
which_flags_columns_neg_ph <- which( grepl(pattern = "flag", x = names(milk_data_neg_ph_summaries_complete) ) )
milk_data_neg_ph_summaries_flags <- milk_data_neg_ph_summaries_complete[,c(1,2,3, which_flags_columns_neg_ph)]
# Extra checking
dim(milk_data_pos_ph_summaries_flags)
dim(milk_data_neg_ph_summaries_flags)



# Dropping cfriteria flags based on threhsolds

columns_names_threshold_005 <- paste("flag_", list_of_groups_treatments_only, "_threshold_005", sep ="")
# Criteria is ->  (rowSums(milk_data_pos_ph_summaries_flags[,columns_names_threshold_005]) == 3)
columns_names_threshold_100 <- paste("flag_", list_of_groups_treatments_only, "_threshold_100", sep ="")
# Criteria is ->  (rowSums(milk_data_pos_ph_summaries_flags[,columns_names_threshold_100]) == 3)
columns_names_threshold_200 <- paste("flag_", list_of_groups_treatments_only, "_threshold_200", sep ="")
# Criteria is ->  (rowSums(milk_data_pos_ph_summaries_flags[,columns_names_threshold_200]) == 3)

# pos
dropping_criteria_pos_ph_threshold_005 <- which( (rowSums(milk_data_pos_ph_summaries_flags[,columns_names_threshold_005]) == 3) )
dropping_criteria_pos_ph_threshold_100 <- which( (rowSums(milk_data_pos_ph_summaries_flags[,columns_names_threshold_100]) == 3) )
dropping_criteria_pos_ph_threshold_200 <- which( (rowSums(milk_data_pos_ph_summaries_flags[,columns_names_threshold_200]) == 3) )
# neg
dropping_criteria_neg_ph_threshold_005 <- which( (rowSums(milk_data_neg_ph_summaries_flags[,columns_names_threshold_005]) == 3) )
dropping_criteria_neg_ph_threshold_100 <- which( (rowSums(milk_data_neg_ph_summaries_flags[,columns_names_threshold_100]) == 3) )
dropping_criteria_neg_ph_threshold_200 <- which( (rowSums(milk_data_neg_ph_summaries_flags[,columns_names_threshold_200]) == 3) )

# Summaries
# pos
length(dropping_criteria_pos_ph_threshold_005)
length(dropping_criteria_pos_ph_threshold_100)
length(dropping_criteria_pos_ph_threshold_200)
# neg
length(dropping_criteria_neg_ph_threshold_005)
length(dropping_criteria_neg_ph_threshold_100)
length(dropping_criteria_neg_ph_threshold_200)



# Dropping cfriteria flags based on "p_value_k_kruskalwallis" and "p_value_f_anova"
# pos
dropping_criteria_pos_ph_anova                   <- which( milk_data_pos_ph_summaries_complete$p_value_f_anova > 0.05 )
dropping_criteria_pos_ph_kruskalwallis           <- which( milk_data_pos_ph_summaries_complete$p_value_k_kruskalwallis > 0.05 )
dropping_criteria_pos_ph_anova_and_kruskalwallis <- union(dropping_criteria_pos_ph_anova, dropping_criteria_pos_ph_kruskalwallis)
# neg
dropping_criteria_neg_ph_anova                   <- which( milk_data_neg_ph_summaries_complete$p_value_f_anova > 0.05 )
dropping_criteria_neg_ph_kruskalwallis           <- which( milk_data_neg_ph_summaries_complete$p_value_k_kruskalwallis > 0.05 )
dropping_criteria_neg_ph_anova_and_kruskalwallis <- union(dropping_criteria_neg_ph_anova, dropping_criteria_neg_ph_kruskalwallis)

# Summaries  of the number of rows to drop
# pos
length(dropping_criteria_pos_ph_anova)
length(dropping_criteria_pos_ph_kruskalwallis)
length(dropping_criteria_pos_ph_anova_and_kruskalwallis)
# neg
length(dropping_criteria_neg_ph_anova)
length(dropping_criteria_neg_ph_kruskalwallis)
length(dropping_criteria_neg_ph_anova_and_kruskalwallis)




# Actual filtering procedure

# Saving complete datasets with threshold filtering
# pos
milk_data_pos_ph_summaries_filter_allgroups_threshold_005 <- milk_data_pos_ph_summaries_complete[ - dropping_criteria_pos_ph_threshold_005, ]
milk_data_pos_ph_summaries_filter_allgroups_threshold_100 <- milk_data_pos_ph_summaries_complete[ - dropping_criteria_pos_ph_threshold_100, ]
milk_data_pos_ph_summaries_filter_allgroups_threshold_200 <- milk_data_pos_ph_summaries_complete[ - dropping_criteria_pos_ph_threshold_200, ]
# neg
milk_data_neg_ph_summaries_filter_allgroups_threshold_005 <- milk_data_neg_ph_summaries_complete[ - dropping_criteria_neg_ph_threshold_005, ]
milk_data_neg_ph_summaries_filter_allgroups_threshold_100 <- milk_data_neg_ph_summaries_complete[ - dropping_criteria_neg_ph_threshold_100, ]
milk_data_neg_ph_summaries_filter_allgroups_threshold_200 <- milk_data_neg_ph_summaries_complete[ - dropping_criteria_neg_ph_threshold_200, ]

# Xinsong adds the following lines to filter original data for future use
# pos
milk_data_pos_raw_filtered_005 <- milk_data_pos_ph[ - dropping_criteria_pos_ph_threshold_005, ]
milk_data_pos_raw_filtered_100 <- milk_data_pos_ph[ - dropping_criteria_pos_ph_threshold_100, ]
milk_data_pos_raw_filtered_200 <- milk_data_pos_ph[ - dropping_criteria_pos_ph_threshold_200, ]
# neg
milk_data_neg_raw_filtered_005 <- milk_data_neg_ph[ - dropping_criteria_neg_ph_threshold_005, ]
milk_data_neg_raw_filtered_100 <- milk_data_neg_ph[ - dropping_criteria_neg_ph_threshold_100, ]
milk_data_neg_raw_filtered_200 <- milk_data_neg_ph[ - dropping_criteria_neg_ph_threshold_200, ]

# Saving complete datasets with significance filtering
# pos
milk_data_pos_ph_summaries_filter_allgroups_anova                   <- milk_data_pos_ph_summaries_complete[ - dropping_criteria_pos_ph_anova, ]
milk_data_pos_ph_summaries_filter_allgroups_kruskalwallis           <- milk_data_pos_ph_summaries_complete[ - dropping_criteria_pos_ph_kruskalwallis, ]
milk_data_pos_ph_summaries_filter_allgroups_anova_and_kruskalwallis <- milk_data_pos_ph_summaries_complete[ - dropping_criteria_pos_ph_anova_and_kruskalwallis, ]
# neg
milk_data_neg_ph_summaries_filter_allgroups_anova                   <- milk_data_neg_ph_summaries_complete[ - dropping_criteria_neg_ph_anova, ]
milk_data_neg_ph_summaries_filter_allgroups_kruskalwallis           <- milk_data_neg_ph_summaries_complete[ - dropping_criteria_neg_ph_kruskalwallis, ]
milk_data_neg_ph_summaries_filter_allgroups_anova_and_kruskalwallis <- milk_data_neg_ph_summaries_complete[ - dropping_criteria_neg_ph_anova_and_kruskalwallis, ]




# Saving complete datasets with threshold and significance filtering
# pos
milk_data_pos_ph_summaries_filter_allgroups_threshold_005_anova_and_kruskalwallis <- milk_data_pos_ph_summaries_complete[ - union(dropping_criteria_pos_ph_threshold_005, dropping_criteria_pos_ph_anova_and_kruskalwallis), ]
milk_data_pos_ph_summaries_filter_allgroups_threshold_100_anova_and_kruskalwallis <- milk_data_pos_ph_summaries_complete[ - union(dropping_criteria_pos_ph_threshold_100, dropping_criteria_pos_ph_anova_and_kruskalwallis), ]
milk_data_pos_ph_summaries_filter_allgroups_threshold_200_anova_and_kruskalwallis <- milk_data_pos_ph_summaries_complete[ - union(dropping_criteria_pos_ph_threshold_200, dropping_criteria_pos_ph_anova_and_kruskalwallis), ]
# neg
milk_data_neg_ph_summaries_filter_allgroups_threshold_005_anova_and_kruskalwallis <- milk_data_neg_ph_summaries_complete[ - union(dropping_criteria_neg_ph_threshold_005, dropping_criteria_neg_ph_anova_and_kruskalwallis), ]
milk_data_neg_ph_summaries_filter_allgroups_threshold_100_anova_and_kruskalwallis <- milk_data_neg_ph_summaries_complete[ - union(dropping_criteria_neg_ph_threshold_100, dropping_criteria_neg_ph_anova_and_kruskalwallis), ]
milk_data_neg_ph_summaries_filter_allgroups_threshold_200_anova_and_kruskalwallis <- milk_data_neg_ph_summaries_complete[ - union(dropping_criteria_neg_ph_threshold_200, dropping_criteria_neg_ph_anova_and_kruskalwallis), ]



# Summaries of the filtering results

# Before filtering
# pos
dim(milk_data_pos_ph_summaries_complete)
# neg
dim(milk_data_neg_ph_summaries_complete)

# Threshold based
# pos
dim(milk_data_pos_ph_summaries_filter_allgroups_threshold_005)
dim(milk_data_pos_ph_summaries_filter_allgroups_threshold_100)
dim(milk_data_pos_ph_summaries_filter_allgroups_threshold_200)
# neg
dim(milk_data_neg_ph_summaries_filter_allgroups_threshold_005)
dim(milk_data_neg_ph_summaries_filter_allgroups_threshold_100)
dim(milk_data_neg_ph_summaries_filter_allgroups_threshold_200)

# Significance based
# pos
dim(milk_data_pos_ph_summaries_filter_allgroups_anova)
dim(milk_data_pos_ph_summaries_filter_allgroups_kruskalwallis)
dim(milk_data_pos_ph_summaries_filter_allgroups_anova_and_kruskalwallis)
# neg
dim(milk_data_neg_ph_summaries_filter_allgroups_anova)
dim(milk_data_neg_ph_summaries_filter_allgroups_kruskalwallis)
dim(milk_data_neg_ph_summaries_filter_allgroups_anova_and_kruskalwallis)

# Threshold and significance based
# pos
dim(milk_data_pos_ph_summaries_filter_allgroups_threshold_005_anova_and_kruskalwallis)
dim(milk_data_pos_ph_summaries_filter_allgroups_threshold_100_anova_and_kruskalwallis)
dim(milk_data_pos_ph_summaries_filter_allgroups_threshold_200_anova_and_kruskalwallis)
# neg
dim(milk_data_neg_ph_summaries_filter_allgroups_threshold_005_anova_and_kruskalwallis)
dim(milk_data_neg_ph_summaries_filter_allgroups_threshold_100_anova_and_kruskalwallis)
dim(milk_data_neg_ph_summaries_filter_allgroups_threshold_200_anova_and_kruskalwallis)

# Saving the outputs as csv Files
# Threshold based

# Xinsong adds the following lines to save filtered original data files
# pos
write.table(milk_data_pos_raw_filtered_005, file = opt$output_POS_raw_filtered_005, row.names = FALSE,  sep="    ")
write.table(milk_data_pos_raw_filtered_100, file = opt$output_POS_raw_filtered_100, row.names = FALSE,  sep="    ")
write.table(milk_data_pos_raw_filtered_200, file = opt$output_POS_raw_filtered_200, row.names = FALSE,  sep="    ")
# neg
write.table(milk_data_neg_raw_filtered_005, file = opt$output_NEG_raw_filtered_005, row.names = FALSE,  sep="    ")
write.table(milk_data_neg_raw_filtered_100, file = opt$output_NEG_raw_filtered_100, row.names = FALSE,  sep="    ")
write.table(milk_data_neg_raw_filtered_200, file = opt$output_NEG_raw_filtered_200, row.names = FALSE,  sep="    ")

# pos
write.csv(milk_data_pos_ph_summaries_filter_allgroups_threshold_005, file = opt$output_POS_allgroups_threshold_005, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_pos_ph_summaries_filter_allgroups_threshold_100, file = opt$output_POS_allgroups_threshold_100, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_pos_ph_summaries_filter_allgroups_threshold_200, file = opt$output_POS_allgroups_threshold_200, row.names = FALSE,  quote = FALSE )
# neg
write.csv(milk_data_neg_ph_summaries_filter_allgroups_threshold_005, file = opt$output_NEG_allgroups_threshold_005, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_filter_allgroups_threshold_100, file = opt$output_NEG_allgroups_threshold_100, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_filter_allgroups_threshold_200, file = opt$output_NEG_allgroups_threshold_200, row.names = FALSE,  quote = FALSE )

# Significance based
# pos
write.csv(milk_data_pos_ph_summaries_filter_allgroups_anova,                   file = opt$output_POS_allgroups_anova, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_pos_ph_summaries_filter_allgroups_kruskalwallis,           file = opt$output_POS_allgroups_kruskalwallis, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_pos_ph_summaries_filter_allgroups_anova_and_kruskalwallis, file = opt$output_POS_allgroups_combination, row.names = FALSE,  quote = FALSE )
# neg
write.csv(milk_data_neg_ph_summaries_filter_allgroups_anova,                   file = opt$output_NEG_allgroups_anova, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_filter_allgroups_kruskalwallis,           file = opt$output_NEG_allgroups_kruskalwallis, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_filter_allgroups_anova_and_kruskalwallis, file = opt$output_NEG_allgroups_combination, row.names = FALSE,  quote = FALSE )

# Threshold and significance based
# pos
write.csv(milk_data_pos_ph_summaries_filter_allgroups_threshold_005_anova_and_kruskalwallis, file = opt$output_POS_allgroups_combination_005, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_pos_ph_summaries_filter_allgroups_threshold_100_anova_and_kruskalwallis, file = opt$output_POS_allgroups_combination_100, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_pos_ph_summaries_filter_allgroups_threshold_200_anova_and_kruskalwallis, file = opt$output_POS_allgroups_combination_200, row.names = FALSE,  quote = FALSE )
# neg
write.csv(milk_data_neg_ph_summaries_filter_allgroups_threshold_005_anova_and_kruskalwallis, file = opt$output_NEG_allgroups_combination_005, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_filter_allgroups_threshold_100_anova_and_kruskalwallis, file = opt$output_NEG_allgroups_combination_100, row.names = FALSE,  quote = FALSE )
write.csv(milk_data_neg_ph_summaries_filter_allgroups_threshold_200_anova_and_kruskalwallis, file = opt$output_NEG_allgroups_combination_200, row.names = FALSE,  quote = FALSE )

