# -*- coding: utf-8 -*-

from plone import api
from zope.container.contained import notifyContainerModified

import datetime
import logging
import re
import transaction


logger = logging.getLogger("Delete task")


PARAMETERS = [
    {
        "title": "DATE PASSAGE COLLEGE",
        "portal_type": "AutomatedMacroTask",
        "after_date": "2024-07-23",
        "licence_type": "codt_article127",
    },
    {
        "title": "ECHEANCE DU DOSSIER",
        "portal_type": "AutomatedMacroTask",
        "after_date": "2024-07-23",
        "licence_type": "codt_article127",
    },
]


def delete_tasks():
    for param in PARAMETERS:
        delete_task(**param)


def check_id_digit(id, keep):
    # If keep is 0 we keep nothing, everything is delelted
    if keep == 0:
        return False
    pattern = r"^TASK_.*-(?P<digit>\d+)$"
    match = re.match(pattern, id)
    if not match:
        # if not match, meaning no suffix digit, we keep at least one element so the first is keep
        return True
    digit = int(match.groupdict()["digit"])
    return digit < keep


def delete_task(title, portal_type, after_date, licence_type, keep=1):
    """
    Funciton used to delete tasks

    :param title: Title of the task
    :type title: string
    :param portal_type: portal_type of the task 'AutomatedMacroTask' or 'AutomatedTask'
    :type portal_type: string
    :param after_date: task created after the date will be deleted
    :type after_date: string
    :param licence_type: portal_type of the licence where to find
    :type licence_type: string
    :param keep: number of occurence of the task to keep, defaults to 1
    :type keep: int, optional
    """
    context = getattr(api.portal.get()["urban"], "{}s".format(licence_type.lower()))
    after_date = datetime.datetime.strptime(after_date, "%Y-%m-%d")
    brains = api.content.find(
        context=context,
        portal_type=portal_type,
        SearchableText=title,
        created={"query": after_date, "range": "min:"},
    )
    objects = {}
    for brain in brains:
        id = brain.getId
        if check_id_digit(id, keep):
            msg = "Task keeped: {}".format(id)
            logger.info(msg)
            continue
        path = brain.getPath()
        parent_path = "/".join(path.split("/")[:-1])
        if parent_path not in objects:
            objects[parent_path] = []
        objects[parent_path].append(id)

    catalog = api.portal.get_tool("portal_catalog")
    for path, ids in objects.items():
        obj = api.content.get(path=path)
        ids.sort()
        for id in ids:
            obj._delObject(id=id, suppress_events=True)
            catalog.uncatalog_object("{}/{}".format(path, id))
            msg = "Task deleted: {}/{}".format(path, id)
            logger.info(msg)
        notifyContainerModified(obj)
    transaction.commit()
