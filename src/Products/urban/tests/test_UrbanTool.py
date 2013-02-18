# -*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL, URBAN_TESTS_PROFILE_INTEGRATION


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL
    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban

    def testGetStaticPylonsHost(self):
        self.portal_urban.setPylonsHost('http://pylon')
        self.assertEqual(self.portal_urban.getStaticPylonsHost(), 'http://pylon')
        self.portal_urban.setPylonsHost('http://urban.communesplone.be/trilili')
        self.assertEqual(self.portal_urban.getStaticPylonsHost(), 'http://urban.communesplone.be')
