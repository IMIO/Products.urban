# -*- coding: utf-8 -*-

from Products.urban.events.urbanEventEvents import setEventTypeType
from Products.urban.interfaces import IEventTypeType
from Products.urban.interfaces import IUrbanEvent


from zope.annotation import IAnnotations
from zope.interface import noLongerProvides
from zope.interface import providedBy


def updateKeyEvent(urban_event_type, event):
    annotations = IAnnotations(urban_event_type)
    previous_key_event_value = annotations.get('urban.is_key_event', [])
    is_key_event = urban_event_type.getIsKeyEvent()
    if previous_key_event_value == is_key_event:
        return

    annotations['urban.eventtype'] = is_key_event

    for urban_event in urban_event_type.getLinkedUrbanEvents():
        licence = urban_event.aq_parent
        licence.reindexObject(['last_key_event'])


def updateEventType(urban_event_type, event):
    """
    """
    annotations = IAnnotations(urban_event_type)
    previous_eventtype_interface = annotations.get('urban.eventtype', [])
    new_eventtype_interface = urban_event_type.getEventTypeType()
    if previous_eventtype_interface == new_eventtype_interface:
        return

    annotations['urban.eventtype'] = new_eventtype_interface

    for urban_event in urban_event_type.getLinkedUrbanEvents():
        if IUrbanEvent.providedBy(urban_event):
            # clean previous event type interface
            for provided_interface in providedBy(urban_event).flattened():
                if IEventTypeType.providedBy(provided_interface):
                    noLongerProvides(urban_event, provided_interface)
            # add new provided interface
            setEventTypeType(urban_event, event)
