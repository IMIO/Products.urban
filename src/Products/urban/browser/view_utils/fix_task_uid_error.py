# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.urban.interfaces import IGenericLicence
from imio.schedule.content.task import IAutomatedTask
from imio.schedule.interfaces import TaskConfigNotFound
from imio.schedule.utils import get_container_tasks
from plone import api

import logging
import re
import transaction


logger = logging.getLogger("Fix task uid error: ")


class FixTaskUidError(BrowserView):
    """View used to fix wrong config uid attach to task."""

    template = ViewPageTemplateFile("templates/fix_task_uid_error.pt")

    def __call__(self):
        if not self.request.form.get("form.submitted", False):
            return self.template()

        self.fix_task()
        return self.template()

    def check_if_task_error(self, task):
        task_config = api.content.get(UID=task.task_config_UID)
        if not task_config or task.task_config_UID == "":
            return False
        return True

    def clear_task_id(self, task_id):
        task_id = task_id.replace("TASK_", "")
        task_id = re.sub("\d*$", "", task_id)
        task_id = task_id.rstrip("-")
        return task_id

    def get_task_id(self, task):
        task_id = []
        parent_task = aq_parent(task)
        if IAutomatedTask.providedBy(parent_task):
            task_id.append(self.clear_task_id(parent_task.id))
        task_id.append(self.clear_task_id(task.id))
        return "/".join(task_id)

    def get_tasks(self):
        tasks = []
        if IGenericLicence.providedBy(self.context):
            tasks += get_container_tasks(self.context)
        else:
            items = self.context.contentItems()
            len_items = len(items)
            for count, item in enumerate(items):
                id, child = item
                if IGenericLicence.providedBy(child):
                    logger.info(
                        "handle licence {} ({}/{})".format(id, count + 1, len_items)
                    )
                    tasks += get_container_tasks(child)
        task_in_error = {}
        for count, task in enumerate(tasks):
            logger.info("handle task {}/{}".format(count + 1, len(tasks)))
            if self.check_if_task_error(task):
                continue
            task_id = self.get_task_id(task)
            if task_id in task_in_error:
                task_in_error[task_id]["UIDs"].append(task.UID())
                continue
            logger.info("new task in error added : {}".format(task.id))
            task_in_error[task_id] = {
                "title": task.title,
                "UIDs": [task.UID()],
                "current_uid": task.task_config_UID,
            }

        return task_in_error

    def fix_task(self):
        form = self.request.form
        del form["form.submitted"]
        del form["submit"]
        for count, item in enumerate(form.items()):
            task, new_uid = item
            if new_uid == "":
                continue
            logger.info("Fix tasks ({}/{}):".format(count + 1, len(form.items())))
            task_uids = task.split("-")
            for count, task_uid in enumerate(task_uids):
                task_to_fix = api.content.get(UID=task_uid)
                logger.info(
                    "\tFixing task {} ({}/{})".format(
                        "/".join(task_to_fix.getPhysicalPath()),
                        count + 1,
                        len(task_uids),
                    )
                )
                task_to_fix.task_config_UID = new_uid
        transaction.commit()
