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

from Products.Archetypes.interfaces import IBaseFolder

from Products.urban.interfaces import IApplicant
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IBaseBuildLicence
from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import IIsArchive
from Products.urban.interfaces import IParcellingTerm
from Products.urban.interfaces import IPortionOut
from Products.urban.interfaces import IUrbanEvent
from Products.urban.interfaces import IUrbanEventType
from Products.urban.interfaces import IUrbanEventInquiry

from plone.indexer import indexer

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


@indexer(IPortionOut)
def parcelinfoindex(obj):
    """
    Indexes some informations about the parcels of 'self'
    It builds a list of parcels infos.  Parcels infos are :
    - code divison
    - division
    - section
    - radical
    - bis
    - exposant
    - puissance
    Separated by a ','
    What we need to do is to do an 'exact' search on it
    This index is a ZCTextIndex based on the plone_lexicon so we
    are sure that indexed values are lowercase
    """
    return [obj.getIndexValue()]


@indexer(IGenericLicence)
def genericlicence_parcelinfoindex(obj):
    """
    Index parcels of a licence
    """
    parcels_infos = []
    if hasattr(obj, 'getParcels'):
        parcels_infos = list(set([p.getIndexValue() for p in obj.getParcels()]))
    return parcels_infos


@indexer(IParcellingTerm)
def parcellingterm_parcelinfoindex(obj):
    """
    Index parcels of a parcelling term
    """
    parcels_infos = []
    if hasattr(obj, 'getParcels'):
        parcels_infos = list(set([p.getIndexValue() for p in obj.getParcels()]))
    return parcels_infos


@indexer(IGenericLicence)
def genericlicence_streetsuid(licence):
    streets = [location['street'] for location in licence.getWorkLocations()]
    return streets


@indexer(IGenericLicence)
def genericlicence_streetnumber(licence):
    numbers = [location['number'] for location in licence.getWorkLocations()]
    return numbers


@indexer(IGenericLicence)
def genericlicence_address(licence):
    return licence.getWorkLocationSignaletic()


@indexer(IGenericLicence)
def genericlicence_lastkeyevent(object):
    for event in reversed(object.getUrbanEvents()):
        event_type = event.getUrbaneventtypes()
        if event_type.getIsKeyEvent() and event.getEventDate().year() >= 1900:
            return "%s,  %s" % (event.getEventDate().strftime("%d/%m/%y"), event_type.Title())


# !!!!
# We use this index to know if an event is schedulable or not.
# Since it's not used for UrbanEventType, we use this one rather
# than define a new index
# !!!!
@indexer(IUrbanEventType)
def urbaneventtype_lastkeyevent(object):
    if object.getDeadLineDelay() > 0:
        return 'schedulable'
    return ''


@indexer(IGenericLicence)
def genericlicence_foldermanager(object):
    return [foldermanager.UID() for foldermanager in object.getFoldermanagers()]


@indexer(IUrbanEvent)
def urbanevent_foldermanager(object):
    return [foldermanager.UID() for foldermanager in object.aq_parent.getFoldermanagers()]


@indexer(IBaseBuildLicence)
def investigation_start_date(object):
    if object.getUrbanEventInquiries():
        event = object.getLastInquiry()
        if event.getInvestigationStart():
            return event.getInvestigationStart()


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
    decision_event = licence.getLastTheLicence(use_catalog=False)
    if decision_event:
        return decision_event.getEventDate()


@indexer(IGenericLicence)
def genericlicence_depositdate(licence):
    deposit_event = licence.getFirstDeposit(use_catalog=False)
    if deposit_event:
        return deposit_event.getEventDate()


@indexer(IGenericLicence)
def genericlicence_archive(licence):
    is_archive = False
    archive_adapter = queryAdapter(licence, IIsArchive)
    if archive_adapter:
        is_archive = archive_adapter.is_archive()
    return is_archive
