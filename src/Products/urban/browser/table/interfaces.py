# -*- coding: utf-8 -*-
from zope.interface import Interface


class IUrbanTable(Interface):
    """
    Marker interface for a table listing urban objects/brains
    """


class IFolderContentTable(IUrbanTable):
    """
    Marker interface for a table listing all objects of a folderish.
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


class IBrainForUrbanTable(IItemForUrbanTable):
    """Marker interface for a brain listing that will be used in urban z3c tables"""


class IObjectForUrbanTable(IItemForUrbanTable):
    """Marker interface for an object listing that will be used in urban z3c tables"""


class ISearchResultTable(IUrbanTable):
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


class IApplicantTable(IContactTable):
    """
    Marker interface for a table displaying applicants
    """


class IApplicantHistoryTable(IContactTable):
    """
    Marker interface for a table displaying applicants
    """


class IProprietaryTable(IContactTable):
    """
    Marker interface for a table displaying proprietaries
    """


class IProprietaryHistoryTable(IContactTable):
    """
    Marker interface for a table displaying proprietaries
    """


class ITenantTable(IContactTable):
    """
    Marker interface for a table displaying tenants
    """


class IPlaintiffTable(IContactTable):
    """
    Marker interface for a table displaying plaintiffs
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


class IRecipientsCadastreTable(IUrbanTable):
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


class IAttachmentsTable(IUrbanTable):
    """
    Marker interface for a table displaying attachments of an urban event
    """


class ILicenceAttachmentsTable(IAttachmentsTable):
    """
    Marker interface for a table displaying attachments of an urban event
    """


class IInternalOpinionServicesTable(Interface):
    """
    Marker interface for a table displaying internal services for opinion requests.
    """


class INestedAttachmentsTable (IAttachmentsTable):
    """
    Marker interface for a table displaying all attachments nested in licence events.
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


class IAddressColumn(Interface):
    """
    Marker interface for a licence worklocation Column
    """


class IParcelReferencesColumn(Interface):
    """
    Marker interface for a licence worklocation Column
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


class IInspectionReportsTable(Interface):
    """
    Marker interface for a table displaying inspection report events.
    """
