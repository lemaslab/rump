# 2018.12.19. ask
rm(list=ls(all=TRUE))

# 20 Digits Precision Representation
options(scipen=20)

# Setting the correct working directory.
# NOTE!!! -> Can be linked differently on different computers.
# setwd("/Users/xinsongdu/mnt/projects/beach01/secimtools")
# Extra check
getwd()

library(optparse) # add this library to enable argparse arguments
options(warn=-1)

## Define input and output arguments
option_list = list(
  make_option(c("-a", "--input_POS_design"), type="character", default="Lemas_POS_mzmine_ht_17DEC18_design.csv", 
              help="input POS design file", metavar="character"),
  make_option(c("-b", "--input_NEG_design"), type="character", default="Lemas_NEG_mzmine_ht_17DEC18_design.csv", 
              help="input NEG design file", metavar="character"),
  make_option(c("-c", "--input_POS_data"), type="character", default="Lemas_POS_mzmine_ht_17DEC18_data.csv", 
              help="input POS data file", metavar="character"),
  make_option(c("-d", "--input_NEG_data"), type="character", default="Lemas_NEG_mzmine_ht_17DEC18_data.csv", 
              help="input NEG data file", metavar="character"),
  make_option(c("-e", "--output_POS_design"), type="character", default="milk_design_pos_ph.Rdata", 
              help="output POS design file", metavar="character"),
  make_option(c("-f", "--output_NEG_design"), type="character", default="milk_design_neg_ph.Rdata", 
              help="output NEG design file", metavar="character"),
  make_option(c("-g", "--output_POS_data"), type="character", default="milk_data_pos_ph.Rdata", 
              help="output POS data file", metavar="character"),
  make_option(c("-i", "--output_NEG_data"), type="character", default="milk_data_neg_ph.Rdata", 
              help="output NEG data file", metavar="character"),
  make_option(c("-j", "--output_POS_data_csv"), type="character", default="milk_data_pos_ph.csv", 
              help="output POS data csv file", metavar="character"),
  make_option(c("-k", "--output_NEG_data_csv"), type="character", default="milk_data_neg_ph.csv", 
              help="output NEG data csv file", metavar="character")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);


# Reading Desing files Into R.
# pos
milk_design_pos_ph_path <- paste(opt$input_POS_design)
milk_design_pos_ph_raw  <- read.csv(milk_design_pos_ph_path, sep= ",", fill = TRUE, header = TRUE)
# neg
milk_design_neg_ph_path <- paste(opt$input_NEG_design)
milk_design_neg_ph_raw  <- read.csv(milk_design_neg_ph_path, sep= ",", fill = TRUE, header = TRUE)
# Checking The Input
dim(milk_design_pos_ph_raw)
dim(milk_design_neg_ph_raw)



# Reading Data files Into R.
# pos
milk_data_pos_ph_path <- paste(opt$input_POS_data)
milk_data_pos_ph_raw  <- read.csv(milk_data_pos_ph_path, sep= ",", fill = TRUE, header = TRUE)
# neg
milk_data_neg_ph_path <- paste(opt$input_NEG_data)
milk_data_neg_ph_raw  <- read.csv(milk_data_neg_ph_path, sep= ",", fill = TRUE, header = TRUE)
# Checking The Input
dim(milk_data_pos_ph_raw)
dim(milk_data_neg_ph_raw)

# Fix 2018.12.19.
# Dropping the group3 values from the design that has "drop" markings
which_drop_milk_design_pos_ph_raw <- which(milk_design_pos_ph_raw$group3 == "drop")
which_drop_milk_design_neg_ph_raw <- which(milk_design_neg_ph_raw$group3 == "drop")
milk_design_pos_ph <- milk_design_pos_ph_raw[ - which_drop_milk_design_pos_ph_raw, ]
milk_design_neg_ph <- milk_design_neg_ph_raw[ - which_drop_milk_design_neg_ph_raw, ]
# Extra check
unique(as.character(milk_design_pos_ph$group3))
unique(as.character(milk_design_neg_ph$group3))
# Removing group3
which_design_pos_ph_group3_drop <- which( names(milk_design_pos_ph_raw) == "group3" )
which_design_neg_ph_group3_drop <- which( names(milk_design_pos_ph_raw) == "group3" )
milk_design_pos_ph <- milk_design_pos_ph[ , - which_design_pos_ph_group3_drop ] 
milk_design_neg_ph <- milk_design_neg_ph[ , - which_design_neg_ph_group3_drop ] 




