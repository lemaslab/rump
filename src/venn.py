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
from matplotlib_venn import venn2

import warnings
warnings.filterwarnings('ignore')

def vd(input_file, design_file, output_fig, BS, group1_csv, group2_csv, both_csv):

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

    logger.info("generating venn diagram")

    if BS == "1":
        only_group1 = data[(data[str(group1_name) + "_selected"]) == True & (data[str(group2_name) + "_selected"] == False)]
        only_group2 = data[(data[str(group1_name) + "_selected"]) == False & (data[str(group2_name) + "_selected"] == True)]
        both = data[(data[str(group1_name) + "_selected"]) == True & (data[str(group2_name) + "_selected"] == True)]
    else:
        only_group1 = data[(data[str(group1_name) + "_zero"]) == True & (data[str(group2_name) + "_zero"] == False)]
        only_group2 = data[(data[str(group1_name) + "_zero"]) == False & (data[str(group2_name) + "_zero"] == True)]
        both = data[(data[str(group1_name) + "_zero"]) == True & (data[str(group2_name) + "_zero"] == True)]

    v2 = venn2(subsets = {'10': len(only_group1),
                          '01': len(only_group2),
                          '11': len(both)},
               set_labels=('', ''))
    v2.get_patch_by_id('10').set_color('yellow')
    v2.get_patch_by_id('01').set_color('red')
    v2.get_patch_by_id('11').set_color('orange')

    v2.get_patch_by_id('10').set_edgecolor('black')
    v2.get_patch_by_id('01').set_edgecolor('black')
    v2.get_patch_by_id('11').set_edgecolor('black')

    v2.get_label_by_id('10').set_text('%s\n%d\n(%.0f%%)' % (group1_name,
                                                            len(only_group1),
                                                            len(only_group1)*100/len(data)))

    v2.get_label_by_id('01').set_text('%s\n%d\n(%.0f%%)' % (group2_name,
                                                            len(only_group2),
                                                            len(only_group2)*100/len(data)))

    v2.get_label_by_id('11').set_text('%s\n%d\n(%.0f%%)' % ("both",
                                                            len(both),
                                                            len(both)*100/len(data)))

    for text in v2.subset_labels:
        text.set_fontsize(12)

    logger.info("saving venn diagram")

    plt.savefig(output_fig)

    only_group1.to_csv(group1_csv)
    only_group2.to_csv(group2_csv)
    both.to_csv(both_csv)

if __name__ == '__main__':

    logger.info('generating venn diagram...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="data_pos_ph.csv", required = False)
    parser.add_argument(
        '-d', '--design', help="define the location of input design csv file;", default="pos_design.csv", dest = "design", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="barplot_pos_withbg.png", required = False)
    parser.add_argument(
        '-bs', '--blank_subtraction', help="whether use blank subtraction;", dest = "blank_subtraction", default="1", required = False)
    parser.add_argument(
        '-g1', '--group1_csv', help="matched metabolites that only exist in group 1;", dest = "group1_csv", default="group1.csv", required = False)
    parser.add_argument(
        '-g2', '--group2_csv', help="matched metabolites that only exist in group 2;", dest = "group2_csv", default="group2.csv", required = False)
    parser.add_argument(
        '-bt', '--both', help="matched metabolites that exist both groups;", dest = "both_csv", default="both.csv", required = False)

    
    args = parser.parse_args()
    vd(args.input, args.design, args.output, args.blank_subtraction, args.group1_csv, args.group2_csv, args.both_csv)


