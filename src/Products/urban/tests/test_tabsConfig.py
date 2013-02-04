#-*- coding: utf-8 -*-
import unittest
from urllib2 import HTTPError
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL

from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from testfixtures import compare, StringComparison as S


class TestTabsConfigView(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.statsview = self.urban.restrictedTraverse('urbanstatsview')
        login(self.portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.open("%s%s" % (self.urban.absolute_url(), "/urbanstatsview"))

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def testLicenceViewsDisplay(self):
        """
          check that any licence view is not broken for whatsoever reason
        """
        from Products.urban.config import URBAN_TYPES
        for licence_type in URBAN_TYPES:
            licences = getattr(self.urban, '%ss' % licence_type.lower()).objectValues()
            if licences:
                licence = licences[0]
                try:
                    self.browser.open(licence.absolute_url())
                except HTTPError:
                    self.fail()


    def testTabsReordering(self):
        """
         Put location tab on first postion in the buildlicence tabs config
         then check that this order is respected on some buildlicence view
        """
        config = self.portal.portal_urban.buildlicence
        order = config.getTabsConfig()
        new_tab_order = [order[2]] + list(order[:2]) + list(order[3:])
        field = config.getField('tabsConfig')
        field.allow_delete = True
        config.setTabsConfig(new_tab_order)
        config.reindexObject()
        field.allow_delete = False
        buildlicence = self.urban.buildlicences.objectValues()[0]
        try:
            self.browser.open(buildlicence.absolute_url())
        except HTTPError:
            self.fail()
        compare(S(".*fieldsetlegend-urban_location.*fieldsetlegend-urban_description.*"), self.browser.contents.replace('\n', ''))
