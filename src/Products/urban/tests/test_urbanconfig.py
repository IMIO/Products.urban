# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.tests.helpers import BrowserTestCase

from plone.app.testing import login
from plone.testing.z2 import Browser


class TestUrbanConfig(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.config = portal.portal_urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        self.browser.handleErrors = False

    def test_urbanconfig_view_display(self):
        """
         Tests urban config view is not broken for whatsoever reason
        """
        self.browser.open(self.config.absolute_url())

    def test_architects_config_view_display(self):
        """
         Tests architects folder view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.architects.absolute_url())

    def test_notaries_config_view_display(self):
        """
         Tests notaries folder view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.notaries.absolute_url())

    def test_geometricians_config_view_display(self):
        """
         Tests geometricians folder view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.geometricians.absolute_url())

    def test_parcellings_config_view_display(self):
        """
         Tests parcellings view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.parcellings.absolute_url())

    def test_foldermanagers_view_layout(self):
        """
        foldermanagers layout should be sorted_title_folderview
        """
        fm_folder = self.portal.portal_urban.foldermanagers
        self.assertEqual()
