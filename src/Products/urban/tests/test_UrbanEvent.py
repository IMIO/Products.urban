# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from Products.urban.tests.helpers import BrowserTestCase
from Products.urban.tests.helpers import SchemaFieldsTestCase
from Products.urban import utils

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

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
        createdEvent = self.licence.createUrbanEvent('accuse-de-reception')
        self.failUnless(len(createdEvent.objectValues()) == 0)

        #now check the behaviour when the option is selected
        self.portal_urban.setGenerateSingletonDocuments(True)
        createdEvent = self.licence.createUrbanEvent('accuse-de-reception')
        #if the urbanEvent can generate a single document, this document should be generated
        self.failUnless(len(createdEvent.objectValues()) == 1)
        createdEvent = self.licence.createUrbanEvent('rapport-du-college')
        #if the urbanEvent can generate more than one document, no document should be generated at all
        self.failUnless(len(createdEvent.objectValues()) == 0)


class TestUrbanEventInstance(SchemaFieldsTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence
        login(self.portal, 'urbaneditor')
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)

        # create a test UrbanEvent in test_buildlicence
        catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = catalog(portal_type='UrbanEventType', id='prorogation')[0]
        self.event_type = event_type_brain.getObject()
        self.urban_event = self.licence.createUrbanEvent(self.event_type)
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def tearDown(self):
        api.content.delete(self.licence)
        transaction.commit()

    def test_urbanevent_has_attribute_eventDate(self):
        self.assertTrue(hasattr(self.urban_event, 'eventDate'))

    def test_urbanevent_has_attribute_depositType(self):
        self.assertTrue(hasattr(self.urban_event, 'depositType'))

    def test_urbanevent_has_attribute_transmitDate(self):
        self.assertTrue(hasattr(self.urban_event, 'transmitDate'))

    def test_urbanevent_has_attribute_reiceptDate(self):
        self.assertTrue(hasattr(self.urban_event, 'receiptDate'))

    def test_urbanevent_has_attribute_reicevedDocumentReference(self):
        self.assertTrue(hasattr(self.urban_event, 'receivedDocumentReference'))

    def test_urbanevent_has_attribute_auditionDate(self):
        self.assertTrue(hasattr(self.urban_event, 'auditionDate'))

    def test_urbanevent_has_attribute_decisionDate(self):
        self.assertTrue(hasattr(self.urban_event, 'decisionDate'))

    def test_urbanevent_has_attribute_decision(self):
        self.assertTrue(hasattr(self.urban_event, 'decision'))

    def test_urbanevent_has_attribute_decisionText(self):
        self.assertTrue(hasattr(self.urban_event, 'decisionText'))

    def test_urbanevent_has_attribute_recourseDecisionDisplayDate(self):
        self.assertTrue(hasattr(self.urban_event, 'recourseDecisionDisplayDate'))

    def test_urbanevent_has_attribute_recourseDecision(self):
        self.assertTrue(hasattr(self.urban_event, 'recourseDecision'))

    def test_urbanevent_has_attribute_adviceAgreementlevel(self):
        self.assertTrue(hasattr(self.urban_event, 'adviceAgreementLevel'))

    def test_urbanevent_has_attribute_opinionText(self):
        self.assertTrue(hasattr(self.urban_event, 'opinionText'))

    def test_urbanevent_has_attribute_eventRecipient(self):
        self.assertTrue(hasattr(self.urban_event, 'getEventRecipient'))

    def test_urbanevent_has_attribute_urbaneventtypes(self):
        self.assertTrue(hasattr(self.urban_event, 'getUrbaneventtypes'))

    def test_urbanevent_has_attribute_pmTitle(self):
        self.assertTrue(hasattr(self.urban_event, 'pmTitle'))

    def test_urbanevent_has_attribute_pmDescription(self):
        self.assertTrue(hasattr(self.urban_event, 'pmDescription'))


class TestUrbanEventInquiryView(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        login(self.portal, 'urbaneditor')

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def _create_test_licence_with_inquiry(self, portal_type):
        licence_folder = utils.getLicenceFolder(portal_type)
        testlicence_id = 'test_{}'.format(portal_type.lower())
        licence_folder.invokeFactory(portal_type, id=testlicence_id)
        licence = getattr(licence_folder, testlicence_id)
        licence.setInvestigationStart(DateTime())

        # create a test UrbanEventInquiry in test_licence
        inquiry = licence.objectValues('UrbanEventInquiry')
        if not inquiry:
            inquiry = licence.createUrbanEvent('enquete-publique')
            transaction.commit()
        else:
            inquiry = inquiry[0]

        return licence, inquiry

    def test_Buildicence_UrbanEventInquiry_view_display(self):
        """ Test UrbanEventInquiry view is not broken """
        buildlicence, inquiry = self._create_test_licence_with_inquiry('BuildLicence')
        self.browser.open(inquiry.absolute_url())

    def test_EnvClassOne_UrbanEventInquiry_view_display(self):
        """ Test UrbanEventInquiry view is not broken """
        envclassone, inquiry = self._create_test_licence_with_inquiry('EnvClassOne')
        self.browser.open(inquiry.absolute_url())

    def test_200m_radius_when_EnvironmentImpactStudy(self):
        envclassone, inquiry = self._create_test_licence_with_inquiry('EnvClassOne')
        envclassone.setHasEnvironmentImpactStudy(False)
        transaction.commit()

        self.browser.open(inquiry.absolute_url())
        contents = self.browser.contents
        self.assertTrue("dans un rayon de 50m" in contents)

        envclassone.setHasEnvironmentImpactStudy(True)
        transaction.commit()

        self.browser.open(inquiry.absolute_url())
        contents = self.browser.contents
        self.assertTrue("dans un rayon de 200m" in contents)
