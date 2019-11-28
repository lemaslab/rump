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

def vd(input_file, output_fig, group1_out, group2_out, group3_out):

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

    # Common
    different = data[(data.p_value_f_anova<0.05) & 
        (data.p_value_whole_fat_anova<0.05) & 
        (data.p_value_whole_skim_anova<0.05) & 
        (data.p_value_skim_fat_anova<0.05) & 
        (abs(data.foldchange_whole_skim)>2) &
        (abs(data.foldchange_skim_fat)>2) &
        (abs(data.foldchange_whole_fat)>2)]

    # Plot Venn Diagram
    v3 = venn3(subsets = {'100':30, '010':30, '110':17,
                      '001':30, '101':17, '011':17, '111':5},
               set_labels = ('Skim vs Fat', 'Whole vs Fat', 'Whole vs Skim'))

    v3.get_patch_by_id('100').set_color('red')
    v3.get_patch_by_id('010').set_color('yellow')
    v3.get_patch_by_id('001').set_color('blue')
    v3.get_patch_by_id('110').set_color('orange')
    v3.get_patch_by_id('101').set_color('purple')
    v3.get_patch_by_id('011').set_color('green')
    v3.get_patch_by_id('111').set_color('grey')

    v3.get_label_by_id('100').set_text(str(len(skim_fat)))
    v3.get_label_by_id('010').set_text(str(len(whole_fat)))
    v3.get_label_by_id('001').set_text(str(len(whole_skim)))
    v3.get_label_by_id('110').set_text(str(len(fat)))
    v3.get_label_by_id('101').set_text(str(len(skim)))
    v3.get_label_by_id('011').set_text(str(len(whole)))
    v3.get_label_by_id('111').set_text(str(len(different)))

    for text in v3.subset_labels:
        text.set_fontsize(13)

    plt.savefig(output_fig)

    fat.to_csv(group1_out, index = False)
    skim.to_csv(group2_out, index = False)
    whole.to_csv(group3_out, index = False)

if __name__ == '__main__':

    logger.info('generating venn diagram...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="milk_data_pos_ph.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="pca_pos_withbg.png", required = False)
    parser.add_argument(
        '-g1', '--group1_out', help="define the location of first group dataframe;", default="fat.csv", required = False)
    parser.add_argument(
        '-g2', '--group2_out', help="define the location of second group dataframe;", default="skim.csv", required = False)
    parser.add_argument(
        '-g3', '--group3_out', help="define the location of third group dataframe;", default="whole.csv", required = False)

    
    args = parser.parse_args()
    vd(args.input, args.output, args.group1_out, args.group2_out, args.group3_out)


