#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description : This code do principal component analysis for
              peak table output by MZmine-2.53, peak table should
              firstly be processed by "add_stats.py" before input to this program
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python pca.py -i $input_peak_table
                            -d $design_file
                            -o $output_figure
"""

import sys
import logging
import logging.handlers
import warnings

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')
warnings.filterwarnings('ignore')

# reference for the following function:
# https://gist.github.com/CarstenSchelp/b992645537660bda692f218b562d0712
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`

    See how and why this works:
    https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html

    Or, once matplotlib 3.1 has been released:
    https://matplotlib.org/gallery/index.html#statistics

    I update this gist according to the version there, because thanks to the matplotlib community
    the code has improved quite a bit.
    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.
    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.
    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.
    Returns
    -------
    matplotlib.patches.Ellipse
    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), \
        width=ell_radius_x * 2, \
        height=ell_radius_y * 2, \
        facecolor=facecolor, \
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def pca_2g(data_file, design_file, output_fig):
    """
    Draw principal component analysis (PCA) plot for two groups comparison.

    # Arguments:
        data_file: peak table.
        design_file: design file corresponding to the peak table.
        output_fig: the name of outpuf PCA figure.

    # Outputs:
        PCA figure.
    """

    # load design file
    design = pd.read_csv(design_file)

    group_names = list(set(design['group']))
    group_names.sort()
#    blank_group_name = "zero-blank"
    group1_name = group_names[0]
    group2_name = group_names[1]

    data_pca = pd.read_csv(data_file)
    if len(data_pca) <= 2:
        logger.info("empty fig")
        plt.savefig(output_fig)
        sys.exit()
#    data_pca.columns = data_pca.columns.str.replace("\"", "")

    group1_columns = design[design.group == group1_name].sampleID.tolist()
    group2_columns = design[design.group == group2_name].sampleID.tolist()
#    blank_columns = design[design.group == blank_group_name].sampleID.tolist()

    logger.info("generating principal component analysis figure")

    data_filtered = data_pca[group1_columns + group2_columns]

    x = data_filtered.as_matrix().T
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=min(x.shape))
    principal_components = pca.fit_transform(x)

    columns_components = []
    for i in range(pca.n_components_):
        columns_components.append('principal component ' + str(i+1))

    principal_df = pd.DataFrame(data=principal_components, columns=columns_components)

    target_data = \
    {"label": [group1_name] * len(group1_columns) + [group2_name] * len(group2_columns)}

    target_df = pd.DataFrame(target_data)

    final_df = pd.concat([principal_df, target_df.label], axis=1)

    # draw figure

    x_group1 = final_df[final_df.label == group1_name]["principal component 1"].as_matrix()
    y_group1 = final_df[final_df.label == group1_name]["principal component 2"].as_matrix()
    x_group2 = final_df[final_df.label == group2_name]["principal component 1"].as_matrix()
    y_group2 = final_df[final_df.label == group2_name]["principal component 2"].as_matrix()

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)
    targets = [group1_name, group2_name]
    colors = ['r', 'b']
    for target, color in zip(targets, colors):
        indices_to_keep = final_df['label'] == target
        ax.scatter(final_df.loc[indices_to_keep, 'principal component 1']
                   , final_df.loc[indices_to_keep, 'principal component 2']
                   , c=color
                   , s=50)
    ax.legend(targets)
    ax.grid()
    confidence_ellipse(x_group1, y_group1, ax, n_std=1.96, facecolor="r", alpha=0.1)
    confidence_ellipse(x_group2, y_group2, ax, n_std=1.96, facecolor="b", alpha=0.1)

    logger.info("saving principal component analysis figure")

    plt.savefig(output_fig, bbox_inches="tight")

if __name__ == '__main__':

    logger.info('generating pca plots...')

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
        default="pca_pos_withbg.png", required=False)

    args = parser.parse_args()
    pca_2g(args.input, args.design, args.output)
