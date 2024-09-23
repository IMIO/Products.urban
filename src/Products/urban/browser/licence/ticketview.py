# -*- coding: utf-8 -*-

from Products.urban.browser.licence.licenceview import LicenceView
from Products.urban.browser.table.urbantable import InspectionReportsTable
from Products.urban.browser.table.urbantable import PlaintiffTable
from Products.urban.browser.table.urbantable import TenantTable
from Products.CMFPlone import PloneMessageFactory as _

from plone import api


class TicketView(LicenceView):
    def __init__(self, context, request):
        super(TicketView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)

    def getMacroViewName(self):
        return "ticket-macros"

    def getInspectionFields(self, exclude=[]):
        return self.getSchemataFields("urban_inspection", exclude)

    def renderTenantListing(self):
        if not self.context.getTenants():
            return ""
        contacttable = TenantTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderPlaintiffListing(self):
        if not self.context.getPlaintiffs():
            return ""
        contacttable = PlaintiffTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderRepportsListing(self):
        reporttable = InspectionReportsTable(self.context, self.request)
        return self.renderListing(reporttable)
