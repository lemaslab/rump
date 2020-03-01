#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description : Unit tests for ReUMP
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License 
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python -m unittest -v ReUMP_test
'''

import unittest
import os
#pylint: disable=no-name-in-module
#from bionitio import FastaStats

class test_reump(unittest.TestCase):
    '''Unit tests for ReUMP'''
    def test_file_type(self, input_dir):
        "Test if input files are .mzXML format"
        for file in os.listdir(input_dir):
            self.assertTrue(file.endswith('.mzXML'), 
                            msg="Wrong file type included, please use .mzXML file as inputs")


    def test_ion_balance(self, pos_design, neg_design):
        

if __name__ == '__main__':
    unittest.main()


