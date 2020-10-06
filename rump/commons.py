#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description : This file includes functions frequently used by other files
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, djlemas@ufl.edu
"""

import copy
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt

def group_info_generator(design_file):
    """
    Generate group information based on design file.

    # Arguments:
        design_file: design file corresponding to the peak table.

    # Outputs:
        group names and their columns in the peak table.
    """

    design = pd.read_csv(design_file)

    group_names = list(set(design['group']))
    group_names.sort()
#    blank_group_name = "zero-blank"
    group1_name = group_names[0]
    group2_name = group_names[1]

    group1_columns = design[design.group == group1_name].sampleID.tolist()
    group2_columns = design[design.group == group2_name].sampleID.tolist()

    return group1_name, group2_name, group1_columns, group2_columns

def supervised_data_generator(data_file, design_file):
    """
    Generate data, labels, and variable names for supervised learning models.

    # Arguments:
        data_file: peak table.
        design_file: design file corresponding to the peak table.

    # Outputs:
        SVM variable importance figure.
    """

    # load group information
    group1_name, group2_name, group1_columns, group2_columns = group_info_generator(design_file)

    data = pd.read_csv(data_file)
    data_filtered_supervised = copy.deepcopy(data)
    data_filtered_supervised.index = data_filtered_supervised.label
    data_filtered_supervised = data_filtered_supervised[group1_columns + group2_columns]

    for i, group1_column in enumerate(group1_columns):
        data_filtered_supervised.rename(columns = \
            {group1_column: group1_name + '_' + str(i)}, inplace = True)
    for i, group2_column in enumerate(group2_columns):
        data_filtered_supervised.rename(columns = \
            {group2_column: group2_name + '_' + str(i)}, inplace = True)

    data_filtered_supervised = data_filtered_supervised.T
    data_filtered_supervised["label"] = \
        [group1_name] * len(group1_columns) + [group2_name] * len(group2_columns)
    data_filtered_supervised.reset_index(drop = True, inplace = True)

    names = list(data_filtered_supervised.columns)
    names.pop()

    X = data_filtered_supervised.loc[:, data_filtered_supervised.columns != "label"].values
    y = np.array(data_filtered_supervised.label)

    scaler = preprocessing.StandardScaler().fit(X)
    x = scaler.transform(X)

    return x, y, names

def plot_coefficients_linear(classifier, feature_names, \
    top_features=10, output_fig="sample_fig.png"):
    """
    Plot variable importance for linear models.

    # Arguments:
        classifier: trained classifier.
        names: list of variable names.
        top_features: number of top positive/negative variables included in the figure
        output_fig: location of the output figure.

    # Outputs:
        Variable importance figure for linear model.
    """

    importance_df = pd.DataFrame(list(zip(feature_names, classifier.coef_.ravel())), \
                                 columns = ['var_name', 'importance_score']).sort_values(by = \
                                ["importance_score"])
    top_positive_names = list(importance_df.var_name)[-top_features:]
    top_positive_coefficients = list(importance_df.importance_score)[-top_features:]
    top_negative_names = list(importance_df.var_name)[:top_features]
    top_negative_coefficients = list(importance_df.importance_score)[:top_features]
    top_names = top_negative_names + top_positive_names
    top_coefficients = top_negative_coefficients + top_positive_coefficients

    # create plot
    figure = plt.figure(figsize=(15, 5))
    colors = ['red' if c < 0 else 'blue' for c in top_coefficients]

    plt.bar(np.arange(2 * top_features), top_coefficients, color=colors)
    plt.xlabel("Metabolite Identity")
    plt.suptitle("Top Positive and Negative Features")
    plt.ylabel("Relative Importance")
    r = np.arange(1, 1 + 2 * top_features) # coordinates of bars
    plt.xticks(r,
               top_names,
               rotation=60,
               ha='right')
    figure.savefig(output_fig)

def plot_coefficients_nonlinear(classifier, feature_names, top_features=20, output_fig="sample_fig.png"):
    """
    Plot variable importance for non-linear models.

    # Arguments:
        classifier: trained classifier.
        names: list of variable names.
        top_features: number of top ranked variables included in the figure
        output_fig: location of the output figure.

    # Outputs:
        Variable importance figure for non-linear model.
    """
    importance_df = pd.DataFrame(list(zip(feature_names, classifier.feature_importances_.ravel())), \
                                 columns = ['var_name', 'importance_score']).sort_values(by = \
                                ["importance_score"], ascending=False)
    top_positive_names = list(importance_df.var_name)[0: top_features]
    top_positive_coefficients = list(importance_df.importance_score)[0: top_features]
    top_names = top_positive_names
    top_coefficients = top_positive_coefficients
    # create plot
    figure = plt.figure(figsize=(15, 5))
    colors = ['red' if c < 0 else 'blue' for c in top_coefficients]

    plt.bar(np.arange(top_features), top_coefficients, color=colors)
    plt.xlabel("Metabolite Identity")
    plt.suptitle("Most Important Features")
    plt.ylabel("Relative Importance")
    r = np.arange(1, 1 + top_features)
    plt.xticks(r,
               top_names,
               rotation=60,
               ha='right')
    figure.savefig(output_fig)
