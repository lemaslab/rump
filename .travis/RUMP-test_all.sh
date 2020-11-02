#!/usr/bin/env bash

# Pull MZmine-2.53
wget https://github.com/mzmine/mzmine2/releases/download/v2.53/MZmine-2.53-Linux.zip && unzip MZmine-2.53-Linux.zip && rm MZmine-2.53-Linux.zip

# Test all processes with sample data
./nextflow main.nf --input_dir_pos .travis/data/POS/ --input_dir_neg .travis/data/NEG --POS_design_path .travis/pos_design.csv --NEG_design_path .travis/neg_design.csv --unknown_search 0 --cutoff 0.05 -with-docker xinsongdu/lemaslab_rump:v1.0.0

