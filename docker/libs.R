# DO NOT EDIT 'install.R'; instead, edit 'install.R.in' and
# use 'rake' to generate 'install.R'.

##
## Obtain list of packages in view, as defined in config.yml
##
source("https://bioconductor.org/biocLite.R")

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("xcms", version = "3.8")

BiocInstaller::biocLite('BiocStyle')