# -*- coding: utf-8 -*-

from Products.urban.indexes import genericlicence_rubrics

import unittest


class FakeRubric(object):
    def __init__(self, number, description):
        self.number = number
        self.description = description

    def getId(self):
        return self.number

    def Description(self):
        return self.description


class FakeLicence(object):
    def __init__(self, rubrics):
        self.rubrics = rubrics

    def getRubrics(self):
        return self.rubrics


class TestRubricsIndex(unittest.TestCase):
    def test_rubrics_index_contains_number_and_description(self):
        licence = FakeLicence(
            [
                FakeRubric("01.10.01", "<p>Affectation de terres incultes</p>"),
                FakeRubric("40.10.01.01", "Installation de combustion"),
            ]
        )
        indexed = genericlicence_rubrics(licence)()
        self.assertEqual(
            indexed,
            u"01.10.01 Affectation de terres incultes "
            u"40.10.01.01 Installation de combustion",
        )

    def test_rubrics_index_without_rubrics(self):
        licence = FakeLicence([])
        self.assertIsNone(genericlicence_rubrics(licence)())
