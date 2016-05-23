# -*- coding: utf-8 -*-

from plone import api


def fix():
    """
    """
    catalog = api.portal.get_tool('portal_catalog')
    or_events = [brain.getObject() for brain in catalog(portal_type='UrbanEventOpinionRequest')]
    for or_event in or_events:
        if not or_event.getLinkedInquiry():
            or_event.setLinkedInquiry(or_event.aq_parent.UID())
