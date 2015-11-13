## -*- coding: utf-8 -*-

from z3c.table.table import Table
from z3c.table.table import SequenceTable

from zope.interface import implements

from Products.ZCatalog.Lazy import LazyMap

from Products.urban.browser.table.interfaces import IApplicantTable
from Products.urban.browser.table.interfaces import IArchitectsTable
from Products.urban.browser.table.interfaces import IAttachmentsTable
from Products.urban.browser.table.interfaces import IClaimantsTable
from Products.urban.browser.table.interfaces import IContactTable
from Products.urban.browser.table.interfaces import IDocumentsTable
from Products.urban.browser.table.interfaces import IEventsTable
from Products.urban.browser.table.interfaces import IFolderContentTable
from Products.urban.browser.table.interfaces import IGeometriciansTable
from Products.urban.browser.table.interfaces import INestedAttachmentsTable
from Products.urban.browser.table.interfaces import INotariesTable
from Products.urban.browser.table.interfaces import IParcellingsTable
from Products.urban.browser.table.interfaces import IParcelsTable
from Products.urban.browser.table.interfaces import IProprietaryTable
from Products.urban.browser.table.interfaces import IRecipientsCadastreTable
from Products.urban.browser.table.interfaces import ISearchResultTable
from Products.urban.browser.table.interfaces import IUrbanColumn


def getSortMethod(idx):
    """ customized from z3c.table.table.py """

    def getSortKey(item):
        sublist = item[idx]

        def getColumnSortKey(sublist):
            # custom part: we unwrap the item if we are not in an UrbanTable
            column = sublist[1]
            item = sublist[0]
            if not IUrbanColumn.providedBy(column):
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
    implements(IFolderContentTable)


class SearchResultTable(UrbanTable, SequenceTable):
    """
    """
    implements(ISearchResultTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    batchSize = 20


class ParcellingsTable(FolderContentTable):
    """ Table used to display parcellings"""
    implements(IParcellingsTable)

    cssClasses = {'table': 'listing largetable'}
    batchSize = 20


class ContactTable(UrbanTable):
    """
    """
    implements(IContactTable)

    sortOn = None
    cssClasses = {'table': 'listing largetable'}


class ApplicantTable(ContactTable):
    """
    """
    implements(IApplicantTable)

    cssClasses = {'table': 'listing largetable'}


class ProprietaryTable(ContactTable):
    """
    """
    implements(IProprietaryTable)

    cssClasses = {'table': 'listing largetable'}


class NotariesTable(FolderContentTable, ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(INotariesTable)

    batchSize = 20


class GeometriciansTable(FolderContentTable, ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IGeometriciansTable)

    batchSize = 20


class ArchitectsTable(FolderContentTable, ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IArchitectsTable)

    batchSize = 20


class ClaimantsTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IClaimantsTable)


class RecipientsCadastreTable(UrbanTable, SequenceTable):
    """  """
    implements(IRecipientsCadastreTable)

    cssClasses = {'table': 'listing largetable'}
    batchStart = 0
    batchSize = 999
    startBatchingAt = 999


class ParcelsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IParcelsTable)

    cssClasses = {'table': 'listing largetable'}
    batchStart = 0
    batchSize = 999
    startBatchingAt = 999


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


class AttachmentsTable(UrbanTable, SequenceTable):
    """
    Documents and annexes use (almost) the same listing tables.
    """
    implements(IAttachmentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing largetable'}


class NestedAttachmentsTable(UrbanTable, SequenceTable):
    """
    Render nested attachments from subfolders.
    """
    implements(INestedAttachmentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing largetable'}
