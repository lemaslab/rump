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
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

import warnings
warnings.filterwarnings('ignore')

# reference for the following function: https://gist.github.com/CarstenSchelp/b992645537660bda692f218b562d0712
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`
    
    See how and why this works: https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html
    
    This function has made it into the matplotlib examples collection:
    https://matplotlib.org/devdocs/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py
    
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
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
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

def pca_3g(input_file, output_fig, ion):

    fat_names = ["X10_BLS010A_" + ion + "_mzXML_Peak_height", "X4_BLS002A_" + ion + "_mzXML_Peak_height", "X1_BLS001A_" + ion + "_mzXML_Peak_height", "X7_BLS003A_" + ion + "_mzXML_Peak_height"]
    whole_names = ["X12_BLS010A_" + ion + "_mzXML_Peak_height", "X6_BLS002A_" + ion + "_mzXML_Peak_height", "X3_BLS001A_" + ion + "_mzXML_Peak_height", "X9_BLS003A_" + ion + "_mzXML_Peak_height"]
    skim_names = ["X11_BLS010A_" + ion + "_mzXML_Peak_height", "X5_BLS002A_" + ion + "_mzXML_Peak_height", "X2_BLS001A_" + ion + "_mzXML_Peak_height", "X8_BLS003A_" + ion + "_mzXML_Peak_height"]

    data_pca = pd.read_csv(input_file)
#    data_pca.columns = data_pca.columns.str.replace("\"", "")

    milk_data = data_pca[fat_names + whole_names + skim_names]

    x = milk_data.as_matrix().T
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=min(x.shape))
    principal_components = pca.fit_transform(x)

    columns_components = []
    for i in range(pca.n_components_):
        columns_components.append('principal component ' + str(i+1))

    principal_df = pd.DataFrame(data = principal_components
             , columns = columns_components)

    target_data = {"label": ["fat"] * 4 + ["whole"] * 4 + ["skim"] * 4}

    target_df = pd.DataFrame(target_data)

    final_df = pd.concat([principal_df, target_df.label], axis = 1)

    # draw figure

    x_fat = final_df[final_df.label == "fat"]["principal component 1"].as_matrix()
    y_fat = final_df[final_df.label == "fat"]["principal component 2"].as_matrix()
    x_whole = final_df[final_df.label == "whole"]["principal component 1"].as_matrix()
    y_whole = final_df[final_df.label == "whole"]["principal component 2"].as_matrix()
    x_skim = final_df[final_df.label == "skim"]["principal component 1"].as_matrix()
    y_skim = final_df[final_df.label == "skim"]["principal component 2"].as_matrix()

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    targets = ['fat', 'whole', 'skim']
    colors = ['r', 'g', 'b']
    for target, color in zip(targets,colors):
        indices_to_keep = final_df['label'] == target
        ax.scatter(final_df.loc[indices_to_keep, 'principal component 1']
                   , final_df.loc[indices_to_keep, 'principal component 2']
                   , c = color
                   , s = 50)
    ax.legend(targets)
    ax.grid()
    confidence_ellipse(x_fat, y_fat, ax, n_std = 1.96, facecolor = "r", alpha = 0.1)
    confidence_ellipse(x_whole, y_whole, ax, n_std = 1.96, facecolor = "g", alpha = 0.1)
    confidence_ellipse(x_skim, y_skim, ax, n_std = 1.96, facecolor = "b", alpha = 0.1)
    plt.savefig(output_fig)

def pca_2g(input_file, design_file, output_fig, ion):

    # load design file
    design = pd.read_csv('../data/two_groups/pos_design.csv')

    group_names = list(set(design['group']))
    group_names.sort()
#    blank_group_name = "zero-blank"
    group1_name = group_names[0]
    group2_name = group_names[1]
    ratio_bar = 100

    data_pca = pd.read_csv(input_file)
#    data_pca.columns = data_pca.columns.str.replace("\"", "")

    group1_columns = design[design.group == group1_name].sampleID.tolist()
    group2_columns = design[design.group == group2_name].sampleID.tolist()
#    blank_columns = design[design.group == blank_group_name].sampleID.tolist()

    data_selected = data_pca[group1_columns + group2_columns]

    x = milk_data.as_matrix().T
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=min(x.shape))
    principal_components = pca.fit_transform(x)

    columns_components = []
    for i in range(pca.n_components_):
        columns_components.append('principal component ' + str(i+1))

    principal_df = pd.DataFrame(data = principal_components
             , columns = columns_components)

    target_data = {"label": ["fat"] * 4 + ["whole"] * 4 + ["skim"] * 4}

    target_df = pd.DataFrame(target_data)

    final_df = pd.concat([principal_df, target_df.label], axis = 1)

    # draw figure

    x_fat = final_df[final_df.label == "fat"]["principal component 1"].as_matrix()
    y_fat = final_df[final_df.label == "fat"]["principal component 2"].as_matrix()
    x_whole = final_df[final_df.label == "whole"]["principal component 1"].as_matrix()
    y_whole = final_df[final_df.label == "whole"]["principal component 2"].as_matrix()
    x_skim = final_df[final_df.label == "skim"]["principal component 1"].as_matrix()
    y_skim = final_df[final_df.label == "skim"]["principal component 2"].as_matrix()

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    targets = ['fat', 'whole', 'skim']
    colors = ['r', 'g', 'b']
    for target, color in zip(targets,colors):
        indices_to_keep = final_df['label'] == target
        ax.scatter(final_df.loc[indices_to_keep, 'principal component 1']
                   , final_df.loc[indices_to_keep, 'principal component 2']
                   , c = color
                   , s = 50)
    ax.legend(targets)
    ax.grid()
    confidence_ellipse(x_fat, y_fat, ax, n_std = 1.96, facecolor = "r", alpha = 0.1)
    confidence_ellipse(x_whole, y_whole, ax, n_std = 1.96, facecolor = "g", alpha = 0.1)
    confidence_ellipse(x_skim, y_skim, ax, n_std = 1.96, facecolor = "b", alpha = 0.1)
    plt.savefig(output_fig)

if __name__ == '__main__':

    logger.info('generating pca plots...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", default="milk_data_pos_ph.csv", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output figure;", default="pca_pos_withbg.png", required = False)
    parser.add_argument(
        '-n', '--ion', help="positive data or negative data;", default="p", dest = "ion", required = False)
    
    args = parser.parse_args()
    pca_3g(args.input, args.output, args.ion)


