# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api

import logging
import time
import transaction

logger = logging.getLogger("urban: reindex event dates:")


def check_brain(catalog, brain, indexes):
    """Verify possible indexes that need to be reindexed because empty"""
    obj_rid = catalog.getrid(brain.getPath())
    indexed_values = catalog.getIndexDataForRID(obj_rid)
    missing_indexes = []
    for index_name in indexes:
        if index_name in indexed_values:
            if indexed_values[index_name] == "":
                missing_indexes.append(index_name)
    return missing_indexes


def reindex_brain(brain, indexes):
    brain.getObject().reindexObject(idxs=indexes)


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


def reindex_event_dates():
    """Reindex all objects only during non working hours for all
    event date related indexes"""
    catalog = api.portal.get_tool("portal_catalog")
    index = 0
    modified = 0
    indexes = (
        "getDecisionDate",
        "getDepositDate",
        "getRecourseDecisionDisplayDate",
        "getValidityDate",
        "investigationStart",
        "investigationEnd",
    )
    for brain in get_brains():
        while check_working_hours(datetime.now()) is False:
            time.sleep(60)
            logger.info("Not during working hour")
        index += 1
        to_reindex = check_brain(catalog, brain, indexes)
        if to_reindex:
            modified += 1
            reindex_brain(brain, to_reindex)
            if modified % 1000 == 0:
                logger.info("Commit {0} objects modified".format(modified))
                transaction.commit()
        if index % 1000 == 0:
            logger.info("{0} objects analyzed".format(index))