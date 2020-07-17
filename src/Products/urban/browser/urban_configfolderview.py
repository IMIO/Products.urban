# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five import BrowserView

from Products.urban.browser.table.urbantable import GeometriciansTable
from Products.urban.browser.table.urbantable import NotariesTable
from Products.urban.browser.table.urbantable import ArchitectsTable
from Products.urban.browser.table.urbantable import ParcellingsTable
from Products.urban.browser.table.urbantable import UrbanTable
from Products.urban import UrbanMessage as _

from plone import api
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import form, field

from zope.interface import Interface
from zope.schema import TextLine


class ISearchForm(Interface):

    name = TextLine(
        title=_(u'Name'),
        required=False
    )


class SearchForm(form.Form):

    method = 'get'
    fields = field.Fields(ISearchForm)
    ignoreContext = True

    def updateWidgets(self):
        super(SearchForm, self).updateWidgets()

    @button.buttonAndHandler(u'Search')
    def handleSearch(self, action):
        data, errors = self.extractData()
        if errors:
            return False


class UrbanConfigFolderView(FormWrapper):
    """
      This manage methods common in all config folders view out of the portal_urban
    """
    form = SearchForm
    table = None  # to override with a z3c.table Table class

    def __init__(self, context, request):
        super(UrbanConfigFolderView, self).__init__(context, request)
        # disable portlets on licences

    def search_submitted(self):
        """
        """
        form_inputs = self.form_instance.extractData()[0]
        submitted = any(form_inputs.values())
        return submitted

    @property
    def search_args(self):
        """
        """
        form_inputs = self.form_instance.extractData()[0]
        return form_inputs

    def update(self):
        super(UrbanConfigFolderView, self).update()
        values = self.context.objectValues()
        if self.search_submitted():
            catalog = api.portal.get_tool('portal_catalog')
            brains = catalog(
                Title=u'*{}*'.format(self.search_args['name']),
                path={'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1}
            )
            values = [b.getObject() for b in brains]
        self.search_result = self.table(self.context, self.request, values=values)
        self.search_result.update()

    def refreshBatch(self, batch_start):
        self.search_result.batchStart = batch_start
        self.search_result.update()

    def getCSSClass(self):
        return 'context'


class ParcellingsFolderView(UrbanConfigFolderView):
    """
      This manage the parcellings folder config view
    """
    table = ParcellingsTable


class ContactsFolderView(UrbanConfigFolderView):
    """ """
    def getEmails(self):
        context = aq_inner(self.context)
        contacts = context.objectValues('Contact')
        raw_emails = ['%s %s <%s>' % (ct.getName1(), ct.getName2(), ct.getEmail()) for ct in contacts if ct.getEmail()]
        emails = '; '.join(raw_emails)
        emails = emails.replace(',', ' ')

        self.request.response.setHeader('Content-type', 'text/plain;charset=utf-8')
        self.request.response.setHeader('Content-Disposition', "attachment; filename=%s_emails.txt" % context.id)
        self.request.response.setHeader('Content-Length', str(len(emails)))
        return emails


class ArchitectsFolderView(ContactsFolderView):
    """
      This manage the architects folder config view
    """
    table = ArchitectsTable

    def getCSSClass(self):
        base_css = super(ArchitectsFolderView, self).getCSSClass()
        return '{} contenttype-architect'.format(base_css)


class GeometriciansFolderView(ContactsFolderView):
    """
      This manage the geometricans folder config view
    """
    table = GeometriciansTable

    def getCSSClass(self):
        base_css = super(GeometriciansFolderView, self).getCSSClass()
        return '{} contenttype-geometrician'.format(base_css)


class NotariesFolderView(ContactsFolderView):
    """
      This manage the notaries folder config view
    """
    table = NotariesTable

    def getCSSClass(self):
        base_css = super(NotariesFolderView, self).getCSSClass()
        return '{} contenttype-notary'.format(base_css)


class SortedTitleFolderView(BrowserView):
    """
      This manage the sorted title folder view
    """
    def renderListing(self):
        return self.renderObjectListing(UrbanTable)

    def renderObjectListing(self, table):
        if not self.context.objectIds():
            return ''
        listing = table(self.context, self.request, values=self.context.objectValues())
        listing.update()
        listing_render = listing.render()
        batch_render = listing.renderBatch()
        return '%s%s' % (listing_render, batch_render)

    def getCSSClass(self):
        base_css = super(SortedTitleFolderView, self).getCSSClass()
        return '{} contenttype-sortedtitleobject'.format(base_css)
