#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description : This code generate file that can be used by mummichog for pathway analysi,
              according to peak table
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python mummichog_input_prepare.py -i $input_peak_table
                                                -o $output_file
"""

import logging
import logging.handlers
import warnings
import matplotlib
import pandas as pd

matplotlib.use('agg')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

def mummichog_input_prepare(input_file, output_file):
    """Convert peak table to text file that can be used as mummichog input."""
    data = pd.read_csv(input_file)

    data_formummichog = data[["row m/z", "row retention time", "p_value", "t_value", "label"]]
    data_formummichog.rename(columns=\
        {"row m/z": "m/z", "row retention time": "retention_time", \
        "p_value": "p-value", "t_value": "t-score", "label": "custom_id"}, inplace=True)

    data_formummichog.to_csv(output_file, index=False, sep="\t")

if __name__ == '__main__':

    logger.info('generating venn diagram...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", \
        default="data_pos_ph.csv", required=False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", \
        default="pos_withstats.csv", required=False)

    args = parser.parse_args()
    mummichog_input_prepare(args.input, args.output)
