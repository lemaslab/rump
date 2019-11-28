# 2018.12.18. ask
rm(list=ls(all=TRUE))

# 20 Digits Precision Representation
options(scipen=20)

# Setting the correct working directory.
# NOTE!!! -> Can be linked differently on different computers.
# setwd("E:/Alexander/UF Research/2018 - Lemas Milk Metabolomics")
# Extra check
getwd()


# loading library for rows standard deviations
library(matrixStats)
library(optparse) # add this library to enable argparse arguments
options(warn=-1)

## Define input and output arguments
option_list = list(
  make_option(c("-a", "--input_POS_design"), type="character", default="milk_design_pos_ph.Rdata", 
              help="input POS design file", metavar="character"),
  make_option(c("-b", "--input_NEG_design"), type="character", default="milk_design_neg_ph.Rdata", 
              help="input NEG design file", metavar="character"),
  make_option(c("-c", "--input_POS_data"), type="character", default="milk_data_pos_ph.Rdata", 
              help="input POS data file", metavar="character"),
  make_option(c("-d", "--input_NEG_data"), type="character", default="milk_data_neg_ph.Rdata", 
              help="input NEG data file", metavar="character"),
  make_option(c("-e", "--output_POS_blankbased"), type="character", default="milk_data_pos_ph_blankbased_threshold_flags_array.Rdata", 
              help="output POS absolute file", metavar="character"),
  make_option(c("-f", "--output_NEG_blankbased"), type="character", default="milk_data_neg_ph_blankbased_threshold_flags_array.Rdata", 
              help="output NEG absolute file", metavar="character")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

# Saving cleaned design files into the RData objects
load(file = opt$input_POS_design)
load(file = opt$input_NEG_design)

# Saving cleaned data ph files into the RData objects
load(file = opt$input_POS_data)
load(file = opt$input_NEG_data)

ls()






# Performing Blanks Based Flags from SECIMTools

# Groups to perform flags overof interest
# Extrack check that the groups are the same.
unique(milk_design_pos_ph$group2)
unique(milk_design_neg_ph$group2) 

table(milk_design_pos_ph$group2)
table(milk_design_neg_ph$group2) 


# complete list of groups
list_of_groups <- unique(milk_design_pos_ph$group2)
list_of_groups_treatments_only <- unique(milk_design_pos_ph$group2)[c(2,5,6)]


# List of blankbased thresholds
# Definign the blank group name.
blank_group_name <- list_of_groups[1]
# Extracting blank sample group only
blank_data_pos_ph <- as.matrix( milk_data_pos_ph[,  milk_design_pos_ph$sampleID[ milk_design_pos_ph$group2 == blank_group_name ] ] )
blank_data_neg_ph <- as.matrix( milk_data_neg_ph[,  milk_design_neg_ph$sampleID[ milk_design_neg_ph$group2 == blank_group_name ] ] )
head(blank_data_pos_ph)
head(blank_data_neg_ph)

# COmputing row means and standard deviations.
blank_data_pos_ph_mean  <- rowMeans(blank_data_pos_ph)
blank_data_neg_ph_mean  <- rowMeans(blank_data_neg_ph)
blank_data_pos_ph_stdev <- rowSds(blank_data_pos_ph)
blank_data_neg_ph_stdev <- rowSds(blank_data_neg_ph)

# Computing thresholds
blank_data_pos_ph_threshold  <- blank_data_pos_ph_mean + 3 * blank_data_pos_ph_stdev
blank_data_neg_ph_threshold  <- blank_data_neg_ph_mean + 3 * blank_data_neg_ph_stdev
# Overiding thresholds less or equal to zero with threshold 5000.

# Identifying below the threhsold.
which_pos_ph_less_equal_zero <- which( blank_data_pos_ph_threshold <= 0 )
which_neg_ph_less_equal_zero <- which( blank_data_neg_ph_threshold <= 0 )
# Overwriting them wiht 5000 threshold.
blank_data_pos_ph_threshold[which_pos_ph_less_equal_zero] <- 5000
blank_data_neg_ph_threshold[which_neg_ph_less_equal_zero] <- 5000



grid_of_blankbased_thresholds <- c(1:40)* 5


# List of ion model
list_of_ion_modes <- c("pos", "neg")


# Creating three dimensional arrays in R to store the thresholding results.
milk_data_pos_ph_blankbased_threshold_flags_array <- array(0, dim = c( length(grid_of_blankbased_thresholds), dim(milk_data_pos_ph)[1], length(list_of_groups) )  )
milk_data_neg_ph_blankbased_threshold_flags_array <- array(0, dim = c( length(grid_of_blankbased_thresholds), dim(milk_data_neg_ph)[1], length(list_of_groups) )  )
dim(milk_data_pos_ph_blankbased_threshold_flags_array)
dim(milk_data_neg_ph_blankbased_threshold_flags_array)



# Looping via ion modes
for ( current_ion_mode in list_of_ion_modes )
{
  # Debugging step
  # current_ion_mode <- list_of_ion_modes[1]
  # current_ion_mode <- list_of_ion_modes[2]
  
  # Generating a table of flags for the current ion mode.
  
  
  # Looping via threshold values
  for ( threshold_current in grid_of_blankbased_thresholds )
  {
    # Debugging step
    # threshold_current <- grid_of_blankbased_thresholds[1]
    
    for ( current_group in list_of_groups )
    {
      # Debugging step
      # current_group <- list_of_groups[1]
      # current_group <- list_of_groups[2]
        
      # Parsing subset data of interest 
      # Samples names fo samples in the surrent group
      sample_names_current_group_threshold_current <- eval( parse( text=paste( "milk_design_", current_ion_mode, "_ph$sampleID[ milk_design_", current_ion_mode, "_ph$group2 == current_group]", sep ="") )  )
      # Extracting dataset with those samples extracted to sample_names_current_group_threshold_current
      current_mode_and_group_subset <- 
      eval( parse( text=paste( "milk_data_", current_ion_mode, "_ph[,sample_names_current_group_threshold_current]", sep ="") )  )
      

      current_group_ratio_to_compare_with_the_threshold <-       
      eval( parse( text=paste( "( rowMeans(current_mode_and_group_subset) - blank_data_", current_ion_mode, "_ph_threshold ) / blank_data_", current_ion_mode, "_ph_threshold", sep ="") )  )

      # Flags of interest.
      # If the number of samples with the value below the sepcified trehsold is bigger then the half samples in the group then 
      boolean_matrix_numeric_current_sums_final <- as.numeric( current_group_ratio_to_compare_with_the_threshold < threshold_current )
      
            
      # Combining the results.
      
      # If the first group.
      if ( current_group == list_of_groups[1] )
      {
        eval( parse( text = paste( "milk_data_", current_ion_mode, "_ph_threshold_flags <- as.matrix( boolean_matrix_numeric_current_sums_final )", sep ="") )  )
        eval( parse( text = paste( "colnames(milk_data_", current_ion_mode, "_ph_threshold_flags) <- current_group", sep ="") )  )
      }


      # If the more then the first group.
      if ( current_group != list_of_groups[1] )
      {
        eval( parse( text = paste( "milk_data_", current_ion_mode, "_ph_threshold_flags <- cbind( milk_data_", current_ion_mode, "_ph_threshold_flags, as.matrix( boolean_matrix_numeric_current_sums_final ) )", sep ="") )  )
        eval( parse( text = paste( "colnames(milk_data_", current_ion_mode, "_ph_threshold_flags)[ dim(milk_data_", current_ion_mode, "_ph_threshold_flags)[2] ] <- current_group", sep ="") )  )
      }

    # End of -> for ( current_group in list_of_groups )  
    }

    # Saving the results into the array
    
    # Extracting the array index
    which_threshold_index <- which( grid_of_blankbased_thresholds == threshold_current )

    # Saving the value to the corresponding array
    eval( parse( text = paste( "milk_data_", current_ion_mode, "_ph_blankbased_threshold_flags_array[which_threshold_index, , ] <- milk_data_", current_ion_mode, "_ph_threshold_flags", sep ="") )  )
    
    
  # End of ->  for ( threshold_current in grid_of_blankbased_thresholds )    
  }  
  
  
  # Saving the correspondingthreshold value names
  eval( parse( text = paste( "dimnames(milk_data_", current_ion_mode, "_ph_blankbased_threshold_flags_array)[[1]] <- grid_of_blankbased_thresholds", sep ="") )  )
  
  # Saving the corresponding groupnames
  eval( parse( text = paste( "dimnames(milk_data_", current_ion_mode, "_ph_blankbased_threshold_flags_array)[[3]] <- list_of_groups", sep ="") )  )
  
  
# End of -> for ( current_ion_mode in list_of_ion_modes )  
}  


# Saving cleanded threshold flags for the array into the RData objects
save(milk_data_pos_ph_blankbased_threshold_flags_array, file = opt$output_POS_blankbased)
save(milk_data_neg_ph_blankbased_threshold_flags_array, file = opt$output_NEG_blankbased)