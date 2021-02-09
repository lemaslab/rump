#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description : This code do bar plot for peak table output by MZmine-2.53,
              peak table should firstly be processed by "add_stats.py" before
              input to this program
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : MIT License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python bar_plot.py -i $input_peak_table
                                 -d $design_file_location
                                 -o $output_figure_location
                                 -m $only_use_identified_metabolites_or_not
                                 -bs $do_blank_subtraction_or_not
"""
import sys
import warnings
import logging
import logging.handlers
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

sns.set(color_codes=True)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

def bar_plot(data_file, design_file, output_fig, only_matched, bs):
    """
    Draw bar plot for two group comparison based on peak table.

    # Arguments:
        data_file: peak table.
        design_file: design file corresponding to the peak table.
        output_fig: the name of outpuf bar plot figure.
        bs: if the peak table is produced before (False) or after (True) blank subtraction.

    # Outputs:
        bar plot figure.
    """

    # load design file
    design = pd.read_csv(design_file)

    group_names = list(set(design['group']))
    group_names.sort()
#    blank_group_name = "zero-blank"
    group1_name = group_names[0]
    group2_name = group_names[1]

    data = pd.read_csv(data_file)

    if only_matched == "1":
        data_matched = data[data.ppm < 5]
    else:
        data_matched = data
    data_matched_sign = data_matched[data_matched.adjusted_p_value < 0.05]

    logger.info("generating bar plot")

    fold_change_sorted = data_matched_sign.sort_values(by=\
        ['fold_change' + '(' + str(group1_name) + ' versus ' + str(group2_name) + ')'])

    n_pos = min(10, len(data_matched_sign[data_matched_sign['fold_change' + '(' + \
        str(group1_name) + ' versus ' + str(group2_name) + ')'] >= 0]))

    n_neg = min(10, len(data_matched_sign[data_matched_sign['fold_change' + '(' + \
        str(group1_name) + ' versus ' + str(group2_name) + ')'] < 0]))

    if n_neg != 0:
        names = fold_change_sorted.label[0:n_pos].tolist() + \
        fold_change_sorted.label[-n_neg:].tolist()

        values = fold_change_sorted['log2_fold_change' + '(' + \
        str(group1_name) + ' versus ' + str(group2_name) + ')'][0:n_pos].tolist() + \
        fold_change_sorted['log2_fold_change' + '(' + str(group1_name) + ' versus ' + \
        str(group2_name) + ')'][-n_neg:].tolist()
    else:
        names = fold_change_sorted.label[0:n_pos].tolist()
        values = fold_change_sorted['log2_fold_change' + '(' + str(group1_name) + \
        ' versus ' + str(group2_name) + ')'][0:n_pos].tolist()

    if len(names) == 0:
        logger.info("empty fig")
        plt.savefig(output_fig)
        sys.exit()

    index = np.arange(len(names))
    plt.barh(names, values, color=["red"] * n_neg + ["green"] * n_pos)
    plt.xlabel('Log2 Fold Change' + "(" + str(group1_name) + " versus " + \
        str(group2_name) + ")", fontsize=10)
    plt.ylabel('Metabolites', fontsize=10)
    plt.yticks(index, names, fontsize=10)
    plt.title("Log2 Mean Fold Change"  + " (" + str(group1_name) + \
        " versus " + str(group2_name) + ")")

    logger.info("saving bar plot")

    plt.savefig(output_fig, bbox_inches="tight")

if __name__ == '__main__':

    logger.info('generating bar plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", \
        default="data_pos_ph.csv", required=False)
    parser.add_argument(
        '-d', '--design', help="define the location of input design csv file;", \
        default="pos_design.csv", dest="design", required=False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", \
        default="barplot_pos_withbg.png", required=False)
    parser.add_argument(
        '-m', '--only_matched', help="if only include matched metabolites;", \
        default="1", dest="only_matched", required=True)
    parser.add_argument(
        '-bs', '--blank_subtraction', help="whether use blank subtraction;", \
        dest="blank_subtraction", default="1", required=False)

    args = parser.parse_args()
    bar_plot(args.input, args.design, args.output, args.only_matched, args.blank_subtraction)
