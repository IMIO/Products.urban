# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
from zope.interface.interfaces import IInterface

from Products.Archetypes.interfaces import IVocabulary
from Products.urban import UrbanMessage as _


class IProprietary(Interface):
    """Marker interface for .Proprietary.Proprietary
    """
class INotary(Interface):
    """Marker interface for .Notary.Notary
    """
class IApplicant(Interface):
    """Marker interface for .Architect.Architect
    """
class IArchitect(Interface):
    """Marker interface for .Architect.Architect
    """

CONTACT_INTERFACES = {
    'Applicant' : IApplicant,
    'Architect' : IArchitect,
#    'Notary' : INotary,  # to be taken into account if notary.py is removed
#    'Proprietary' : IProprietary, # to be taken into account if proprietary.py is removed
}

##/code-section HEAD

class IGenericLicence(Interface):
    """Marker interface for .GenericLicence.GenericLicence
    """

class IContact(Interface):
    """Marker interface for .Contact.Contact
    """

class IUrbanTool(Interface):
    """Marker interface for .UrbanTool.UrbanTool
    """

class IStreet(Interface):
    """Marker interface for .Street.Street
    """

class IUrbanEvent(Interface):
    """Marker interface for .UrbanEvent.UrbanEvent
    """

class IUrbanEventType(Interface):
    """Marker interface for .UrbanEventType.UrbanEventType
    """

class IRecipient(Interface):
    """Marker interface for .Recipient.Recipient
    """

class IBuildLicence(Interface):
    """Marker interface for .BuildLicence.BuildLicence
    """

class IParcelOutLicence(Interface):
    """Marker interface for .ParcelOutLicence.ParcelOutLicence
    """

class IGeometrician(Interface):
    """Marker interface for .Geometrician.Geometrician
    """

class IFolderManager(Interface):
    """Marker interface for .FolderManager.FolderManager
    """

class IUrbanVocabularyTerm(Interface):
    """Marker interface for .UrbanVocabularyTerm.UrbanVocabularyTerm
    """

class IPortionOut(Interface):
    """Marker interface for .PortionOut.PortionOut
    """

class IRecipientCadastre(Interface):
    """Marker interface for .RecipientCadastre.RecipientCadastre
    """

class ILayer(Interface):
    """Marker interface for .Layer.Layer
    """

class IDeclaration(Interface):
    """Marker interface for .Declaration.Declaration
    """

class IParcellingTerm(Interface):
    """Marker interface for .ParcellingTerm.ParcellingTerm
    """

class IPcaTerm(Interface):
    """Marker interface for .PcaTerm.PcaTerm
    """

class ICity(Interface):
    """Marker interface for .City.City
    """

class IUrbanCertificateBase(Interface):
    """Marker interface for .UrbanCertificateBase.UrbanCertificateBase
    """

class IUrbanCertificateTwo(Interface):
    """Marker interface for .UrbanCertificateTwo.UrbanCertificateTwo
    """

class IEnvironmentalDeclaration(Interface):
    """Marker interface for .EnvironmentalDeclaration.EnvironmentalDeclaration
    """

class IEquipment(Interface):
    """Marker interface for .Equipment.Equipment
    """

class ILot(Interface):
    """Marker interface for .Lot.Lot
    """

class IDivision(Interface):
    """Marker interface for .Division.Division
    """

class IWorkLocation(Interface):
    """Marker interface for .WorkLocation.WorkLocation
    """

class IUrbanDelay(Interface):
    """Marker interface for .UrbanDelay.UrbanDelay
    """

class ILocality(Interface):
    """Marker interface for .Locality.Locality
    """

class ILicenceConfig(Interface):
    """Marker interface for .LicenceConfig.LicenceConfig
    """

class IPersonTitleTerm(Interface):
    """Marker interface for .PersonTitleTerm.PersonTitleTerm
    """

class IInquiry(Interface):
    """Marker interface for .Inquiry.Inquiry
    """

class IUrbanEventInquiry(Interface):
    """Marker interface for .UrbanEventInquiry.UrbanEventInquiry
    """

##code-section FOOT
class IEventTypeType(IInterface):
    """
    Basic event type
    """

class IOpinionRequestEvent(Interface):
    __doc__ = _("""IOpinionRequest type marker interface""")


class IWalloonRegionPrimoEvent(Interface):
    __doc__ = _("""IWalloonRegionPrimo type marker interface""")

class IWalloonRegionOpinionRequestEvent(Interface):
    __doc__ = _("""IWalloonRegionOpinionRequest type marker interface""")


class IAcknowledgmentEvent(Interface):
    __doc__ = _("""IAcknowledgment type marker interface""")


class ICollegeReportEvent(Interface):
    __doc__ = _("""ICollegeReport type marker interface""")


class IDepositEvent(Interface):
    __doc__ = _("""IDeposit type marker interface""")


class IMissingPartDepositEvent(IDepositEvent):
    __doc__ = _("""IMissingPartDeposit type marker interface""")


class IModificationDepositEvent(IDepositEvent):
    __doc__ = _("""IModificationDeposit type marker interface""")


class IMissingPartEvent(Interface):
    __doc__ = _("""IMissingPart type marker interface""")


class IInquiryEvent(Interface):
    __doc__ = _("""IInquiry type marker interface""")


class ICollegeReportEvent(Interface):
    __doc__ = _("""ICollegeReport type marker interface""")


class ITheLicenceEvent(Interface):
    __doc__ = _("""ITheLicence type marker interface""")


class IWorkBeginningEvent(Interface):
    __doc__ = _("""IWorkBeginning type marker interface""")


class IUrbanBase(Interface):
    """Marker interface for .Base.UrbanBase
    """

class IReferenceableVocabulary(IVocabulary):
    """vocabulary used in referenceintegrity"""

    def getObjectsSet(content_instance, values):
        """returns the set of objects corresponding to the values"""



##/code-section FOOT
