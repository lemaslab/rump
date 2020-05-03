#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description : Unit tests for RUMP.
Copyright   : (c) LemasLab, 02/23/2020
Author      : Xinsong Du
License     : GNU GPL-v3.0 License
Maintainer  : xinsongdu@ufl.edu, manfiol@ufl.edu, djlemas@ufl.edu
Usage       : python -m unittest -v unit_tests.py
"""

import unittest
#pylint: disable=no-name-in-module
from blank_subtraction import blank_subtraction
from add_stats import add_stats
from venn import vd

class RumpTest(unittest.TestCase):
    """Unit tests for RUMP"""

    def do_test(self, result, expected):
        """Wrapper function for testing RUMP.
        """
        self.assertEqual(expected, result)

    def test_add_stats(self):
        """Test blank subtraction outputs correct result.
        """
        expected = "CITRATE" in add_stats(data_file=".travis/pos_data.csv", \
            design_file=".travis/pos_design.csv", output_file=".travis/pos_withstats.csv")
        self.do_test(True, expected)

    def test_blank_subtraction(self):
        """Test blank subtraction outputs correct result.
        """
        expected = blank_subtraction(data_file=".travis/pos_withstats.csv", \
            design_file=".travis/pos_design.csv")
        self.do_test(41, expected)

    def test_venn(self):
        """Test venn diagram code outputs correct result.
        """
        expected = vd(data_file=".travis/pos_withstats.csv", \
            design_file=".travis/pos_design.csv")
        self.do_test(48, expected)

if __name__ == '__main__':
    unittest.main()
