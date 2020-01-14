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
from scipy import stats
import copy
import csv
import seaborn as sns; sns.set(color_codes=True)

import warnings
warnings.filterwarnings('ignore')

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

def H_clustering(input_file, design_file, output_fig, ion):

    # load design file
    design = pd.read_csv(design_file)

    group_names = list(set(design['group']))
    group_names.sort()
#    blank_group_name = "zero-blank"
    group1_name = group_names[0]
    group2_name = group_names[1]

    data = pd.read_csv(input_file)
    group1_columns = design[design.group == group1_name].sampleID.tolist()
    group2_columns = design[design.group == group2_name].sampleID.tolist()

    data_filtered = copy.deepcopy(data)
    data_filtered = data_filtered.sort_values(by = "p_value").iloc[0:50]
    data_filtered.index = data_filtered.label
    data_filtered = data_filtered[group1_columns + group2_columns]

    # rename for each milk section
    for i, group1_column in enumerate(group1_columns):
        data_filtered.rename(columns = {group1_column: group1_name + '_' + str(i)}, inplace = True)
    for i, group2_column in enumerate(group2_columns):
        data_filtered.rename(columns = {group2_column: group2_name + '_' + str(i)}, inplace = True)

    logger.info(data_filtered.head())

    # Plots
    logger.info("generating plot")
    g = sns.clustermap(np.log2(data_filtered + 1), figsize = (10, 20), xticklabels=True, yticklabels=True, cmap = "seismic", cbar_kws={'label': 'log2(intension)'}, method = 'ward')
    logger.info("adjusting direction of words")
    plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)
    logger.info("saving figures")
    g.savefig(output_fig)

if __name__ == '__main__':

    logger.info('generating hierachical clustering plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="milk_data_pos_ph.csv", required = False)
    parser.add_argument(
        '-d', '--design', help="define the location of input design csv file;", default="pos_design.csv", dest = "design", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="h_cluster_pos_withbg.png", required = False)
    parser.add_argument(
        '-n', '--ion', help="positive data or negative data;", default="p", dest = "ion", required = False)

    args = parser.parse_args()
    H_clustering(args.input, args.design, args.output, args.ion)


