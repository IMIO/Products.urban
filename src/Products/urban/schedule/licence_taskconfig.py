# -*- coding: utf-8 -*-

from Products.urban.interfaces import IGenericLicence

from imio.schedule.content.task import ConfigurableMacroTask
from imio.schedule.content.task import ConfigurableTask


class BaseLicenceTask(object):
    """
    Base class for LicenceTask content types.
    """

    def get_licence(self):
        licence = self
        while not IGenericLicence.providedBy(licence):
            licence = licence.aq_parent
        return licence


class LicenceTask(ConfigurableTask, BaseLicenceTask):
    """
    Configurable task created on licences.
    """

    def get_evaluation_contexts(self):
        """
        Return additional objects and values to be passed to evaluate
        start and end condition of the task.
        """
        contexts = {"licence": self.get_licence()}
        return contexts


class LicenceMacroTask(ConfigurableMacroTask, BaseLicenceTask):
    """
    Configurable macro task created on licences.
    """

    def get_evaluation_contexts(self):
        """
        Return additional objects and values to be passed to evaluate
        start and end condition of the task.
        """
        contexts = {"licence": self.get_licence()}
        return contexts
