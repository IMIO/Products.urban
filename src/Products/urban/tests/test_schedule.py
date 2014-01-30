# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

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

    def test_UrbanEvent_foldermanager_indexing(self):
        """
         Since we have to filter results by foldermanager, the foldermanager of a licence
         will be indexed on all its urban event
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence = self.urban.buildlicences.objectValues()[-1]
        event = licence.objectValues('UrbanEvent')[0]
        opinionrequest_event = licence.objectValues('UrbanEventOpinionRequest')[0]
        foldermanagers = self.portal_urban.foldermanagers
        foldermanager = foldermanagers.objectValues()[0]

        event_brain = catalog(UID=event.UID())[0]
        self.assertTrue(foldermanager.UID() in event_brain.folder_manager)

        opinionevent_brain = catalog(UID=opinionrequest_event.UID())[0]
        self.assertTrue(foldermanager.UID() in opinionevent_brain.folder_manager)

    def test_UrbanEvent_foldermanager_reindexing_when_updating_foldermanager_on_licence(self):
        """
        """

    def test_EventType_schedulability_indexing(self):
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

    def testGetAllSchedulabeEventTypes(self):
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
            event_type.setDeadLineDelay(10)
            event_type.reindexObject()

        self.assertTrue(len(_getAllSchedulableEventTypes(licence_config)) == len(eventtypes_folder.objectValues()))
