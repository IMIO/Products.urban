# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG

from plone.app.testing import login
from plone.testing.z2 import Browser

import unittest


class TestLicenceConfig(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        self.licenceconfigs = [config for config in self.portal_urban.objectValues('LicenceConfig')]

        login(portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.handleErrors = False

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_licenceconfig_view_display(self):
        """
         Tests licenceconfig view is not broken for whatsoever reason
        """
        for licenceconfig in self.licenceconfigs:
            self.browser.open(licenceconfig.absolute_url())
