# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from Products.urban.interfaces import CONTACT_INTERFACES
from Products.urban.config import URBAN_TYPES
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def setInterface(contact, event):
    if not contact.getPortalTypeName() in CONTACT_INTERFACES:
        return
    alsoProvides(contact, CONTACT_INTERFACES[contact.getPortalTypeName()])


def updateLicenceTitle(contact, event):
        #only update parent's title if an applicant or a proprietary is added
        if not contact.portal_type in ['Applicant', 'Proprietary', ]:
            return
        parent = contact.aq_inner.aq_parent
        if parent.portal_type in URBAN_TYPES:
            event = ObjectModifiedEvent(parent)
            notify(event)
