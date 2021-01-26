# -*- coding: utf-8 -*-
#
# File: Contact.py
#
# Copyright (c) 2010 by CommunesPlone
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>,
Stephan GEULETTE <stephan.geulette@uvcw.be>,
Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from datetime import date

from imio.schedule.content.task import IAutomatedTask

from Products.Archetypes.interfaces import IBaseFolder

from Products.urban.interfaces import IApplicant
from Products.urban.interfaces import IBaseBuildLicence
from Products.urban.interfaces import ICODT_BaseBuildLicence
from Products.urban.interfaces import ICorporation
from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IInspection
from Products.urban.interfaces import IIsArchive
from Products.urban.interfaces import IMiscDemand
from Products.urban.interfaces import IPatrimonyCertificate
from Products.urban.interfaces import IProprietary
from Products.urban.interfaces import ITicket
from Products.urban.interfaces import IUrbanDoc
from Products.urban.interfaces import IUrbanEvent
from Products.urban.schedule.interfaces import ILicenceDeliveryTask
from Products.urban.utils import get_ws_meetingitem_infos

from plone import api
from plone.indexer import indexer

from suds import WebFault

from zope.component import queryAdapter


@indexer(IApplicant)
def applicant_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    return _get_applicantsinfoindex(object)


@indexer(IGenericLicence)
def genericlicence_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    contacts_info = []
    contacts = object.getApplicants() + object.getProprietaries()
    for contact in contacts:
        contacts_info.extend(_get_applicantsinfoindex(contact))
    return list(set(contacts_info))


@indexer(IEnvironmentLicence)
def environmentlicence_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    applicants_info = []
    for applicant in object.getApplicants():
        applicants_info.extend(_get_applicantsinfoindex(applicant))
    return list(set(applicants_info))


@indexer(IInspection)
@indexer(ITicket)
def inspection_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    applicants_info = []
    contacts = object.getApplicants() + object.getProprietaries() \
               + object.getPlaintiffs() + object.getTenants()
    for applicant in contacts:
        applicants_info.extend(_get_applicantsinfoindex(applicant))
    return list(set(applicants_info))


def _get_applicantsinfoindex(applicant):
    applicants_info = [
        applicant.getName1(),
        applicant.getName2(),
        applicant.getSociety(),
        applicant.getNationalRegister(),
    ]
    if hasattr(applicant, 'getDenomination'):
        applicants_info.append(applicant.getDenomination())
    if hasattr(applicant, 'getBceNumber'):
        applicants_info.append(applicant.getBceNumber())
    return [info for info in applicants_info if info]


@indexer(IBaseBuildLicence)
@indexer(ICODT_BaseBuildLicence)
@indexer(IMiscDemand)
@indexer(IPatrimonyCertificate)
def licence_architectinfoindex(object):
    """
    Return the informations to index about the architects
    """
    architects_info = []
    architects = object.getArchitects()
    for architect in architects:
        architects_info.extend(_get_applicantsinfoindex(architect))
    return list(set(architects_info))


@indexer(IGenericLicence)
def genericlicence_parcelinfoindex(obj):
    parcels_infos = []
    if hasattr(obj, 'getParcels'):
        parcels_infos = list(set([p.get_capakey() for p in obj.getParcels()]))
    return parcels_infos


@indexer(IGenericLicence)
def genericlicence_modified(licence):
    wf_modification = licence.workflow_history[licence.workflow_history.keys()[0]][-1]['time']
    if wf_modification > licence.modified():
        return wf_modification
    return licence.modified()


@indexer(IGenericLicence)
def genericlicence_streetsuid(licence):
    streets = [location['street'] for location in licence.getWorkLocations()]
    return streets


@indexer(IGenericLicence)
def genericlicence_streetnumber(licence):
    numbers = [location['number'] or '0' for location in licence.getWorkLocations()] or ['0']
    return numbers


@indexer(IGenericLicence)
def genericlicence_address(licence):
    return licence.getStreetAndNumber()


