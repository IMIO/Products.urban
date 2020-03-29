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


class IInspectionFollowUpTask(Interface):
    """ Marker interface for inspection followup events task."""


class ICreateFollowupTask(Interface):
    """ Marker interface for inspection followup events creation task."""


class IValidateFollowupTask(Interface):
    """ Marker interface for inspection followup events validation task."""


class ISendFollowupTask(Interface):
    """ Marker interface for inspection followup events send task."""


class ITaskToCheckDaily(Interface):
    """ Marker interface for tasks that shold be re-evaluated every night """


class ITaskCron(Interface):
    """A cron task"""

    def condition(self):
        """A condition for the execution of the cron task"""

    def execute(self):
        """The execution method of the cron"""


class ITaskWithSuspensionDelay(Interface):
    """ Task where the delay should be prorogated by the suspension period prorata"""


class ITaskWithWholeSuspensionDelay(Interface):
    """ Task where the delay should be prorogated by the whole suspension period """
