#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import yaml
import csv

def comparison_info(input_file, output_txt):

    c_ms = []
    b_ms = []
    sames = []
    with open(input_file, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            c_ms.append(row['click_metabolomics'])
            b_ms.append(row['batch_metabolomics'])
            sames.append(row['same'])

    data = ""
    for i in range(len(c_ms)):
        data += "{0}            {1}            {2}            {3}            \n".format(i, c_ms[i].replace(' ', '_'), b_ms[i].replace(' ', '_'), sames[i])

    with open(output_txt, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'Components comparison'\n\
# description: 'Comparison of identified components between click-point and commoned-line'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'click_metabolomics'\n\
#         description: 'metabolomics identified with click-point'\n\
#     col2:\n\
#         title: 'batch_metabolomics'\n\
#         description: 'metabolomics identified with commond-line and batchfile'\n\
#     col3:\n\
#         title: 'same'\n\
#         description: 'comparison results'\n\
components            col1            col2            col3\n" + data)


if __name__ == '__main__':

    logger.info('generating yaml file for input data information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", default="../results/click_batch_comparison/mzmine_click_batch_comparison_identified_metabs.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="./click_batch_comparison_peak_components.txt", required = False)
    
    args = parser.parse_args()
    comparison_info(args.input, args.output)


