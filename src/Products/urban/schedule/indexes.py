# -*- coding: utf-8 -*-

from datetime import date

from imio.schedule.content.task import IAutomatedTask

from plone.indexer import indexer

from Products.urban.indexes import genericlicence_applicantinfoindex
from Products.urban.indexes import genericlicence_streetsuid
from Products.urban.indexes import genericlicence_streetnumber
from Products.urban.schedule.interfaces import ILicenceDeliveryTask


@indexer(IAutomatedTask)
def licence_final_duedate(task):
    """
    Index licence reference on their tasks to be able
    to query on it.
    """
    licence = task.get_container()
    tasks_to_check = [obj for obj in licence.objectValues() if IAutomatedTask.providedBy(obj)]

    while tasks_to_check:
        task = tasks_to_check.pop()
        if ILicenceDeliveryTask.providedBy(task):
            return task.due_date
        else:
            subtasks = task.get_subtasks()
            tasks_to_check.extend(subtasks)

    return date(9999, 1, 1)


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


@indexer(IAutomatedTask)
def licence_applicant_index(task):
    """
    Index licence applicants on their tasks to be able
    to query on it.
    """
    licence = task.get_container()
    applicants = genericlicence_applicantinfoindex(licence)
    return applicants
