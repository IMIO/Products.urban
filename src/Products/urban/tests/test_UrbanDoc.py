#-*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName


class TestUrbanDoc(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

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
        self.browser.open(self.portal_urban.absolute_url() + '/buildlicence/urbaneventtypes/accuse-de-reception/urb-accuse.odt/view')
        self.failUnless('TALCondition' in self.browser.contents)

    def testTALConditionHidden(self):
        #check that the TAL condition of urbanDoc is hidden for generated documents
        # retrieve the event 'accusé de réception'
        licence = self.portal.urban.buildlicences.objectValues()[-1]
        events = licence.objectValues('UrbanEvent')
        event = [event for event in events if event.Title().startswith('Accus')][0]
        doc = event.objectValues()[0]
        self.browser.open(doc.absolute_url() + '/view')
        self.failUnless('TALCondition' not in self.browser.contents)
