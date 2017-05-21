# -*- coding: utf-8 -*-

from zope.interface import implementer

from Products.urban.schedule.interfaces import ITaskCron


@implementer(ITaskCron)
class TaskCron(object):
    """
    A task cron that will be executed automatically every x minutes

    Features:
    - A condition can be defined and will be verified before the execution
      of the of the cron
    """

    def condition(self):
        """Can be overrided by your cron task"""
        return True

    def execute(self):
        raise NotImplementedError

    def run(self):
        """
        Main function of the cron task that will be called by the cron view
        """
        if self.condition is False:
            return
        self.execute()
