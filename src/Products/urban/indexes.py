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

from plone.indexer import indexer
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import IParcellingTerm
from Products.urban.interfaces import IUrbanEvent
from Products.urban.interfaces import IUrbanEventType


@indexer(IGenericLicence)
def genericlicence_applicantinfoindex(object):
    """
        Return the informations to index about the applicants
    """
    applicants_info = []
    for applicant in object.getApplicants():
        applicants_info.append(applicant.getName1())
        applicants_info.append(applicant.getName2())
        applicants_info.append(applicant.getSociety())
        applicants_info.append(applicant.getNationalRegister())
    return applicants_info


@indexer(IEnvironmentLicence)
def environmentlicence_applicantinfoindex(object):
    """
        Return the informations to index about the applicants
    """
    applicants_info = []
    for applicant in object.getApplicants():
        applicants_info.append(applicant.getName1())
        applicants_info.append(applicant.getName2())
        applicants_info.append(applicant.getSociety())
        applicants_info.append(applicant.getNationalRegister())
    for corporation in object.getCorporations():
        applicants_info.append(applicant.getName1())
        applicants_info.append(applicant.getName2())
        applicants_info.append(applicant.getDenomination())
        applicants_info.append(applicant.getBceNumber())
    return applicants_info


@indexer(IGenericLicence)
def genericlicence_parcelinfoindex(object):
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
    parcelsInfos = []
    try:
        for parcel in object.getParcels():
            parcelsInfos.append(parcel.getIndexValue())
    except:
        pass
    return parcelsInfos


@indexer(IParcellingTerm)
def parcellingterm_parcelinfoindex(object):
    """
    Indexes some informations about the parcels of a parcelling term
    """
    parcelsInfos = []
    try:
        for parcel in object.getParcels():
            parcelsInfos.append(parcel.getIndexValue())
    except:
        pass
    return parcelsInfos


@indexer(IGenericLicence)
def genericlicence_streetsuid(object):
    streets = []
    for location in object.getWorkLocations():
        streets.append(location['street'])
    return streets


@indexer(IGenericLicence)
def genericlicence_lastkeyevent(object):
    for event in reversed(object.getUrbanEvents()):
        event_type = event.getUrbaneventtypes()
        if event_type.getIsKeyEvent():
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
