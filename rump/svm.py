#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description : This code generates variable importance figure based on SVM
Copyright   : (c) LemasLab, 02/23/2020
Author      : Hailey Ballard, Xinsong Du
License     : MIT License
Maintainer  : xinsongdu@ufl.edu, djlemas@ufl.edu
Usage       : python svm.py -i $input_peak_table
                            -d $design_file
                            -o $output_figure
"""
import logging
import logging.handlers
import warnings
from sklearn.svm import LinearSVC
from commons import supervised_data_generator, plot_coefficients_linear

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

def svm(data_file, design_file, output_fig):
    """
    Draw variable importance plot of support vector machine (SVM)
    for two groups comparison.

    # Arguments:
        data_file: peak table.
        design_file: design file corresponding to the peak table.
        output_fig: the name of outpuf PCA figure.

    # Outputs:
        SVM variable importance figure.
    """

    # load group information
    x, y, names = supervised_data_generator(data_file, design_file)

    svm_clf = LinearSVC()
    svm_clf.fit(x, y)

    plot_coefficients_linear(svm_clf, names, 10, output_fig)

if __name__ == '__main__':

    logger.info('generating svm varible importance plot...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", \
        default="data_pos_ph.csv", required=False)
    parser.add_argument(
        '-d', '--design', help="define the location of input design csv file;", \
        default="pos_design.csv", dest="design", required=False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", \
        default="svm_pos_withbg.png", required=False)

    args = parser.parse_args()
    svm(args.input, args.design, args.output)
