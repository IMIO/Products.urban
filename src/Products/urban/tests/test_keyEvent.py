# -*- coding: utf-8 -*-
import unittest
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent import ObjectRemovedEvent
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_LICENCES


class TestKeyEvent(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def testCreateKeyEvent(self):
        portal = self.layer['portal']
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
        buildlicence.createUrbanEvent(urban_event_type.UID())
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        event = ObjectModifiedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type.Title())

    def testDeleteKeyEvent(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        old_index_value = catalog(portal_type='BuildLicence')[0].last_key_event
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event_type = urban_event.getUrbaneventtypes()
        urban_event_type.setIsKeyEvent(True)
        #we remove the key event, the index last_key_event of the licence should be back to its original value
        buildlicence.manage_delObjects(urban_event.id)
        event = ObjectRemovedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event, old_index_value)

    def testEventDateAsKeyDate(self):
        """
        test the method that returns all the key dates found on created urbanEvents
        these dates appears on the licence summary tab
        """
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
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
        catalog = getToolByName(portal, 'portal_catalog')
        buildlicence = catalog(portal_type='BuildLicence')[0].getObject()
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event.setDecisionDate('18/09/1986')
        urban_event_type = urban_event.getUrbaneventtypes()
        urban_event_type.setIsKeyEvent(True)
        urban_event_type.setKeyDates(('decisionDate',))
        view = buildlicence.restrictedTraverse('@@buildlicenceview')
        dates = view.getKeyDates()
        self.assertEqual(dates[-1]['date'], 'Sep 18, 1986')
        self.failUnless(urban_event.Title().decode('utf8') in dates[-1]['label'])
