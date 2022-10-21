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
from DateTime import DateTime

from imio.schedule.content.task import IAutomatedTask

from Products.Archetypes.interfaces import IBaseFolder

from Products.urban import interfaces
from Products.urban.schedule.interfaces import ILicenceDeliveryTask
from Products.urban.utils import get_ws_meetingitem_infos

from plone import api
from plone.indexer import indexer

from suds import WebFault

from zope.component import queryAdapter


@indexer(interfaces.IApplicant)
def applicant_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    return _get_applicantsinfoindex(object)


@indexer(interfaces.IGenericLicence)
def genericlicence_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    contacts_info = []
    contacts = object.getApplicants() + object.getProprietaries() +\
        object.get_applicants_history() + object.get_proprietaries_history() +\
        object.getCouples() + object.get_couples_history() +\
        object.getProprietaryCouples() + object.get_proprietary_couples_history()
    for contact in contacts:
        contacts_info.extend(_get_applicantsinfoindex(contact))
    return list(set(contacts_info))


@indexer(interfaces.IEnvironmentLicence)
def environmentlicence_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    applicants_info = []
    applicants = object.getApplicants() + object.get_applicants_history()
    for applicant in applicants:
        applicants_info.extend(_get_applicantsinfoindex(applicant))
    return list(set(applicants_info))


@indexer(interfaces.IInspection)
@indexer(interfaces.ITicket)
def inspection_applicantinfoindex(object):
    """
    Return the informations to index about the applicants
    """
    applicants_info = []
    contacts = object.getApplicants() + object.getProprietaries() +\
        object.get_applicants_history() + object.get_proprietaries_history() +\
        object.getCouples() + object.get_couples_history() +\
        object.getProprietaryCouples() + object.get_proprietary_couples_history() +\
        object.getPlaintiffs() + object.getTenants()
    for applicant in contacts:
        applicants_info.extend(_get_applicantsinfoindex(applicant))
    return list(set(applicants_info))


def _get_applicantsinfoindex(applicant):
    if applicant.meta_type == 'Couple':
        applicants_info = [
            applicant.getCouplePerson1Name(),
            applicant.getCouplePerson1Firstname(),
            applicant.getCouplePerson2Name(),
            applicant.getCouplePerson2Firstname(),
            applicant.getNationalRegisterPerson1(),
            applicant.getNationalRegisterPerson2(),
        ]
    else:
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


@indexer(interfaces.IBaseBuildLicence)
@indexer(interfaces.ICODT_BaseBuildLicence)
@indexer(interfaces.IMiscDemand)
@indexer(interfaces.IPatrimonyCertificate)
def licence_architectinfoindex(object):
    """
    Return the informations to index about the architects
    """
    architects_info = []
    architects = object.getArchitects()
    for architect in architects:
        architects_info.extend(_get_applicantsinfoindex(architect))
    return list(set(architects_info))


@indexer(interfaces.IGenericLicence)
def genericlicence_parcelinfoindex(obj):
    parcels_infos = []
    if hasattr(obj, 'getParcels'):
        parcels_infos = list(set([p.get_capakey() for p in obj.getParcels()]))
    return parcels_infos


@indexer(interfaces.IGenericLicence)
def genericlicence_modified(licence):
    wf_modification = licence.workflow_history[licence.workflow_history.keys()[0]][-1]['time']
    if wf_modification > licence.modified():
        return wf_modification
    return licence.modified()


@indexer(interfaces.IGenericLicence)
def genericlicence_streetsuid(licence):
    if licence.portal_type in ['EnvClassBordering']:
        return []
    streets = [location['street'] for location in licence.getWorkLocations()]
    return streets


@indexer(interfaces.IGenericLicence)
def genericlicence_streetnumber(licence):
    numbers = [location['number'] or '0' for location in licence.getWorkLocations()] or ['0']
    return numbers


@indexer(interfaces.IGenericLicence)
def genericlicence_address(licence):
    return licence.getStreetAndNumber()


@indexer(interfaces.IGenericLicence)
def genericlicence_lastkeyevent(object):
    for event in reversed(object.getUrbanEvents()):
        event_type = event.getUrbaneventtypes()
        if event_type.getIsKeyEvent() and event.getEventDate().year() >= 1900:
            return "%s,  %s" % (event.getEventDate().strftime("%d/%m/%y"), event_type.Title())


@indexer(interfaces.IGenericLicence)
def genericlicence_foldermanager(object):
    return [foldermanager.UID() for foldermanager in object.getFoldermanagers()]


