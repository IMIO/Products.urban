# -*- coding: utf-8 -*-
from Products.urban.events.urbanEventEvents import setEventMarkerInterfaces
from Products.urban import interfaces

from zope.annotation import IAnnotations
from zope.interface import noLongerProvides
from zope.interface import providedBy


def updateKeyEvent(event_config, event):
    annotations = IAnnotations(event_config)
    is_key_event = event_config.getIsKeyEvent()
    # make sure to not trigger the reindex when setting the annotation for
    # the first time
    previous_key_event_value = annotations.get('urban.is_key_event', is_key_event)
    annotations['urban.is_key_event'] = is_key_event
    if previous_key_event_value == is_key_event:
        return

    for urban_event in event_config.getLinkedUrbanEvents():
        licence = urban_event.aq_parent
        licence.reindexObject(['last_key_event'])


def updateEventType(event_config, event):
    """
    """
    annotations = IAnnotations(event_config)
    previous_eventconfig_interface = annotations.get('urban.eventtype', set([]))
    new_eventconfig_interface = set(event_config.getEventType())
    if previous_eventconfig_interface == new_eventconfig_interface:
        return

    annotations['urban.eventtype'] = set(new_eventconfig_interface)

    for urban_event in event_config.getLinkedUrbanEvents():
        if interfaces.IUrbanEvent.providedBy(urban_event):
            # clean previous event type interface
            for provided_interface in providedBy(urban_event).flattened():
                if interfaces.IEventTypeType.providedBy(provided_interface):
                    try:
                        noLongerProvides(urban_event, provided_interface)
                    except:
                        pass
            # add new provided interface
            setEventMarkerInterfaces(urban_event, event)


def forceEventTypeCollege(event_config, event):
    """
    """

    college_event_interfaces = set([
        interfaces.ISimpleCollegeEvent.__identifier__,
        interfaces.IEnvironmentSimpleCollegeEvent.__identifier__,
    ])
    default_college_interface = interfaces.ISimpleCollegeEvent.__identifier__

    if event_config.getEventPortalType().endswith('College'):
        selected_interfaces = event_config.getEventType()
        if not college_event_interfaces.intersection(set(selected_interfaces)):
            new_marker_interfaces = [default_college_interface]
            new_marker_interfaces += selected_interfaces or []
            event_config.eventType = new_marker_interfaces
