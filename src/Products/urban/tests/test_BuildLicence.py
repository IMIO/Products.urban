# -*- coding: utf-8 -*-
import unittest
from time import sleep
from zope.component import createObject
from plone.app.testing import login
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
        #we can add a 'demande-avis-swde' UrbanEvent if 'swde' is selected
        #in the list solicitOpinionsTo
        opinionsToSolicit = self.buildLicence.getSolicitOpinionsTo()
        extraOpinion = ('belgacom',)
        self.buildLicence.setSolicitOpinionsTo(opinionsToSolicit+extraOpinion)
        opinionRequest = createObject('UrbanEvent', 'demande-avis-belgacom', self.buildLicence)
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
