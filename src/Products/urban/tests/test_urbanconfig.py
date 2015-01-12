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

        login(portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.handleErrors = False

    def test_urbanconfig_view_display(self):
        """
         Tests search  view is not broken for whatsoever reason
        """
        self.browser.open(self.config.absolute_url())
