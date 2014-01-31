# -*- coding: utf-8 -*-

from Products.Archetypes.event import ObjectEditedEvent

from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

from z3c.table.interfaces import IValues

from zope import event
from zope.component import getMultiAdapter

import unittest


class TestScheduleView(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.urban = portal.urban
        self.portal_urban = portal.portal_urban

        login(portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.handleErrors = False

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def testi_schedule_view_display(self):
        """
         Tests schedule view is not broken
        """
        schedule_url = '{base_url}/schedule'.format(base_url=self.urban.absolute_url())
        self.browser.open(schedule_url)

    def test_UrbanEvent_foldermanager_index(self):
        """
         Since we have to filter results by foldermanager, the foldermanager of a licence
         will be indexed on all its urban event
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence = self.urban.buildlicences.objectValues()[-1]
        urban_event = licence.objectValues('UrbanEvent')[0]
        opinionrequest_event = licence.objectValues('UrbanEventOpinionRequest')[0]
        foldermanagers = self.portal_urban.foldermanagers
        foldermanager = foldermanagers.objectValues()[0]

        event_brain = catalog(UID=urban_event.UID())[0]
        self.assertTrue(foldermanager.UID() in event_brain.folder_manager)

        opinionevent_brain = catalog(UID=opinionrequest_event.UID())[0]
        self.assertTrue(foldermanager.UID() in opinionevent_brain.folder_manager)

    def test_UrbanEvent_foldermanager_reindex_when_updating_foldermanager_on_licence(self):
        """
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence = self.urban.buildlicences.objectValues()[-1]
        urban_event = licence.objectValues('UrbanEvent')[0]
        opinionrequest_event = licence.objectValues('UrbanEventOpinionRequest')[0]
        foldermanagers = self.portal_urban.foldermanagers
        new_foldermanager_id = foldermanagers.invokeFactory('FolderManager', id='fm_1')

        new_foldermanager = getattr(foldermanagers, new_foldermanager_id)

        licence.setFoldermanagers([new_foldermanager.UID()])
        event.notify(ObjectEditedEvent(licence))

        event_brain = catalog(UID=urban_event.UID())[0]
        self.assertTrue(new_foldermanager.UID() in event_brain.folder_manager)

        opinionevent_brain = catalog(UID=opinionrequest_event.UID())[0]
        self.assertTrue(new_foldermanager.UID() in opinionevent_brain.folder_manager)

    def test_EventType_schedulability_index(self):
        """
         Tests that once the deadlineDelay of an UrbanEventType is set > 0
         then the index 'last_key_event' is set to 'schedulable'.
         This index will be use to browse catalog for schedulable UrbanEventType.
        """
        catalog = api.portal.get_tool('portal_catalog')
        buildlicences_eventtypes = self.portal_urban.buildlicence.urbaneventtypes
        event_type = buildlicences_eventtypes.objectValues()[0]

        event_type.setDeadLineDelay(100)
        event_type.reindexObject()
        eventtype_brain = catalog(UID=event_type.UID())[0]

        self.assertTrue(eventtype_brain.last_key_event == 'schedulable')

        event_type.setDeadLineDelay(0)
        event_type.reindexObject()
        eventtype_brain = catalog(UID=event_type.UID())[0]

        self.assertTrue(eventtype_brain.last_key_event == '')

    def test_GetAllSchedulabeEventTypes(self):
        """
         This methods should return all the UrbanEventType with a deadlineDelay > 0
         of a licence config.
        """
        from Products.urban.browser.schedule.vocabulary import _getAllSchedulableEventTypes

        licence_config = self.portal_urban.buildlicence
        eventtypes_folder = licence_config.urbaneventtypes
        # lets be sure there's some UrbanEventType to configure ...
        self.assertTrue(len(licence_config.objectValues()) > 0)

        for event_type in eventtypes_folder.objectValues():
            event_type.setDeadLineDelay(0)
            event_type.reindexObject()

        self.assertTrue(len(_getAllSchedulableEventTypes(licence_config)) == 0)

        for event_type in eventtypes_folder.objectValues():
            event_type.setDeadLineDelay(42)
            event_type.reindexObject()

        self.assertTrue(len(_getAllSchedulableEventTypes(licence_config)) == len(eventtypes_folder.objectValues()))

    def test_findSchedulableUrbanEvents_results_schedulability(self):
        """
         Check that every event returned by findSchedulableUrbanEvents is schedulable
        """
        scheduleview = self.portal.restrictedTraverse('schedule')
        scheduleview.update()
        table = scheduleview.schedulelisting
        schedule_values = getMultiAdapter((self.portal, self.portal.REQUEST, table), IValues)

        licence_type = 'buildlicence'
        eventtype_uids = ['all']
        foldermanager = 'all'

        event_brains = schedule_values.findSchedulableUrbanEvents(licence_type, eventtype_uids, foldermanager)
        # we must have results..
        self.assertTrue(len(event_brains) > 0)

        for brain in event_brains:
            event = brain.getObject()
            eventtype = event.getUrbaneventtypes()

            # we check that the eventype of each returned event is 'schedulable'
            self.assertTrue(eventtype.getDeadLineDelay() > 0)

        # disable schedulability of every eventtype of buildlicence
        licence_config = self.portal_urban.buildlicence
        eventtypes_folder = licence_config.urbaneventtypes
        for event_type in eventtypes_folder.objectValues():
            event_type.setDeadLineDelay(0)
            event_type.reindexObject()

        event_brains = schedule_values.findSchedulableUrbanEvents(licence_type, eventtype_uids, foldermanager)
        # we shouldnt have any result anymore
        self.assertTrue(len(event_brains) == 0)
