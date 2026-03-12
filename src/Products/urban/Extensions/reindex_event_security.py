# -*- coding: utf-8 -*-

from Products.urban.migration.utils import refresh_object_workflow_permissions
from datetime import datetime
from plone import api

import logging
import time
import transaction

logger = logging.getLogger("urban: reindex event security:")


def get_brains():
    for brain in api.content.find(
        object_provides=["Products.urban.interfaces.IGenericLicence"],
        sort_on="modified",
        sort_order="ascending",
    ):
        yield brain


def check_working_hours(date):
    if date.date().isoweekday() in (6, 7):
        return True
    if date.hour >= 17:
        return True
    if date.hour < 7:
        return True
    return False


def get_workflow(portal_type):
    portal_workflow = api.portal.get_tool("portal_workflow")
    workflows = dict(portal_workflow._chains_by_type)
    return workflows[portal_type][0]


def reindex_event_security(max_counter=20000, working_hour=False):
    """Reindex all objects only during non working hours for all
    event date related indexes"""
    logger.info("Start reindexing event security")
    workflow_mapping = {}
    index = 0
    for brain in get_brains():
        if working_hour is False:
            while check_working_hours(datetime.now()) is False:
                time.sleep(60)
                logger.info("Not during working hour")
        index += 1
        licence = brain.getObject()
        events = licence.getAllEvents()
        for event in events:
            portal_type = event.portal_type
            if portal_type not in workflow_mapping:
                workflow_mapping[portal_type] = get_workflow(portal_type)
            refresh_object_workflow_permissions(event, workflow_mapping[portal_type])
        if index % 1000 == 0:
            transaction.commit()
            logger.info("Commit {0} objects modified".format(index))
        if index >= max_counter:
            logger.info("Stop indexing as we reach {0} elements".format(index))
            break
    logger.info("End of reindexing event security")


def reindex_event_security_working_hour(max_counter=20000):
    """Reindex all objects only during non working hours for all
    event date related indexes"""
    reindex_event_security(max_counter=max_counter, working_hour=True)


def reindex_current_event_security():
    portal = api.portal.get()
    request = portal.REQUEST
    context = request["PARENTS"][0]
    logger.info(
        "Start reindexing event security on {0}".format(context.absolute_url())
    )
    events = context.getAllEvents()
    for event in events:
        portal_type = event.portal_type
        workflow = get_workflow(portal_type)
        refresh_object_workflow_permissions(event, workflow)
    logger.info("End of reindexing event security")