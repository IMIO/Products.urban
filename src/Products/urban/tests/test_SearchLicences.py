#-*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL
from Products.CMFCore.utils import getToolByName


class TestSearchLicencesView(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.searchview = self.urban.restrictedTraverse('urbansearchview')
        login(self.portal, 'urbaneditor')
