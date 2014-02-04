# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.testing import URBAN_TESTS_CONFIG

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.component import createObject

import transaction
import unittest


class TestUrbanEvent(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.licence = portal.urban.buildlicences.objectValues()[0]
        login(portal, 'urbaneditor')

    def testAutomaticallyGenerateSingletonDocument(self):

        #if the option is not selected, no document should be generated at all
        self.portal_urban.setGenerateSingletonDocuments(False)
        createdEvent = createObject('UrbanEvent', 'accuse-de-reception', self.licence)
        self.failUnless(len(createdEvent.objectValues()) == 0)

        #now check the behaviour when the option is selected
        self.portal_urban.setGenerateSingletonDocuments(True)
        createdEvent = createObject('UrbanEvent', 'accuse-de-reception', self.licence)
        #if the urbanEvent can generate a single document, this document should be generated
        self.failUnless(len(createdEvent.objectValues()) == 1)
        createdEvent = createObject('UrbanEvent', 'rapport-du-college', self.licence)
        #if the urbanEvent can generate more than one document, no document should be generated at all
        self.failUnless(len(createdEvent.objectValues()) == 0)


class TestUrbanEventInstance(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence
        login(self.portal, 'urbaneditor')
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        if testlicence_id not in buildlicence_folder.objectIds():
            buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        licence = getattr(buildlicence_folder, testlicence_id)

        # create a test UrbanEvent in test_buildlicence
        catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = catalog(portal_type='UrbanEventType', id='prorogation')[0]
        self.event_type = event_type_brain.getObject()
        self.urban_event = licence.createUrbanEvent(self.event_type.UID())
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_urbanevent_has_attribute_pmTitle(self):
        self.assertTrue(hasattr(self.urban_event, 'pmTitle'))

    def test_urbanevent_has_attribute_pmDescription(self):
        self.assertTrue(hasattr(self.urban_event, 'pmDescription'))


class TestUrbanEventInquiryView(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence
        login(self.portal, 'urbaneditor')
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        if testlicence_id not in buildlicence_folder.objectIds():
            buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        licence = getattr(buildlicence_folder, testlicence_id)
        self.licence = licence
        licence.setInvestigationStart(DateTime())

        # create a test UrbanEventInquiry in test_buildlicence
        catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = catalog(portal_type='UrbanEventType', id='enquete-publique')[0]
        self.event_type = event_type_brain.getObject()
        self.inquiry = licence.createUrbanEvent(self.event_type.UID())
        self.view = self.inquiry.restrictedTraverse('urbaneventinquiryview')
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_UrbanEventInquiry_view_display(self):
        """ Test UrbanEventInquiry view is not broken """
        self.browser.open(self.inquiry.absolute_url())
