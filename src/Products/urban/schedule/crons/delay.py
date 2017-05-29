# -*- coding: utf-8 -*-

from Products.urban.schedule.cron import TaskCron
from plone import api
from DateTime import DateTime


class AutoAccepted20days(TaskCron):

    def execute(self):
        for brain in self.brains:
            api.content.transition(
                obj=brain.getObject(),
                to_state='complete',
            )

    @property
    def brains(self):
        date_range = {
            'query': (DateTime() - 50, DateTime() - 20),
            'range': 'min:max'
        }
        return api.content.find(
            portal_type='CODT_BuildLicence',
            review_state='deposit',
            getDepositDate=date_range,
        )
