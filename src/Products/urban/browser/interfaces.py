# -*- coding: utf-8 -*-
from zope.interface import Interface


class IUrbanTable(Interface):
    """
    Marker interface for a table listing urban objects/brains
    """


class IItemForUrbanTable(Interface):
    """
    Wrapper for object/brains that will be displayed in Urban z3c tables
    """

    def getRawValue(self):
        """ return the raw item """

    def getObject(self):
        """ return an AT object """

    def getPortalType(self):
        """ return the object portal type """

    def getURL(self):
        """ used here and there to generate html  links """

    def getState(self):
        """ used for element title css class """

    def getWorkflowTransitions(self):
        """ used in the Actions column """

    def getActions(self):
        """ used in the Actions column """


class IBrainForUrbanTable(IItemForUrbanTable):
    """Marker interface for a brain listing that will be used in urban z3c tables"""


class ISearchResultTable(IUrbanTable):
    """
    Marker interface for a search result table
    """


class ILicenceListingTable(IUrbanTable):
    """
    Marker interface for a search result table
    """


class IParcellingsTable(IUrbanTable):
    """
    Marker interface for a parcellings table
    """


class IContactTable(IUrbanTable):
    """
    Marker interface for a table displaying contacts
    """


class INotariesTable(IUrbanTable):
    """
    Marker interface for a table displaying notaries
    """


class IGeometriciansTable(IUrbanTable):
    """
    Marker interface for a table displaying geometricians
    """


class IArchitectsTable(IUrbanTable):
    """
    Marker interface for a table displaying architects
    """


class IClaimantsTable(IUrbanTable):
    """
    Marker interface for a table displaying claimants
    """


class IRecipientsCadastreTable(Interface):
    """
    Marker interface for a table displaying recipients cadastre (peoples concerned
    by the 50m radius inquiry)
    """


class IParcelsTable(IUrbanTable):
    """
    Marker interface for a table displaying parcels
    """


class IEventsTable(IUrbanTable):
    """
    Marker interface for a table displaying licence events
    """


class IDocumentsTable(IUrbanTable):
    """
    Marker interface for a table displaying generated documents of an urban event
    """


class IAnnexesTable(IUrbanTable):
    """
    Marker interface for a table displaying annexes of an urban event
    """


class IUrbanColumn(Interface):
    """
    Marker interface for an Urban Column (a column expecting IItemForUrbanTable items to display)
    """


class ITitleColumn(Interface):
    """
    Marker interface for a title Column
    """


class IActionsColumn(Interface):
    """
    Marker interface for an Actions Column
    """


class INameColumn(Interface):
    """
    Marker interface for an Name Column
    """


class ILocalityColumn(Interface):
    """
    Marker interface for an Locality Column
    """


class IStreetColumn(Interface):
    """
    Marker interface for an Street Column
    """


class ICell(Interface):
    """
    Interface that describes a table cell behaviour
    """
    def render():
        """ return the HTML render of an object's title """


class ITitleCell(ICell):
    """
    Interface that describes TitleCell behaviour
    """
    def render():
        """ return the html rendering of Title Column cell """


class IActionsCell(ICell):
    """
    Interface that describes TitleCell behaviour
    """
