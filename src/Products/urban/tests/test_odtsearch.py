# -*- coding: utf-8 -*-

from Products.urban.profiles import testsWithConfig
from Products.urban.scripts.odtsearch import SearchPODTemplates

import os

import unittest


class TestODTSearchScript(unittest.TestCase):
    def setUp(self):
        self.templates_folder_path = "{}/templates/".format(testsWithConfig.__path__[0])

        odt_names = os.listdir(self.templates_folder_path)
        self.odt_files = [
            self.templates_folder_path + filename for filename in odt_names
        ]

    def test_search_for_existing_pattern(self):
        to_find = ["get"]
        odtsearch = SearchPODTemplates(to_find, self.odt_files, silent=True)
        result = odtsearch.run()

        self.assertTrue(len(result) > 0)

    def test_search_for_non_existing_pattern(self):
        to_find = ["trolololo"]
        odtsearch = SearchPODTemplates(to_find, self.odt_files, silent=True)
        result = odtsearch.run()

        self.assertTrue(not result)

    def test_recursive_folder_search(self):
        from Products import urban

        to_find = ["get"]
        odtsearch = SearchPODTemplates(
            to_find, urban.__path__[0] + "/", silent=True, recursive=True
        )
        result = odtsearch.run()

        self.assertTrue(len(result) > 0)

    def test_case_sensitive_search_with_existing_pattern(self):
        to_find = ["GeT"]
        odtsearch = SearchPODTemplates(
            to_find, self.odt_files, silent=True, ignorecase=False
        )
        result = odtsearch.run()

        self.assertTrue(not result)

    def test_case_insensitive_search_with_existing_pattern(self):
        to_find = ["GeT"]
        odtsearch = SearchPODTemplates(
            to_find, self.odt_files, silent=True, ignorecase=True
        )
        result = odtsearch.run()

        self.assertTrue(len(result) > 0)

    def test_result_display(self):
        to_find = ["get"]
        odtsearch = SearchPODTemplates(to_find, self.odt_files, silent=True)
        result = odtsearch.run()
        result_display = odtsearch.get_result_display(result)
        self.assertTrue("170 matches" in result_display)
