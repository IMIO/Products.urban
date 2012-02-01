# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from zope.component.interface import getInterface
from Products.CMFCore.utils import getToolByName

def setEventTypeType(urbanEvent, event):
    urbanEventType = urbanEvent.getUrbaneventtypes()
    urbanEventTypeType = urbanEventType.getEventTypeType()
    if not urbanEventTypeType:
        return
    eventTypeTypeInterface = getInterface('', urbanEventTypeType)
    alsoProvides(urbanEvent, eventTypeTypeInterface)
    urbanEvent.reindexObject(['object_provides'])


def setCreationDate(urbanEvent, event):
    urbanEvent.setCreationDate(urbanEvent.getEventDate())
    urbanEvent.reindexObject(['created'])

def generateSingletonDocument(urbanEvent, event):
    urban_tool = getToolByName(urbanEvent, 'portal_urban')
    if not urban_tool.getGenerateSingletonDocuments():
        return
    templates = urbanEvent.getTemplates()
    if len(templates) == 1:
        urban_tool.createUrbanDoc(templates[0].UID(), urbanEvent.UID())

def updateKeyEvent(urbanEvent, event):
    event_type = urbanEvent.getUrbaneventtypes()
    if not event_type or event_type.getIsKeyEvent():
        licence = urbanEvent.aq_parent
        licence.reindexObject(['last_key_event'])
