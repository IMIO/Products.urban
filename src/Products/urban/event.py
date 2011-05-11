# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from zope.component.interface import getInterface


def setEventTypeType(urbanEvent, event):
    urbanEventType = urbanEvent.getUrbaneventtypes()
    urbanEventTypeType = urbanEventType.getEventTypeType()
    if not urbanEventTypeType:
        return
    eventTypeTypeInterface = getInterface('', urbanEventTypeType)
    alsoProvides(urbanEvent, eventTypeTypeInterface)
    urbanEvent.reindexObject(['object_provides'])