@indexer(IGenericLicence)
def genericlicence_lastkeyevent(object):
    for event in reversed(object.getUrbanEvents()):
        event_type = event.getUrbaneventtypes()
        if event_type.getIsKeyEvent() and event.getEventDate().year() >= 1900:
            return "%s,  %s" % (event.getEventDate().strftime("%d/%m/%y"), event_type.Title())


@indexer(IGenericLicence)
def genericlicence_foldermanager(object):
    return [foldermanager.UID() for foldermanager in object.getFoldermanagers()]


@indexer(IUrbanEvent)
def urbanevent_foldermanager(object):
    return [foldermanager.UID() for foldermanager in object.aq_parent.getFoldermanagers()]


@indexer(IBaseBuildLicence)
def investigation_start_date(object):
    if object.getUrbanEventInquiries():
        event = object.getLastInquiry(use_catalog=False)
        if event.getInvestigationStart():
            return event.getInvestigationStart()


@indexer(IBaseBuildLicence)
def investigation_end_date(object):
    if object.getUrbanEventInquiries():
        event = object.getLastInquiry(use_catalog=False)
        end_date = event.getInvestigationEnd()
        if end_date:
            return end_date


@indexer(IBaseFolder)
def rubricsfolders_extravalue(object):
    if object.portal_type == 'Folder' and 'rubrics' in object.getPhysicalPath():
        return ['0', '1', '2', '3']
    else:
        return ['']


@indexer(IGenericLicence)
def genericlicence_representative(licence):
    representatives_uids = [rep.UID() for rep in licence.getRepresentatives()]
    return representatives_uids


@indexer(IGenericLicence)
def genericlicence_decisiondate(licence):
    decision_event = licence.getLastTheLicence()
    if decision_event:
        try:
            linked_pm_items = get_ws_meetingitem_infos(decision_event)
        except WebFault:
            catalog = api.portal.get_tool('portal_catalog')
            brain = catalog(UID=licence.UID())
            if brain.getDecisionDate:
                return brain.getDecisionDate
        if linked_pm_items:
            meeting_date = linked_pm_items[0]['meeting_date']
            if not (meeting_date.day == meeting_date.month == 1 and meeting_date.year == 1950):
                return meeting_date
        return decision_event.getDecisionDate() or decision_event.getEventDate()


@indexer(IGenericLicence)
def genericlicence_depositdate(licence):
    deposit_event = licence.getFirstDeposit()
    if deposit_event:
        return deposit_event.getEventDate()


@indexer(IGenericLicence)
def genericlicence_archive(licence):
    is_archive = False
    archive_adapter = queryAdapter(licence, IIsArchive)
    if archive_adapter:
        is_archive = archive_adapter.is_archive()
    return is_archive


@indexer(IUrbanEvent)
def event_not_indexed(obj):
    raise AttributeError()


@indexer(IUrbanDoc)
def doc_not_indexed(obj):
    raise AttributeError()


@indexer(IApplicant)
@indexer(IProprietary)
@indexer(ICorporation)
def contact_not_indexed(obj):
    raise AttributeError()


@indexer(IGenericLicence)
def genericlicence_final_duedate(licence):
    """
    Index licence reference on their tasks to be able
    to query on it.
    """
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
def inspection_task_followups(task):
    """
    Index inspection tasks with all the followup actions
    found in the last report event.
    This will put in the unused index 'Subject'
    """
    licence = task.get_container()
    # only index Inspection and Ticket licence
    if not IInspection.providedBy(licence) and not ITicket.providedBy(licence):
        return []
    last_report = licence.getLastReportEvent()
    follow_ups = last_report and last_report.getFollowup_proposition() or []
    return follow_ups


@indexer(IAutomatedTask)
def task_covid(task):
    """
    """
    licence = task.get_container()
    covid = licence.getCovid() and ['COVID'] or None
    return covid


@indexer(IGenericLicence)
def licence_covid(licence):
    """
    """
    covid = licence.getCovid() and ['COVID'] or None
    return covid
