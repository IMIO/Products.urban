# -*- coding: utf-8 -*-

from Products.urban.interfaces import IUrbanWarningCondition
from plone import api
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations

class WarningCondition(object):
    """
    Base class for any object adapting a licence into a warning
    """

    implements(IUrbanWarningCondition)

    def __init__(self, licence):
        self.licence = licence


class ParcelsWarning(WarningCondition):
    """
    Check if parcels are defined.
    """

    def evaluate(self):
        return not self.licence.getParcels()


class BoundTicketSettlementEventDone(WarningCondition):
    """ """

    def evaluate(self):
        bound_tickets = self.licence.get_bound_tickets()
        bound_inspections = self.licence.get_bound_inspections()
        if bound_inspections:
            for inspection in bound_inspections:
                bound_tickets.extend(inspection.get_bound_tickets())
        if bound_tickets:
            for ticket in bound_tickets:
                settlement_event = ticket.getLastSettlement()
                if (
                    settlement_event
                    and api.content.get_state(settlement_event) == "closed"
                ):
                    return True
        return False


class NoticeWarning(WarningCondition):
    """
    Check if license is a notice folder.
    """

    def evaluate(self):
        events = self.licence.getAllEvents()

        for event in events:
            annotations = IAnnotations(event)
            notice = annotations.get("notice_notification", {})

            if notice:
                return True

        return False