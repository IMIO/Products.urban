# -*- coding: utf-8 -*-

from Products.urban.profiles import testsWithConfig
from Products.urban.scripts import odtsearch

import os

import unittest


class TestODTSearchScript(unittest.TestCase):
    def setUp(self):
        self.templates_folder_path = "{}/templates/".format(testsWithConfig.__path__[0])
        # we do not display any search result on console
        odtsearch.verbosity = -1

        odt_names = os.listdir(self.templates_folder_path)
        self.odt_names = [
            self.templates_folder_path + filename for filename in odt_names
        ]

    def test_search_for_existing_pattern(self):
        to_find = ["get"]
        result = odtsearch.searchODTs(self.odt_names, to_find, silent=True)

        self.assertTrue(len(result) > 0)

    def test_search_for_non_existing_pattern(self):
        to_find = ["trolololo"]
        result = odtsearch.searchODTs(self.odt_names, to_find, silent=True)

        self.assertTrue(not result)

    def test_recursive_folder_search(self):
        from Products import urban

        to_find = ["get"]
        result = odtsearch.searchODTs(
            urban.__path__, to_find, recursive=True, silent=True
        )

        self.assertTrue(len(result) > 0)

    def test_case_sensitive_search_with_exsiting_pattern(self):
        to_find = ["GeT"]
        result = odtsearch.searchODTs(
            self.odt_names, to_find, ignorecase=False, silent=True
        )

        self.assertTrue(not result)

    def test_case_insensitive_search_with_exsiting_pattern(self):
        to_find = ["GeT"]
        result = odtsearch.searchODTs(
            self.odt_names, to_find, ignorecase=True, silent=True
        )

        self.assertTrue(len(result) > 0)

    def test_result_display(self):
        to_find = ["get"]
        result = odtsearch.searchODTs(self.odt_names, to_find, silent=True)

        result_display = odtsearch.displaySearchSummary(
            result, self.odt_names, to_find, ""
        )
        self.assertTrue("160 matches" in result_display)
