# -*- coding: utf-8 -*-

from Products.urban.interfaces import IEnvironmentBase
from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import ILicencePortionOut
from Products.urban import services

from plone import api

from zope.interface import alsoProvides


def onDelete(parcel, event):
    """
      Reindex licence of this parcel after deletion.
    """
    parcel.aq_inner.aq_parent.reindexObject(idxs=["parcelInfosIndex"])


def set_ILicencePortionOut_interface(parcel, event):
    """
    Mark PortionOut in licences with a specific marker interface.
    """
    container = parcel.aq_parent
    if IGenericLicence.providedBy(container):
        alsoProvides(parcel, ILicencePortionOut)


def setValidParcel(parcel, event):
    """
     Check if the manually added parcel exists in he cadastral DB
     and set its "isvalidparcel" attribute accordingly.
    """

    is_official = True
    references = parcel.reference_as_dict()
    try:
        cadastre = services.cadastre.new_session()
        is_outdated = cadastre.is_outdated_parcel(**references)
        cadastre.close()
        parcel.setOutdated(is_outdated)
    except:
        is_official = False

    parcel.setIsOfficialParcel(is_official)
    parcel.reindexObject()


def setDivisionCode(parcel, event):
    """
     Set the division code value of the parcel
    """
    parcel.setDivisionCode(parcel.getDivision())
    parcel.reindexObject()


def setEnvironmentLicencePreviousLicencesField(parcel, event):
    licence = parcel.aq_parent

    if not IEnvironmentLicence.providedBy(licence):
        return

    catalog = api.portal.get_tool('portal_catalog')
    parcels = licence.objectValues('PortionOut')
    parcel_infos = set()
    cadastre = services.cadastre.new_session()

    for parcel in parcels:
        parcel_infos.add(parcel.getIndexValue())

        if not parcel.getIsOfficialParcel() or not parcel.getDivision():
            break

        references = parcel.reference_as_dict()
        parcel_historic = cadastre.query_parcel_historic(**references)

        if not parcel_historic:
            break

        for ref in parcel_historic.get_all_reference_indexes():
            parcel_infos.add(ref)

    cadastre.close()

    related_brains = catalog(
        object_provides=IEnvironmentBase.__identifier__,
        parcelInfosIndex=list(parcel_infos),
        sort_on='sortable_title'
    )
    relatedlicences_UIDs = [brain.UID for brain in related_brains]

    licence.setPreviousLicences(relatedlicences_UIDs)
