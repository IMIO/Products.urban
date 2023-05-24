# -*- coding: utf-8 -*-

from imio.actionspanel.browser.comments import ConfirmTransitionView

from imio.schedule.config import STARTED
from imio.schedule.utils import get_task_configs


class UrbanConfirmTransitionView(ConfirmTransitionView):
    """
      This manage the overlay popup displayed when a transition needs to be confirmed.
      For other transitions, this views is also used but the confirmation popup is not shown.
    """

    def has_open_tasks(self):
        """
        Say wheter the object has open tasks (tasks)
        """
        return self.get_started_tasks()

    def get_created_tasks(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """
        tasks = []
        for task_config in get_task_configs(self.context):
            task = task_config.get_created_task(self.context)
            if not task:
                continue
            matched, not_matched = task.start_conditions_status()
            if not not_matched:
                continue
            tasks.append((task, not_matched))

        return tasks

    def get_started_tasks(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """
        tasks = []
        for task_config in get_task_configs(self.context):
            task = task_config.get_started_task(self.context)
            if not task:
                continue
            matched, not_matched = task.end_conditions_status()
            if not not_matched:
                continue

            subtasks_open = False
            for sub_task in task.get_subtasks():
                if sub_task.get_status() == STARTED:
                    subtasks_open = True
                    break
            if subtasks_open:
                continue

            tasks.append((task, not_matched))

        return tasks

    @property
    def actions_panel_view(self):
        view = self.context.restrictedTraverse("@@actions_panel")
        view.forceRedirectAfterTransition = True
        return view
