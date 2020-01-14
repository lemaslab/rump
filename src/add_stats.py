#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib_venn import venn3

import warnings
warnings.filterwarnings('ignore')

def add_threshold(row, names):
    value = np.mean(row[names]) + 3*np.std(row[names])
    return value if value >0 else 5000 

def blank_subtraction_flag(row, name_group, name_threshold, bar):
    return (np.mean(row[name_group]) - row[name_threshold])/row[name_threshold] > bar

def add_pvalue(row, left_names, right_names):
    t, p = stats.ttest_ind(row[left_names], row[right_names])
    return p

def fold_change(row, left, right):
    if row[right] == 0:
        return np.inf
    elif row[left] == 0:
        return -np.inf
    else:
        result = row[left]/row[right]
        return result if result >=1 else -1/result

def add_label(row):
    if pd.isnull(row["row identity (main ID + details)"]):
        return str(round(row["row m/z"],2)) + "/" + str(round(row["row retention time"], 2))
    else:
        return row["row identity (main ID + details)"]

def add_stats(input_file, design_file, output_file):

    data = pd.read_csv(input_file)

    blank_group_name = "zero-blank"
    design = pd.read_csv(design_file)
    ratio_bar = 100

    group_names = list(set(design['group']))
    group_names.sort()

    group1_name = group_names[0]
    group2_name = group_names[1]

    group1_columns = design[design.group == group1_name].sampleID.tolist()
    group2_columns = design[design.group == group2_name].sampleID.tolist()
    blank_columns = design[design.group == blank_group_name].sampleID.tolist()

    data['group1_mean'] = data[group1_columns].mean(axis = 1)
    data['group2_mean'] = data[group2_columns].mean(axis = 1)

    data['label'] = data.apply(lambda row: add_label(row), axis = 1)
    data['fold_change'] = data.apply(lambda row: fold_change(row, "group1_mean", "group2_mean"), axis = 1)
    data['p_value'] = data.apply(lambda row: add_pvalue(row, group1_columns, group2_columns), axis = 1)
    if blank_group_name in data.columns:
        data['threshold'] = data.apply(lambda row: add_threshold(row, blank_columns), axis = 1)
        data['group1_selected'] = data.apply(lambda row: blank_subtraction_flag(row, group1_columns, "threshold", ratio_bar), axis = 1)
        data['group2_selected'] = data.apply(lambda row: blank_subtraction_flag(row, group2_columns, "threshold", ratio_bar), axis = 1)

    data.to_csv(output_file)

if __name__ == '__main__':

    logger.info('generating venn diagram...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-ir', '--input_raw', help="define the location of input (raw) csv file;", default="milk_data_pos_filtered_100.csv", dest = "input_raw", required = False)
    parser.add_argument(
        '-is', '--input_stats', help="define the location of input (stats) csv file;", default="milk_data_pos_ph_allgroups_threshold_100.csv", dest = "input_stats", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="pca_pos_withbg.png", required = False)
    
    args = parser.parse_args()
    raw_stats_merge(args.input_raw, args.input_stats, args.output)


