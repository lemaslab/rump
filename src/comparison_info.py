#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import yaml
import csv

def comparison_info(input_file, output_yaml):

    peak_lists = []
    n_oris = []
    n_reps = []
    n_diffs = []
    with open(input_file, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            peak_lists.append(row['peak_lists'])
            n_oris.append(row['Lemas_POS'])
            n_reps.append(row['Xinsong_repliation'])
            n_diffs.append(row['difference'])

    data = ""
    for i in range(len(peak_lists)):
        data += "{0}            {1}            {2}            {3}            \n".format(peak_lists[i].replace(' ', '_'), n_oris[i], n_reps[i], n_diffs[i])

    with open(output_yaml, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'My section with a table'\n\
# description: 'a custom text introduction (a few sentences) for this section'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'Lemas_POS'\n\
#         description: 'This is a longer hover text for my column'\n\
#     col2:\n\
#         title: 'Xinsong_repliation'\n\
#         description: 'Hover description text'\n\
#     col3:\n\
#         title: 'difference'\n\
#         description: 'Hover description text'\n\
Peak_lists            col1            col2            col3\n" + data)


if __name__ == '__main__':

    logger.info('generating yaml file for input data information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", default="../results/mzmine_POS_results_comparison.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="./comparison.txt", required = False)
    
    args = parser.parse_args()
    comparison_info(args.input, args.output)


