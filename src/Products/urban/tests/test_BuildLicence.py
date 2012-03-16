# -*- coding: utf-8 -*-
import unittest
from time import sleep
from DateTime import DateTime
from zope.component import createObject
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestBuildLicence(unittest.TestCase):

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

    def testKeyEventDefaultCase(self):
        portal = self.layer['portal']
        portal.urban.buildlicences.manage_delObjects('licence1')
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        #so far the index should still be empty
        self.assertEqual(buildlicence_brain.last_key_event, None)


    def testNoKeyEventCreated(self):
        portal = self.layer['portal']
        portal.urban.buildlicences.manage_delObjects('licence1')
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event_type = urban_event.getUrbaneventtypes()
        #we delete the urban event from the buildlicence and set the urbanEventType UET as a key event
        #the index should remains empty as the licence does not contains an urbanEvent UET
        buildlicence.manage_delObjects(urban_event.id)
        urban_event_type.setIsKeyEvent(True)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event, None)

    def testCreateKeyEvent(self):
        portal = self.layer['portal']
        portal.urban.buildlicences.manage_delObjects('licence1')
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event_type = urban_event.getUrbaneventtypes()
        #we delete the urban event from the buildlicence and set the urbanEventType UET as a key event
        buildlicence.manage_delObjects(urban_event.id)
        urban_event_type.setIsKeyEvent(True)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        #we add an urbanEvent of type UET, the index last_key_event of the licence should be updated
        self.portal_urban.createUrbanEvent(buildlicence.UID(), urban_event_type.UID())
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type.Title())

    def testDeleteKeyEvent(self):
        portal = self.layer['portal']
        portal.urban.buildlicences.manage_delObjects('licence1')
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event_type = urban_event.getUrbaneventtypes()
        urban_event_type.setIsKeyEvent(True)
        #we remove the key event, the index last_key_event of the licence should be back to empty value
        buildlicence.manage_delObjects(urban_event.id)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event, None)

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
        sleep(1)
        event = self.buildLicence._getLastEvent()
        self.failUnless(event is not None)
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)

    def testGetAllOpinionRequests(self):
        self.assertEqual(self.buildLicence.getAllOpinionRequests(), [])

        # create opinion request
        opinions = ('belgacom', )
        self.buildLicence.setInvestigationStart(DateTime('01/01/2011'))
        self.buildLicence.setSolicitOpinionsTo(opinions)
        opinionRequest = createObject('UrbanEvent',
                'belgacom-opinion-request', self.buildLicence)

        self.assertEqual(self.buildLicence.getAllOpinionRequests(), [opinionRequest])

    def testGetLastDeposit(self):
        self.assertEqual(self.buildLicence.getLastDeposit(), None)
        createObject('UrbanEvent', 'dossier-incomplet', self.buildLicence, description='A')
        sleep(1)
        createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='B')
        sleep(1)
        ev3 = createObject('UrbanEvent', 'depot-de-la-demande', self.buildLicence, description='C')
        sleep(1)
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

    def testGetCurrentFolderManager(self):
        #1 link login on treatment agent
        at = getattr(self.portal_urban.buildlicence.foldermanagers,'foldermanager1')
        at.setPloneUserId('urbaneditor')
        #2 create an empty buildlicence
        LICENCE_ID = 'licence2'
        self.buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence2 = getattr(self.buildLicences, LICENCE_ID)
        buildLicence2.setFoldermanagers(self.portal_urban.getCurrentFolderManager(buildLicence2,initials=False))
        #3 check if agent treatment exist
        self.assertEqual(buildLicence2.getFoldermanagers()[0].getPloneUserId(),'urbaneditor')
        at.setPloneUserId('urbanreader')
        LICENCE_ID = 'licence3'
        self.buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence3 = getattr(self.buildLicences, LICENCE_ID)
        buildLicence3.setFoldermanagers(self.portal_urban.getCurrentFolderManager(buildLicence3,initials=False))
        self.assertEqual(len(buildLicence3.getFoldermanagers()),0)

    def testGetAllAdvicesWithoutOpinionRequest(self):
        self.assertEqual(self.buildLicence.getAllAdvices(), [])

    def testGetAllAdvicesWithOpinionRequest(self):
        self.buildLicence.setInvestigationStart(DateTime('01/01/2011'))
        opinions = ('belgacom',)
        self.buildLicence.setSolicitOpinionsTo(opinions)
        self.assertEqual(len(self.buildLicence.getAllAdvices()), 1)

    def testCreateAllAdvicesWithoutOpinionRequest(self):
        self.buildLicence.createAllAdvices()
        self.assertEqual(self.buildLicence.getAllOpinionRequests(), [])

    def testCreateAllAdvicesWithOpinionRequest(self):
        self.buildLicence.setInvestigationStart(DateTime('01/01/2011'))
        opinions = ('belgacom',)
        self.buildLicence.setSolicitOpinionsTo(opinions)
        self.buildLicence.createAllAdvices()
        self.assertEqual(len(self.buildLicence.getAllOpinionRequests()), 1)
