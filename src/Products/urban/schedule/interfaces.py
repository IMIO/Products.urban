# -*- coding: utf-8 -*-

from zope.interface import Interface


class ILicenceDeliveryTask(Interface):
    """ Marker interface for the licence delivery task. """


class ICreateOpinionRequestsTask(Interface):
    """ Marker interface for opinion requests creation task."""


class ISendOpinionRequestsTask(Interface):
    """ Marker interface for opinion requests sending task."""


class IReceiveOpinionRequestsTask(Interface):
    """ Marker interface for opinion requests reception task."""


class ITaskToCheckDaily(Interface):
    """ Marker interface for tasks that shold be revevaluated every night """


class ITaskCron(Interface):
    """A cron task"""

    def condition(self):
        """A condition for the execution of the cron task"""

    def execute(self):
        """The execution method of the cron"""
