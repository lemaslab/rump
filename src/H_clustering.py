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

def H_clustering(input_file, ion, output_fig_fat, output_fig_whole, output_fig_skim):

    data, skim_fat, whole_fat, whole_skim, fat, skim, whole, different = data_grouping(input_file)

    fig_rowsize = 0.26315789 # the height of each row in the heatmap
    n_samples = 12

    # column names for each milk section
    fat_names = ["X10_BLS010A_" + ion + "_mzXML_Peak_height", "X4_BLS002A_" + ion + "_mzXML_Peak_height", "X1_BLS001A_" + ion + "_mzXML_Peak_height", "X7_BLS003A_" + ion + "_mzXML_Peak_height"]
    whole_names = ["X12_BLS010A_" + ion + "_mzXML_Peak_height", "X6_BLS002A_" + ion + "_mzXML_Peak_height", "X3_BLS001A_" + ion + "_mzXML_Peak_height", "X9_BLS003A_" + ion + "_mzXML_Peak_height"]
    skim_names = ["X11_BLS010A_" + ion + "_mzXML_Peak_height", "X5_BLS002A_" + ion + "_mzXML_Peak_height", "X2_BLS001A_" + ion + "_mzXML_Peak_height", "X8_BLS003A_" + ion + "_mzXML_Peak_height"]

    # Extract data for each milk section
    milk_data = data[fat_names + whole_names + skim_names]
    milk_data_fat_filtered = milk_data.iloc[fat.index]
    milk_data_fat_filtered.index = fat.label
    milk_data_whole_filtered = milk_data.iloc[whole.index]
    milk_data_whole_filtered.index = whole.label
    milk_data_skim_filtered = milk_data.iloc[skim.index]
    milk_data_skim_filtered.index = skim.label

    # rename for each milk section
    for i, fat_name in enumerate(fat_names):
        milk_data_fat_filtered.rename(columns = {fat_name: 'fat_' + str(i)}, inplace = True)
    for i, whole_name in enumerate(whole_names):
        milk_data_whole_filtered.rename(columns = {whole_name: 'whole_' + str(i)}, inplace = True)
    for i, skim_name in enumerate(skim_names):
        milk_data_skim_filtered.rename(columns = {skim_name: 'skim_' + str(i)}, inplace = True)

    # Plots
    if len(milk_data_fat_filtered) > 0:
        plot_fat = sns.clustermap(np.log2(milk_data_fat_filtered + 1), figsize = (max(fig_rowsize * len(milk_data_fat_filtered) / 2, n_samples), fig_rowsize * len(milk_data_fat_filtered)), xticklabels=True, yticklabels=True, cmap = "seismic", cbar_kws={'label': 'log2(intension)'}, method = 'ward')
        plot_fat.savefig(output_fig_fat)
    else:
        plt.savefig(output_fig_fat)

    if len(milk_data_whole_filtered) > 0:
        plot_whole = sns.clustermap(np.log2(milk_data_whole_filtered + 1), figsize = (max(fig_rowsize * len(milk_data_whole_filtered) / 2, n_samples), fig_rowsize * len(milk_data_whole_filtered)), xticklabels=True, yticklabels=True, cmap = "seismic", cbar_kws={'label': 'log2(intension)'}, method = 'ward')
        plot_whole.savefig(output_fig_whole)
    else:
        plt.savefig(output_fig_whole)

    if len(milk_data_skim_filtered) > 0:
        plot_skim = sns.clustermap(np.log2(milk_data_skim_filtered + 1), figsize = (max(fig_rowsize * len(milk_data_whole_filtered) / 2, n_samples), fig_rowsize * len(milk_data_skim_filtered)), xticklabels=True, yticklabels=True, cmap = "seismic", cbar_kws={'label': 'log2(intension)'}, method = 'ward')
        plot_skim.savefig(output_fig_skim)
    else:
        plt.savefig(output_fig_skim)


if __name__ == '__main__':

    logger.info('generating hierachical clustering plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="milk_data_pos_ph.csv", required = False)
    parser.add_argument(
        '-n', '--ion', help="positive data or negative data;", default="p", dest = "ion", required = False)
    parser.add_argument(
        '-f1', '--fig1_out', help="define the location of first figure;", default="fat.csv", required = False)
    parser.add_argument(
        '-f2', '--fig2_out', help="define the location of second figure;", default="whole.csv", required = False)
    parser.add_argument(
        '-f3', '--fig3_out', help="define the location of third figure;", default="skim.csv", required = False)

    
    args = parser.parse_args()
    H_clustering(args.input, args.ion, args.fig1_out, args.fig2_out, args.fig3_out)


