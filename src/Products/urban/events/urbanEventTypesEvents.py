# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from Products.urban.events.urbanEventEvents import setEventTypeType
from Products.urban.interfaces import IUrbanEvent
from Products.urban.interfaces import IEventTypeType
from Products.urban.interfaces import IUrbanEvent

from plone import api

from zope.annotation import IAnnotations
from zope.interface import noLongerProvides
from zope.interface import providedBy


def updateKeyEvent(urbanEventType, event):
    catalog = getToolByName(urbanEventType, 'portal_catalog')
    uet_path = urbanEventType.absolute_url_path().split('/')
    licence_path = uet_path[:2]
    licence_path.extend(['urban', '%ss' % uet_path[3]])
    licence_path = '/'.join(licence_path)
    for brain in catalog(portal_type='UrbanEvent', path=licence_path, Title=urbanEventType.Title().split('(')[0]):
        urban_event = brain.getObject()
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

    ref_catalog = api.portal.get_tool('reference_catalog')
    ref_brains = ref_catalog(targetUID=urban_event_type.UID())
    for ref_brain in ref_brains:
        ref = ref_brain.getObject()
        urban_event = ref.getSourceObject()
        if IUrbanEvent.providedBy(urban_event):
            # clean previous event type interface
            for provided_interface in providedBy(urban_event).flattened():
                if IEventTypeType.providedBy(provided_interface):
                    noLongerProvides(urban_event, provided_interface)
            # add new provided interface
            setEventTypeType(urban_event, event)
