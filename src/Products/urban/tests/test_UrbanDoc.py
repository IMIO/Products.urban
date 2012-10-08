#-*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from testfixtures import compare, StringComparison as S


class TestUrbanDoc(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        login(self.portal, 'urbaneditor')
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def testTALConditionVisibleInConfig(self):
        #check that the TAL condition of urbanDoc is displayed in the urban config
        self.browser.open(self.portal_urban.absolute_url() + '/buildlicence/urbaneventtypes/depot-de-la-demande/urb-recepisse.odt/view')
        self.failUnless('TALCondition' in self.browser.contents)

    def testTALConditionHidden(self):
        #check that the TAL condition of urbanDoc is hidden for generated documents
        doc = self.urban.buildlicences.objectValues()[0].listFolderContents(contentFilter={"portal_type" : "UrbanEvent"})[0].objectValues()[0]
        self.browser.open(doc.absolute_url() + '/view')
        self.failUnless('TALCondition' not in self.browser.contents)

