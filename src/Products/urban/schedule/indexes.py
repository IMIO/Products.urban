# -*- coding: utf-8 -*-

from imio.schedule.content.task import IAutomatedTask

from plone.indexer import indexer

from Products.urban.indexes import genericlicence_applicantinfoindex
from Products.urban.indexes import genericlicence_final_duedate
from Products.urban.indexes import genericlicence_foldermanager
from Products.urban.indexes import genericlicence_streetsuid
from Products.urban.indexes import genericlicence_streetnumber
from Products.urban.interfaces import IGenericLicence


def get_task_licence(task):
    """ """
    container = task.get_container()
    while not IGenericLicence.providedBy(container):
        container = container.aq_parent
    return container


@indexer(IAutomatedTask)
def licence_final_duedate(task):
    """
    Index licence reference on their tasks to be able
    to query on it.
    """
    licence = get_task_licence(task)
    due_date = genericlicence_final_duedate(licence)
    return due_date


@indexer(IAutomatedTask)
def licence_reference_index(task):
    """
    Index licence reference on their tasks to be able
    to query on it.
    """
    licence = get_task_licence(task)
    reference = licence.getReference()
    return reference


@indexer(IAutomatedTask)
def licence_street_index(task):
    """
    Index licence street on their tasks to be able
    to query on it.
    """
    licence = get_task_licence(task)
    street_UIDS = genericlicence_streetsuid(licence)
    return street_UIDS


@indexer(IAutomatedTask)
def licence_streetnumber_index(task):
    """
    Index licence street number on their tasks to be able
    to query on it.
    """
    licence = get_task_licence(task)
    street_numbers = genericlicence_streetnumber(licence)
    return street_numbers


@indexer(IAutomatedTask)
def licence_foldermanager_index(task):
    """
    Index licence folder_managers on their tasks to be able
    to query on it.
    """
    licence = get_task_licence(task)
    foldermanagers = genericlicence_foldermanager(licence)
    return foldermanagers


@indexer(IAutomatedTask)
def licence_applicant_index(task):
    """
    Index licence applicants on their tasks to be able
    to query on it.
    """
    licence = get_task_licence(task)
    applicants = genericlicence_applicantinfoindex(licence)
    return applicants
