# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from zope.component.interface import getInterface


def setEventTypeType(urbanEvent, event):
    #bypass this for now...
    return
    urbanEventType = urbanEvent.getUrbaneventtypes()
    urbanEventTypeType = urbanEventType.getEventTypeType()
    eventTypeTypeInterface = getInterface('', urbanEventTypeType)
    alsoProvides(urbanEvent, eventTypeTypeInterface)
    urbanEvent.reindexObject(['object_provides'])
