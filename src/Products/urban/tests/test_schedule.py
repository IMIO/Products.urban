# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.Archetypes.event import ObjectEditedEvent

from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

from zope.event import notify

import unittest


class TestScheduleView(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.urban = portal.urban
        self.portal_urban = portal.portal_urban
        self.scheduleview = portal.restrictedTraverse('schedule')

        login(portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.handleErrors = False

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_schedule_view_display(self):
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
        notify(ObjectEditedEvent(licence))

        event_brain = catalog(UID=urban_event.UID())[0]
        self.assertTrue(new_foldermanager.UID() in event_brain.folder_manager)

        opinionevent_brain = catalog(UID=opinionrequest_event.UID())[0]
        self.assertTrue(new_foldermanager.UID() in opinionevent_brain.folder_manager)

    def test_UrbanEventType_has_attribute_deadLineDelay(self):
        catalog = api.portal.get_tool('portal_catalog')
        eventtype = catalog(portal_type='UrbanEventType')[0].getObject()
        self.assertTrue(hasattr(eventtype, 'deadLineDelay'))

    def test_UrbanEventType_has_attribute_alertDelay(self):
        catalog = api.portal.get_tool('portal_catalog')
        eventtype = catalog(portal_type='UrbanEventType')[0].getObject()
        self.assertTrue(hasattr(eventtype, 'alertDelay'))

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
         and that our result is complete.
        """
        scheduleview = self.scheduleview
        scheduleview.update()

        licence_type = 'buildlicence'
        eventtype_uids = ['all']
        foldermanager = 'all'

        event_brains = scheduleview.findSchedulableUrbanEvents(licence_type, eventtype_uids, foldermanager)
        events_found = [brain.getObject() for brain in event_brains]

        # check soundness and completeness
        for licence in self.urban.buildlicences.objectValues():
            for event in licence.objectValues(['UrbanEvent', 'UrbanEventOpinionRequest']):
                eventtype = event.getUrbaneventtypes()
                # completeness: each schedulable event MUST be in the result
                if eventtype.getDeadLineDelay() > 0:
                    self.assertTrue(event in events_found)
                # soundness: our result only includes correct results (schedulable events)
                else:
                    self.assertTrue(event not in events_found)

    def test_findSchedulableUrbanEvents_eventtype_filter(self):
        """
         Restrict the search to some eventtypes.
         Check that every event returned is of the given eventtype and that our result
         is complete.
        """
        scheduleview = self.scheduleview
        scheduleview.update()

        # restrict the search to only two types of events
        eventtypes_folder = self.portal_urban.buildlicence.urbaneventtypes
        eventtypes_restriction = eventtypes_folder.objectValues()[:2]

        eventtype_uids = [eventtype.UID() for eventtype in eventtypes_restriction]
        licence_type = 'buildlicence'
        foldermanager = 'all'

        # make sure to find at least one result
        licence = self.urban.buildlicences.objectValues()[0]
        licence.createUrbanEvent(eventtype_uids[0])

        event_brains = scheduleview.findSchedulableUrbanEvents(licence_type, eventtype_uids, foldermanager)
        events_found = [brain.getObject() for brain in event_brains]

        # check soundness and completeness
        for licence in self.urban.buildlicences.objectValues():
            for event in licence.objectValues(['UrbanEvent', 'UrbanEventOpinionRequest']):
                eventtype = event.getUrbaneventtypes()
                # completeness: each event with the desired type MUST be in the result
                if eventtype in eventtypes_restriction:
                    self.assertTrue(event in events_found)
                # soundness: our result only includes correct results
                else:
                    self.assertTrue(event not in events_found)

    def test_findSchedulableUrbanEvents_foldermanager_filter(self):
        """
         Restrict the search to a FolderManager.
         Check that every event returned is in a licence handled by the given foldermanager
         and that our result is complete.
        """
        scheduleview = self.scheduleview
        scheduleview.update()

        # restrict the search to a specific foldermanager
        foldermanager = self.portal_urban.foldermanagers.objectValues()[0]
        foldermanager_uid = foldermanager.UID()
        eventtype_uids = ['all']
        licence_type = 'buildlicence'

        # make sure to find at least one result
        licence = self.urban.buildlicences.objectValues()[-1]
        licence.setFoldermanagers(foldermanager_uid)
        notify(ObjectEditedEvent(licence))

        event_brains = scheduleview.findSchedulableUrbanEvents(licence_type, eventtype_uids, foldermanager_uid)
        events_found = [brain.getObject() for brain in event_brains]

        # check soundness and completeness
        for licence in self.urban.buildlicences.objectValues():
            for event in licence.objectValues(['UrbanEvent', 'UrbanEventOpinionRequest']):
                eventtype = event.getUrbaneventtypes()
                schedulable = eventtype.getDeadLineDelay() > 0
                # completeness: each schedulabe event in a licence with the desired foldermanager MUST be in the results
                if schedulable and foldermanager in licence.getFoldermanagers():
                    self.assertTrue(event in events_found)
                # soundness: our result only includes correct results
                else:
                    self.assertTrue(event not in events_found)

    def test_default_resuts_ordered_by_lateness(self):
        """ By default events should be sorted by delay lateness """

        scheduleview = self.scheduleview
        scheduleview.update()
        table = scheduleview.schedulelisting
        results = table.values

        delays = [result.delay for result in results]
        delays.reverse()

        # we need events with different deadlines to be sure the list is sorted correctly
        self.assertTrue(len(delays) > 4 and delays[0] != delays[-1])

        self.assertTrue(delays == sorted(delays))

    def test_no_default_result_displayed_when_current_user_is_not_urban_foldermanager(self):
        """
         The default results should be the licences of of the current user.
         If the current user is not an urban foldermanager, no result should be displayed
        """
        login(self.portal, 'urbaneditor')
        self.browserLogin('urbaneditor')

        scheduleview = self.scheduleview
        scheduleview.update()
        table = scheduleview.schedulelisting
        results = table.values

        self.assertTrue(len(results) == 0)

    def test_licences_in_default_result_only_belongs_to_current_foldermanager(self):
        """
         The licences listed in the default result should always belongs to the
         current urban foldermanager
        """
        from Products.urban.utils import getCurrentFolderManager

        scheduleview = self.scheduleview
        scheduleview.update()
        table = scheduleview.schedulelisting

        results = table.values
        current_foldermanager = getCurrentFolderManager()

        # we need results to be be able to prove our statement..
        self.assertTrue(len(results) > 0)

        for result in results:
            licence = result.licence.getObject()
            licence_foldermanagers = licence.getFoldermanagers()
            self.assertTrue(current_foldermanager in licence_foldermanagers)

    def test_UrbanEventType_has_attribute_delayComputation(self):
        catalog = api.portal.get_tool('portal_catalog')
        eventtype = catalog(portal_type='UrbanEventType')[0].getObject()
        self.assertTrue(hasattr(eventtype, 'delayComputation'))

    def test_default_delay_computation(self):
        """ Test the delay and the deadline date to display are computed correctly. """

        scheduleview = self.scheduleview
        scheduleview.update()
        table = scheduleview.schedulelisting
        results = table.values

        # make sure we have computation delays to verify
        self.assertTrue(len(results) > 0)

        for result in results:
            event = result.event
            eventtype = event.getUrbaneventtypes()
            event_date = event.getEventDate()
            deadline_delay = eventtype.getDeadLineDelay()
            expected_delay = int(DateTime() - (deadline_delay + event_date))
            expected_delayterm = event_date + deadline_delay

            self.assertTrue(result.delay == expected_delay)
            self.assertTrue(result.delay_term == expected_delayterm)

    def test_custom_delay_computation(self):
        """
         Test the delay and the deadline date to display are computed correctly
         when using the custom delay computation on an UrbanEventType.
        """
        scheduleview = self.scheduleview
        scheduleview.update()
        table = scheduleview.schedulelisting
        result = table.values[0]
        event = result.event
        eventtype = event.getUrbaneventtypes()

        # Set the delayComputation to a correct TAL expression.
        TAL_computation = 'python: event.getEventDate() + 4242'
        eventtype.setDelayComputation(TAL_computation)
        event_date = event.getEventDate()
        expected_delay = int(DateTime() - (4242 + event_date))

        scheduleview.update()
        # with 4242 days allowed to complete the event, it should be the last
        # in the schedule result list ;-)
        result = table.values[-1]

        self.assertTrue(result.delay == expected_delay)

    def test_custom_delay_computation_with_wrong_TAL_expression(self):
        """
         If the tal expression to compute delay is incorrect, delay should be
         infinite (9999).
        """
        scheduleview = self.scheduleview
        scheduleview.update()
        table = scheduleview.schedulelisting
        result = table.values[0]
        event = result.event
        eventtype = event.getUrbaneventtypes()

        # set the delayComputation with a wrong TAL expression
        TAL_computation = 'trololo'
        eventtype.setDelayComputation(TAL_computation)
        expected_delay = 999999

        scheduleview.update()
        result = table.values[0]

        self.assertTrue(result.delay == expected_delay)
