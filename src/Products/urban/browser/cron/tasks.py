# -*- coding: utf-8 -*-

from imio.schedule.config import STARTED
from imio.schedule.config import states_by_status
from imio.schedule.content.task import IAutomatedTask
from plone import api

from Products.Five import BrowserView

from Products.urban.interfaces import ICollegeEvent
from Products.urban.schedule.interfaces import ITaskCron

from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TaskCronView(BrowserView):

    def __call__(self):
        for name, utility in getUtilitiesFor(ITaskCron):
            utility.run()


class UpdateCollegeEventDoneTasks(BrowserView):
    """
    Gather all in progress college events and check if the decision is
    done in plone meeting.
    """

    def __call__(self):
        """ """
        ws4pm = getMultiAdapter((api.portal.get(), self.request), name='ws4pmclient-settings')

        catalog = api.portal.get_tool('portal_catalog')

        college_events_brains = catalog(
            object_provides=ICollegeEvent.__identifier__,
            review_state='decision_in_progress'
        )
        for brain in college_events_brains:
            college_event = brain.getObject()
            items = ws4pm._soap_searchItems({'externalIdentifier': college_event.UID()})
            accepted_states = ['accepted', 'accepted_but_modified', 'accepted_and_returned']
            college_done = items and items[0]['review_state'] in accepted_states
            if college_done:
                # udpate tasks by simulating an ObjectModifiedEvent on the college urban event
                notify(ObjectModifiedEvent(college_event))


class UpdateOpenTasksLicences(BrowserView):
    """
    Update all licences with at least an open tasks.
    """
    def __call__(self):
        """ """
        catalog = api.portal.get_tool('portal_catalog')

        open_tasks_brains = catalog(
            object_provides=IAutomatedTask.__identifier__,
            review_state=states_by_status[STARTED]
        )
        licences = [t.getObject().get_container() for t in open_tasks_brains]
        for licence in licences:
            notify(ObjectModifiedEvent(licence))
