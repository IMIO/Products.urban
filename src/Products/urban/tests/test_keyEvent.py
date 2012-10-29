# -*- coding: utf-8 -*-
import unittest
from time import sleep
from DateTime import DateTime
from zope.component import createObject
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestKeyEvent(unittest.TestCase):

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
        self.failUnless(not buildlicence_brain.last_key_event.endswith('vrance du permis (octroi ou refus)' )

    def testEventDateAsKeyDate(self):
        """
        test the method that returns all the key dates found on created urbanEvents
        these dates appears on the licence summary tab
        """
        portal = self.layer['portal']
        portal.urban.buildlicences.manage_delObjects('licence1')
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event.setEventDate('18/09/1986')
        urban_event_type = urban_event.getUrbaneventtypes()
        urban_event_type.setIsKeyEvent(True)
        urban_event_type.setKeyDates(('eventDate',))
        view = buildlicence.restrictedTraverse('@@buildlicenceview')
        dates = view.getKeyDates()
        self.assertEqual(dates[-1]['date'], 'Sep 18, 1986')
        self.assertEqual(dates[-1]['label'], urban_event.Title())

    def testOptionalDateAsKeyDate(self):
        """
        test the method that returns all the key dates found on created urbanEvents
        these dates appears on the licence summary tab
        """
        portal = self.layer['portal']
        portal.urban.buildlicences.manage_delObjects('licence1')
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event.setDecisionDate('18/09/1986')
        urban_event_type = urban_event.getUrbaneventtypes()
        urban_event_type.setIsKeyEvent(True)
        urban_event_type.setKeyDates(('decisionDate',))
        view = buildlicence.restrictedTraverse('@@buildlicenceview')
        dates = view.getKeyDates()
        self.assertEqual(dates[-1]['date'], 'Sep 18, 1986')
        self.failUnless(urban_event.Title().decode('utf8') in dates[-1]['label'])
