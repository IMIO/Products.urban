# -*- coding: utf-8 -*-

from zope.interface import alsoProvides
from zope.component import createObject
from zope.component.interface import getInterface

from plone import api


def setDefaultValuesEvent(urbanevent, event):
    """
     set default values on urban event fields
    """
    _setDefaultTextValues(urbanevent)


def _setDefaultTextValues(urbanevent):

    portal_urban = api.portal.get_tool('portal_urban')

    select_fields = [field for field in urbanevent.schema.fields() if field.default_method == 'getDefaultText']

    for field in select_fields:
        is_html = field.default_content_type == 'text/html'
        default_text = urbanevent.getDefaultText(urbanevent, field, is_html)
        rendered_text = portal_urban.renderText(default_text, urbanevent)
        field_mutator = getattr(urbanevent, field.mutator)
        field_mutator(rendered_text)


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


def generateSingletonDocument(urban_event, event):
    urban_tool = api.portal.get_tool('portal_urban')
    if not urban_tool.getGenerateSingletonDocuments():
        return
    templates = urban_event.getTemplates()
    if len(templates) == 1:
        odt_template = templates[0]
        createObject('GeneratedUrbanDoc', urban_event, odt_template)


def updateKeyEvent(urbanEvent, event):
    event_type = urbanEvent.getUrbaneventtypes()
    if not event_type or event_type.getIsKeyEvent():
        licence = urbanEvent.aq_inner.aq_parent
        licence.reindexObject(['last_key_event'])
