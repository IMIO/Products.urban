# -*- coding: utf-8 -*-
import unittest
from time import sleep
from DateTime import DateTime
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestUrbanEvent(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        urban = portal.urban
        self.buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        self.buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        self.buildLicence = getattr(self.buildLicences, LICENCE_ID)


    def testAutomaticallyGenerateSingletonDocument(self):

        #if the option is not selected, no document should be generated at all
        self.portal_urban.setGenerateSingletonDocuments(False)
        createdEvent = createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence)
        self.failUnless(len(createdEvent.objectValues()) == 0)

        #now check the behaviour when the option is selected
        self.portal_urban.setGenerateSingletonDocuments(True)
        createdEvent = createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence)
        #if the urbanEvent can generate a single document, this document should be generated
        self.failUnless(len(createdEvent.objectValues()) == 1)
        createdEvent = createObject('UrbanEvent', 'accuse-de-reception', self.buildLicence)
        #if the urbanEvent can generate more than one document, no document should be generated at all
        self.failUnless(len(createdEvent.objectValues()) == 0)
