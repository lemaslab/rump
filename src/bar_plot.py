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
import math
import csv
import seaborn as sns; sns.set(color_codes=True)

import warnings
warnings.filterwarnings('ignore')

def data_grouping(input_file):

    data = pd.read_csv(input_file)

    # Skim && Fat
    skim_fat = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova>0.05) & 
        (data.p_value_whole_skim_anova>0.05) & 
        (data.p_value_skim_fat_anova<0.05) &
        (abs(data.foldchange_skim_fat)>2)]

    # Whole && Fat
    whole_fat = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova<0.05) & 
        (data.p_value_whole_skim_anova>0.05) & 
        (data.p_value_skim_fat_anova>0.05) &
        (abs(data.foldchange_whole_fat)>2)]

     # Whole && Skim
    whole_skim = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova>0.05) & 
        (data.p_value_whole_skim_anova<0.05) & 
        (data.p_value_skim_fat_anova>0.05) & 
        (abs(data.foldchange_whole_skim)>2)]

    # Fat
    fat = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova<0.05) & 
        (data.p_value_whole_skim_anova>0.05) & 
        (data.p_value_skim_fat_anova<0.05) & 
        (abs(data.foldchange_whole_fat)>2) &
        (abs(data.foldchange_skim_fat)>2)]

    # Skim
    skim = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova>0.05) & 
        (data.p_value_whole_skim_anova<0.05) & 
        (data.p_value_skim_fat_anova<0.05) & 
        (abs(data.foldchange_whole_skim)>2) &
        (abs(data.foldchange_skim_fat)>2)]

    # Whole
    whole = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova<0.05) & 
        (data.p_value_whole_skim_anova<0.05) & 
        (data.p_value_skim_fat_anova>0.05) & 
        (abs(data.foldchange_whole_skim)>2) &
        (abs(data.foldchange_whole_fat)>2)]

    # Difference
    different = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova<0.05) & 
        (data.p_value_whole_skim_anova<0.05) & 
        (data.p_value_skim_fat_anova<0.05) & 
        (abs(data.foldchange_whole_skim)>2) &
        (abs(data.foldchange_skim_fat)>2) &
        (abs(data.foldchange_whole_fat)>2)]

    return data, skim_fat, whole_fat, whole_skim, fat, skim, whole, different

def mean_fold_change(row, left, right, sign_left, sign_right):
    if sign_left == sign_right == "p":
        return (row[left]+row[right])/2
    elif sign_left == sign_right == "n":
        return -(row[left]+row[right])/2
    elif sign_left == "p" and sign_right == "n":
        return (row[left] - row[right])/2
    else:
        return (-row[left] + row[right])/2

def bar_plot(input_file, design_file, output_fig):

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

    data_matched = data.dropna(subset = ["row identity (main ID)"])
    data_matched_sign = data_matched[data_matched.p_value < 0.05]

    logger.info("generating bar plot")

    fold_change_sorted = data_matched_sign.sort_values(by=['fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')'])
    n_pos = min(10, len(data_matched_sign[data_matched_sign['fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')']>=0]))
    n_neg = min(10, len(data_matched_sign[data_matched_sign['fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')']<0]))
    names = fold_change_sorted.label[0:n_pos].tolist() + fold_change_sorted.label[-n_neg:].tolist()
    values = fold_change_sorted['log2_fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')'][0:n_pos].tolist() + fold_change_sorted['log2_fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')'][-n_neg:].tolist()

    index = np.arange(len(names))
    plt.barh(names, values, color = ["red"] * n_neg + ["green"] * n_pos)
    plt.xlabel('Fold Change' + "(" + str(group1_name) + " versus " + str(group2_name) + ")", fontsize=10)
    plt.ylabel('Metabolites', fontsize=10)
    plt.yticks(index, names, fontsize=10)
    plt.title("Log2 Mean Fold Change"  + " (" + str(group1_name) + " versus " + str(group2_name) + ")")

    logger.info("saving bar plot")

    plt.savefig(output_fig)

if __name__ == '__main__':

    logger.info('generating bar plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="data_pos_ph.csv", required = False)
    parser.add_argument(
        '-d', '--design', help="define the location of input design csv file;", default="pos_design.csv", dest = "design", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="barplot_pos_withbg.png", required = False)

    
    args = parser.parse_args()
    bar_plot(args.input, args.design, args.output)


