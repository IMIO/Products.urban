## -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five import BrowserView

from Products.urban.browser.table.urbantable import GeometriciansTable
from Products.urban.browser.table.urbantable import NotariesTable
from Products.urban.browser.table.urbantable import ArchitectsTable
from Products.urban.browser.table.urbantable import ParcellingsTable
from Products.urban.browser.table.urbantable import UrbanTable


class UrbanConfigFolderView(BrowserView):
    """
    This manage methods common in all config folders view out of the portal_urban
    """

    def __init__(self, context, request):
        super(UrbanConfigFolderView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderObjectListing(self, table):
        if not self.context.objectIds():
            return ""
        listing = table(self.context, self.request)
        listing.update()
        listing_render = listing.render()
        batch_render = listing.renderBatch()
        return "%s%s" % (listing_render, batch_render)

    def getCSSClass(self):
        return "context"


class ParcellingsFolderView(UrbanConfigFolderView):
    """
    This manage the parcellings folder config view
    """

    def renderListing(self):
        return self.renderObjectListing(ParcellingsTable)


class ContactsFolderView(UrbanConfigFolderView):
    """ """

    def getEmails(self):
        context = aq_inner(self.context)
        contacts = context.objectValues("Contact")
        raw_emails = [
            "%s %s <%s>" % (ct.getName1(), ct.getName2(), ct.getEmail())
            for ct in contacts
            if ct.getEmail()
        ]
        emails = "; ".join(raw_emails)
        emails = emails.replace(",", " ")

        self.request.response.setHeader("Content-type", "text/plain;charset=utf-8")
        self.request.response.setHeader(
            "Content-Disposition", "attachment; filename=%s_emails.txt" % context.id
        )
        self.request.response.setHeader("Content-Length", str(len(emails)))
        return emails


class ArchitectsFolderView(ContactsFolderView):
    """
    This manage the architects folder config view
    """

    def renderListing(self):
        return self.renderObjectListing(ArchitectsTable)

    def getCSSClass(self):
        base_css = super(ArchitectsFolderView, self).getCSSClass()
        return "{} contenttype-architect".format(base_css)


class GeometriciansFolderView(ContactsFolderView):
    """
    This manage the geometricans folder config view
    """

    def renderListing(self):
        return self.renderObjectListing(GeometriciansTable)

    def getCSSClass(self):
        base_css = super(GeometriciansFolderView, self).getCSSClass()
        return "{} contenttype-geometrician".format(base_css)


class NotariesFolderView(ContactsFolderView):
    """
    This manage the notaries folder config view
    """

    def renderListing(self):
        return self.renderObjectListing(NotariesTable)

    def getCSSClass(self):
        base_css = super(NotariesFolderView, self).getCSSClass()
        return "{} contenttype-notary".format(base_css)


class SortedTitleFolderView(BrowserView):
    """
    This manage the sorted title folder view
    """

    def renderListing(self):
        return self.renderObjectListing(UrbanTable)

    def renderObjectListing(self, table):
        if not self.context.objectIds():
            return ""
        listing = table(self.context, self.request, values=self.context.objectValues())
        listing.update()
        listing_render = listing.render()
        batch_render = listing.renderBatch()
        return "%s%s" % (listing_render, batch_render)

    def getCSSClass(self):
        base_css = super(SortedTitleFolderView, self).getCSSClass()
        return "{} contenttype-sortedtitleobject".format(base_css)
