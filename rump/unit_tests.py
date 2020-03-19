#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Unit tests for RUMP.
Usage: python -m unittest -v unit_tests.py
'''

import unittest
import pandas as pd
#pylint: disable=no-name-in-module
from blank_subtraction import blank_subtraction
from venn import vd

class rump_test(unittest.TestCase):
    '''Unit tests for FastaStats'''

    def do_test(self, result, expected):
        "Wrapper function for testing FastaStats"
        self.assertEqual(expected, result)

    def test_blank_subtraction(self):
        "test blank subtraction outputs correct result"
        expected = blank_subtraction(data_file=".travis/pos_data.csv", design_file=".travis/pos_design.csv")
        self.do_test(813, expected)

    def test_venn(self):
        "Test venn diagram code outputs correct result"
        expected = vd(data_file=".travis/pos_data.csv", design_file=".travis/pos_design.csv")
        self.do_test(49, expected)

if __name__ == '__main__':
    unittest.main()