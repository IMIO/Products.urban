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

import transaction

COMMIT_INTERVAL = 100

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
        ws4pm = getMultiAdapter(
            (api.portal.get(), self.request), name="ws4pmclient-settings"
        )

        catalog = api.portal.get_tool("portal_catalog")

        college_events_brains = catalog(
            object_provides=ICollegeEvent.__identifier__,
            review_state="decision_in_progress",
        )
        for brain in college_events_brains:
            college_event = brain.getObject()
            items = ws4pm._soap_searchItems({"externalIdentifier": college_event.UID()})
            accepted_states = [
                "accepted",
                "accepted_but_modified",
                "accepted_and_returned",
            ]
            college_done = items and items[0]["review_state"] in accepted_states
            if college_done:
                # udpate tasks by simulating an ObjectModifiedEvent on the college urban event
                notify(ObjectModifiedEvent(college_event))


class UpdateOpenTasksLicences(BrowserView):
    """
    Update all licences with at least an open tasks.
    """

    def __call__(self):
        """ """
        catalog = api.portal.get_tool("portal_catalog")
        known_parents = []

        open_tasks_brains = catalog(
            object_provides=IAutomatedTask.__identifier__,
            review_state=states_by_status[STARTED],
        )
        licences = list(set([t.getObject().get_container() for t in open_tasks_brains]))
        filtered_licences = []
        for licence in licences:
            if (
                len(
                    [e for e in licence.getUrbanEvents() if ICollegeEvent.providedBy(e)]
                )
                > 0
            ):
                filtered_licences.append(licence)
        from Products.urban import logger

        # from imio.schedule.utils import get_task_configs
        for count, licence in enumerate(filtered_licences):
            logger.info("UpdateOpenTasksLicences: %s" % str(licence.absolute_url()))
            logger.info(
                "getHasModifiedBlueprints: %s"
                % str(
                    hasattr(licence, "getHasModifiedBlueprints")
                    and licence.getHasModifiedBlueprints()
                )
            )
            logger.info(
                "getLastAcknowledgment: %s"
                % str(
                    hasattr(licence, "getLastAcknowledgment")
                    and (
                        licence.getLastAcknowledgment()
                        and licence.getLastAcknowledgment()
                        or "None"
                    )
                )
            )
            notify(ObjectModifiedEvent(licence))
            licence.reindexObject()
            if count % COMMIT_INTERVAL == 0:
                transaction.commit()
            # task_configs = licence.portal_type != 'CODT_BuildLicence' and get_task_configs(licence) or []
            # for config in task_configs:
            # task = config.get_open_task(licence)
            # if task:
            # task.due_date = config.compute_due_date(licence, task)
            # task.reindexObject(idxs=('due_date',))
            # if licence.id == "codt_buildlicence.2022-07-12.3145384997":
            #    notify(ObjectModifiedEvent(licence))
            #    licence.reindexObject()
