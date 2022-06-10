# -*- coding: utf-8 -*-

from Products.urban.browser.default_text import DefaultTextRenderer
from Products.urban.events.licenceEvents import _setDefaultSelectValues
from Products.urban.interfaces import IEventTypeType
from Products.urban.interfaces import ITheLicenceEvent

from imio.schedule.utils import get_task_configs

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
    _setDefaultSelectValues(urbanevent)


def _setDefaultTextValues(urbanevent):

    select_fields = [field for field in urbanevent.schema.fields() if field.default_method == 'getDefaultText']

    text_renderer = None

    for field in select_fields:
        is_html = 'html' in str(field.default_content_type)
        default_text = urbanevent.getDefaultText(urbanevent, field, is_html)

        if default_text:
            # only load the text renderer if theres text to generate.
            text_renderer = text_renderer is None and DefaultTextRenderer(urbanevent)
            rendered_text = text_renderer(default_text)
            field_mutator = getattr(urbanevent, field.mutator)
            field_mutator(rendered_text)


def setEventTypeType(urban_event, event):
    urban_eventType = urban_event.getUrbaneventtypes()
    urban_eventTypeTypes = urban_eventType.getEventTypeType()
    if not urban_eventTypeTypes:
        return

    for urban_eventTypeType in urban_eventTypeTypes:
        to_explore = set([getInterface('', urban_eventTypeType)])

        while to_explore:
            type_interface = to_explore.pop()
            if IEventTypeType.providedBy(type_interface):
                alsoProvides(urban_event, type_interface)
                for base_interface in type_interface.getBases():
                    to_explore.add(base_interface)

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
        if pod_template.can_be_generated(urban_event):
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
    if not urban_event.checkCreationFlag():
        licence = urban_event.aq_parent
        notify(ObjectModifiedEvent(licence))


def updateTaskIndexes(task_container, event):
    task_configs = get_task_configs(task_container)

    if not task_configs:
        return

    with api.env.adopt_roles(['Manager']):
        for config in task_configs:
            tasks = config.get_task_instances(task_container)
            for task in tasks:
                task.reindexObject(idxs=['commentators'])
