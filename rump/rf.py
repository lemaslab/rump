#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Description : This code generates variable importance figure based on SVM
Copyright   : (c) LemasLab, 02/23/2020
Author      : Hailey Ballard, Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, djlemas@ufl.edu
Usage       : python svm.py -i $input_peak_table
                            -d $design_file
                            -o $output_figure
"""
import logging
import logging.handlers
import warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from commons import supervised_data_generator, plot_coefficients_nonlinear

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

def rf(data_file, design_file, output_fig):
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

    tuned_parameters = {'max_depth': [8, 16, 32, 64, 128, 256, 512, None], \
                        "max_features": ['log2', 'sqrt']}
    gs_rf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv=3,
               scoring='roc_auc', n_jobs = 5)

    gs_rf.fit(x, y)

    plot_coefficients_nonlinear(gs_rf.best_estimator_, names, 10, output_fig)

if __name__ == '__main__':

    logger.info('generating random forest varible importance plot...')

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
    rf(args.input, args.design, args.output)
