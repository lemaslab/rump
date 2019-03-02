## ----style, echo = FALSE, results = 'asis'---------------------------------
BiocStyle::markdown()

## ----echo = FALSE, results = "hide", message = FALSE-----------------------
library(BiocStyle)

## ----load-libs, message = FALSE--------------------------------------------
library(xcms)
library(msdata)

## Disable parallel processing
register(SerialParam())

## ----raw-files-------------------------------------------------------------
mzdatapath <- system.file("iontrap", package = "msdata")
list.files(mzdatapath, recursive = TRUE)

## --------------------------------------------------------------------------
library(xcms)
mzdatafiles <- list.files(mzdatapath, pattern = "extracted.mzData",
                          recursive = TRUE, full.names = TRUE)
xraw <- xcmsRaw(mzdatafiles[1], includeMSn=TRUE)
xraw


## --------------------------------------------------------------------------
peaks <- findPeaks(xraw, method="MS1")

## --------------------------------------------------------------------------
xs <- xcmsSet(mzdatafiles, method = "MS1")
xfrag <- xcmsFragments(xs)
xfrag


## --------------------------------------------------------------------------
plotTree(xfrag, xcmsFragmentPeakID = 6, textOnly = TRUE)

