# -*- coding: utf-8 -*-

from Products.urban.interfaces import IEnvironmentBase
from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import ILicencePortionOut

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
    urban_tool = api.portal.get_tool('portal_urban')
    references = {
        'division': parcel.getDivisionCode(),
        'section': parcel.getSection(),
        'radical': parcel.getRadical(),
        'bis': parcel.getBis(),
        'exposant': parcel.getExposant(),
        'puissance': parcel.getPuissance(),
    }
    exists_in_DB = urban_tool.queryParcels(
        browseold=True,
        fuzzy=False,
        **references
    ) and True or False
    parcel.setIsOfficialParcel(exists_in_DB)
    if exists_in_DB:
        if not urban_tool.queryParcels(fuzzy=False, **references):
            parcel.setOutdated(True)
        else:
            parcel.setOutdated(False)
    else:
        parcel.setIsOfficialParcel(False)
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
    portal_urban = api.portal.get_tool('portal_urban')
    parcels = licence.objectValues('PortionOut')
    parcel_infos = set()

    for parcel in parcels:
        parcel_infos.add(parcel.getIndexValue())
        parcels_historic = portal_urban.queryParcels(
            parcel.getDivisionCode(), parcel.getSection(), parcel.getRadical(), parcel.getBis(), parcel.getExposant(), parcel.getPuissance(),
            historic=True, fuzzy=False, browseold=True
        )
        if not parcels_historic:
            break

        parcels_historic = parcels_historic[0]
        for ref in parcels_historic.getAllIndexableRefs():
            parcel_infos.add(ref)

    related_brains = catalog(
        object_provides=IEnvironmentBase.__identifier__,
        parcelInfosIndex=list(parcel_infos),
        sort_on='sortable_title'
    )
    relatedlicences_UIDs = [brain.UID for brain in related_brains]

    licence.setPreviousLicences(relatedlicences_UIDs)
