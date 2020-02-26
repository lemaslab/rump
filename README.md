[![travis](https://travis-ci.com/lemaslab/ReUMP.svg?branch=master)](https://travis-ci.com/lemaslab/ReUMP)
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://github.com/lemaslab/ReUMP/blob/master/LICENSE)

# Overview

Data processing for metabolomics data. Pipeline overview:

![alt text](https://github.com/lemaslab/ReUMP/blob/master/figs/pipeline.png)

# Licence

This program is released as open source software under the terms of [GNU GPL-v3.0 License](https://github.com/GalaxyDream/ReUMP/blob/master/LICENSE).

# Installing

ReUMP can be run in any UNIX-like system. [Docker](https://www.docker.com/) (or [Singularity](https://singularity.lbl.gov/) if using high-performance computing) are required for this software

1. Clone this repository: 
```
$ git clone https://github.com/lemaslab/ReUMP.git
```
2. Move into the repository directory:
```
$ cd ReUMP
```
3. Download [Nextflow](https://www.nextflow.io/) and [MZmine-2.53](https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip) to the repository
```
curl -s https://get.nextflow.io | bash && wget https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip && unzip MZmine-2.53-Linux.zip && rm MZmine-2.53-Linux.zip
```
4. Pull singularity image if using high-performance computing (**if using local machine, skip this step**)
```
mkdir -p work/singularity && singularity pull --name work/singularity/galaxydream-metabolomics_pipeline.img docker://galaxydream/metabolomics_pipeline
```

# General Behavior

ReUMP accepts `.mzXML` and `.mzXL` files. Files are processed in parallel using [MZmine-2.53](http://mzmine.github.io/); several statists are calculated using [Python3](https://www.python.org/download/releases/3.0/) codes; interactive report is generated with [MultiQC](https://multiqc.info/); and pathway analysis are done with [mummichog](http://mummichog.org/).

#### Default parameter settings for MZmine-2.53 (the following parameters are specifically for data processed by [SECIM Core](http://secim.ufl.edu/)):

Positive ion mode:
- Mass detection (detector: Centoid; noise level: 1,000; mass list name: masses; Scans: MS level - 1)
- Chromatogram buider (Mass list: masses; Min time span: 0.06; Min height: 1.0E5; m/z tolerance: 0.002 m/z or 5.0 ppm; Suffix: "chromatograms-1E5")
- Smoothing (Filename suffix: "smoothed"; Filter width: 5; Remove original peak list: False)
- Chromatogram deconvolution (Suffix: "deconvoluted"; Algorithm: Local minimum search; Chromatographic threshold: 0.95; Search minimum in RT range (min): 0.05; Minimum relative height: 0.05; Minimum absolute height: 30000.0; Min ratio of peak top/edge: 3.0; Minimum peak duration range (min): 0.06; Maximum peak duration range (min): 1.0; Remove original peak list: True)
- Isotopic peak grouper (Name suffix: deisopoted; m/z tolerance: 0.002 m/z or 5.0 ppm; Retention time tolerance: 0.05; Monotonic shape: false; Maximum charge: 3; Representative isotope: Most intense; Remove original peaklist: true)
- Join aligner (Feature list name: Aligned feature list; m/z tolerance: 0.003 m/z or 5.0 ppm; Weight for m/z: 20.0; Retention time tolerance: 0.05; Weight for RT: 20.0; Require same charge state: false; Require same ID: false; Compare isotope pattern: false; compare spectra similarity: false)
- Peak finder (Name suffix: gap-filled; intensity tolerance: 0.25; m/z tolerance: 0.003 m/z or 5.0 ppm; Retention time tolerance: absolute, 0.05; RT correction: false; Parallel: false; Remove original feature list: false)
- Duplicate peak filter (Name suffix: filtered; Filter mode: NEW AVERAGE; m/z tolerance: 0.002 m/z or 5.0 ppm; RT tolerance: absolute, 0.05; Require same identification: false; Remove original peaklist: false)
- Adduct search (RT tolerance: absolute, 0.05; select all Adducts; m/z tolerance: 0.003 m/z or 5.0 ppm; Max relative adduct peak height: 0.4)
- Complex search (Ionization method: [M+H]+; Retention time tolerance: absolute, 0.05; m/z tolerance: 0.002 m/z or 5.0 ppm; Max complex peak height: 5.0)
- Custom database search (m/z tolerance: 0.001 m/z or 5.0 ppm; Retention time tolerance: absolute, 0.2)

Negative mode:
- Mass detection (detector: Centoid; noise level: 1,000; mass list name: masses; Scans: MS level - 1)
- Chromatogram buider (Mass list: masses; Min time span: 0.06; Min height: 1.0E5; m/z tolerance: 0.005 m/z or 10.0 ppm; Suffix: "chromatograms-1E5")
- Smoothing (Filename suffix: "smoothed"; Filter width: 5; Remove original peak list: False)
- Chromatogram deconvolution (Suffix: "deconvoluted"; Algorithm: Local minimum search; Chromatographic threshold: 0.95; Search minimum in RT range (min): 0.2; Minimum relative height: 0.05; Minimum absolute height: 30000.0; Min ratio of peak top/edge: 3.0; Minimum peak duration range (min): 0.06; Maximum peak duration range (min): 1.0; Remove original peak list: True)
- Isotopic peak grouper (Name suffix: deisopoted; m/z tolerance: 0.005 m/z or 10.0 ppm; Retention time tolerance: 0.05; Monotonic shape: false; Maximum charge: 2; Representative isotope: Most intense; Remove original peaklist: true)
- Join aligner (Feature list name: Aligned feature list; m/z tolerance: 0.005 m/z or 10.0 ppm; Weight for m/z: 20.0; Retention time tolerance: 0.05; Weight for RT: 15.0; Require same charge state: false; Require same ID: false; Compare isotope pattern: false; compare spectra similarity: false)
- Peak finder (Name suffix: gap-filled; intensity tolerance: 0.25; m/z tolerance: 0.005 m/z or 10.0 ppm; Retention time tolerance: absolute, 0.3; RT correction: false; Parallel: false; Remove original feature list: false)
- Duplicate peak filter (Name suffix: filtered; Filter mode: NEW AVERAGE; m/z tolerance: 0.003 m/z or 10.0 ppm; RT tolerance: absolute, 0.05; Require same identification: false; Remove original peaklist: false)
- Adduct search (RT tolerance: absolute, 0.05; select all Adducts; m/z tolerance: 0.003 m/z or 10.0 ppm; Max relative adduct peak height: 0.4)
- Complex search (Ionization method: [M-H]-; Retention time tolerance: absolute, 0.05; m/z tolerance: 0.003 m/z or 10.0 ppm; Max complex peak height: 0.4)
- Custom database search (m/z tolerance: 0.003 m/z or 10.0 ppm; Retention time tolerance: absolute, 0.2)

### Following statistics are currently included in ReUMP

* *Student t-test*: Test if there is a significant statistical difference of certain peak intensities between the two groups of samples.
* *Venn diagram*: Report the number of peaks that are significantly enriched in one of the groups, and the number of peaks that have no significant difference between two groups.
* *Principal component analysis*: Dimensional reduction using the peak intensities of the two group samples, and visualize the difference.
* *Hierarchical clustering*: Cluster all samples and plot a heatmap to show the difference between samples and peaks.
* *Bar plot*: plot the metabolites with top-10 and bottom-10 fold-change for the comparison between two groups. (note: the figure will display abnormally if there is an infinite fold change value)

### Process your own data

- Save your positive data files to `data/POS/` and negative data to `data/NEG/`
- Create design files for positve data and negative data, indicating the group of each file. Sample design file can be found in `data/sample_data/pos_design.csv` and `data/sample_data/neg_design.csv`
- Process your data with default parameters using local machine
```
Nextflow run_all.nf -with-docker galaxydream/metabolomics_pipeline
```
- Process your data with default parameters using high-performance computing (It is recommended to maximize CPU and memory in pos_peakDetection_mzmine and neg_peakDetection_mzmine processes in `nextflow.config` if using high-performance computing)
```
Nextflow run_all.nf --use_singularity 1 -with-singularity docker://galaxydream/metabolomics_pipeline
```

### Process dataframe generatd by MZmine-2.53

- Save the dataframe for positive data and negative data to `data/pos_data.csv` and `data/neg_data.csv`
- Create design files describing the group of each column of positive/negative data, save them to `data/pos_design.csv` and `data/neg_design.csv`
- Get statistical analysis and pathway analysis
```
Nextflow run_aftermzmine.nf -with-docker galaxydream/metabolomics_pipeline
```

### Help message

ReUMP can display usage information on the command line:
```
Nextflow run_all.nf --help true
```

### Logging

Log file `nextflow_report.html` will be output to current folder.

### Clean repository

Run the following command to clean all the files generated by Nextflow
```
bash clear.sh
```

# Testing

### Test data

- Sample test input files are provided in the `functional_test/sample_data/POS` and `functional_test/sample_data/NEG` folders, which are from [Metabolomics Workbench PR000188](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Project&ProjectID=PR000188).
- Design files are `functional_test/sample_data/pos_design.csv` and `functional_test/sample_data/neg_design.csv`.
- It may take around 6 hours to finish if using default resource settings in `nextflow.config`. See `functional_test/sample_Nextflow_output/timeline.html` for detail.

### Running tests on local machine

```
nextflow run_all.nf --input_dir_pos functional_test/sample_data/POS/ --input_dir_neg functional_test/sample_data/NEG --POS_design_path functional_test/sample_data/pos_design.csv --NEG_design_path functional_test/sample_data/neg_design.csv -with-docker galaxydream/metabolomics_pipeline
```

### Running tests on high-performance computing

```
nextflow run_all.nf --input_dir_pos functional_test/sample_data/POS/ --input_dir_neg functional_test/sample_data/NEG --POS_design_path functional_test/sample_data/pos_design.csv --NEG_design_path functional_test/sample_data/neg_design.csv --use_singularity 1 -with-singularity docker://galaxydream/metabolomics_pipeline
```

# Bug reporting and feature requests

Please submit bug reports and feature requests to the issue tracker on GitHub:

[ReUMP issue tracker](https://github.com/lemaslab/ReUMP/issues)