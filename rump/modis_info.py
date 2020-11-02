#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description : This code generate file that can be parsed by MultiQC,
              including modis data quality test results.
Copyright   : (c) LemasLab, 10/31/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, djlemas@ufl.edu
Usage       : python modis_info.py -i $modis_table -t $threshold -o $output_file

"""
import logging
import logging.handlers
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def modis_info_generator(modis_table_path, threshold=22, output_txt="modis_mqc.txt"):
    """
    Produce file containing MODIS tests results that can be parsed by MultiQC.
    MODIS paper can be found here: https://www.future-science.com/doi/10.4155/bio-2018-0303

    # Arguments:
        modis_table_path: path of the spreadsheet containing MODIS information.
        threshold: threshold that counts "pass", 22 (default value) was used in the paper.

    # Outputs:
        txt file containing MODIS test results information, which can be parsed by MultiQC.
    """

    modis_table = pd.read_excel(modis_table_path, sheet_name="Metadata")
    modis_table["Provided (Type 1 if yes else 0)"].fillna(0, inplace=True)
    modis_table["required"].fillna(0, inplace=True)
    modis_table["required_QC"].fillna(0, inplace=True)

    if int(modis_table[modis_table["Column title"]==\
        "Authentic spectra reference used"]["Provided (Type 1 if yes else 0)"]) == 1:
        score = (modis_table["Provided (Type 1 if yes else 0)"]*\
            modis_table.score*modis_table.score_scale).sum()
    else:
        score = modis_table["Provided (Type 1 if yes else 0)"]*modis_table.score.sum()

    if (modis_table["Provided (Type 1 if yes else 0)"]*modis_table.required).sum() == 5:
        required_info = True
    else:
        required_info = False

    if (modis_table["Provided (Type 1 if yes else 0)"]*modis_table.required_QC).sum() == 9:
        required_qc_info = True
    else:
        required_qc_info = False

    if score >= float(threshold) and required_info and required_qc_info:
        test_result = "pass"
    else:
        test_result = "fail"

    name_col = ["Required information provided", "Required QC information provided", \
                 "MODIS score", "MODIS test result"]
    value_col = [required_info, required_qc_info, score, test_result]

    data = ""
    for i, name in enumerate(name_col):
        data += "{0}            {1}            \n".format(name, value_col[i])

    with open(output_txt, 'w') as txt_file:
        txt_file.write("# plot_type: 'table'\n\
# section_name: 'MODIS test results'\n\
# description: 'This section describes if RUMP user has already provided enough information\
                to ensure data reusability'\n\
# pconfig:\n\
#     namespace: 'Cust Data'\n\
# headers:\n\
#     col1:\n\
#         title: 'Value'\n\
#         description: 'Value of MODIS test results'\n\
Items            col1\n" + data)


if __name__ == '__main__':

    logger.info('Calculating MODIS test results...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', \
        help="Input Excel table containing MODIS information;", \
        default="", dest="input", required=True)
    parser.add_argument(
        '-t', '--threshold', \
        help="MODIS test passing score threshold;", \
        default="22", dest="threshold", required=False)
    parser.add_argument(
        '-o', '--output', \
        help="define the location of output csv file;", \
        default="modis_mqc.txt", required=False)

    args = parser.parse_args()
    modis_info_generator(args.input, args.threshold, args.output)
