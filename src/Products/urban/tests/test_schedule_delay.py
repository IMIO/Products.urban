# -*- coding: utf-8 -*-
from Products.urban.schedule.delay import AnnoncedDelay
from Products.urban.schedule.delay import get_delay_value

import unittest


class FakeTask(object):
    def get_task_config(self):
        return None


class FakeLicence(object):
    def __init__(self, annonced_delay, modified_blueprints_delay=None):
        self.annonced_delay = annonced_delay
        self.modified_blueprints_delay = modified_blueprints_delay

    def getAnnoncedDelay(self):
        return self.annonced_delay

    def getHasModifiedBlueprints(self):
        return self.modified_blueprints_delay is not None

    def getDelayAfterModifiedBlueprints(self):
        return self.modified_blueprints_delay


class TestGetDelayValue(unittest.TestCase):
    def test_string_value(self):
        self.assertEqual(get_delay_value("30j"), "30j")

    def test_list_value(self):
        self.assertEqual(get_delay_value(["30j"]), "30j")
        self.assertEqual(get_delay_value(("30j", "60j")), "30j")

    def test_empty_values(self):
        self.assertEqual(get_delay_value([]), "")
        self.assertEqual(get_delay_value(None), None)


class TestAnnoncedDelay(unittest.TestCase):
    def _calculate(self, licence):
        return AnnoncedDelay(licence, FakeTask()).calculate_delay()

    def test_string_delay(self):
        self.assertEqual(self._calculate(FakeLicence("30j")), 30)

    def test_list_delay(self):
        # default value of the field is stored as a list (e.g. NOTICe)
        self.assertEqual(self._calculate(FakeLicence(["30j"])), 30)

    def test_empty_list_delay(self):
        self.assertEqual(self._calculate(FakeLicence([])), 0)

    def test_list_delay_after_modified_blueprints(self):
        self.assertEqual(self._calculate(FakeLicence("30j", ["75j"])), 75)
