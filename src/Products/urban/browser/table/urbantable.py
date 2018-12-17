# -*- coding: utf-8 -*-

from plone import api

from z3c.table.table import Table
from z3c.table.table import SequenceTable

from zope.interface import implements

from Products.ZCatalog.Lazy import LazyMap

from Products.urban.browser.table import interfaces


def getSortMethod(idx):
    """ customized from z3c.table.table.py """

    def getSortKey(item):
        sublist = item[idx]

        def getColumnSortKey(sublist):
            # custom part: we unwrap the item if we are not in an UrbanTable
            column = sublist[1]
            item = sublist[0]
            if not interfaces.IUrbanColumn.providedBy(column):
                item = item.getRawValue()
            # custom part end
            return column.getSortKey(item)

        return getColumnSortKey(sublist)

    return getSortKey


class UrbanTable(Table):
    """
    """

    batchProviderName = 'plonebatch'
    startBatchingAt = 20

    # override setUpRows: use a Lazymap rather than a comprehension list for
    # performance issues (see #6444)
    def setUpRows(self):
        return LazyMap(self.setUpRow, self.values)


class FolderContentTable(UrbanTable):
    """
    """
    implements(interfaces.IFolderContentTable)


class SearchResultTable(UrbanTable, SequenceTable):
    """
    """
    implements(interfaces.ISearchResultTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    batchSize = 20


class ParcellingsTable(FolderContentTable):
    """ Table used to display parcellings"""
    implements(interfaces.IParcellingsTable)

    cssClasses = {'table': 'listing nosort largetable'}
    batchSize = 20


class ContactTable(UrbanTable):
    """
    """
    implements(interfaces.IContactTable)

    sortOn = None
    cssClasses = {'table': 'listing nosort largetable'}


class ApplicantTable(ContactTable):
    """
    """
    implements(interfaces.IApplicantTable)

    cssClasses = {'table': 'listing nosort largetable'}


class ApplicantHistoryTable(ContactTable):
    """
    """
    implements(interfaces.IApplicantHistoryTable)

    cssClasses = {'table': 'listing nosort largetable'}


class ProprietaryTable(ContactTable):
    """
    """
    implements(interfaces.IProprietaryTable)

    cssClasses = {'table': 'listing nosort largetable'}


class NotariesTable(FolderContentTable, ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(interfaces.INotariesTable)

    batchSize = 20


class GeometriciansTable(FolderContentTable, ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(interfaces.IGeometriciansTable)

    batchSize = 20


class ArchitectsTable(FolderContentTable, ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(interfaces.IArchitectsTable)

    batchSize = 20


class ClaimantsTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(interfaces.IClaimantsTable)

    batchSize = 999


class RecipientsCadastreTable(UrbanTable, SequenceTable):
    """  """
    implements(interfaces.IRecipientsCadastreTable)

    cssClasses = {'table': 'listing nosort largetable'}
    batchStart = 0
    batchSize = 999
    startBatchingAt = 999


class ParcelsTable(UrbanTable, SequenceTable):
    """
    """
    implements(interfaces.IParcelsTable)

    cssClasses = {'table': 'listing nosort largetable'}
    batchStart = 0
    batchSize = 999
    startBatchingAt = 999


class EventsTable(UrbanTable, SequenceTable):
    """
    """
    implements(interfaces.IEventsTable)

    sortOn = 'table-eventdateColumn-1'
    cssClasses = {'table': 'listing nosort largetable'}
    batchSize = 999


class DocumentsTable(UrbanTable, SequenceTable):
    """
    """
    implements(interfaces.IDocumentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing largetable'}


class AttachmentsTable(UrbanTable, SequenceTable):
    """
    Documents and annexes use (almost) the same listing tables.
    """
    implements(interfaces.IAttachmentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing nosort largetable'}


class NestedAttachmentsTable(UrbanTable, SequenceTable):
    """
    Render nested attachments from subfolders.
    """
    implements(interfaces.INestedAttachmentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing nosort largetable'}


class InternalOpinionServicesTable(SequenceTable):
    """
    Render nested attachments from subfolders.
    """
    implements(interfaces.IInternalOpinionServicesTable)

    cssClasses = {'table': 'listing largetable'}

    @property
    def values(self):
        registry = api.portal.get_tool('portal_registry')
        all_services = registry['Products.urban.interfaces.IInternalOpinionServices.services']
        if all_services:
            for key, values in all_services.iteritems():
                values['id'] = key
            return all_services.values()
        else:
            return []
