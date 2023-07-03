# -*- coding: utf-8 -*-

from imio.schedule.content.schedule_config import IScheduleConfig
from imio.schedule.content.task_config import ITaskConfig


def set_dashboard_columns(dashboard_collection, event):
    """
    """
    if ITaskConfig.providedBy(dashboard_collection.aq_parent):
        columns = (
            u'sortable_title',
            u'address_column',
            u'assigned_user',
            u'status',
            u'due_date',
            u'licence_final_duedate',
            u'task_actions_column'
        )
    elif IScheduleConfig.providedBy(dashboard_collection.aq_parent):
        columns = (
            u'sortable_title',
            u'pretty_link',
            u'address_column',
            u'assigned_user',
            u'status',
            u'due_date',
            u'licence_final_duedate',
            u'task_actions_column'
        )
    else:
        return

    dashboard_collection.setCustomViewFields(columns)
