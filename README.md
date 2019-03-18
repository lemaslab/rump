# metabolomics_data_processing

Data processing for metabolomics data

---
## Usage (for UFRC)

1. Load singularity and nextflow:
```
ml singularity && ml nextflow && ml gcc/5.2.0 && ml multiqc/1.5
```
2. Run sample code (If you use `slurm`, please remove the `//` of 29th line in `nextflow.config`. Output files will be stored in `results` folder):
```
nextflow run_sample.nf -with-singularity docker://galaxydream/bioconductor_metabolomics --plot_1 <file name of the first plot, default is "chromatograms_1_mqc.jpeg"> --plot_2 <file name of the second plot, default is "ion_current_mqc.jpeg"> --plot_3 <file name of the third plot, default is "chromatograms_2_mqc.jpeg">
```
3. Get report with [MultiQC](https://multiqc.info/)
```
multiqc results/
```
> R codes are stored in `xcms_R`

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

## Some docker notes

- Dockerfile reference (with minor modification):
> [bioconductor/devel_metabolomics2](https://github.com/Bioconductor/bioc_docker/tree/master/out/release_metabolomics)
- `install.R` has some problem (the error message is about `failed to install library MAIT`). `libs.R` was used instead to install required R libraries for xcms codes.
- [container-xcms](https://github.com/phnmnl/container-xcms) generated an error (see logs/container_xcms_err.out) when trying to installing libraries for xcms, which might because their R version is 3.4 and not be able to install `BioManager`
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
