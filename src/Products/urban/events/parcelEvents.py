# -*- coding: utf-8 -*-

from Products.urban import services

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def updateParcellingTitle(contact, event):
        parent = contact.aq_inner.aq_parent
        if parent.portal_type == 'ParcellingTerm':
            event = ObjectModifiedEvent(parent)
            notify(event)


def onDelete(parcel, event):
    """
      Reindex licence of this parcel after deletion.
    """
    parcel.aq_inner.aq_parent.reindexObject(idxs=["parcelInfosIndex"])


def setValidParcel(parcel, event):
    """
     Check if the manually added parcel exists in he cadastral DB
     and set its "isvalidparcel" attribute accordingly.
    """
    parcel_status = False
    try:
        cadastre = services.cadastre.new_session()
        parcel_status = cadastre.get_parcel_status(parcel.capakey)
        cadastre.close()
    except services.cadastral.UnreferencedParcelError:
        pass

    parcel.isOfficialParcel = parcel_status in ['old_parcel', 'actual_parcel']
    parcel.outdated = parcel_status in ['old_parcel']
    parcel.reindexObject()
