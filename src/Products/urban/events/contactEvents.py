# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from Products.urban.interfaces import CONTACT_INTERFACES
from Products.urban.config import APPLICANTS_TYPES
from Products.urban.config import URBAN_TYPES
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def setInterface(contact, event):
    if not contact.getPortalTypeName() in CONTACT_INTERFACES:
        return
    alsoProvides(contact, CONTACT_INTERFACES[contact.getPortalTypeName()])


def updateLicenceTitle(contact, event):
    # only update parent's title if an applicant or a proprietary is added
    if not contact.portal_type in APPLICANTS_TYPES:
        return
    parent = contact.aq_inner.aq_parent
    if parent.portal_type in URBAN_TYPES:
        parent.reindexObject(
            idxs=[
                "applicantInfosIndex",
            ]
        )
        event = ObjectModifiedEvent(parent)
        notify(event)


def sortByAlphabeticalOrder(contact, event):
    if not contact.portal_type in [
        "Notary",
        "Architect",
        "Geometrician",
        "FolderManager",
    ]:
        return
    container = contact.aq_inner.aq_parent
    name = contact.getName1() + contact.getName2()
    for other_contact in container.objectValues():
        other_name = other_contact.getName1() + other_contact.getName2()
        if name.lower() < other_name.lower():
            new_position = container.getObjectPosition(other_contact.getId())
            container.moveObjectToPosition(contact.getId(), new_position)
            return
    container.moveObjectsToBottom(contact.getId())
