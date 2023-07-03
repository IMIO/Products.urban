# -*- coding: utf-8 -*-

from collective.faceted.task.browser.task_table_view import FacetedTaskTableView


class UrbanTaskTableView(FacetedTaskTableView):
    """
    """

    ignoreColumnWeight = True

    def _getViewFields(self):
        """Returns fields we want to show in the table."""

        col_names = [
            u'simple_status',
            u'path',
            u'assigned_user',
            u'due_date',
            u'task_actions_column',
        ]

        return col_names
