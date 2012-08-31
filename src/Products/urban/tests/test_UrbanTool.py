# -*- coding: utf-8 -*-
import unittest
from time import sleep
from DateTime import DateTime
from zope.component import createObject
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL, URBAN_INTEGRATION


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL
    layer = URBAN_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban

    def testGetStaticPylonsHost(self):
        self.portal_urban.setPylonsHost('pylon')
        self.assertEqual(self.portal_urban.getStaticPylonsHost(), 'http://pylon')
        self.portal_urban.setPylonsHost('urban.communesplone.be/trilili')
        self.assertEqual(self.portal_urban.getStaticPylonsHost(), 'http://urban.communesplone.be')
