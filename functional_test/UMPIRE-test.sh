#!/usr/bin/env bash

# Pull MZmine-2.53
wget https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip && unzip MZmine-2.53-Linux.zip && rm MZmine-2.53-Linux.zip

# Test with sample data
./nextflow run_all.nf --input_dir_pos functional_test/sample_data/POS/ --input_dir_neg functional_test/sample_data/NEG --POS_design_path functional_test/sample_data/pos_design.csv --NEG_design_path functional_test/sample_data/neg_design.csv -with-docker galaxydream/metabolomics_pipeline