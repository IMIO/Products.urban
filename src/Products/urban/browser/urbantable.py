## -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.interfaces import ICatalogBrain
from plone.memoize import instance

from z3c.table.table import Table, SequenceTable
from z3c.table.value import ValuesMixin

from zope.interface import implements

from Products.urban.config import URBAN_TYPES
from Products.urban.browser.interfaces import \
    ILicenceListingTable, IContactTable, IParcelsTable, \
    IEventsTable, IDocumentsTable, IAnnexesTable, \
    INotariesTable, IArchitectsTable, IGeometriciansTable, IClaimantsTable, \
    IRecipientsCadastreTable, ISearchResultTable


class UrbanTable(Table):
    """
    """

    batchProviderName = 'plonebatch'
    startBatchingAt = 0

    @instance.memoize
    def getObject(self, item):
        """
         Our columns expect objects (not brains).
         Sometimes we want to display result from a catalog query and only wake up the objects
         that are currently displayed in the batch table.
         This method allow us to instanciate table with brains but to still access the object when
         it needs to be do be displayed by a column.

         We could have look to override the z3c Table method that 'distributes' the items
         through the different columns and to try to convert brains into objects at this moment
         but the problem is ALL the column objects are created before being rendered (even if
         they are bacthed). The rendering is dynamical but not the 'columns creation'/'items distribution'
         which is done only once at table init (see z3c.table.table.Table setUpRows method)
        """
        if ICatalogBrain.providedBy(item):
            return item.getObject()
        return item


class LicenceListingTable(UrbanTable):
    """
    """
    implements(ILicenceListingTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    batchSize = 20


class AllLicencesListingTable(LicenceListingTable):
    """
     Licence listing for urban main page, we sort on creation date rather than title
    """
    sortOn = 'table-creationdateColumn-1'


class SearchResultTable(UrbanTable, SequenceTable):
    """
    """
    implements(ISearchResultTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    batchSize = 20


class ContactTable(UrbanTable):
    """
    """
    implements(IContactTable)

    cssClasses = {'table': 'listing largetable'}


class NotariesTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(INotariesTable)


class GeometriciansTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IGeometriciansTable)


class ArchitectsTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IArchitectsTable)


class ClaimantsTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IClaimantsTable)


class RecipientsCadastreTable(SequenceTable):
    """  """
    implements(IRecipientsCadastreTable)

    cssClasses = {'table': 'listing largetable'}

    @instance.memoize
    def getObject(self, item):
        if ICatalogBrain.providedBy(item):
            return item.getObject()
        return item


class ParcelsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IParcelsTable)

    cssClasses = {'table': 'listing largetable'}


class EventsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IEventsTable)

    sortOn = 'table-eventdateColumn-1'
    cssClasses = {'table': 'listing largetable'}


class DocumentsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IDocumentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing largetable'}


class AnnexesTable(DocumentsTable):
    """
     Documents and annexes use (almost) the same listing tables
    """
    implements(IAnnexesTable)


class ValuesForContactListing (ValuesMixin):
    """  return contact values from the context """

    @property
    def values(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        query_string = {
            'meta_type': 'Contact',
            'path': {
                'query': '/'.join(context.getPhysicalPath()),
                'depth': 1,
            },
        }
        contacts = catalog(query_string)
        return  contacts


class ValuesForLicenceListing (ValuesMixin):
    """ return licence values from the context  """

    @property
    def values(self):
        licence_brains = self.queryLicences()
        return licence_brains

    def queryLicences(self, **kwargs):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        catalog = getToolByName(context, 'portal_catalog')

        queryString = {
            'portal_type': URBAN_TYPES,
            'path': '/'.join(context.getPhysicalPath()),
        }

        foldermanager = request.get('foldermanager', '')
        if foldermanager:
            queryString['folder_manager'] = foldermanager

        state = request.get('review_state', '')
        if state:
            queryString['review_state'] = state

        queryString.update(kwargs)
        licence_brains = catalog(queryString)
        return licence_brains
