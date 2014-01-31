# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

import unittest


class TestScheduleView(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.urban = portal.urban
        self.searchview = portal.restrictedTraverse('urbansearchview')

        login(portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.handleErrors = False

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_search_view_display(self):
        """
         Tests search  view is not broken for whatsoever reason
        """
        search_url = '{base_url}/schedule'.format(base_url=self.urban.absolute_url())
        self.browser.open(search_url)
