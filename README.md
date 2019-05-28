# metabolomics_data_processing

Data processing for metabolomics data. Pipeline overview (note: peak alignment and peak filling need to be done for multiple samples before merging peaks of the three tools, the process is also needed to be added to the following figure):

![alt text](https://github.com/GalaxyDream/metabolomics_data_processing/blob/master/figs/pipeline.png)

---
## Usage (for UFRC)

1. Load [Singularity](https://singularity.lbl.gov/), [Nextflow](https://www.nextflow.io/) and [MultiQC](https://multiqc.info/):
```
ml singularity && ml nextflow && ml gcc/5.2.0 && ml multiqc/1.5
```
2. Run pipeline on local machine using default parameters (Before running, change `input_file` in `nextflow.config` to the location of your input data file on your local machine; change `mzmine_dir` in `nextflow.config` to the location of the mzmine directory on your local machine):
```
nextflow run.nf -with-docker galaxydream/bioconductor_metabolomics
```
3. Get report with MultiQC (under development):
```
multiqc results/
```
> R codes are stored in `xcms_R`

## Parameters description

- Use the following line to get the help information:
```
nextflow run.nf --help true
```
- Use the following line to get the version information:
```
nextflow run.nf --version true
```

## R scripts notes:

1. Install [R 3.5](https://cran.r-project.org/bin/macosx/)
2. Open R 3.5, run `source("http://bioconductor.org/biocLite.R")`
3. Codes description:
> - `xcms-direct-injection.R`: Grouping FTICR-MS data with xcms
> - `xcms.R`: LCMS data preprocessing and analysis with xcms
> - `new_functionality.R`: New and modified functionality in xcms
> - `xcmsMSn.R`: Processing Tandem-MS and MSn data with xcms
> - `xcms-faahKO.R`: Modified sample file

#### Reference

[bioconductor](https://bioconductor.org/packages/release/bioc/html/xcms.html)

## xcms notes
- The peak detection result using xcms is very different with [this paper](https://pubs.acs.org/doi/ipdf/10.1021/acs.analchem.7b01069), this [docker file](https://cloud.docker.com/u/galaxydream/repository/docker/galaxydream/xcms_modified) is used to replicate the experiment in the paper.
- Good xcms tutorial: https://www.uab.edu/proteomics/metabolomics/workshop/2017/day3/intro_to_XCMS_in_R.pdf
- Modify `xcms v1.47.2` to enable it to detect peaks with mzTolerance instead of ppm: modify **findPeaks.centWave** in `xcmsRaw.R`; modify **getLocalNoiseEstimate** in `cwTools.R`; modify `mzROI.c`
- The xcms used in this pipeline is the most updated xcms, which only allows to define ppm as m/z tolerance.

## mzmine notes
- The peak detection result using MZmine is slightly different with [this paper](https://pubs.acs.org/doi/ipdf/10.1021/acs.analchem.7b01069), this [docker file](https://cloud.docker.com/repository/docker/galaxydream/mzmine_oldversion) is used to replicate the experiment in the paper.
- All paths in mzmine batch file (paths in config file, the path of the generated config file when running mzmine) need to be the format that xml can accept (i.e. either using absolute path, or using relative path with "./" at the begaining).
- For mass detector, we use `Wavelet transform`; for chromatogram deconvolution, we use `Wavelets (XCMS)`

## docker notes

- Dockerfile reference (with minor modification):
> [bioconductor/devel_metabolomics2](https://github.com/Bioconductor/bioc_docker/tree/master/out/release_metabolomics)
- `install.R` has some problem (the error message is about `failed to install library MAIT`). `libs.R` was used instead to install required R libraries for xcms codes.
- [container-xcms](https://github.com/phnmnl/container-xcms) generated an error (see logs/container_xcms_err.out) when trying to installing libraries for xcms, which might because their R version is 3.4 and not be able to install `BioManager`
- Start to run a docker image, after which you can "login" to it and inspect the content:
```
docker run --name <image name> -t <docker image> sh
```
- Inspect inside of docker environment:
```
docker exec -t -i <image name> /bin/bash
```
- Copy file from docker to local machine:
```
docker cp <image name>:/path/to/file /des/to/file
```
- Delete all containers that have a status of `exited`:
```
docker rm $(docker ps -a -q -f status=exited)
```

## multiqc notes
- File name (ends with **_mqc**) decides the sequence of sections.