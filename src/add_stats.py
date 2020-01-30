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
from sklearn.preprocessing import StandardScaler
import math
from scipy import stats

import warnings
warnings.filterwarnings('ignore')

def add_threshold(row, names):
    value = np.mean(row[names]) + 3*np.std(row[names])
    return value if value >0 else 5000 

def blank_subtraction_flag(row, name_group, name_threshold, bar):
    return (np.mean(row[name_group]) - row[name_threshold])/row[name_threshold] > bar

def zero_intension_flag(row, name_group):
    return np.mean(row[name_group]) <= 0

def add_pvalue(row, left_names, right_names):
    _, p = stats.ttest_ind(row[left_names], row[right_names])
    return p

def add_tvalue(row, left_names, right_names):
    t, _ = stats.ttest_ind(row[left_names], row[right_names])
    return t

def fold_change(row, left, right):
    if row[right] == 0:
        return np.inf
    elif row[left] == 0:
        return -np.inf
    else:
        result = row[left]/row[right]
        return result if result >=1 else -1/result

def abs_fold_change(row, fold_change_column):
        return abs(row[fold_change_column])

def add_ppm(row, library_df):
    if pd.isnull(row['row identity (main ID)']):
        return None
    mzs = list(library_df[library_df.Name.str.strip() == row['row identity (main ID)']]['M/Z'])
    mz_observe = row["row m/z"]
    diff = []
    for mz in mzs:
        diff.append(abs(mz_observe - mz))
    mz_theoretical = mzs[diff.index(min(diff))]
    return abs((mz_observe-mz_theoretical)*10e6/mz_theoretical)

def add_label(row):
    if pd.isnull(row["row identity (main ID)"]):
        return str(round(row["row m/z"],2)) + "/" + str(round(row["row retention time"], 2))
    else:
        return str(row["row identity (main ID)"]) + "/" + str(round(row["fold_change" + "(" + str(group1_name) + " versus " + str(group2_name) + ")"], 2))

def add_stats(input_file, design_file, output_file, library):

    data = pd.read_csv(input_file)
    data["number of comparisons"] = len(data)

    data_library = pd.read_csv(library)
    data["ppm"] = data.apply(lambda row: add_ppm(row, data_library), axis = 1)

    blank_group_name = "zero-blank"
    design = pd.read_csv(design_file)
    ratio_bar = 100

    group_names = list(set(design['group']))
    group_names.sort()

    group1_name = group_names[0]
    group2_name = group_names[1]

    group1_columns = design[design.group == group1_name].sampleID.tolist()
    group2_columns = design[design.group == group2_name].sampleID.tolist()

    data[str(group1_name) + '_mean'] = data[group1_columns].mean(axis = 1)
    data[str(group2_name) + '_mean'] = data[group2_columns].mean(axis = 1)

    data['label'] = data.apply(lambda row: add_label(row), axis = 1)

    logger.info("calculating fold change")

    data['fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')'] = data.apply(lambda row: fold_change(row, str(group1_name) + '_mean', str(group2_name) + '_mean'), axis = 1)
    data['log2_fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')'] = np.log2(data[str(group1_name) + '_mean']/data[str(group2_name) + '_mean'])
    data['abs_fold_change' + "(" + str(group1_name) + " versus " + str(group2_name) + ")"] = data.apply(lambda row: abs_fold_change(row, 'fold_change' + "(" + str(group1_name) + " versus " + str(group2_name) + ")"), axis = 1)

    logger.info("calculating t-test p-value")

    data['p_value'] = data.apply(lambda row: add_pvalue(row, group1_columns, group2_columns), axis = 1)
    data['t_value'] = data.apply(lambda row: add_tvalue(row, group1_columns, group2_columns), axis = 1)
    data[str(group1_name) + '_zero'] = data.apply(lambda row: zero_intension_flag(row, group1_columns), axis = 1)
    data[str(group2_name) + '_zero'] = data.apply(lambda row: zero_intension_flag(row, group2_columns), axis = 1)
    if blank_group_name in group_names:
        blank_columns = design[design.group == blank_group_name].sampleID.tolist()
        data['threshold'] = data.apply(lambda row: add_threshold(row, blank_columns), axis = 1)
        data[str(group1_name) + "_selected"] = data.apply(lambda row: blank_subtraction_flag(row, group1_columns, "threshold", ratio_bar), axis = 1)
        data[str(group2_name) + "_selected"] = data.apply(lambda row: blank_subtraction_flag(row, group2_columns, "threshold", ratio_bar), axis = 1)

    data.to_csv(output_file, index = False)

if __name__ == '__main__':

    logger.info('generating venn diagram...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="data_pos_ph.csv", required = False)
    parser.add_argument(
        '-d', '--design', help="define the location of input design csv file;", default="pos_design.csv", dest = "design", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="pos_withstats.csv", required = False)
    parser.add_argument(
        '-l', '--library', help="define the location of library file;", default="library.csv", dest = "library", required = False)

    
    args = parser.parse_args()
    add_stats(args.input, args.design, args.output, args.library)


