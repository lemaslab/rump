## ----biocstyle, echo = FALSE, results = "asis"-----------------------------
BiocStyle::markdown() 

## ----message = FALSE, warning = FALSE--------------------------------------
library(xcms)
library(RColorBrewer)
register(SerialParam()) 

## ----message = FALSE-------------------------------------------------------
## Defining the variables:
set.seed(123)
X <- sort(abs(rnorm(30, mean = 20, sd = 25))) ## 10
Y <- abs(rnorm(30, mean = 50, sd = 30))

## Bin the values in Y into 20 bins defined on X
res <- binYonX(X, Y, nBins = 22)

res 

## ----binning-imputation-example, fig = TRUE, message = FALSE, fig.width = 10, fig.height = 7, fig.cap = 'Binning and missing value imputation results. Black points represent the input values, red the results from the binning and blue and green the results from the imputation (with method lin and linbase, respectively).'----
## Plot the actual data values.
plot(X, Y, pch = 16, ylim = c(0, max(Y)))
## Visualizing the bins
abline(v = breaks_on_nBins(min(X), max(X), nBins = 22), col = "grey")

## Define colors:
point_colors <- paste0(brewer.pal(4, "Set1"), 80)
## Plot the binned values.
points(x = res$x, y = res$y, col = point_colors[1], pch = 15)

## Perform the linear imputation.
res_lin <- imputeLinInterpol(res$y)

points(x = res$x, y = res_lin, col = point_colors[2], type = "b")

## Perform the linear imputation "linbase"
res_linbase <- imputeLinInterpol(res$y, method = "linbase")
points(x = res$x, y = res_linbase, col = point_colors[3], type = "b", lty = 2) 

## --------------------------------------------------------------------------
## Define a vector with empty values at the end.
X <- 1:11
set.seed(123)
Y <- sort(rnorm(11, mean = 20, sd = 10))
Y[9:11] <- NA
nas <- is.na(Y)
## Do interpolation with profBinLin:
resX <- xcms:::profBinLin(X[!nas], Y[!nas], 5, xstart = min(X),
                          xend = max(X))
resX
res <- binYonX(X, Y, nBins = 5L, shiftByHalfBinSize = TRUE)
resM <- imputeLinInterpol(res$y, method = "lin",
                          noInterpolAtEnds = TRUE)
resM 

## ----profBinLin-problems, fig = TRUE, message = FALSE, fig.align = 'center', fig.width=10, fig.height = 7, fig.cap = "Illustration of the two bugs in profBinLin. The input values are represented by black points, grey vertical lines indicate the bins. The results from binning and interpolation with profBinLin are shown in blue and those from binYonX in combination with imputeLinInterpol in green."----
plot(x = X, y = Y, pch = 16, ylim = c(0, max(Y, na.rm = TRUE)),
     xlim = c(0, 12))
## Plot the breaks
abline(v = breaks_on_nBins(min(X), max(X), 5L, TRUE), col = "grey")
## Result from profBinLin:
points(x = res$x, y = resX, col = "blue", type = "b")
## Results from imputeLinInterpol
points(x = res$x, y = resM, col = "green", type = "b",
       pch = 4, lty = 2)
 

## ----eval = FALSE----------------------------------------------------------
#  mzarea <- seq(which.min(abs(mzs - peakArea[i, "mzmin"])),
#         which.min(abs(mzs - peakArea[i, "mzmax"])))
#  