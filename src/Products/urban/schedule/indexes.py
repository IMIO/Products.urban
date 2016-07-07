# -*- coding: utf-8 -*-

from imio.schedule.content.task import IAutomatedTask

from plone.indexer import indexer

from Products.urban.indexes import genericlicence_streetsuid
from Products.urban.indexes import genericlicence_streetnumber


@indexer(IAutomatedTask)
def licence_reference_index(task):
    """
    Index licence reference on their tasks to be able
    to query on it.
    """
    licence = task.get_container()
    reference = licence.getReference()
    return reference


@indexer(IAutomatedTask)
def licence_street_index(task):
    """
    Index licence street on their tasks to be able
    to query on it.
    """
    licence = task.get_container()
    street_UIDS = genericlicence_streetsuid(licence)
    return street_UIDS


@indexer(IAutomatedTask)
def licence_streetnumber_index(task):
    """
    Index licence street number on their tasks to be able
    to query on it.
    """
    licence = task.get_container()
    street_numbers = genericlicence_streetnumber(licence)
    return street_numbers
