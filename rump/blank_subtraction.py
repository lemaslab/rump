#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description : This code do blank subtraction for peak table output by MZmine-2.53,
              peak table should firstly be processed by "add_stats.py"
              before input to this program
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python blank_subtraction.py -i $input_peak_table_before_blank_subtraction
                                          -d $design_file_location
                                          -o $output_peak_table_after_blank_subtraction
'''

import logging
import logging.handlers
import warnings
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 500)

def blank_subtraction(data_file="pos_data.csv", \
    design_file="pos_design.csv", output_file="pos_data_with_bs.csv"):
    '''Do blank subtraction based on blank_subtraction_flag
    (see function "blank_subtraction_flag" in "add_stats.py" for detail).

    # Arguments:
        data_file: peak table.
        design_file: design file corresponding to the peak table.
        output_file: peak table after removing metabolites that below blank signals.

    # returns:
        number of metabolites after blank subtraction

    # Outputs:
        peak table after blank subtraction.
    '''

    data = pd.read_csv(data_file)
    design = pd.read_csv(design_file)

    group_names = list(set(design['group']))
    group_names.sort()

    group1_name = group_names[0]
    group2_name = group_names[1]

    logger.info("start blank subtraction")

    data_with_bs = data[(data[str(group1_name) + "_selected"] == 1) | \
    (data[str(group2_name) + "_selected"] == 1)]

    logger.info("blank subtraction done")

    data_with_bs.to_csv(output_file, index=False)

    # This returned value is used for unit test
    return len(data_with_bs)

if __name__ == '__main__':

    logger.info('generating bar plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", \
        default="pos_data.csv", required=False)
    parser.add_argument(
        '-d', '--design', help="define the location of first figure;", \
        default="pos_design.csv", required=False)
    parser.add_argument(
        '-o', '--output', help="define the location of second figure;", \
        default="pos_data_withBS.csv", required=False)

    args = parser.parse_args()
    blank_subtraction(args.input, args.design, args.output)
