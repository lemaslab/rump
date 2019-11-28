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

def bar_plot(input_file, output_fig_fat, output_fig_whole, output_fig_skim):

    data, skim_fat, whole_fat, whole_skim, fat, skim, whole, different = data_grouping(input_file)

    if len(fat) > 0:
        fat["mean_foldchange_fat"] = data.apply(lambda row: mean_fold_change(row, 'logfoldchange_skim_fat', 'logfoldchange_whole_fat', 'n', 'n'), axis = 1)
        fat_fold_change_sorted = fat.sort_values(by=["mean_foldchange_fat"])
        n_pos = min(10, len(fat[fat.mean_foldchange_fat>=0]))
        n_neg = min(10, len(fat[fat.mean_foldchange_fat<0]))
        names_fat = fat_fold_change_sorted.label[0:n_pos].tolist() + fat_fold_change_sorted.label[-n_neg:].tolist()
        values = fat_fold_change_sorted.mean_foldchange_fat[0:n_pos].tolist() + fat_fold_change_sorted.mean_foldchange_fat[-n_neg:].tolist()

        index = np.arange(len(names_fat))
        plt.barh(names_fat, values, color = ["red"] * n_neg + ["green"] * n_pos)
        plt.xlabel('Mean Fold Change', fontsize=10)
        plt.ylabel('Metabolites', fontsize=10)
        plt.yticks(index, names_fat, fontsize=10)
        plt.title('Log2 Mean Fold Change (Threshold is Fat)')
    plt.savefig(output_fig_fat, bbox_inches="tight")
    plt.clf()

    if len(whole) > 0:
        whole["mean_foldchange_whole"] = data.apply(lambda row: mean_fold_change(row, 'logfoldchange_whole_skim', 'logfoldchange_whole_fat', 'p', 'p'), axis = 1)
        whole_fold_change_sorted = whole.sort_values(by=["mean_foldchange_whole"])
        n_pos = min(10, len(whole[whole.mean_foldchange_whole>=0]))
        n_neg = min(10, len(whole[whole.mean_foldchange_whole<0]))
        names_whole = whole_fold_change_sorted.label[0:n_pos].tolist() + whole_fold_change_sorted.label[-n_neg:].tolist()
        values = whole_fold_change_sorted.mean_foldchange_whole[0:n_pos].tolist() + whole_fold_change_sorted.mean_foldchange_whole[-n_neg:].tolist()

        index = np.arange(len(names_whole))
        plt.barh(names_whole, values, color = ["red"] * n_neg + ["green"] * n_pos)
        plt.xlabel('Mean Fold Change', fontsize=10)
        plt.ylabel('Metabolites', fontsize=10)
        plt.yticks(index, names_whole, fontsize=10)
        plt.title('Log2 Mean Fold Change (Threshold is whole)')
    plt.savefig(output_fig_whole, bbox_inches="tight")
    plt.clf()

    if len(skim) > 0:
        skim["mean_foldchange_skim"] = data.apply(lambda row: mean_fold_change(row, 'logfoldchange_skim_fat', 'logfoldchange_whole_skim', 'p', 'n'), axis = 1)
        skim_fold_change_sorted = skim.sort_values(by=["mean_foldchange_skim"])
        n_pos = min(10, len(skim[skim.mean_foldchange_skim>=0]))
        n_neg = min(10, len(skim[skim.mean_foldchange_skim<0]))
        names_skim = skim_fold_change_sorted.label[0:n_pos].tolist() + skim_fold_change_sorted.label[-n_neg:].tolist()
        values = skim_fold_change_sorted.mean_foldchange_skim[0:n_pos].tolist() + skim_fold_change_sorted.mean_foldchange_skim[-n_neg:].tolist()

        index = np.arange(len(names_skim))
        plt.barh(names_skim, values, color = ["red"] * n_neg + ["green"] * n_pos)
        plt.xlabel('Mean Fold Change', fontsize=10)
        plt.ylabel('Metabolites', fontsize=10)
        plt.yticks(index, names_skim, fontsize=10)
        plt.title('Log2 Mean Fold Change (Threshold is skim)')
    plt.savefig(output_fig_skim, bbox_inches="tight")
    plt.clf()

if __name__ == '__main__':

    logger.info('generating bar plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="milk_data_pos_ph.csv", required = False)
    parser.add_argument(
        '-f1', '--fig1_out', help="define the location of first figure;", default="fat.png", required = False)
    parser.add_argument(
        '-f2', '--fig2_out', help="define the location of second figure;", default="whole.png", required = False)
    parser.add_argument(
        '-f3', '--fig3_out', help="define the location of third figure;", default="skim.png", required = False)

    
    args = parser.parse_args()
    bar_plot(args.input, args.fig1_out, args.fig2_out, args.fig3_out)


