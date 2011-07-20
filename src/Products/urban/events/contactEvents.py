# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from Products.urban.interfaces import CONTACT_INTERFACES

def setInterface(contact, event):
    if not CONTACT_INTERFACES.has_key(contact.getPortalTypeName()):
        return
    alsoProvides(contact, CONTACT_INTERFACES[contact.getPortalTypeName()])
