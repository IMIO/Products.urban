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
    if not urban_tool.getGenerateSingletonDocuments:
        return
    templates = urbanEvent.getTemplates()
    if len(templates) == 1:
        urban_tool = getToolByName(urbanEvent, 'portal_urban')
        urban_tool.createUrbanDoc(templates[0].UID(), urbanEvent.UID())
