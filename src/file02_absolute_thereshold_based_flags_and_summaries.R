# 2018.12.18. ask
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
  make_option(c("-a", "--input_POS_design"), type="character", default="milk_design_pos_ph.Rdata", 
              help="input POS design file", metavar="character"),
  make_option(c("-b", "--input_NEG_design"), type="character", default="milk_design_neg_ph.Rdata", 
              help="input NEG design file", metavar="character"),
  make_option(c("-c", "--input_POS_data"), type="character", default="milk_data_pos_ph.Rdata", 
              help="input POS data file", metavar="character"),
  make_option(c("-d", "--input_NEG_data"), type="character", default="milk_data_neg_ph.Rdata", 
              help="input NEG data file", metavar="character"),
  make_option(c("-e", "--output_POS_absolute"), type="character", default="milk_data_pos_ph_absolute_threshold_flags_array.Rdata", 
              help="output POS absolute file", metavar="character"),
  make_option(c("-f", "--output_NEG_absolute"), type="character", default="milk_data_neg_ph_absolute_threshold_flags_array.Rdata", 
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






# Performing Threshold Based Flags from SECIMTools

# Groups to perform flags overof interest
# Extrack check that the groups are the same.
unique(milk_design_pos_ph$group2)
unique(milk_design_neg_ph$group2)

table(milk_design_pos_ph$group2)
table(milk_design_neg_ph$group2)

# complete list of groups
list_of_groups <- unique(milk_design_pos_ph$group2)
list_of_groups_treatments_only <- unique(milk_design_pos_ph$group2)[c(2,5,6)]


# List of absolute thresholds
grid_of_absolute_thresholds <- c(0:50)* 5000


# List of ion model
list_of_ion_modes <- c("pos", "neg")


# Creating three dimensional arrays in R to store the thresholding results.
milk_data_pos_ph_absolute_threshold_flags_array <- array(0, dim = c( length(grid_of_absolute_thresholds), dim(milk_data_pos_ph)[1], length(list_of_groups) )  )
milk_data_neg_ph_absolute_threshold_flags_array <- array(0, dim = c( length(grid_of_absolute_thresholds), dim(milk_data_neg_ph)[1], length(list_of_groups) )  )
dim(milk_data_pos_ph_absolute_threshold_flags_array)
dim(milk_data_neg_ph_absolute_threshold_flags_array)



# Looping via ion modes
for ( current_ion_mode in list_of_ion_modes )
{
  # Debugging step
  # current_ion_mode <- list_of_ion_modes[1]
  # current_ion_mode <- list_of_ion_modes[2]
  
  # Generating a table of flags for the current ion mode.
  
  
  # Looping via threshold values
  for ( threshold_current in grid_of_absolute_thresholds )
  {
    # Debugging step
    # threshold_current <- grid_of_absolute_thresholds[1]
    
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
      
      # Checking for the criteria. Flag = 1 if for the given sample the value is BELOW the given threshold.
      boolean_matrix_current_below <- current_mode_and_group_subset <  threshold_current
      boolean_matrix_numeric_current_below <- 1 * boolean_matrix_current_below
      
      # Flags of interest.
      # If the number of samples with the value below the sepcified trehsold is bigger then the half samples in the group then 
      boolean_matrix_numeric_current_sums_final <- as.numeric( rowSums(boolean_matrix_numeric_current_below) >= dim(current_mode_and_group_subset)[2]/2 )

            
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
    which_threshold_index <- which( grid_of_absolute_thresholds == threshold_current )

    # Saving the value to the corresponding array
    eval( parse( text = paste( "milk_data_", current_ion_mode, "_ph_absolute_threshold_flags_array[which_threshold_index, , ] <- milk_data_", current_ion_mode, "_ph_threshold_flags", sep ="") )  )
    
    
  # End of ->  for ( threshold_current in grid_of_absolute_thresholds )    
  }  
  
  
  # Saving the correspondingthreshold value names
  eval( parse( text = paste( "dimnames(milk_data_", current_ion_mode, "_ph_absolute_threshold_flags_array)[[1]] <- grid_of_absolute_thresholds", sep ="") )  )
  
  # Saving the corresponding groupnames
  eval( parse( text = paste( "dimnames(milk_data_", current_ion_mode, "_ph_absolute_threshold_flags_array)[[3]] <- list_of_groups", sep ="") )  )
  
  
# End of -> for ( current_ion_mode in list_of_ion_modes )  
}  


# Saving cleanded threshold flags for the array into the RData objects
save(milk_data_pos_ph_absolute_threshold_flags_array, file = opt$output_POS_absolute)
save(milk_data_neg_ph_absolute_threshold_flags_array, file = opt$output_NEG_absolute)
