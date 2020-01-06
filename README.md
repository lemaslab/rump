# metabolomics_data_processing

Data processing for metabolomics data. Pipeline overview (note: peak alignment and peak filling need to be done for multiple samples before merging peaks of the three tools, the process is also needed to be added to the following figure):

![alt text](https://github.com/GalaxyDream/metabolomics_data_processing/blob/master/figs/pipeline.png)

---
## Usage 

#### For SECIM and UFRC users

Adjust Slurm parameters in `run_all.nf` and Nextflow parameters in `run_all.sh`, then use the following command to run the pipeline:
```
sbatch run.sh
```

#### For other users

1. Store your positive data to `data/POS` and negative data to `data/NEG`
2. Adjust resource allocation in `nextflow.config` to make it fit to your local machine.
3. Run the following code in terminal:
```
nextflow run run_all.nf --pos_mzmine_peak_output pos_data.csv --mzmine_dir MZmine-2.28 --neg_mzmine_peak_output neg_data.csv --input_dir_pos data/POS --input_dir_neg data/NEG -with-docker galaxydream/metabolomics_pipeline
```

## Parameters description

- Use the following line to get the help information:
```
nextflow run.nf --help true
```
- Use the following line to get the version information:
```
nextflow run.nf --version true
```

## Reproducibility test according to peak detection

We aim to test whether using the exact same parameters for peak detection in MZmine is able to give us the same result. We tried it with different versions of MZmine and different operating systems, which simulates the situation that one research wants to reproduce the other researcher's published work with a different host machine.

The MZmine parameters and steps we used for peak detection are:
- Import mzXML files to MZmine
- Mass detection (detector: Centoid; noise level: 1,000; mass list name: masses; MS level: 1)
- Chromatogram buider (Mass list: masses; Min time span: 0.06; Min height: 1.0E5; m/z tolerance: 0.002 m/z or 5.0 ppm; Suffix: "chromatograms-1E5")
- Smoothing (Filename suffix: "smoothed"; Filter width: 5; Remove original peak list: False)
- Chromatogram deconvolution (Suffix: "deconvolutedTG-dd"; Algorithm: Local minimum search; Remove original peak list: True)
- Export to CSV file.

#### Using Nextflow pipeline

1. Create folders `reproducibility_test/POS/` and `reproducibility_test/NEG/`, store one mzXML file that you want to use as a test case under each of the folders.
2. Store the MZmine-2.28 folder under `reproducibility_test/`
3. Run the following code (the file `reproducibility_test/batchfile_generator.py` was created based on the MZmine parameters above):
```
nextflow run_all.nf --pos_mzmine_peak_output pos.csv --mzmine_dir reproducibility/MZmine-2.28 --neg_mzmine_peak_output neg.csv --input_dir_pos reproducibility_test/POS --input_dir_neg reproducibility_test/NEG --bs 0 --batchfile_generator reproducibility_test/batchfile_generator.py -with-docker galaxydream/metabolomics_pipeline
```
4. You will be able to see the peak detection results under `result` folder.
5. Repeat the above procedures using a different host machine, you should be able to get very similar or exact same number of peaks.

#### Without using Nextflow pipeline

1. Download a random MZmine version (e.g., MZmine-2.11) from this download page.
2. Open the downloaded MZmine.
3. Using the parameters described above for peak detection. The import files should be the mzXML files that you want to use as test cases. Record the number of peaks detected for each file.
4. Repeat the above procedures using a different host machine (usually a different operating system) and a different version of MZmine (e.g., MZmine-2.38), the detected number of peaks should be obviously different.

#### Our results

![alt text](https://github.com/GalaxyDream/metabolomics_data_processing/blob/peak_detection_nobs/figs/reproducibility_test.png)

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

## msconvert notes
- XCMS cannot process profile mode data. If the data we got is in profile mode, then we need to use `msconvert` to convert the data from profile mode to centroid mode before feeding it to XCMS.
- [msconvert (docker version)](https://hub.docker.com/r/chambm/pwiz-skyline-i-agree-to-the-vendor-licenses)
- Example command line for using msconvert (`DCSM.mzXML` stands for the data):
```
wine msconvert DCSM.mzXML --filter "peakPicking [cwt[snr=1.0][peakSpace=0.1][msLevel=1-]]" --outfile "DCSM_centroid.mzXML" --mzXML
```

## XCMS notes
- The peak detection result using xcms is very different with [this paper](https://pubs.acs.org/doi/ipdf/10.1021/acs.analchem.7b01069), this [docker file](https://cloud.docker.com/u/galaxydream/repository/docker/galaxydream/xcms_modified) is used to replicate the experiment in the paper.
- Good xcms tutorial: https://www.uab.edu/proteomics/metabolomics/workshop/2017/day3/intro_to_XCMS_in_R.pdf
- Modify `xcms v1.47.2` to enable it to detect peaks with mzTolerance instead of ppm: modify **findPeaks.centWave** in `xcmsRaw.R`; modify **getLocalNoiseEstimate** in `cwTools.R`; modify `mzROI.c`
- The xcms used in this pipeline is the most updated xcms, which only allows to define ppm as m/z tolerance.

## mzmine notes
- The peak detection result using MZmine is slightly different with [this paper](https://pubs.acs.org/doi/ipdf/10.1021/acs.analchem.7b01069), this [docker file](https://cloud.docker.com/repository/docker/galaxydream/mzmine_oldversion) is used to replicate the experiment in the paper.
- All paths in mzmine batch file (paths in config file, the path of the generated config file when running mzmine) need to be the format that xml can accept (i.e. either using absolute path, or using relative path with "./" at the begining).
- For mass detector, we use `Wavelet transform`; for chromatogram deconvolution, we use `Wavelets (XCMS)`
- If we want to export the intermidiate result and load it back, we need to export it to XML. When loading back (e.g. after doing some parse and processing with the peaks in the XML file), we need to make sure that the original data has already been imported to the left side of the window before loading the XML, otherwide a `raw data file is not found` error would be generated.

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
- For singularity on UFRC, set TMPDIR to `./tmp` after loading singularity, otherwise you may encounter "no space" error later.

## multiqc notes
- File name (ends with **\_mqc**) decides the sequence of sections.
- Use `multiqc_confit.yaml` to set the order of sections and other characteristics. Click [here](https://github.com/ewels/MultiQC/blob/master/docs/customisation.md) for detailed guideline.

## Nextflow notes
- If there is output in a process needs to be used for another process, do not add the following line to the process, otherwise it will generate error:
```
publishDir 'path/of/your/folder/', mode: 'move'
```
- Use the following line in a process if you want to save the output of the process to certain folder:
```
publishDir 'path/of/your/folder/', mode: 'copy'
```
- "$" stands for variable defined in Nextflow script, instead of system variable. If using system defined variable, use "\$".
- If system variables and Nextflow variables exist in the same shell script block, then use `!{var}` to represent Nextflow variable while use `$var` to represent system variable.
- Comment out "executor = 'slurm'", otherwise there would be an resource allocation error. It seems you need to allocate a big size of memory and cpu covering the need of all process to avoid the error.
- Check the original MZmine foder, make sure there is no additional files in it (e.g. additional data files generated by MZmine, etc.). Otherwise, these files might become input files of some processes and mess up the nextflow pipeline.