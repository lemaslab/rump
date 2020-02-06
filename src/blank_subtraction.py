#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import pandas as pd
import numpy as np
import csv
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 500)

def blank_subtraction(input_file, design_file, output_file):

    data = pd.read_csv(input_file)

    logger.info("start blank subtraction")

    data_withBS = data[data["selected"] == 1]

    logger.info("blank subtraction done")

    data_withBS.to_csv(output_file, index = False)

if __name__ == '__main__':

    logger.info('generating bar plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="pos_data.csv", required = False)
    parser.add_argument(
        '-d', '--design', help="define the location of first figure;", default="pos_design.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of second figure;", default="pos_data_withBS.csv", required = False)
    
    args = parser.parse_args()
    blank_subtraction(args.input, args.design, args.output)


