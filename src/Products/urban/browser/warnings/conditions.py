# -*- coding: utf-8 -*-

from plone import api

from Products.urban.interfaces import IUrbanWarningCondition

from zope.interface import implements


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
    """
    """

    def evaluate(self):
        bound_tickets = self.licence.get_bound_tickets()
        bound_inspections = self.licence.get_bound_inspections()
        if bound_inspections:
            for inspection in bound_inspections:
                bound_tickets.extend(inspection.get_bound_tickets())
        if bound_tickets:
            for ticket in bound_tickets:
                settlement_event = ticket.getLastSettlement()
                if settlement_event and api.content.get_state(settlement_event) == 'closed':
                    return True
        return False
