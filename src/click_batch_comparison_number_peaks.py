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

    steps = []
    click_peaks = []
    batch_peaks = []
    with open(input_file, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            steps.append(row['step'])
            click_peaks.append(row['click_peak'])
            batch_peaks.append(row['batch_peak'])

    data = ""
    for i in range(len(steps)):
        data += "{0}            {1}            {2}            \n".format(steps[i].replace(' ', '_'), click_peaks[i], batch_peaks[i])

    with open(output_yaml, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'My section with a table'\n\
# description: 'a custom text introduction (a few sentences) for this section'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'click_peaks'\n\
#         description: 'This is a longer hover text for my column'\n\
#     col2:\n\
#         title: 'batch_peaks'\n\
#         description: 'Hover description text'\n\
steps            col1            col2\n" + data)


if __name__ == '__main__':

    logger.info('generating report file for input data information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", default="../results/click_batch_comparison/mzmine_click_batch_comparison_peaknumber.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="./click_batch_comparison_peak_number.txt", required = False)
    
    args = parser.parse_args()
    comparison_info(args.input, args.output)


