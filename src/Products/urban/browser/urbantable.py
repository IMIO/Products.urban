## -*- coding: utf-8 -*-

from z3c.table.table import Table, SequenceTable

from zope.interface import implements

from Products.urban.browser.interfaces import \
    ILicenceListingTable, IContactTable, IParcelsTable, \
    IEventsTable, IDocumentsTable, IAnnexesTable, \
    INotariesTable, IArchitectsTable, IGeometriciansTable, IClaimantsTable, \
    IRecipientsCadastreTable, ISearchResultTable, IParcellingsTable, IUrbanColumn


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
    startBatchingAt = 0


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


class ParcellingsTable(UrbanTable):
    """ Table used to display parcellings"""
    implements(IParcellingsTable)

    cssClasses = {'table': 'listing largetable'}
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

    batchSize = 20


class GeometriciansTable(ContactTable):
    """
     Same as a ContactTable.
     We define our own class so we can implement a marker interface used to find
     the correct translation for column headers
    """
    implements(IGeometriciansTable)

    batchSize = 20


class ArchitectsTable(ContactTable):
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
