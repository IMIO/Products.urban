# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_CONFIG


class TestParcellingTerm(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.parcellingterm = portal.urban.parcellings.objectValues()[0]
        self.portal_urban = portal.portal_urban
        login(self.portal, self.layer.default_user)

    def test_parcellingTerm_title(self):
        parcelling = self.parcellingterm
        self.assertEquals(parcelling.Title(), 'Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005)')
