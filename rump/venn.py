#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description : This code generates two-group comparison venn diagram for
              MZmine-2.53 to process positive data
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python venn.py -i $input_peak_table
                             -d $design_file_location
                             -o $output_figure_location
                             -m $only_use_identified_metabolites_or_not
                             -bs $do_blank_subtraction_or_not
                             -g1 $peak_table_for_metabolites_enriched_in_group1
                             -g2 $peak_table_for_metabolites_enriched_in_group1
                             -bt $peak_table_for_all_metabolites_in_two_groups
"""

import sys
import logging
import logging.handlers
import warnings
import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_venn import venn2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

def vd(data_file="data_pos_ph.csv", design_file="pos_design.csv", \
    output_fig="barplot_pos_withbg.png", bs="1", group1_csv="group1.csv", \
    group2_csv="group1.csv", both_csv="both.csv"):
    """
    Draw venn diagram for two groups comparison.

    # Arguments:
        data_file: peak table.
        design_file: design file corresponding to the peak table.
        output_fig: the name of outpuf venn diagram.
        bs: The peak table is before (False) or after (True) blank subtraction.
        group1_csv: peak table for metabolites enriched in the first group.
        group2_csv: peak table for metabolites enriched in the second group.
        both_csv: peak table for all metabolites.

    # Outputs:
        venn diagram.
        peak table for metabolites enriched in the first group.
        peak table for metabolites enriched in the second group.
        peak table for all metabolites
    """

    # load design file
    design = pd.read_csv(design_file)

    group_names = list(set(design['group']))
    group_names.sort()
#    blank_group_name = "zero-blank"
    group1_name = group_names[0]
    group2_name = group_names[1]

    data = pd.read_csv(data_file)

    group1 = data[data[str(group1_name) + '_mean'] > data[str(group2_name) + '_mean']]
    group2 = data[data[str(group1_name) + '_mean'] < data[str(group2_name) + '_mean']]

    logger.info("generating venn diagram")

    if bs == "1":
        only_group1 = data[(data.adjusted_p_value < 0.05) & \
        (data[str(group1_name) + '_mean'] > data[str(group2_name) + '_mean'])]
        only_group2 = data[(data.adjusted_p_value < 0.05) & \
        (data[str(group1_name) + '_mean'] < data[str(group2_name) + '_mean'])]
        both = data[data.adjusted_p_value >= 0.05]
    else:
        only_group1 = data[(data[str(group1_name) + "_zero"] == True) & \
        (data[str(group2_name) + "_zero"] == False)]
        only_group2 = data[(data[str(group1_name) + "_zero"] == False) & \
        (data[str(group2_name) + "_zero"] == True)]
        both = data[(data[str(group1_name) + "_zero"] == False) & \
        (data[str(group2_name) + "_zero"] == False)]

    group1.to_csv(group1_csv, index=False)
    group2.to_csv(group2_csv, index=False)
    data.to_csv(both_csv, index=False) # the output "both.csv" contains all peaks

    with open(group1_csv.split(".")[0] + "_cutoff.txt", "w+") as f:
        f.write(str(0.05))
    with open(group2_csv.split(".")[0] + "_cutoff.txt", "w+") as f:
        f.write(str(0.05))
    with open(both_csv.split(".")[0] + "_cutoff.txt", "w+") as f:
        f.write(str(0.05))

    if len(both) * len(only_group1) * len(only_group2) == 0:
        logger.info("empty fig")
        plt.savefig(output_fig)
        sys.exit()

    v2 = venn2(subsets={'10': len(only_group1), \
                          '01': len(only_group2), \
                          '11': len(both)}, \
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

    plt.savefig(output_fig, bbox_inches="tight")

    # This returned value is used for unit test
    return len(only_group1)

if __name__ == '__main__':

    logger.info('generating venn diagram...')

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
        '-bs', '--blank_subtraction', help="whether use blank subtraction;", \
        dest="blank_subtraction", default="1", required=False)
    parser.add_argument(
        '-g1', '--group1_csv', help="matched metabolites that only exist in group 1;", \
        dest="group1_csv", default="group1.csv", required=False)
    parser.add_argument(
        '-g2', '--group2_csv', help="matched metabolites that only exist in group 2;", \
        dest="group2_csv", default="group2.csv", required=False)
    parser.add_argument(
        '-bt', '--both', help="matched metabolites that exist both groups;", dest="both_csv", \
        default="both.csv", required=False)

    args = parser.parse_args()
    vd(args.input, args.design, args.output, args.blank_subtraction, \
        args.group1_csv, args.group2_csv, args.both_csv)
