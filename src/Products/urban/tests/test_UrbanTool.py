# -*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL, URBAN_TESTS_CONFIG


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL
    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
