# -*- coding: utf-8 -*-

from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IUrbanEvent

from plone import api


def list_missing_events():
    """ """
    catalog = api.portal.get_tool("portal_catalog")
    licences = [
        b.getObject() for b in catalog(object_provides=IGenericLicence.__identifier__)
    ]
    all_broken_events = {}
    for licence in licences:
        broken_events = [
            obj
            for obj in licence.objectValues()
            if IUrbanEvent.providedBy(obj) and not obj.getUrbaneventtypes()
        ]
        for broken_event in broken_events:
            if licence.portal_type not in all_broken_events:
                all_broken_events[licence.portal_type] = {}
            events_by_licence = all_broken_events[licence.portal_type]
            if broken_event.Title() in events_by_licence:
                events_by_licence[broken_event.Title()].append(licence)
            else:
                events_by_licence[broken_event.Title()] = [licence]

    return all_broken_events


def fix_missing_event_types():
    all_broken_events = list_missing_events()
    mapping = {}
    for licence_type, events_to_fix in all_broken_events.iteritems():
        urban_config = api.portal.get_tool("portal_urban")
        licence_cfg = getattr(urban_config, licence_type.lower()).urbaneventtypes
        all_event_types = licence_cfg.objectValues()
        for event_name in events_to_fix:
            event_types = [
                evt
                for evt in all_event_types
                if evt.Title() in event_name
                or mapping[licence_type].get(event_name, None) == evt.id
            ]
            if len(event_types) > 1:
                event_types = [
                    evt
                    for evt in event_types
                    if api.content.get_state(evt) == "enabled"
                ]
            if len(event_types) == 1:
                event_type = event_types[0]
                licences_to_fix = events_to_fix[event_name]
                for licence in licences_to_fix:
                    to_fixes = [
                        obj
                        for obj in licence.objectValues()
                        if IUrbanEvent.providedBy(obj) and obj.Title() == event_name
                    ]
                    for to_fix in to_fixes:
                        to_fix.setUrbaneventtypes(event_type)
                        print "fixed event {} on licence {}".format(
                            event_name, licence.Title()
                        )
