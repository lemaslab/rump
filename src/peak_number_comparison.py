#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import yaml
import csv

def peak_number_comparison(pos_nobg, neg_nobg, pos_005, neg_005, pos_100, neg_100, pos_200, neg_200, output_txt):

    data_category = ["pos", "neg"]
    no_bg = [pos_nobg, neg_nobg]
    with_bg_005 = [pos_005, neg_005]
    with_bg_100 = [pos_100, neg_100]
    with_bg_200 = [pos_200, neg_200]

    data = ""
    for i in range(len(data_category)):
        data += "{0}            {1}            {2}            {3}            {4}            \n".format(data_category[i], no_bg[i], with_bg_005[i], with_bg_100[i], with_bg_200[i])

    with open(output_txt, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'Number of peaks corresponding to different threshold of background subtraction'\n\
# description: 'Number of peaks for no background subtraction (BS), BS with threshold of 005, 100 and 200'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'no background subtraction'\n\
#         description: 'This is a longer hover text for my column'\n\
#     col2:\n\
#         title: 'background subtraction with threshold of 005'\n\
#         description: 'Hover description text'\n\
#     col3:\n\
#         title: 'background subtraction with threshold of 100'\n\
#         description: 'Hover description text'\n\
#     col4:\n\
#         title: 'background subtraction with threshold of 200'\n\
#         description: 'Hover description text'\n\
Data_category            col1            col2            col3            col4\n" + data)


if __name__ == '__main__':

    logger.info('generating txt file for input peaks information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i1', '--pos_nobg', help="number of peaks for positive and without background subtraction;", default="0", dest = "pos_nobg", required = False)
    parser.add_argument(
        '-i2', '--neg_nobg', help="number of peaks for negative and without background subtraction;", default="0", dest = "neg_nobg", required = False)
    parser.add_argument(
        '-i3', '--pos_005', help="number of peaks for positive and after background subtraction with a threshold of 005;", default="0", dest = "pos_005", required = False)
    parser.add_argument(
        '-i4', '--neg_005', help="number of peaks for negative and after background subtraction with a threshold of 005;", default="0", dest = "neg_005", required = False)
    parser.add_argument(
        '-i5', '--pos_100', help="number of peaks for positive and after background subtraction with a threshold of 100;", default="0", dest = "pos_100", required = False)
    parser.add_argument(
        '-i6', '--neg_100', help="number of peaks for negative and after background subtraction with a threshold of 100;", default="0", dest = "neg_100", required = False)
    parser.add_argument(
        '-i7', '--pos_200', help="number of peaks for positive and after background subtraction with a threshold of 200;", default="0", dest = "pos_200", required = False)
    parser.add_argument(
        '-i8', '--neg_200', help="number of peaks for negative and after background subtraction with a threshold of 200;", default="0", dest = "neg_200", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="c_peak_number_comparison_mqc.txt", required = False)
    
    args = parser.parse_args()
    peak_number_comparison(args.pos_nobg, args.neg_nobg, args.pos_005, args.neg_005, args.pos_100, args.neg_100, args.pos_200, args.neg_200, args.output)


