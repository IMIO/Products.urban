# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.component import getUtilitiesFor

from Products.urban.schedule.interfaces import ITaskCron


class TaskCronView(BrowserView):

    def __call__(self):
        for name, utility in getUtilitiesFor(ITaskCron):
            utility.run()
