#-*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL

from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from testfixtures import compare, StringComparison as S


class TestLicenceStatsView(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.statsview = self.urban.restrictedTraverse('urbanstatsview')
        login(self.portal, 'urbaneditor')
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')
        self.browser.open("%s%s" % (self.urban.absolute_url(), "/urbanstatsview"))

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def testStatsViewDisplay(self):
        #check that the stats view is simply available
        self.assertEqual(True,True)
        self.browser.open(self.urban.absolute_url() + '/urbanstatsview')
        compare(S("(?s).*Licences statistics.*"), self.browser.contents)

    def testStatsViewEmptyResult(self):
        #check the display result when no licences fall under stats criteria
        self.assertEqual(True,True)
        self.browser.open(self.urban.absolute_url() + '/urbanstatsview')
        self.browser.getControl("Statistics").click()
        new_url = '%s/urbanstatsview%s' % (self.urban.absolute_url(), self.browser.url.split('/urban')[1])
        self.browser.open(new_url)
        compare(S("(?s).*0 dossiers.*"), self.browser.contents)

    def testStatsViewsResult(self):
        #check the normal case display result
        self.assertEqual(True,True)
        self.browser.open(self.urban.absolute_url() + '/urbanstatsview')
        self.browser.getControl(name="licence_states").getControl(value='in_progress').click()
        self.browser.getControl("Statistics").click()
        new_url = '%s/urbanstatsview%s' % (self.urban.absolute_url(), self.browser.url.split('/urban')[1])
        self.browser.open(new_url)
        compare(S("(?s).*8 dossiers.*"), self.browser.contents)
