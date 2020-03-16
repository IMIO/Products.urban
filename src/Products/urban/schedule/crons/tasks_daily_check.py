# -*- coding: utf-8 -*-

from imio.schedule.config import states_by_status
from imio.schedule.config import STARTED

from Products.urban.schedule.cron import TaskCron
from plone import api

from Products.urban.schedule.interfaces import ITaskToCheckDaily

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class CheckTasks(TaskCron):

    def execute(self):
        catalog = api.portal.get_tool('portal_catalog')
        containers_already_checked = set()

        tasks_brains = catalog(
            object_provides=ITaskToCheckDaily.__identifier__,
            review_state=states_by_status[STARTED]
        )
        for brain in tasks_brains:
            task = brain.getObject()
            container = task.get_container()
            if container.id not in containers_already_checked:
                notify(ObjectModifiedEvent(container))
                containers_already_checked.add(container.id)
