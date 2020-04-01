#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description : This code generates yaml file that can be parsed by MultiQC,
              including input data information
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python data_info.py -i $input_data_location
                                  -o $output_yaml_file
                                  -n $ion_mode
'''

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def data_info(input_dir, output_yaml, ion):
    '''Generate file that can be parsed by MultiQC and
    containing basic information of input data files.

    # Arguments:
        input_dir: input data folder
        output_yaml: produced yaml file

    # Outputs:
        yaml file that can be parsed by MultiQC.
    '''

    filenames = []
    sizes = []
    total = 0
    for root, _, files in os.walk(os.path.abspath(input_dir)):
        for f in files:
            if f.endswith("mzXML"):
                filenames.append(f)
                size = os.path.getsize(os.path.join(root, f))/1024
                total += size
                size_report = filesize_converter(size)
                sizes.append(size_report)
    filenames.append("Total")
    sizes.append(filesize_converter(total))

    data = ""
    for i, _ in enumerate(filenames):
        data += "   {0}:\n\
        size: {1}\n".format(filenames[i], sizes[i])

    with open(output_yaml, 'w') as yaml_file:
        yaml_file.write("id: 'download_links_" + ion + "'\n\
section_name: '" + ion + " data information'\n\
description: ''\n\
plot_type: 'table'\n\
pconfig:\n\
    id: 'download_links_table'\n\
    namespace: 'Download links'\n\
    title: '" + ion + " data information'\n\
    scale: false\n\
data:\n" + data)

def filesize_converter(size):
    '''Convert filesize unit to KB, MB and GB based on the size value.

    # Arguments:
        size: number of bytes

    # Returns:
        converted size.
    '''

    if size <= 1024:
        size_report = str(round(size, 2)) + " KB"
    elif size <= 1024*1024:
        size_report = str(round(size/1024, 2)) + " MB"
    else:
        size_report = str(round(size/(1024*1024), 2)) + " GB"
    return size_report


if __name__ == '__main__':

    logger.info('generating yaml file for input data information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", \
        default="../../../data/metabolomics/POS/", required=False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", \
        default="./pos_data_info_mqc.yaml", required=False)
    parser.add_argument(
        '-n', '--ion', help="whether it is positive or negative data;", \
        default="pos", dest="ion", required=False)

    args = parser.parse_args()
    data_info(args.input, args.output, args.ion)
