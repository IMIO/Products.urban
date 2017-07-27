# -*- coding: utf-8 -*-

from imio.schedule.content.schedule_config import IScheduleConfig


def set_dashboard_columns(dashboard_collection, event):
    """
    """
    columns = (
        u'sortable_title',
        u'address_column',
        u'assigned_user_column',
        u'status',
        u'due_date',
        u'final_duedate',
        u'task_actions_column'
    )
    if IScheduleConfig.providedBy(dashboard_collection.aq_parent):
        columns = (
            u'sortable_title',
            u'pretty_link',
            u'address_column',
            u'assigned_user_column',
            u'status',
            u'due_date',
            u'final_duedate',
            u'task_actions_column'
        )
    dashboard_collection.setCustomViewFields(columns)
