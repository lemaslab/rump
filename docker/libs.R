##
## Obtain list of packages needed for running xcms
##
source("https://bioconductor.org/biocLite.R")

if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("xcms", version = "3.8")

BiocInstaller::biocLite('BiocStyle')
BiocInstaller::biocLite('faahKO')
BiocInstaller::biocLite('pander')
BiocInstaller::biocLite('RColorBrewer')
BiocInstaller::biocLite('magrittr')
install.packages("optparse")