#!/usr/bin/env bash

# Pull MZmine-2.53
wget https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip && unzip MZmine-2.53-Linux.zip && rm MZmine-2.53-Linux.zip

# Test all processes with sample data
./nextflow run_all.nf --input_dir_pos .travis/data/POS/ --input_dir_neg .travis/data/NEG --POS_design_path .travis/pos_design.csv --NEG_design_path .travis/neg_design.csv --cutoff 1 -with-docker galaxydream/metabolomics_pipeline

# Test processes after MZmine with sample data
./nextflow run_aftermzmine.nf --input_dir_pos .travis/data/POS/ --input_dir_neg .travis/data/NEG --POS_design_path .travis/pos_design.csv --NEG_design_path .travis/neg_design.csv --cutoff 1 --pos_mzmine_peak_output .travis/pos_data.csv --neg_mzmine_peak_output .travis/neg_data.csv -with-docker galaxydream/metabolomics_pipeline
