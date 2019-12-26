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
    sizes = []
    for root, dirs, files in os.walk(os.path.abspath(input_dir)):
        for f in files:
            if f.endswith("mzXML"):
                filenames.append(f)
                size = os.path.getsize(os.path.join(root, f))/1024
                if size <= 1024:
                    size_report = str(round(size, 2)) + " KB"
                elif size <= 1024*1024:
                    size_report = str(round(size/1024, 2)) + " MB"
                else:
                    size_report = str(round(size/(1024*1024), 2)) + " GB"
                sizes.append(size_report)

    data = ""
    for i in range(len(filenames)):
        data += "   {0}:\n\
        size: {1}\n".format(filenames[i], sizes[i])

    with open(output_yaml, 'w') as yaml_file:
        yaml_file.write("id: 'download_links'\n\
section_name: 'Raw data information'\n\
description: 'Raw data files information.'\n\
plot_type: 'table'\n\
pconfig:\n\
    id: 'download_links_table'\n\
    namespace: 'Download links'\n\
    title: 'Raw data information'\n\
    scale: false\n\
data:\n" + data)


if __name__ == '__main__':

    logger.info('generating yaml file for input data information...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", default="../../../data/metabolomics/POS/", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="./result.yaml", required = False)
    
    args = parser.parse_args()
    data_info(args.input, args.output)


