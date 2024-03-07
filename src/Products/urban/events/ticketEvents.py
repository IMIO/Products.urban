# -*- coding: utf-8 -*-

from plone import api

from zope.annotation import IAnnotations
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


def setTicketBoundInspection(ticket, event):
    annotations = IAnnotations(ticket)
    previous_bound_UIDs = annotations.get("urban.ticket_bound_inspections") or ""
    new_bound_UIDs = ticket.getField("bound_inspection").getRaw(ticket) or ""
    if previous_bound_UIDs == new_bound_UIDs:
        return

    catalog = api.portal.get_tool("portal_catalog")
    # unrefer previous ticket
    if previous_bound_UIDs:
        for previous_inspection_brain in catalog(UID=previous_bound_UIDs):
            previous_inspection = previous_inspection_brain.getObject()
            previous_inspection_annotations = IAnnotations(previous_inspection)
            values = previous_inspection_annotations.get("urban.bound_tickets") or set(
                []
            )
            if ticket.UID() in values:
                values.remove(ticket.UID())
                previous_inspection_annotations["urban.bound_tickets"] = values
            notify(ObjectModifiedEvent(previous_inspection))

    # refer new ticket
    if any(new_bound_UIDs):
        for new_inspection_brain in catalog(UID=new_bound_UIDs):
            new_inspection = new_inspection_brain.getObject()
            new_inspection_annotations = IAnnotations(new_inspection)
            values = new_inspection_annotations.get("urban.bound_tickets") or set([])
            if ticket.UID() not in values:
                values.add(ticket.UID())
                new_inspection_annotations["urban.bound_tickets"] = values
            notify(ObjectModifiedEvent(new_inspection))

    annotations["urban.ticket_bound_inspections"] = new_bound_UIDs


def setTicketBoundLicence(ticket, event):
    annotations = IAnnotations(ticket)
    previous_bound_UIDs = list(
        annotations.get("urban.ticket_bound_licences") or set([])
    )
    new_bound_UIDs = ticket.getField("bound_licences").getRaw(ticket) or []
    if set(previous_bound_UIDs) == set(new_bound_UIDs):
        return

    catalog = api.portal.get_tool("portal_catalog")
    # unrefer previous ticket
    if previous_bound_UIDs:
        for previous_licence_brain in catalog(UID=previous_bound_UIDs):
            previous_licence = previous_licence_brain.getObject()
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get("urban.bound_tickets") or set([])
            if ticket.UID() in values:
                values.remove(ticket.UID())
                previous_licence_annotations["urban.bound_tickets"] = values

    # refer new ticket
    if new_bound_UIDs:
        for new_licence_brain in catalog(UID=new_bound_UIDs):
            new_licence = new_licence_brain.getObject()
            new_licence_annotations = IAnnotations(new_licence)
            values = new_licence_annotations.get("urban.bound_tickets") or set([])
            if ticket.UID() not in values:
                values.add(ticket.UID())
                new_licence_annotations["urban.bound_tickets"] = values

    annotations["urban.ticket_bound_licences"] = new_bound_UIDs


def notifyBoundInspections(ticket, event):
    """
    When changing the ticket state -> notify the bound inspections
    """
    catalog = api.portal.get_tool("portal_catalog")
    annotations = IAnnotations(ticket)
    inspection_UIDs = annotations.get("urban.ticket_bound_inspections") or ""
    for inspection_brain in catalog(UID=inspection_UIDs):
        inspection = inspection_brain.getObject()
        notify(ObjectModifiedEvent(inspection))
