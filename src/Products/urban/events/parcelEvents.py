# -*- coding: utf-8 -*-
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def updateParcellingTitle(contact, event):
    parent = contact.aq_inner.aq_parent
    if parent.portal_type == "ParcellingTerm":
        event = ObjectModifiedEvent(parent)
        notify(event)
