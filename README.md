[![travis](https://travis-ci.com/lemaslab/RUMP.svg?branch=master)](https://travis-ci.com/lemaslab/RUMP)
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://github.com/lemaslab/RUMP/blob/master/LICENSE)

# Overview

Data processing for metabolomics data. Pipeline overview:

![alt text](https://github.com/lemaslab/RUMP/blob/master/figs/Metabolomics_Pipeline_V4.png)

# Licence

This program is released as open source software under the terms of [GNU GPL-v3.0 License](https://github.com/GalaxyDream/RUMP/blob/master/LICENSE).

# Installing

RUMP can be run in any UNIX-like system. [Nextflow](https://www.nextflow.io/) and [Docker](https://www.docker.com/) (or [Singularity](https://singularity.lbl.gov/) if using high-performance computing) are required for this software

1. Clone this repository: 
```
$ git clone https://github.com/lemaslab/RUMP.git
```
2. Move into the repository directory:
```
$ cd RUMP
```
3. Download and [MZmine-2.53](https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip) to the repository
```
wget https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip && unzip MZmine-2.53-Linux.zip && rm MZmine-2.53-Linux.zip
```
4. Pull singularity image if using high-performance computing (**if using local machine, skip this step**)
```
mkdir -p work/singularity && singularity pull --name work/singularity/xinsongdu-lemaslab_reump.img docker://xinsongdu/lemaslab_rump:v1.0.0
```

# General Behavior

RUMP accepts `.mzXML` and `.mzXL` files. Files are processed in parallel using [MZmine-2.53](http://mzmine.github.io/); several statists are calculated using [Python3](https://www.python.org/download/releases/3.0/) codes; interactive report is generated with [MultiQC](https://multiqc.info/); and pathway analysis are done with [mummichog](http://mummichog.org/).

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

### Following statistics are currently included in RUMP

* *Student t-test*: Test if there is a significant statistical difference of certain peak intensities between the two groups of samples.
* *Venn diagram*: Report the number of peaks that are significantly enriched in one of the groups, and the number of peaks that have no significant difference between two groups.
* *Principal component analysis*: Dimensional reduction using the peak intensities of the two group samples, and visualize the difference.
* *Hierarchical clustering*: Cluster all samples and plot a heatmap to show the difference between samples and peaks.
* *Bar plot*: plot the metabolites with top-10 and bottom-10 fold-change for the comparison between two groups. (note: the figure will display abnormally if there is an infinite fold change value)

### Process your own data

- Save your positive data files to `data/POS/` and negative data to `data/NEG/`
- Create design files for positve data and negative data, indicating the group of each file, save them to `data/pos_design.csv` and `data/neg_design.csv`. Sample design file can be found in `data/sample_data/pos_design.csv` and `data/sample_data/neg_design.csv`
- Process your data with default parameters using local machine
```
nextflow main.nf -with-docker xinsongdu/lemaslab_rump:v1.0.0
```
- Process your data with default parameters using high-performance computing (It is recommended to maximize CPU and memory in pos_peakDetection_mzmine and neg_peakDetection_mzmine processes in `nextflow.config` if using high-performance computing)
```
nextflow main.nf --container singularity -with-singularity docker://xinsongdu/lemaslab_rump:v1.0.0
```

### Process dataframe generatd by MZmine-2.53

- Save the dataframe for positive data and negative data to `data/pos_data.csv` and `data/neg_data.csv`
- Create design files describing the group of each column of positive/negative data, save them to `data/pos_design.csv` and `data/neg_design.csv`
- Get statistical analysis and pathway analysis
```
nextflow run_aftermzmine.nf -with-docker xinsongdu/lemaslab_rump:v1.0.0
```

### Help message

RUMP can display usage information on the command line:
```
$ Nextflow main.nf --help true
N E X T F L O W  ~  version 19.01.0
Launching `run_all.nf` [happy_heyrovsky] - revision: ae03ed6970
WARN: There's no process matching config selector: raw_stats_merge_nobg

UMPIRE: A Reproducible Untargeted Metabolomics Data Processing Pipeline - Version: 0.0.0 (20200226)
This pipeline is distributed in the hope that it will be useful
but WITHOUT ANY WARRANTY. See the GNU GPL v3.0 for more details.

Please report comments and bugs to xinsongdu@ufl.edu
or at https://github.com/lemaslab/RUMP/issues.
Check https://github.com/lemaslab/RUMP for updates, and refer to
https://github.com/lemaslab/RUMP/wiki

Usage:
   nextflow run_all.nf [options] -with-docker xinsongdu/lemaslab_rump:v1.0.0

Arguments (it is mandatory to change `input_file` and `mzmine_dir` before running:
----------------------------- common parameters ----------------------------------
    --input_dir_pos                         folder location for positive data, default is 'data/POS'
    --input_dir_neg                         folder location for positive data, default is 'data/NEG'
    --POS_design_path                       location for positive design file, default is 'data/pos_design.csv'
    --NEG_design_path                       location for negative design file, default is 'data/neg_design.csv'
    --cutoff                                cutoff p-value for mummichog pathway analysis, default is 0.05
    --version                               whether to show version information or not, default is null
    --help                                  whether to show help information or not, default is null
Please refer to nextflow.config for more options.

Container:
    Docker image to use with -with-docker|-with-singularity options is
    'docker://xinsongdu/lemaslab_rump:v1.0.0'

RUMP supports .mzXML format files.
```

### Logging

Logs and error reports will be stored under `logs` folder after running.

### Clean repository

Run the following command to clean all the files generated by Nextflow
```
bash clear.sh
```

### Exit status values

RUMP returns the following exit status values:
- 3: Positive file groups are not the same as negative file groups, please check design files.
- 4: Not all input files are in .mzXML format, please check input data folders.
- 5: One or more input files does not exist.
- Other Linux reserved exit codes: https://tldp.org/LDP/abs/html/exitcodes.html

# Testing

### Test data

- Sample test input files are provided in the `functional_test/sample_data/POS` and `functional_test/sample_data/NEG` folders, which are from [Metabolomics Workbench PR000188](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Project&ProjectID=PR000188).
- Design files are `functional_test/sample_data/pos_design.csv` and `functional_test/sample_data/neg_design.csv`.
- It may take around 8 hours to finish if using default resource settings in `nextflow.config`. See `functional_test/sample_Nextflow_output/timeline.html` for detail.

### Running tests on local machine

```
nextflow main.nf --input_dir_pos functional_test/sample_data/POS/ --input_dir_neg functional_test/sample_data/NEG --POS_design_path functional_test/sample_data/pos_design.csv --NEG_design_path functional_test/sample_data/neg_design.csv -with-docker xinsongdu/lemaslab_rump:v1.0.0
```

### Running tests on high-performance computing

```
nextflow main.nf --input_dir_pos functional_test/sample_data/POS/ --input_dir_neg functional_test/sample_data/NEG --POS_design_path functional_test/sample_data/pos_design.csv --NEG_design_path functional_test/sample_data/neg_design.csv --container singularity -with-singularity docker://xinsongdu/lemaslab_rump:v1.0.0
```

# Bug reporting and feature requests

Please submit bug reports and feature requests to the issue tracker on GitHub:

[RUMP issue tracker](https://github.com/lemaslab/RUMP/issues)