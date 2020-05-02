[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0b6bdc545b50439596d40f3917ef3aa6)](https://app.codacy.com/gh/lemaslab/RUMP?utm_source=github.com&utm_medium=referral&utm_content=lemaslab/RUMP&utm_campaign=Badge_Grade_Dashboard)
[![release](https://zenodo.org/badge/DOI/10.5281/zenodo.3774470.svg)](https://zenodo.org/record/3774470#.XqiOhBcnaL8)
[![travis](https://travis-ci.com/lemaslab/RUMP.svg?branch=master)](https://travis-ci.com/lemaslab/RUMP)
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://github.com/lemaslab/RUMP/blob/master/LICENSE)

# RUMP

![alt text](https://github.com/lemaslab/RUMP/blob/master/figs/Metabolomics_Pipeline_V4.png)

## Licence

This program is released as open source software under the terms of [GNU GPL-v3.0 License](https://github.com/GalaxyDream/RUMP/blob/master/LICENSE).

## Usage
Please refer to our [wiki](https://github.com/lemaslab/RUMP/wiki) for how to install and use RUMP

## Help message

RUMP can display usage information on the command line:
```
$ Nextflow main.nf --help true
N E X T F L O W  ~  version 19.01.0
Launching `main.nf` [romantic_celsius] - revision: 9004e52396
Project : /Users/xinsongdu/mnt/projects/RUMP
Git info: null - null [null]
Cmd line: /Users/xinsongdu/.pyenv/shims/Nextflow main.nf --help true
Manifest's pipeline version: 0.0.0

RUMP: A Reproducible Untargeted Metabolomics Data Processing Pipeline - Version: 0.0.0 (20200226)
This pipeline is distributed in the hope that it will be useful
but WITHOUT ANY WARRANTY. See the GNU GPL v3.0 for more details.

Please report comments and bugs to xinsongdu@ufl.edu
or at https://github.com/lemaslab/RUMP/issues.
Check https://github.com/lemaslab/RUMP for updates, and refer to
https://github.com/lemaslab/RUMP/wiki

Usage:
   nextflow run_all.nf [options] -with-docker xinsongdu/lemaslab_rump:v0.0.0

Arguments (it is mandatory to change `input_file` and `mzmine_dir` before running:
----------------------------- common parameters ----------------------------------
    --input_dir_pos                         folder location for positive data, default is 'data/POS'
    --input_dir_neg                         folder location for positive data, default is 'data/NEG'
    --POS_design_path                       location for positive design file, default is 'data/pos_design.csv'
    --NEG_design_path                       location for negative design file, default is 'data/neg_design.csv'
    --cutoff                                cutoff p-value for mummichog pathway analysis, default is 0.05
    --unknown_search                        whether do unknown search for unidentified metabolites or not, default is '0', please set it to '1' when needed
    --version                               whether to show version information or not, default is null
    --help                                  whether to show help information or not, default is null
Please refer to nextflow.config for more options.

Container:
    Docker image to use with -with-docker|-with-singularity options is
    'docker://xinsongdu/lemaslab_rump:v0.0.0'

RUMP supports .mzXML format files.
```

## Components

RUMP accepts `.mzXML` and `.mzXL` files. Files are processed in parallel using [MZmine-2.53](http://mzmine.github.io/); several statists are calculated using [Python3](https://www.python.org/download/releases/3.0/) codes; interactive report is generated with [MultiQC](https://multiqc.info/); pathway analysis are done with [mummichog](http://mummichog.org/); unknown metabolites search are done with [CEU Mass Mediator](https://github.com/lzyacht/cmmr). Note that the processes related to unknow search with CEU Mass Mediator is turned off by default due to their unstable server, it can be turned on by setting parameter `--unknown_search` to "1".

## Default parameter settings for MZmine-2.53 (the following parameters are specifically for data processed by [SECIM Core](http://secim.ufl.edu/)):

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

## Currently included statistical analysis

* *Student t-test*: Test if there is a significant statistical difference of certain peak intensities between the two groups of samples.
* *Venn diagram*: Report the number of peaks that are significantly enriched in one of the groups, and the number of peaks that have no significant difference between two groups.
* *Principal component analysis*: Dimensional reduction using the peak intensities of the two group samples, and visualize the difference.
* *Hierarchical clustering*: Cluster all samples and plot a heatmap to show the difference between samples and peaks.
* *Bar plot*: plot the metabolites with top-10 and bottom-10 fold-change for the comparison between two groups. (note: the figure will display abnormally if there is an infinite fold change value)

## Logging

Logs and error reports will be stored under `logs/` folder after running.

## Clean repository

Run the following command to clean all the files generated by Nextflow
```
bash clear.sh
```

## Exit status values

RUMP returns the following exit status values:
- 3: Positive file groups are not the same as negative file groups, please check design files.
- 4: Not all input files are in .mzXML format, please check input data folders.
- 5: One or more input files does not exist.
- Other Linux reserved exit codes: https://tldp.org/LDP/abs/html/exitcodes.html

## Bug reporting and feature requests

Please submit questions, bug reports and feature requests to the issue tracker on GitHub:

[RUMP issue tracker](https://github.com/lemaslab/RUMP/issues)