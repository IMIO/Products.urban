# -*- coding: utf-8 -*-

from urban.schedule.content.task import IAutomatedTask

from plone.indexer import indexer


@indexer(IAutomatedTask)
def licence_reference_index(task):
    """
    Index licence reference on their tasks to be able
    to query on it.
    """
    licence = task.get_container()
    reference = licence.getReference()
    return reference
