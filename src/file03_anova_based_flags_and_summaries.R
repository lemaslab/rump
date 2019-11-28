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
  make_option(c("-a", "--input_POS_design"), type="character", default="milk_design_pos_ph.Rdata", 
              help="input POS design file", metavar="character"),
  make_option(c("-b", "--input_NEG_design"), type="character", default="milk_design_neg_ph.Rdata", 
              help="input NEG design file", metavar="character"),
  make_option(c("-c", "--input_POS_data"), type="character", default="milk_data_pos_ph.Rdata", 
              help="input POS data file", metavar="character"),
  make_option(c("-d", "--input_NEG_data"), type="character", default="milk_data_neg_ph.Rdata", 
              help="input NEG data file", metavar="character"),
  make_option(c("-e", "--output_POS_anova"), type="character", default="milk_data_pos_ph_anova.Rdata", 
              help="output POS absolute file", metavar="character"),
  make_option(c("-f", "--output_NEG_anova"), type="character", default="milk_data_neg_ph_anova.Rdata", 
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


# Groups to perform flags overof interest
# Extrack check that the groups are the same.
unique(milk_design_pos_ph$group2)
unique(milk_design_neg_ph$group2)

table(milk_design_pos_ph$group2)
table(milk_design_neg_ph$group2)


# complete list of groups
list_of_groups <- unique(milk_design_pos_ph$group2)
list_of_groups_treatments_only <- unique(milk_design_pos_ph$group2)[c(2,5,6)]
no_of_groups_treatment_only <- length(list_of_groups_treatments_only)

# List of ion model
list_of_ion_modes <- c("pos", "neg")



# Number of contrasts
number_of_contrasts <- length(list_of_groups_treatments_only) * ( length(list_of_groups_treatments_only) - 1 )/2

# Defining the contrasts.
contrasts_matrix <- t(matrix( c( list_of_groups_treatments_only[2], list_of_groups_treatments_only[1],
                                 list_of_groups_treatments_only[3], list_of_groups_treatments_only[2],
                                 list_of_groups_treatments_only[3], list_of_groups_treatments_only[1] ), nrow = 2, ncol = 3))



# Creating three dimensional arrays in R to store the thresholding results.
# pos
milk_data_pos_ph_anova_summaries_array  <- data.frame(matrix(0, nrow = dim(milk_data_pos_ph)[1], ncol = 18 ))
# neg
milk_data_neg_ph_anova_summaries_array  <- data.frame(matrix(0, nrow = dim(milk_data_neg_ph)[1], ncol = 18 ))



# Fixing names
# pos
colnames(milk_data_pos_ph_anova_summaries_array) <- c("row_ID", "f_value", "p_value_f", "mean_fat", "mean_skim", "mean_whole", 
                                                   "sd_fat", "sd_skim", "sd_whole", "mean_skim_fat", "mean_whole_skim", "mean_whole_fat",
                                                   "p_value_skim_fat", "p_value_whole_skim", "p_value_whole_fat", "flag_skim_fat", "flag_whole_skim", "flag_whole_fat" )
# neg
colnames(milk_data_neg_ph_anova_summaries_array) <- c("row_ID", "f_value", "p_value_f", "mean_fat", "mean_skim", "mean_whole", 
                                                   "sd_fat", "sd_skim", "sd_whole", "mean_skim_fat", "mean_whole_skim", "mean_whole_fat",
                                                   "p_value_skim_fat", "p_value_whole_skim", "p_value_whole_fat", "flag_skim_fat", "flag_whole_skim", "flag_whole_fat" )




# pos
dim(milk_data_pos_ph_anova_summaries_array)
# neg
dim(milk_data_neg_ph_anova_summaries_array)




# Looping via ion modes
for ( current_ion_mode in list_of_ion_modes )
{
  
  # Debugging step
  # current_ion_mode <- list_of_ion_modes[1]
  # current_ion_mode <- list_of_ion_modes[2]

  
  # Reassinging the name to the generic one called milk_data_current_mode_ph
  eval( parse( text = paste( "milk_data_current_mode_ph <- milk_data_", current_ion_mode, "_ph", sep ="") )  )

  # Reassinging the name to the generic one called milk_design_current_mode_ph
  eval( parse( text = paste( "milk_design_current_mode_ph <- milk_design_", current_ion_mode, "_ph", sep ="") )  )

  
  # Reassinging the name to the generic one called milk_data_current_mode_ph_anova_summaries_array
  eval( parse( text = paste( "milk_data_current_mode_ph_anova_summaries_array <- milk_data_", current_ion_mode, "_ph_anova_summaries_array", sep ="") )  )
  

  
  for ( current_group in list_of_groups_treatments_only )
  {

    # Debugging step
    # current_group <- list_of_groups_treatments_only[1]
    # current_group <- list_of_groups_treatments_only[2]
    
    # Parsing subset data of interest 
    # Samples names fo samples in the surrent group
    sample_names_current_group <- eval( parse( text=paste( "milk_design_current_mode_ph$sampleID[ milk_design_current_mode_ph$group2 == current_group]", sep ="") )  )
    # Extracting dataset with those samples extracted to sample_names_current_group_threshold_current
    eval( parse( text = paste( "milk_data_current_mode_ph_", current_group , " <-  milk_data_current_mode_ph[,sample_names_current_group]", sep ="") )  )

    # Generating mean variable for each group
    mean_variable <- paste("mean_",current_group, sep ="" )
    eval( parse( text = paste( "milk_data_current_mode_ph_anova_summaries_array[, mean_variable] <- rowMeans(milk_data_current_mode_ph_", current_group , ")", sep ="") )  )

    # Generating sd variable for each group
    sd_variable <- paste("sd_",current_group, sep ="" )
    eval( parse( text = paste( "milk_data_current_mode_ph_anova_summaries_array[, sd_variable] <- rowSds(as.matrix(milk_data_current_mode_ph_", current_group , "))", sep ="") )  )        
  }


  # Debugging step
  # head(milk_data_current_mode_ph_anova_summaries_array)
  
  
  # Saving number of rows into the variable.
  eval( parse( text = paste( "number_of_rows_current_model <- dim(milk_data_", current_ion_mode, "_ph)[1]", sep ="") )  )
  


  # Looping via row_ids and running ANOVA for each of those.
  for ( row_id_current in c(1:number_of_rows_current_model) )
  {
    # Debugging step
    # row_id_current <- 1
    
    # Combinign matrix for the current test
    
    # response for ANOVA
    eval( parse( text = paste( "anova_response_list <- c(milk_data_current_mode_ph_",list_of_groups_treatments_only[1] , "[row_id_current, ], 
                                                         milk_data_current_mode_ph_",list_of_groups_treatments_only[2] , "[row_id_current, ],
                                                         milk_data_current_mode_ph_",list_of_groups_treatments_only[3] , "[row_id_current, ])", sep ="") )  )  
    anova_response  <-  unlist( anova_response_list )
    
      
    # predictors for ANOVA
    eval( parse( text = paste( "anova_predictors_list <- c( rep( list_of_groups_treatments_only[1] , dim(milk_data_current_mode_ph_",list_of_groups_treatments_only[1] , ")[2]), 
                                                            rep( list_of_groups_treatments_only[2] , dim(milk_data_current_mode_ph_",list_of_groups_treatments_only[2] , ")[2]), 
                                                            rep( list_of_groups_treatments_only[3] , dim(milk_data_current_mode_ph_",list_of_groups_treatments_only[3] , ")[2]) )", sep ="") )  )     
    anova_predictors  <-  unlist( anova_predictors_list )


    # Fitting anova model.
    anova_fit <- aov( anova_response ~ anova_predictors  )
    # summary(anova_fit)
    # Extractking Tukey CI-s 
    tukey_fit <- TukeyHSD(anova_fit)$anova_predictors

    
    # Saving the results of the ANOVA F-test.
   
    # Passing row_ID
    milk_data_current_mode_ph_anova_summaries_array[row_id_current, "row_ID" ]  <- milk_data_current_mode_ph[row_id_current, "row_ID" ]

    # Saving the outputs  
    milk_data_current_mode_ph_anova_summaries_array[row_id_current, "f_value" ]    <-  summary(anova_fit)[[1]][["F value"]][1] 
    milk_data_current_mode_ph_anova_summaries_array[row_id_current, "p_value_f" ]  <-  summary(anova_fit)[[1]][["Pr(>F)"]][1] 
    
    # Debugging step
    # head(milk_data_current_mode_ph_anova_summaries_array) 

    
    for (current_contrast in c(1:nrow(contrasts_matrix)) )
    {

      # Debuging step
      # current_contrast <- 1

      # Definging constrast strings
      current_contrast_string_minus      <- paste( contrasts_matrix[current_contrast, 1], "-", contrasts_matrix[current_contrast, 2], sep="" )
      current_contrast_string_underscore <- paste( contrasts_matrix[current_contrast, 1], "_", contrasts_matrix[current_contrast, 2], sep="" )

      # Save strings for the mean, p-values and flags
      # Defining constrast strings
      mean_current_contrast_string_underscore    <- paste( "mean_", current_contrast_string_underscore, sep="" )
      p_value_current_contrast_string_underscore <- paste( "p_value_", current_contrast_string_underscore, sep="" )
      flag_current_contrast_string_underscore    <- paste( "flag_", current_contrast_string_underscore, sep="" )
      
      
      # extracting the Tupey HSD row index
      tukey_hsd_current_row <- which( rownames(tukey_fit) == current_contrast_string_minus )
      
      
      # Assigning the values
      # mean
      milk_data_current_mode_ph_anova_summaries_array[row_id_current, mean_current_contrast_string_underscore ]    <- tukey_fit[tukey_hsd_current_row, "diff" ] 
      # p-value
      milk_data_current_mode_ph_anova_summaries_array[row_id_current, p_value_current_contrast_string_underscore ] <- tukey_fit[tukey_hsd_current_row, "p adj" ] 
      # flags
      milk_data_current_mode_ph_anova_summaries_array[row_id_current, flag_current_contrast_string_underscore ]    <- tukey_fit[tukey_hsd_current_row, "p adj" ] < 0.05 
      
      # Debuggins step
      # head(milk_data_current_mode_ph_anova_summaries_array)
      
    }  
    
    # Debugging
    # head(milk_data_current_mode_ph_anova_summaries_array)
    
  # End of -> for ( row_id_current in c(1:number_of_rows_current_model) )  
  }  
    
  # Reassinging the name to the generic one called milk_data_current_mode_ph_anova_summaries_array
  eval( parse( text = paste( "milk_data_", current_ion_mode, "_ph_anova_summaries_array <- milk_data_current_mode_ph_anova_summaries_array", sep ="") )  )
    
  # Path for saving
#  current_mode_saving_path_rdata <- paste("R_Data/milk_data_", current_ion_mode, "_ph_anova_summaries_array.RData", sep = "")
#  current_mode_saving_path_csv   <- paste("R_Output/milk_data_", current_ion_mode, "_ph_anova_summaries_array.csv", sep = "")
  
  # Saving cleanded threshold flags for the array into the RData objects
  # RData
#  eval( parse( text = paste( "save( milk_data_", current_ion_mode, "_ph_anova_summaries_array, file = current_mode_saving_path_rdata )", sep =""  )  ) )
  # csv file
#  eval( parse( text = paste( "write.csv( milk_data_", current_ion_mode, "_ph_anova_summaries_array, file = current_mode_saving_path_csv, , row.names = FALSE,  quote = FALSE )", sep =""  )  ) )

# End of -> for ( current_ion_mode in list_of_ion_modes )  
}  

save( milk_data_pos_ph_anova_summaries_array, file = opt$output_POS_anova )
save( milk_data_neg_ph_anova_summaries_array, file = opt$output_NEG_anova )



