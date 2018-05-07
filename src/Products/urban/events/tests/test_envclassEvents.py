# -*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_INTEGRATION

from Products.urban.events import envclassEvents


class TestEnvEvent(unittest.TestCase):
    layer = URBAN_TESTS_INTEGRATION

    def test_update_history_for_vocabulary_field(self):
        pass

    def test_get_value_history_by_index_without_history(self):
        """
        Test get_value_history_by_index function when there is no history
        """
        pass

    def test_get_value_history_by_index_without_history_index(self):
        """
        Test get_value_history_by_index function when there is no history
        record for the given index
        """
        pass

    def test_get_value_history_by_index_with_action(self):
        """
        Test get_value_history_by_index function when an action is specified
        """
        pass

    def test_get_value_history_by_index(self):
        pass

    def test_has_changes(self):
        pass
