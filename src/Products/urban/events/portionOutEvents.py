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
    parcel.setDivisionCode(parcel.getDivision())
    parcel.bis = parcel.bis or '0'
    parcel.puissance = parcel.puissance or '0'
    parcel.reindexObject()

    references = parcel.reference_as_dict(True)

    is_official = False
    try:
        cadastre = services.cadastre.new_session()
        is_official = cadastre.is_official_parcel(**references)
        cadastre.close()
    except:
        pass

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
    capakeys = set()
    cadastre = services.cadastre.new_session()

    for parcel in parcels:
        capakeys.add(parcel.get_capakey())

        if not parcel.getIsOfficialParcel() or not parcel.getDivision():
            continue

    cadastre.close()

    related_brains = catalog(
        object_provides=IEnvironmentBase.__identifier__,
        parcelInfosIndex=list(capakeys),
        sort_on='sortable_title'
    )
    relatedlicences_UIDs = [brain.UID for brain in related_brains]

    licence.setPreviousLicences(relatedlicences_UIDs)
