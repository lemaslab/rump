#!/bin/bash

# Test processes MZmine output files with sample data
./nextflow run_aftermzmine.nf --input_dir_pos .travis/data/POS/ --input_dir_neg .travis/data/NEG --POS_design_path .travis/pos_design.csv --NEG_design_path .travis/neg_design.csv --cutoff 1 --pos_mzmine_peak_output .travis/pos_data.csv --neg_mzmine_peak_output .travis/neg_data.csv -with-docker xinsongdu/lemaslab_rump:v1.0.0
