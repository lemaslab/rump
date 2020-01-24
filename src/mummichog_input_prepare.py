#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import StandardScaler
import math
from scipy import stats

import warnings
warnings.filterwarnings('ignore')

def mummichog_input_prepare(input_file, output_file):

    data = pd.read_csv(input_file)

    data_formummichog = data[["row m/z", "row retention time", "p_value", "t_value", "label"]]
    data_formummichog.rename(columns = {"row m/z": "m/z", "row retention time": "retention_time", "p_value": "p-value", "t_value": "t-score", "label": "custom_id"}, inplace = True)

    data.to_csv(output_file, index = False, sep = "\t")

if __name__ == '__main__':

    logger.info('generating venn diagram...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="data_pos_ph.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="pos_withstats.csv", required = False)

    
    args = parser.parse_args()
    add_stats(args.input, args.output)