@indexer(interfaces.IUrbanEvent)
def urbanevent_foldermanager(object):
    return [foldermanager.UID() for foldermanager in object.aq_parent.getFoldermanagers()]


@indexer(interfaces.IBaseBuildLicence)
def licence_worktype(object):
    return object.getWorkType()


@indexer(interfaces.IBaseBuildLicence)
def investigation_start_date(object):
    if object.getUrbanEventInquiries():
        event = object.getLastInquiry(use_catalog=False)
        if event.getInvestigationStart():
            return event.getInvestigationStart()


@indexer(interfaces.IBaseBuildLicence)
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


@indexer(interfaces.IGenericLicence)
def genericlicence_representative(licence):
    representatives_uids = [rep.UID() for rep in licence.getRepresentatives()]
    return representatives_uids


@indexer(interfaces.IGenericLicence)
def genericlicence_decisiondate(licence):
    decision_event = licence.getLastTheLicence()
    linked_pm_items = None
    if decision_event:
        try:
            linked_pm_items = get_ws_meetingitem_infos(decision_event)
        except WebFault:
            catalog = api.portal.get_tool('portal_catalog')
            brain = catalog(UID=licence.UID())
            if brain and brain[0].getDecisionDate:
                old_decision_date = brain[0].getDecisionDate
                if type(old_decision_date) is DateTime:
                    decision_date = date(old_decision_date.year(), old_decision_date.month(), old_decision_date.day())
                else:
                    decision_date = date(old_decision_date.year, old_decision_date.month, old_decision_date.day)
                return decision_date
        if linked_pm_items:
            meeting_date = linked_pm_items[0]['meeting_date']
            if not (meeting_date.day == meeting_date.month == 1 and meeting_date.year == 1950):
                return meeting_date
        return decision_event.getDecisionDate() or decision_event.getEventDate()


@indexer(interfaces.IGenericLicence)
def genericlicence_depositdate(licence):
    deposit_event = licence.getFirstDeposit()
    if deposit_event:
        return deposit_event.getEventDate()


@indexer(interfaces.IGenericLicence)
def genericlicence_archive(licence):
    is_archive = False
    archive_adapter = queryAdapter(licence, interfaces.IIsArchive)
    if archive_adapter:
        is_archive = archive_adapter.is_archive()
    return is_archive


@indexer(interfaces.IUrbanEvent)
def event_not_indexed(obj):
    raise AttributeError()


@indexer(interfaces.IUrbanDoc)
def doc_not_indexed(obj):
    raise AttributeError()


@indexer(interfaces.IApplicant)
@indexer(interfaces.IProprietary)
@indexer(interfaces.ICorporation)
def contact_not_indexed(obj):
    raise AttributeError()


@indexer(interfaces.IGenericLicence)
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
    if not interfaces.IInspection.providedBy(licence) and \
       not interfaces.ITicket.providedBy(licence):
        return []
    last_report = licence.getLastReportEvent()
    follow_ups = last_report and last_report.getFollowup_proposition() or []
    closed_follow_up_events_ids = [evt.getUrbaneventtypes().id for evt
                                   in licence.getCurrentFollowUpEvents()
                                   if evt.get_state() == 'closed']
    active_follow_ups = [fol for fol in follow_ups if fol not in closed_follow_up_events_ids]
    return active_follow_ups


@indexer(IAutomatedTask)
def task_covid(task):
    """
    """
    licence = task.get_container()
    covid = licence.getCovid() and ['COVID'] or None
    return covid


@indexer(interfaces.IGenericLicence)
def licence_covid_and_opinion_requests(licence):
    """
    commentators index store COVID value and opinion requests
    """
    indexes = licence.getCovid() and ['COVID'] or []
    if interfaces.IInquiry.providedBy(licence):
        inquiries = licence._get_inquiry_objs(all_=True)
        opinions_id = set()
        for inquiry in inquiries:
            opinions_id.update(set(inquiry.getSolicitOpinionsTo()))
            opinions_id.update(set(inquiry.getSolicitOpinionsToOptional()))

        vocabulary = licence.getField('solicitOpinionsTo').vocabulary
        opinions = [v['abbreviation'] for v in vocabulary.get_raw_voc(licence) if v['id'] in opinions_id]
        indexes.extend(opinions)

    return indexes or None


@indexer(interfaces.IUrbanEventType)
def eventconfig_urbaneventtype(event_config):
    """
    Index the portal_type of urban event created by this config.
    """
    event_portal_type = event_config.getEventPortalType()
    return event_portal_type
