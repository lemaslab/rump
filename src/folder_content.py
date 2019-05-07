#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import pandas as pd
import csv

def find_folder_content(folder):
    
    d = {'file_name': os.listdir(folder)}
    result = pd.DataFrame(data = d)
    result.to_csv(os.path.join(folder, "folder_content.csv"), index = False, quoting = csv.QUOTE_ALL)

def find_folder_content_iter(folder):
    folder_name = []
    n_files = []
    for root, dirs, files in os.walk(folder):
        folder_name.append(root)
        n_files.append(len(os.listdir(root)))
#        logger.info(root)
        find_folder_content(root)
    d = {'folder_name': folder_name, 'n_files': n_files}
    result = pd.DataFrame(data = d)
    result.to_csv(os.path.join(folder, "folder_content_summary.csv"), index = False, quoting = csv.QUOTE_ALL)

if __name__ == '__main__':

    logger.info('generating folder content...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of the folder;", default="./", required = False)

    args = parser.parse_args()

    find_folder_content_iter(args.input)