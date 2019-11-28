#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

import pandas as pd
import csv

def mzmine_result_extraction(input_file, output_file, ion):

    data = pd.read_csv(input_file, dtype = str, quoting = csv.QUOTE_ALL)
    selected_columns = ["row ID", "row m/z", "row retention time", "row identity", 
                    "row number of detected peaks", "row comment", "QE2_jdg_115_Lemas_1[Blank]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_2[Blank]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_3[Blank]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_4[Blank]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_1[extBlank]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_2[extBlank]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_3[extBlank]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_4[extBlank]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_1[NeatQC]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_2[NeatQC]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_1[BLS001A]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_10[BLS010A]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_11[BLS010A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_12[BLS010A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_2[BLS001A]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_4[BLS002A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_7[BLS003A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_3[BLS001A]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_5[BLS002A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_8[BLS003A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_9[BLS003A]" + ion + ".mzXML Peak height", 
                    "QE2_jdg_115_Lemas_6[BLS002A]" + ion + ".mzXML Peak height", "QE2_jdg_115_Lemas_1[BLS001A]" + ion + "-dd.mzXML Peak height", "QE2_jdg_115_Lemas_2[BLS001A]" + ion + "-dd.mzXML Peak height", 
                    "QE2_jdg_115_Lemas_3[BLS001A]" + ion + "-dd.mzXML Peak height"]
    logger.info(list(data.columns))
    data_selected = data[selected_columns]
    data_selected = data_selected.rename(index=str, columns={"row ID": "row.ID", 
                                                         "row m/z": "row.m.z",
                                                         "row retention time": "row.retention.time", 
                                                         "row identity": "row.identity", 
                                                         "row number of detected peaks": "row.number.of.detected.peaks",
                                                         "row comment": "row.comment", 
                                                         "QE2_jdg_115_Lemas_1[Blank]" + ion + ".mzXML Peak height": "X1.Blank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_2[Blank]" + ion + ".mzXML Peak height": "X2.Blank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_3[Blank]" + ion + ".mzXML Peak height": "X3.Blank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_4[Blank]" + ion + ".mzXML Peak height": "X4.Blank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_1[extBlank]" + ion + ".mzXML Peak height": "X1.extBlank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_2[extBlank]" + ion + ".mzXML Peak height": "X2.extBlank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_3[extBlank]" + ion + ".mzXML Peak height": "X3.extBlank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_4[extBlank]" + ion + ".mzXML Peak height": "X4.extBlank." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_1[NeatQC]" + ion + ".mzXML Peak height": "X1.NeatQC." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_2[NeatQC]" + ion + ".mzXML Peak height": "X2.NeatQC." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_1[NeatQC]" + ion + ".mzXML Peak height": "X1.NeatQC." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_1[BLS001A]" + ion + ".mzXML Peak height": "X1.BLS001A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_10[BLS010A]" + ion + ".mzXML Peak height": "X10.BLS010A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_11[BLS010A]" + ion + ".mzXML Peak height": "X11.BLS010A." + ion + ".mzXML.Peak.height",
                                                         "QE2_jdg_115_Lemas_12[BLS010A]" + ion + ".mzXML Peak height": "X12.BLS010A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_2[BLS001A]" + ion + ".mzXML Peak height": "X2.BLS001A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_4[BLS002A]" + ion + ".mzXML Peak height": "X4.BLS002A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_7[BLS003A]" + ion + ".mzXML Peak height": "X7.BLS003A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_3[BLS001A]" + ion + ".mzXML Peak height": "X3.BLS001A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_5[BLS002A]" + ion + ".mzXML Peak height": "X5.BLS002A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_8[BLS003A]" + ion + ".mzXML Peak height": "X8.BLS003A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_9[BLS003A]" + ion + ".mzXML Peak height": "X9.BLS003A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_6[BLS002A]" + ion + ".mzXML Peak height": "X6.BLS002A." + ion + ".mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_1[BLS001A]" + ion + "-dd.mzXML Peak height": "X1.BLS001A." + ion + ".dd.mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_2[BLS001A]" + ion + "-dd.mzXML Peak height": "X2.BLS001A." + ion + ".dd.mzXML.Peak.height", 
                                                         "QE2_jdg_115_Lemas_3[BLS001A]" + ion + "-dd.mzXML Peak height": "X3.BLS001A." + ion + ".dd.mzXML.Peak.height"})
    data_selected.to_csv(output_file, index = False)

if __name__ == '__main__':

    logger.info('extracting useful columns...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="define the location of input csv file;", required = True)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", required = True)
    parser.add_argument(
        '-n', '--ion', help="define the ion;", dest = "ion", required = True)
    
    args = parser.parse_args()
    mzmine_result_extraction(args.input, args.output, args.ion)


