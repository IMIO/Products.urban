# -*- coding: utf-8 -*-

from Products.urban.interfaces import ITheLicenceEvent

from zope.component.interface import getInterface
from zope.interface import alsoProvides
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

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
        is_html = 'html' in str(field.default_content_type)
        default_text = urbanevent.getDefaultText(urbanevent, field, is_html)
        rendered_text = portal_urban.renderText(default_text, urbanevent)
        field_mutator = getattr(urbanevent, field.mutator)
        field_mutator(rendered_text)


def setEventTypeType(urban_event, event):
    urban_eventType = urban_event.getUrbaneventtypes()
    urban_eventTypeType = urban_eventType.getEventTypeType()
    if not urban_eventTypeType:
        return
    eventTypeTypeInterface = getInterface('', urban_eventTypeType)
    alsoProvides(urban_event, eventTypeTypeInterface)
    urban_event.reindexObject(['object_provides'])


def setCreationDate(urban_event, event):
    urban_event.setCreationDate(urban_event.getEventDate())
    urban_event.reindexObject(['created'])


def generateSingletonDocument(urban_event, event):
    urban_tool = api.portal.get_tool('portal_urban')
    if not urban_tool.getGenerateSingletonDocuments():
        return

    templates = urban_event.getTemplates()
    if len(templates) == 1:
        pod_template = templates[0]
        output_format = 'odt'
        generation_view = urban_event.restrictedTraverse('urban-document-generation')
        generation_view(pod_template.UID(), output_format)


def updateKeyEvent(urban_event, event):
    event_type = urban_event.getUrbaneventtypes()
    if not event_type or event_type.getIsKeyEvent():
        licence = urban_event.aq_inner.aq_parent
        licence.reindexObject(['last_key_event'])


def updateDecisionDate(urban_event, event):
    if ITheLicenceEvent.providedBy(urban_event):
        licence = urban_event.aq_inner.aq_parent
        licence.reindexObject(['getDecisionDate'])


def notifyLicence(urban_event, event):
    """
    Notify the licence of changes so schedule events triggers.
    """
    licence = urban_event.aq_parent
    notify(ObjectModifiedEvent(licence))
