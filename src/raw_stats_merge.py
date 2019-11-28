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

def fold_change(row, left, right):
    if row[right] == 0:
        return np.inf
    elif row[left] == 0:
        return -np.inf
    else:
        result = row[left]/row[right]
        return result if result >=1 else -1/result

def add_label(row):
    if row.row_identity == '""':
        return str(round(row["row_m_z"],2)) + "/" + str(round(row["row_retention_time"], 2))
    else:
        return row.row_identity

def raw_stats_merge(input_raw, input_stats, output_file):

    data_raw = pd.read_csv(input_raw, delimiter = "    ")
    data_raw.columns = data_raw.columns.str.replace("\"", "")
    data_raw.row_ID = data_raw.row_ID.str.replace("\"", "")
    data_stats = pd.read_csv(input_stats)
    data_merge = data_stats.merge(data_raw)

    data_merge['label'] = data_merge.apply(lambda row: add_label(row), axis = 1)
    data_merge["foldchange_whole_skim"] = data_merge.apply(lambda row: fold_change(row, 'mean_whole_anova', 'mean_skim_anova'), axis = 1)
    data_merge["foldchange_whole_fat"] = data_merge.apply(lambda row: fold_change(row, 'mean_whole_anova', 'mean_fat_anova'), axis = 1)
    data_merge["foldchange_skim_fat"] = data_merge.apply(lambda row: fold_change(row, 'mean_skim_anova', 'mean_fat_anova'), axis = 1)
    data_merge["logfoldchange_whole_skim"] = np.log(data_merge['mean_whole_anova']/data_merge['mean_skim_anova'])
    data_merge["logfoldchange_whole_fat"] = np.log(data_merge['mean_whole_anova']/data_merge['mean_fat_anova'])
    data_merge["logfoldchange_skim_fat"] = np.log(data_merge['mean_skim_anova']/data_merge['mean_fat_anova'])
    data_merge["logpvalue_whole_fat"] = -np.log(data_merge['p_value_whole_fat_anova'])
    data_merge["logpvalue_whole_skim"] = -np.log(data_merge['p_value_whole_skim_anova'])
    data_merge["logpvalue_skim_fat"] = -np.log(data_merge['p_value_skim_fat_anova'])

    data_merge.to_csv(output_file, index = False)

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


