# -*- coding: utf-8 -*-
import unittest
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        urban = portal.urban
        buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        self.buildLicence = getattr(buildLicences, LICENCE_ID)

    def testGetLastEventWithoutEvent(self):
        self.assertEqual(self.buildLicence._getLastEvent(), None)

    def testGetLastEventWithOneEvent(self):
        self.assertEqual(self.buildLicence._getLastEvent(), None)
        createdEvent = createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence)
        event = self.buildLicence._getLastEvent()
        self.assertEqual(createdEvent, event)
        self.failUnless(event is not None)

    def testGetLastEventWithMoreThanOneEvent(self):
        self.assertEqual(self.buildLicence._getLastEvent(), None)
        createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='A')
        ev2 = createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='B')
        event = self.buildLicence._getLastEvent()
        self.failUnless(event is not None)
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)

    def testGetLastDeposit(self):
        self.assertEqual(self.buildLicence.getLastDeposit(), None)
        createObject('UrbanEvent', 'dossier-incomplet', self.buildLicence, description='A')
        createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='B')
        ev3 = createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='C')
        event = self.buildLicence.getLastDeposit()
        self.assertEqual(event.Description(), 'C')
        self.assertEqual(event, ev3)

    def testGetAcknowledgement(self):
        self.assertEqual(self.buildLicence.getLastAcknowledgment(), None)
        createObject('UrbanEvent', 'dossier-incomplet', self.buildLicence, description='A')
        ev2 = createObject('UrbanEvent', 'accuse-de-reception', self.buildLicence, description='B')
        createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='C')
        event = self.buildLicence.getLastAcknowledgment()
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)
