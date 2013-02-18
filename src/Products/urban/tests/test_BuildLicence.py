# -*- coding: utf-8 -*-
import unittest
from time import sleep
from DateTime import DateTime
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues()[0]
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def testGetLastEventWithoutEvent(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        self.assertEqual(buildlicence._getLastEvent(), None)

    def testGetLastEventWithOneEvent(self):
        buildlicence = self.buildlicence
        createdEvent = createObject('UrbanEvent', 'depot-de-la-demande', buildlicence)
        event = buildlicence._getLastEvent()
        self.assertEqual(createdEvent, event)
        self.failUnless(event is not None)

    def testGetLastEventWithMoreThanOneEvent(self):
        buildlicence = self.buildlicence
        createObject('UrbanEvent', 'depot-de-la-demande', buildlicence, description='A')
        ev2 = createObject('UrbanEvent', 'depot-de-la-demande', buildlicence, description='B')
        sleep(1)
        event = buildlicence._getLastEvent()
        self.failUnless(event is not None)
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)

    def testGetAllOpinionRequests(self):
        buildlicence = self.buildlicence
        opinions = buildlicence.objectValues('UrbanEventOpinionRequest')
        self.assertEqual(buildlicence.getAllOpinionRequests(), opinions)

    def testGetLastDeposit(self):
        buildlicence = self.buildlicence
        createObject('UrbanEvent', 'dossier-incomplet', buildlicence, description='A')
        sleep(1)
        createObject('UrbanEvent', 'depot-de-la-demande', buildlicence, description='B')
        sleep(1)
        ev3 = createObject('UrbanEvent', 'depot-de-la-demande', buildlicence, description='C')
        sleep(1)
        event = buildlicence.getLastDeposit()
        self.assertEqual(event.Description(), 'C')
        self.assertEqual(event, ev3)

    def testGetAcknowledgement(self):
        buildlicence = self.buildlicence
        createObject('UrbanEvent', 'dossier-incomplet', buildlicence, description='A')
        ev2 = createObject('UrbanEvent', 'accuse-de-reception', buildlicence, description='B')
        createObject('UrbanEvent', 'depot-de-la-demande', buildlicence, description='C')
        event = buildlicence.getLastAcknowledgment()
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)

    def testGetCurrentFolderManager(self):
        buildlicences = self.portal.urban.buildlicences
        #1 link login on treatment agent
        at = getattr(self.portal_urban.buildlicence.foldermanagers, 'foldermanager1')
        at.setPloneUserId('urbaneditor')
        #2 create an empty buildlicence
        LICENCE_ID = 'licence2'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence2 = getattr(buildlicences, LICENCE_ID)
        buildLicence2.setFoldermanagers(self.portal_urban.getCurrentFolderManager(initials=False))
        #3 check if agent treatment exist
        self.assertEqual(buildLicence2.getFoldermanagers()[0].getPloneUserId(), 'urbaneditor')
        at.setPloneUserId('urbanreader')
        LICENCE_ID = 'licence3'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence3 = getattr(buildlicences, LICENCE_ID)
        buildLicence3.setFoldermanagers(self.portal_urban.getCurrentFolderManager(initials=False))
        self.assertEqual(len(buildLicence3.getFoldermanagers()), 0)

    def testGetAllAdvicesWithoutOpinionRequest(self):
        buildlicence = self.buildlicence
        self.assertEqual(buildlicence.getAllAdvices(), [])

    def testGetAllAdvicesWithOpinionRequest(self):
        buildlicence = self.buildlicence
        opinions = ('sncb', 'belgacom')
        buildlicence.setSolicitOpinionsTo(opinions)
        # == 1 because the opinion request event of belgacom already exists
        self.assertEqual(len(buildlicence.getAllAdvices()), 1)

    def testCreateAllAdvicesWithoutOpinionRequest(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        buildlicence.createAllAdvices()
        self.assertEqual(buildlicence.getAllOpinionRequests(), [])

    def testCreateAllAdvicesWithOpinionRequest(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        #set opinion request to 'belgacom' and 'sncb'
        startDate = DateTime('01/01/2011')
        opinions = ('sncb', 'belgacom')
        buildlicence.setSolicitOpinionsTo(opinions)
        buildlicence.setInvestigationStart(startDate)
        buildlicence.createAllAdvices()
        self.assertEqual(len(buildlicence.getAllOpinionRequests()), 2)
