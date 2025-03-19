# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from imio.schedule.interfaces import TaskConfigNotFound
from imio.schedule.utils import get_container_tasks
from plone import api

import logging
import transaction


logger = logging.getLogger("Fix task uid error")


def check_if_task_error(task):
    try:
        task.get_task_config()
    except TaskConfigNotFound:
        return True
    return False


class FixTaskUidError(BrowserView):
    """View used to fix wrong config uid attach to task."""

    template = ViewPageTemplateFile("templates/fix_task_uid_error.pt")

    def __call__(self):
        if not self.request.form.get("form.submitted", False):
            return self.template()

        self.fix_task()
        return self.template()

    def get_tasks(self):
        tasks = get_container_tasks(self.context)
        task_in_error = [task for task in tasks if check_if_task_error(task)]
        return task_in_error

    def fix_task(self):
        form = self.request.form
        del form["form.submitted"]
        del form["submit"]
        for task, new_uid in form.items():
            task_uid = task.split("-")[0]
            task_to_fix = api.content.get(UID=task_uid)
            task_to_fix.task_config_UID = new_uid
        transaction.commit()
