# -*- coding: utf-8 -*-
from Products.urban.events.urbanEventEvents import setEventMarkerInterfaces
from Products.urban import interfaces

from zope.annotation import IAnnotations
from zope.interface import noLongerProvides
from zope.interface import providedBy


def updateKeyEvent(urban_event_type, event):
    annotations = IAnnotations(urban_event_type)
    is_key_event = urban_event_type.getIsKeyEvent()
    # make sure to not trigger the reindex when setting the annotation for
    # the first time
    previous_key_event_value = annotations.get("urban.is_key_event", is_key_event)
    annotations["urban.is_key_event"] = is_key_event
    if previous_key_event_value == is_key_event:
        return

    for urban_event in urban_event_type.getLinkedUrbanEvents():
        licence = urban_event.aq_parent
        licence.reindexObject(["last_key_event"])


def updateEventType(urban_event_type, event):
    """ """
    annotations = IAnnotations(urban_event_type)
    previous_eventtype_interface = annotations.get("urban.eventtype", set([]))
    new_eventtype_interface = set(urban_event_type.getEventTypeType())
    if previous_eventtype_interface == new_eventtype_interface:
        return

    annotations["urban.eventtype"] = set(new_eventtype_interface)

    for urban_event in urban_event_type.getLinkedUrbanEvents():
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


def forceEventTypeCollege(urban_event_type, event):
    """ """

    college_event_interfaces = set(
        [
            interfaces.ISimpleCollegeEvent.__identifier__,
            interfaces.IEnvironmentSimpleCollegeEvent.__identifier__,
        ]
    )
    default_college_interface = interfaces.ISimpleCollegeEvent.__identifier__

    if urban_event_type.getEventPortalType().endswith("College"):
        selected_interfaces = urban_event_type.getEventTypeType()
        if not college_event_interfaces.intersection(set(selected_interfaces)):
            new_marker_interfaces = [default_college_interface]
            for old_interface in selected_interfaces:
                new_marker_interfaces.append(old_interface)
            urban_event_type.setEventTypeType(new_marker_interfaces)
