#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import yaml

def data_info(input_dir, output_yaml):

    filenames = []
    n_peaks = []
    for root, dirs, files in os.walk(os.path.abspath(input_dir)):
        for f in files:
            if f.endswith("100.csv"):
                filenames.append(f)
                with open(os.path.join(root, f), 'r') as temp_f:
                    peak_number = len(temp_f.readlines()) - 1
                    n_peaks.append(peak_number)

    data = ""
    for i in range(len(filenames)):
        data += "   {0}:\n\
        number of peaks: {1}\n".format(filenames[i], n_peaks[i])

    with open(output_yaml, 'w') as yaml_file:
        yaml_file.write("id: 'Results'\n\
section_name: 'Results information'\n\
description: 'Results information.'\n\
plot_type: 'table'\n\
pconfig:\n\
    id: 'Results_table'\n\
    namespace: 'Results information'\n\
    title: 'Results information'\n\
    scale: false\n\
data:\n" + data)


if __name__ == '__main__':

    logger.info('generating yaml file for input data information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", default="../results/", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="./result.yaml", required = False)
    
    args = parser.parse_args()
    data_info(args.input, args.output)


