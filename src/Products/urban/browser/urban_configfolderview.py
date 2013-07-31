## -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.urban.browser.urbantable import GeometriciansTable, NotariesTable, \
    ParcellingsTable, ArchitectsTable


class UrbanConfigFolderView(BrowserView):
    """
      This manage methods common in all config folders view out of the portal_urban
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderObjectListing(self, table):
        if not self.context.objectValues():
            return ''
        listing = table(self.context, self.request)
        listing.update()
        listing_render = listing.render()
        batch_render = listing.renderBatch()
        return '%s%s' % (listing_render, batch_render)

    def getCSSClass(self):
        return ''


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
        contacts = context.objectValues('Contact')
        raw_emails = ['%s %s <%s>' % (ct.getName1(), ct.getName2(), ct.getEmail()) for ct in contacts if ct.getEmail()]
        emails = '; '.join(raw_emails)
        emails = emails.replace(',', ' ')

        self.request.response.setHeader('Content-type', 'text/csv;charset=utf-8')
        self.request.response.setHeader('Content-Disposition', "attachment; filename=%s_emails.txt" % context.id)
        self.request.response.setHeader('Content-Length', str(len(emails)))
        return emails


class ArchitectsFolderView(ContactsFolderView):
    """
      This manage the architects folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(ArchitectsTable)

    def getCSSClass(self):
        return 'contenttype-architect button-architect'


class GeometriciansFolderView(ContactsFolderView):
    """
      This manage the geometricans folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(GeometriciansTable)

    def getCSSClass(self):
        return 'contenttype-geometrician button-geometrician'


class NotariesFolderView(ContactsFolderView):
    """
      This manage the notaries folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(NotariesTable)

    def getCSSClass(self):
        return 'contenttype-notary button-notary'
