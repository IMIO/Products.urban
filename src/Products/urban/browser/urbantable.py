## -*- coding: utf-8 -*-

from Products.ZCatalog.interfaces import ICatalogBrain
from plone.memoize import instance

from z3c.table.table import Table, SequenceTable
from z3c.table.interfaces import INoneCell

from zope.interface import implements
from zope.component import queryAdapter

from Products.urban.browser.interfaces import IItemForUrbanTable
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

    def setUpRows(self):
        """ customized from z3c.table.table.py """
        # custom part: we wrap the item into a class that will help us to compute informations
        # on the object at table rendering time
        values = [queryAdapter(value, IItemForUrbanTable) for value in self.values]
        # custom part end
        return [self.setUpRow(item) for item in values]

    def sortRows(self):
        """ copied from z3c.table.table.py to use our own getSortKey method """
        if self.sortOn is not None and self.rows and self.columns:
            sortOnIdx = self.columnIndexById.get(self.sortOn, 0)
            sortKeyGetter = getSortMethod(sortOnIdx)
            rows = sorted(self.rows, key=sortKeyGetter)
            if self.sortOrder in self.reverseSortOrderNames:
                rows.reverse()
            self.rows = rows

    def renderCell(self, item, column, colspan=0):
        """ customized from z3c.table.table.py """
        if INoneCell.providedBy(column):
            return u''
        cssClass = column.cssClasses.get('td')
        cssClass = self.getCSSHighlightClass(column, item, cssClass)
        cssClass = self.getCSSSortClass(column, cssClass)
        cssClass = self.getCSSClass('td', cssClass)
        colspanStr = colspan and ' colspan="%s"' % colspan or ''
        # custom part: we unwrap the item if we are not in an UrbanColumn
        if not IUrbanColumn.providedBy(column):
            item = item.getRawValue()
        # custom part end
        try:
            return u'\n      <td%s%s>%s</td>' % (cssClass, colspanStr, column.renderCell(item))
        except:
            import ipdb; ipdb.set_trace()


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
    batchSize = 20


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
