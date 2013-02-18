# -*- coding: utf-8 -*-
import unittest
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES


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