# Fixing names in data files.
# pos
milk_data_pos_ph <- milk_data_pos_ph_raw
names(milk_data_pos_ph) <- gsub("\\.", "_", names(milk_data_pos_ph_raw)  )
head(milk_data_pos_ph)
milk_data_pos_ph$row_ID <- paste( "rowID_", milk_data_pos_ph$row_ID, sep ="")

# neg
milk_data_neg_ph <- milk_data_neg_ph_raw
names(milk_data_neg_ph) <- gsub("\\.", "_", names(milk_data_neg_ph_raw)  )
head(milk_data_neg_ph)
milk_data_neg_ph$row_ID <- paste( "rowID_", milk_data_neg_ph$row_ID, sep ="")



 

# Fixing names in design files.
# pos
# Coding as characters
milk_design_pos_ph$sampleID <- as.character(milk_design_pos_ph$sampleID)
milk_design_pos_ph$group1 <- as.character(milk_design_pos_ph$group1)
milk_design_pos_ph$group2 <- as.character(milk_design_pos_ph$group2)
# Fixing extraction blank name so it does agree between the pos and neg desing files.
which_extract_blank <- which( milk_design_pos_ph$group2 == "extract-blank" )
milk_design_pos_ph$group2[which_extract_blank] <- "extraction-blank"
# Replacing (.) dots with an uderscore
milk_design_pos_ph$sampleID <- gsub("\\.", "_", milk_design_pos_ph$sampleID  )
# Replacing ( ) spaces with an uderscore
milk_design_pos_ph$sampleID <- gsub(" ", "_", milk_design_pos_ph$sampleID  )
# Replacing (-) hyphens with an uderscore
milk_design_pos_ph$sampleID <- gsub("-", "_", milk_design_pos_ph$sampleID  )
# Replacing ([) and (]) parenthesis with an uderscore
milk_design_pos_ph$sampleID <- gsub("\\[", "_", milk_design_pos_ph$sampleID  )
milk_design_pos_ph$sampleID <- gsub("\\]", "_", milk_design_pos_ph$sampleID  )
# Addin X in the beginning to match the names
# milk_design_pos_ph$sampleID <- paste("X", milk_design_pos_ph$sampleID, sep ="")
# neg
# Coding as characters
milk_design_neg_ph$sampleID <- as.character(milk_design_neg_ph$sampleID)
milk_design_neg_ph$group1 <- as.character(milk_design_neg_ph$group1)
milk_design_neg_ph$group2 <- as.character(milk_design_neg_ph$group2)
# Replacing (.) dots with an uderscore
milk_design_neg_ph$sampleID <- gsub("\\.", "_", milk_design_neg_ph$sampleID  )
# Replacing ( ) spaces with an uderscore
milk_design_neg_ph$sampleID <- gsub(" ", "_", milk_design_neg_ph$sampleID  )
# Replacing (-) hyphens with an uderscore
milk_design_neg_ph$sampleID <- gsub("-", "_", milk_design_neg_ph$sampleID  )
# Replacing ([) and (]) parenthesis with an uderscore
milk_design_neg_ph$sampleID <- gsub("\\[", "_", milk_design_neg_ph$sampleID  )
milk_design_neg_ph$sampleID <- gsub("\\]", "_", milk_design_neg_ph$sampleID  )
# Addin X in the beginning to match the names
# milk_design_neg_ph$sampleID <- paste("X", milk_design_neg_ph$sampleID, sep ="")


# Chekcing the differences between the two sets of names
# pos
setdiff( milk_design_pos_ph$sampleID, names(milk_data_pos_ph)  )
setdiff( names(milk_data_pos_ph) , milk_design_pos_ph$sampleID )
# neg
setdiff( milk_design_neg_ph$sampleID, names(milk_data_neg_ph)  )
setdiff( names(milk_data_neg_ph) , milk_design_neg_ph$sampleID )






# Saving cleaned design files into the RData objects
save(milk_design_pos_ph, file = opt$output_POS_design)
save(milk_design_neg_ph, file = opt$output_NEG_design)

# Saving cleaned data ph files into the RData objects
save(milk_data_pos_ph, file = opt$output_POS_data)
save(milk_data_neg_ph, file = opt$output_NEG_data)

write.table(milk_data_pos_ph, file = opt$output_POS_data_csv, row.names = FALSE,  sep="    ")
write.table(milk_data_neg_ph, file = opt$output_NEG_data_csv, row.names = FALSE,  sep="    ")

