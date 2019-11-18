# -*- coding: utf-8 -*-

from plone import api

from zope.annotation import IAnnotations


def setTicketBoundLicence(licence, event):
    annotations = IAnnotations(licence)
    previous_bound_UIDs = annotations.get('urban.ticket_bound_licences', set([]))
    new_bound_UIDs = licence.getField('bound_licences').getRaw(licence)
    if set(previous_bound_UIDs) == set(new_bound_UIDs):
        return

    catalog = api.portal.get_tool('portal_catalog')
    # unrefer previous licence
    if previous_bound_UIDs:
        for previous_licence_brain in catalog(UID=previous_bound_UIDs):
            previous_licence = previous_licence_brain.getObject()
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get('urban.bound_tickets', set([]))
            if licence.UID() in values:
                values.remove(licence.UID())
                previous_licence_annotations['urban.bound_tickets'] = values

    # refer new licence
    if new_bound_UIDs:
        for new_licence_brain in catalog(UID=previous_bound_UIDs):
            new_licence = new_licence_brain.getObject()
            new_licence_annotations = IAnnotations(new_licence)
            values = new_licence_annotations.get('urban.bound_tickets', set([]))
            if licence.UID() not in values:
                values.add(licence.UID())
                new_licence_annotations['urban.bound_tickets'] = values

    annotations['urban.ticket_bound_licences'] = new_bound_UIDs
