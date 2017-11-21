# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.tests.helpers import BrowserTestCase

from plone.app.testing import login
from plone.testing.z2 import Browser


class TestLicenceConfig(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        self.licenceconfigs = [config for config in self.portal_urban.objectValues('LicenceConfig')]

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        self.browser.handleErrors = False

    def test_licenceconfig_view_display(self):
        """
         Tests licenceconfig view is not broken for whatsoever reason
        """
        for licenceconfig in self.licenceconfigs:
            self.browser.open(licenceconfig.absolute_url())
