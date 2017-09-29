# -*- coding: utf-8 -*-


from plone import api

from imio.schedule.content.task_config import ITaskConfig
from imio.schedule.content.schedule_config import IScheduleConfig


def update_schedule_collections():
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(id='dashboard_collection', portal_type='DashboardCollection')

    for brain in brains:
        collection = brain.getObject()
        parent = collection.aq_parent

        if ITaskConfig.providedBy(parent) or IScheduleConfig.providedBy(parent):
            new_query = collection.query
            new_query[0] = dict(new_query[0])
            new_query[0]['v'] = parent.UID()
            collection.setQuery(new_query)
