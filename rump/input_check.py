#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description : Unit tests for RUMP
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
'''

import os
import sys
import logging
import logging.handlers
import argparse
import pandas as pd
#pylint: disable=no-name-in-module
#from bionitio import FastaStats

PROGRAM_NAME = "RUMP"
EXIT_FILE_BALANCE_ERROR = 3
EXIT_FILE_TYPE_ERROR = 4
EXIT_FILE_EXISTANCE_ERROR = 5

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.
    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
#    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)

def parse_arguments():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Basic information for rump inputs'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-a', '--pos_data',
        help="define the location of input positive data folder;",
        default="pos_data.csv",
        dest="pos_data",
        required=False)
    parser.add_argument(
        '-b', '--neg_data',
        help="define the location of input negative data folder;",
        default="neg_data.csv",
        dest="neg_data",
        required=False)
    parser.add_argument(
        '-c', '--pos_design',
        help="define the location of input positive design csv file;",
        default="pos_design.csv",
        dest="pos_design",
        required=False)
    parser.add_argument(
        '-d', '--neg_design',
        help="define the location of input negative design csv file;",
        default="neg_design.csv",
        dest="neg_design",
        required=False)
    return parser.parse_args()

class DataCheck():
    '''Check inputs for RUMP'''
    def __init__(self, input_dir_pos, input_dir_neg, POS_design_path, NEG_design_path):
        try:
            pos_data_file_names = os.listdir(input_dir_pos)
            neg_data_file_names = os.listdir(input_dir_neg)
            assert len(pos_data_file_names) != 0
            assert len(neg_data_file_names) != 0
        except:
            exit_with_error('one or more input files does not exist.', EXIT_FILE_EXISTANCE_ERROR)

        self.pos_design_file = POS_design_path
        self.neg_design_file = NEG_design_path
        self.pos_data_files = [os.path.join(input_dir_pos, x) for x in pos_data_file_names]
        self.neg_data_files = [os.path.join(input_dir_neg, x) for x in neg_data_file_names]

    def get_pos_groupnames(self):
        '''Get group name of positive data.

        # Returns:
            group name.
        '''
        data = pd.read_csv(self.pos_design_file)
        return sorted(list(data['group']))

    def get_neg_groupnames(self):
        '''Get group name of negative data.

        # Returns:
            group name.
        '''
        data = pd.read_csv(self.neg_design_file)
        return sorted(list(data['group']))

    def get_inputfile_format(self):
        '''Get input file type.

        # Returns:
            input file names extention.
        '''
        formats = []
        for file in self.pos_data_files + self.neg_data_files:
            formats.append(file.split('.')[-1])
        return list(set(formats))

    # Test if positive file groups are the same as negative file groups
    def check_input_existance(self):
        '''Check if input file exist.
        '''
        try:
            for pos_file, neg_file in zip(self.pos_data_files, self.neg_data_files):
                assert os.path.exists(pos_file)
                assert os.path.exists(neg_file)
        except AssertionError:
            exit_with_error('one or more input files does not exist.', EXIT_FILE_EXISTANCE_ERROR)

    def check_input_balance(self):
        '''Check if input positive and negative files balanced.
        '''
        try:
            assert self.get_pos_groupnames() == self.get_neg_groupnames()
        except AssertionError:
            exit_with_error('positive file groups are not the same as \
                negative file groups, please check design files.', EXIT_FILE_BALANCE_ERROR)

    def check_input_formats(self):
        '''Check if input file type is mzXML.
        '''
        try:
            assert self.get_inputfile_format() == ['mzXML']
        except AssertionError:
            exit_with_error('not all input files are in .mzXML format, \
                please check input data folders.', EXIT_FILE_TYPE_ERROR)

def main():
    '''Main function.
    '''
# Orchestrate the execution of the program
    args = parse_arguments()
    check = DataCheck(args.pos_data, args.neg_data, args.pos_design, args.neg_design)
    logger.info("start input check: ")
    check.check_input_existance()
    check.check_input_balance()
    check.check_input_formats()
    logger.info("input check done!")
    logger.info("Some information of input files")
    logger.info("group names: %s, %s", check.get_pos_groupnames(), check.get_pos_groupnames())

if __name__ == '__main__':
    main()
