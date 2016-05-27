# -*- coding: utf-8 -*-

from plone import api

from Products.urban.events.environmentLicenceEvents import createLicenceExpirationEvent
from Products.urban.interfaces import IAcknowledgmentEvent
from Products.urban.interfaces import ITheLicenceEvent


def recompute_due_dates():
    """
    Send "ObjectModifiedEvent' on all the acknowledgement or Licence events
    to recompute due date event.
    """

    marker_interfaces = [ITheLicenceEvent.__identifier__, IAcknowledgmentEvent.__identifier__]
    catalog = api.portal.get_tool('portal_catalog')

    event_brains = catalog(object_provides=marker_interfaces)

    for event_brain in event_brains:
        event = event_brain.getObject()
        createLicenceExpirationEvent(event, None)
