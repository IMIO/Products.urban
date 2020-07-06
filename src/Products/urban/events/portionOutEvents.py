# -*- coding: utf-8 -*-

from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import ILicencePortionOut
from Products.urban import services

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
    parcel.bis = parcel.bis or "0"
    parcel.puissance = parcel.puissance or "0"
    parcel.reindexObject()

    parcel_status = False
    try:
        cadastre = services.cadastre.new_session()
        parcel_status = cadastre.get_parcel_status(parcel.capakey)
        cadastre.close()
    except services.cadastral.UnreferencedParcelError:
        pass

    parcel.setIsOfficialParcel(parcel_status in ["old_parcel", "actual_parcel"])
    parcel.setOutdated(parcel_status in ["old_parcel"])
    parcel.reindexObject()


def setDivisionCode(parcel, event):
    """
    Set the division code value of the parcel
    """
    parcel.setDivisionCode(parcel.getDivision())
    parcel.reindexObject()
