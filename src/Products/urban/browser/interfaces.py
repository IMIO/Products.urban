# -*- coding: utf-8 -*-
from zope.interface import Interface


class IUrbanTable(Interface):
    """
    Marker interface for a table listing urban objects/brains
    """


class ISearchResultTable(IUrbanTable):
    """
    Marker interface for a search result table
    """


class ILicenceListingTable(IUrbanTable):
    """
    Marker interface for a search result table
    """


class IContactTable(IUrbanTable):
    """
    Marker interface for a table displaying contacts
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


class ITitleColumn(Interface):
    """
    Marker interface for a title Column
    """


class IActionsColumn(Interface):
    """
    Marker interface for an Actions Column
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
