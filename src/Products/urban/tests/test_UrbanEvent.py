# -*- coding: utf-8 -*-

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.component import createObject

from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.testing import URBAN_TESTS_INTEGRATION

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

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence , then a test UrbanEvent in it
        login(self.portal, 'urbaneditor')
        envclassone_folder = self.urban.envclassones
        testlicence_id = 'test_buildlicence'
        if testlicence_id not in envclassone_folder.objectIds():
            envclassone_folder.invokeFactory('BuildLicence', id=testlicence_id)
            transaction.commit()
        licence = getattr(envclassone_folder, testlicence_id)
        # create a test UrbanEvent in test_buildlicence
        catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = catalog(portal_type='UrbanEventType', id='prorogation')[0]
        event_type = event_type_brain.getObject()
        licence.createUrbanEvent(event_type.UID())

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')
