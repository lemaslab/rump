#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import yaml
import csv

def peak_number_comparison(pos_nobg, neg_nobg, pos_withbg, neg_withbg, output_txt):

    data_category = ["pos", "neg"]
    no_bg = [pos_nobg, neg_nobg]
    with_bg = [pos_withbg, neg_withbg]

    data = ""
    for i in range(len(data_category)):
        data += "{0}            {1}            {2}            \n".format(data_category[i], no_bg[i], with_bg[i])

    with open(output_txt, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'Number of peaks corresponding to different threshold of background subtraction'\n\
# description: 'Number of peaks for no background subtraction (BS), BS with threshold of 005, 100 and 200'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'no background subtraction'\n\
#         description: 'Number of peaks detected without blank subtraction'\n\
#     col2:\n\
#         title: 'with background subtraction'\n\
#         description: 'Number of peaks detected with blank subtraction'\n\
Data_category            col1            col2\n" + data)


if __name__ == '__main__':

    logger.info('generating txt file for input peaks information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i1', '--pos_nobg', help="number of peaks for positive and without background subtraction;", default="0", dest = "pos_nobg", required = False)
    parser.add_argument(
        '-i2', '--neg_nobg', help="number of peaks for negative and without background subtraction;", default="0", dest = "neg_nobg", required = False)
    parser.add_argument(
        '-i3', '--pos_withbg', help="number of peaks for positive and after background subtraction;", default="0", dest = "pos_withbg", required = False)
    parser.add_argument(
        '-i4', '--neg_withbg', help="number of peaks for negative and after background subtraction;", default="0", dest = "neg_withbg", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="c_peak_number_comparison_mqc.txt", required = False)
    
    args = parser.parse_args()
    peak_number_comparison(args.pos_nobg, args.neg_nobg, args.pos_withbg, args.neg_withbg, args.output)


