# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.schedule.interfaces import ITaskCron

from zope.component import getUtilitiesFor


class TaskCronView(BrowserView):

    def __call__(self):
        for name, utility in getUtilitiesFor(ITaskCron):
            utility.run()
