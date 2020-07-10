#-*- coding: utf-8 -*-
from plone.app.testing import login
from Products.urban.interfaces import IGenericLicence
from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.tests.helpers import BrowserTestCase

from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from testfixtures import compare, StringComparison as S

from plone import api


class TestLicenceStatsView(BrowserTestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.statsview = self.urban.restrictedTraverse('urbanstatsview')
        login(self.portal, 'urbaneditor')
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')
        self.browser.open("%s%s" % (self.urban.absolute_url(), "/urbanstatsview"))

    def testStatsViewDisplay(self):
        #check that the stats view is simply available
        self.browser.open(self.urban.absolute_url() + '/urbanstatsview')
        compare(S("(?s).*Statistiques des dossiers.*"), self.browser.contents)

    def testStatsViewEmptyResult(self):
        #check the display result when no licences fall under stats criteria
        self.browser.open(self.urban.absolute_url() + '/urbanstatsview')
        self.browser.getControl("Statistics").click()
        new_url = '%s/urbanstatsview%s' % (self.urban.absolute_url(), self.browser.url.split('/urban')[1])
        self.browser.open(new_url)
        compare(S("(?s).*0 dossiers.*"), self.browser.contents)

    def testStatsViewsResult(self):
        licences_number = 8
        #check the normal case display result
        self.browser.open(self.urban.absolute_url() + '/urbanstatsview')
        self.browser.getControl(name="licence_states").getControl(value='in_progress').click()
        self.browser.getControl("Statistics").click()
        new_url = '%s/urbanstatsview%s' % (self.urban.absolute_url(), self.browser.url.split('/urban')[1])
        self.browser.open(new_url)
        compare(S("(?s).*{} dossiers.*".format(licences_number)), self.browser.contents)
