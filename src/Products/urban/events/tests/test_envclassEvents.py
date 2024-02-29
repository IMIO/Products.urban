# -*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_INTEGRATION

from Products.urban.events import envclassEvents


class TestEnvEvent(unittest.TestCase):
    layer = URBAN_TESTS_INTEGRATION

    def test_update_history_for_vocabulary_field(self):
        testobj = TestingObject("attr_1_value1")
        # store the initialization
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        self.assertEqual(historized_object["attr_1_history"][0], "attr_1_value1")
        # update object
        testobj.setAttr_1([type("attr_1_object", (object,), {"id": "attr_1_value2"})()])
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        self.assertEqual(historized_object["attr_1_history"][0], "attr_1_value2")

    def test_get_value_history_by_index_without_history(self):
        """
        Test get_value_history_by_index function when there is no history
        """
        testobj = TestingObject("attr_1_value3")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        self.assertTrue(isinstance(historized_object, dict))
        self.assertEqual(historized_object["attr_1_history"], [])

    def test_get_value_history_by_index_without_history_index(self):
        """
        Test get_value_history_by_index function when there is no history
        record for the given index
        """
        testobj = TestingObject("attr_1_value1")
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        self.assertEqual(historized_object["attr_1_history"][0], "attr_1_value1")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -10
        )
        self.assertTrue(isinstance(historized_object, dict))
        self.assertEqual(historized_object["attr_1_history"], [])

    def test_get_value_history_by_index_with_action(self):
        """
        Test get_value_history_by_index function when an action is specified
        """
        pass

    def test_get_value_history_by_index(self):
        testobj = TestingObject("attr_1_value1")
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        self.assertEqual(historized_object["attr_1_history"][0], "attr_1_value1")
        # update object
        testobj.setAttr_1([type("attr_1_object", (object,), {"id": "attr_1_value2"})()])
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        self.assertEqual(historized_object["attr_1_history"][0], "attr_1_value2")
        historized_object = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -2
        )
        self.assertEqual(historized_object["attr_1_history"][0], "attr_1_value1")

    def test_has_changes(self):
        testobj = TestingObject("attr_1_value1")
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        # update object
        testobj.setAttr_1([type("attr_1_object", (object,), {"id": "attr_1_value2"})()])
        envclassEvents.update_history_for_vocabulary_field(testobj, "attr_1")
        historized_object_lastest = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -1
        )
        historized_object_previous = envclassEvents.get_value_history_by_index(
            testobj, "attr_1_history", -2
        )
        self.assertTrue(
            envclassEvents.has_changes(
                historized_object_lastest, historized_object_previous
            )
        )


class TestingObject(object):
    def __init__(self, attr, attr2=None):

        self.attr_1 = [type("attr_1_object", (object,), {"id": attr})()]
        self.attr_2 = [type("attr_2_object", (object,), {"id": attr2})()]

    def getAttr_1(self):
        return self.attr_1

    def setAttr_1(self, value):
        self.attr_1 = value

    def getAttr_2(self):
        return self.attr_2

    def setAttr_2(self, value):
        self.attr_2 = value
