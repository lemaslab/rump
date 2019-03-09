## ----style, echo = FALSE, results = 'asis'---------------------------------
BiocStyle::markdown()

## ----echo = FALSE, results = "hide", message = FALSE-----------------------
library(BiocStyle)

## ----load-libs, message = FALSE, results = "hide"--------------------------
library(xcms)
library(MassSpecWavelet)

register(SerialParam())

## ----load-data, message = FALSE, results = "hide"--------------------------
mzdata_path <- system.file("fticr", package = "msdata")
mzdata_files <- list.files(mzdata_path, recursive = TRUE, full.names = TRUE)

## Create a data.frame assigning samples to sample groups, i.e. ham4 and ham5.
grp <- rep("ham4", length(mzdata_files))
grp[grep(basename(mzdata_files), pattern = "^HAM005")] <- "ham5"
pd <- data.frame(filename = basename(mzdata_files), sample_group = grp)

## Load the data.
ham_raw <- readMSData(files = mzdata_files,
                      pdata = new("NAnnotatedDataFrame", pd),
                      mode = "onDisk")

## --------------------------------------------------------------------------
## Only a single spectrum with an *artificial* retention time is available
## for each sample
rtime(ham_raw)

## ----msw-------------------------------------------------------------------
## Define the parameters for the peak detection
msw <- MSWParam(scales = c(1, 4, 9), nearbyPeak = TRUE, winSize.noise = 500,
                SNR.method = "data.mean", snthresh = 10)

ham_prep <- findChromPeaks(ham_raw, param = msw)

head(chromPeaks(ham_prep))

## ----message = FALSE-------------------------------------------------------
## Subset to the first file.
first_file <- filterFile(ham_prep, file = 1)

## Extract 3 m/z values
calib_mz <- chromPeaks(first_file)[c(1, 4, 7), "mz"]
calib_mz <- calib_mz + 0.00001 * runif(1, 0, 0.4) * calib_mz + 0.0001


## ----message = FALSE-------------------------------------------------------
## Set-up the parameter class for the calibration
prm <- CalibrantMassParam(mz = calib_mz, method = "edgeshift",
                          mzabs = 0.0001, mzppm = 5)
first_file_calibrated <- calibrate(first_file, param = prm)


## ----calibrationresult, fig = TRUE, fig.width = 6, fig.height = 5, fig.align = "center"----
diffs <- chromPeaks(first_file_calibrated)[, "mz"] -
    chromPeaks(first_file)[, "mz"]

plot(x = chromPeaks(first_file)[, "mz"], xlab = expression(m/z[raw]),
     y = diffs, ylab = expression(m/z[calibrated] - m/z[raw]))


## ----correspondence, message = FALSE, results = "hide"---------------------
## Using default settings but define sample group assignment
mzc_prm <- MzClustParam(sampleGroups = ham_prep$sample_group)
ham_prep <- groupChromPeaks(ham_prep, param = mzc_prm)


## --------------------------------------------------------------------------
ham_prep

## --------------------------------------------------------------------------
featureDefinitions(ham_prep)

## ----feature1, fig = TRUE, fig.width = 6, fig.height = 4, fig.align = "center"----
## Get the peaks belonging to the first feature
pks <- chromPeaks(ham_prep)[featureDefinitions(ham_prep)$peakidx[[1]], ]

## Define the m/z range
mzr <- c(min(pks[, "mzmin"]) - 0.001, max(pks[, "mzmax"]) + 0.001)

## Subset the object to the m/z range
ham_prep_sub <- filterMz(ham_prep, mz = mzr)

## Extract the mz and intensity values
mzs <- mz(ham_prep_sub, bySample = TRUE)
ints <- intensity(ham_prep_sub, bySample = TRUE)

## Plot the data
plot(3, 3, pch = NA, xlim = range(mzs), ylim = range(ints), main = "FT01",
     xlab = "m/z", ylab = "intensity")
## Define colors
cols <- rep("#ff000080", length(mzs))
cols[ham_prep_sub$sample_group == "ham5"] <- "#0000ff80"
tmp <- mapply(mzs, ints, cols, FUN = function(x, y, col) {
    points(x, y, col = col, type = "l")
})


## --------------------------------------------------------------------------
feat_vals <- featureValues(ham_prep, value = "into")
head(feat_vals)


## ----fillpeaks, message = FALSE--------------------------------------------
ham_prep <- fillChromPeaks(ham_prep, param = FillChromPeaksParam())

head(featureValues(ham_prep, value = "into"))
