#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description : This code generate file that can be parsed by MultiQC,
              including number of peaks in different data analysis stage
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python peak_number_comparison.py -i1
                                               $peak_table_for_positive_before_blank_subtraction
                                               -i2
                                               $peak_table_for_negative_before_blank_subtraction
                                               -i3
                                               $peak_table_for_positive_after_blank_subtraction
                                               -i4
                                               $peak_table_for_negative_after_blank_subtraction
                                               -o
                                               $output_file
"""

import logging
import logging.handlers
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def peak_number_comparison(pos_nobg, neg_nobg, pos_withbg, neg_withbg, output_txt):
    """Produce file containing peak number information that can be parsed by MultiQC.

    # Arguments:
        pos_nobg: peak table (csv file) of positive data before blank subtraction.
        neg_nobg: peak table (csv file) of negative data before blank subtraction.
        pos_withbg: peak table (csv file) of positive data after blank subtraction.
        neg_withbg: peak table (csv file) of negative data after blank subtraction.
        output_txt: name of output text file

    # Outputs:
        txt file containing peak number information.
    """

    pos = []
    neg = []

    data_pos_nobg = pd.read_csv(pos_nobg)
    pos.append(len(data_pos_nobg))
    data_pos_nobg_matched = data_pos_nobg[data_pos_nobg.ppm < 5]
    pos.append(len(data_pos_nobg_matched))
    pos.append(len(data_pos_nobg_matched[data_pos_nobg_matched.adjusted_p_value < 0.05]))

    data_neg_nobg = pd.read_csv(neg_nobg)
    neg.append(len(data_neg_nobg))
    data_neg_nobg_matched = data_neg_nobg[data_neg_nobg.ppm < 5]
    neg.append(len(data_neg_nobg_matched))
    neg.append(len(data_neg_nobg_matched[data_neg_nobg_matched.adjusted_p_value < 0.05]))

    if pos_withbg != "none":
        steps = ["before_blank_subtraction", "match_before_blank_subtraction", \
        "significant_match_before_blank_subtraction", "after_blank_subtraction", \
        'match_after_blank_subtraction', "significant_match_after_blank_subtraction"]
        data_pos_withbg = pd.read_csv(pos_withbg)
        pos.append(len(data_pos_withbg))
        data_pos_withbg_matched = data_pos_withbg[data_pos_withbg.ppm < 5]
        pos.append(len(data_pos_withbg_matched))
        pos.append(len(data_pos_withbg_matched[data_pos_withbg_matched.adjusted_p_value < 0.05]))

        data_neg_withbg = pd.read_csv(neg_withbg)
        neg.append(len(data_neg_withbg))
        data_neg_withbg_matched = data_neg_withbg[data_neg_withbg.ppm < 5]
        neg.append(len(data_neg_withbg_matched))
        neg.append(len(data_neg_withbg_matched[data_neg_withbg_matched.adjusted_p_value < 0.05]))

    else:
        steps = ["before_blank_subtraction", "match_before_blank_subtraction", \
        "significant_match_before_blank_subtraction"]


#    data_category = ["pos", "neg"]
#    no_bg = [pos_nobg, neg_nobg]
#    with_bg = [pos_withbg, neg_withbg]

    data = ""
    for i, step in enumerate(steps):
        data += "{0}            {1}            {2}            \n".format(step, pos[i], neg[i])

    with open(output_txt, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'Number of peaks before and after background subtraction (BS)'\n\
# description: 'Number of peaks before and after BS'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'Positive'\n\
#         description: 'Number of peaks detected for positive data'\n\
#     col2:\n\
#         title: 'Negative'\n\
#         description: 'Number of peaks detected for negative data'\n\
Steps            col1            col2\n" + data)


if __name__ == '__main__':

    logger.info('generating txt file for input peaks information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i1', '--pos_nobg', \
        help="number of peaks for positive and without background subtraction;", \
        default="0", dest="pos_nobg", required=False)
    parser.add_argument(
        '-i2', '--neg_nobg', \
        help="number of peaks for negative and without background subtraction;", \
        default="0", dest="neg_nobg", required=False)
    parser.add_argument(
        '-i3', '--pos_withbg', \
        help="number of peaks for positive and after background subtraction;", \
        default="0", dest="pos_withbg", required=False)
    parser.add_argument(
        '-i4', '--neg_withbg', \
        help="number of peaks for negative and after background subtraction;", \
        default="0", dest="neg_withbg", required=False)
    parser.add_argument(
        '-o', '--output', \
        help="define the location of output csv file;", \
        default="c_peak_number_comparison_mqc.txt", required=False)

    args = parser.parse_args()
    peak_number_comparison(args.pos_nobg, args.neg_nobg, args.pos_withbg, \
        args.neg_withbg, args.output)
