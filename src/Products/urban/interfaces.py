# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
from zope.interface.interfaces import IInterface

from Products.urban import UrbanMessage as _


class IProprietary(Interface):
    """Marker interface for .Proprietary.Proprietary
    """


class INotary(Interface):
    """Marker interface for .Notary.Notary
    """


class IApplicant(Interface):
    """Marker interface for .Applicant
    """


class IArchitect(Interface):
    """Marker interface for .Architect.Architect
    """


class IGeometrician(Interface):
    """Marker interface for .Geometrician.Geometrician
    """

CONTACT_INTERFACES = {
    'Applicant': IApplicant,
    'Architect': IArchitect,
    # 'Notary' : INotary,  # to be taken into account if notary.py is removed
    # 'Proprietary' : IProprietary, # to be taken into account if proprietary.py is removed
}

##/code-section HEAD

class IGenericLicence(Interface):
    """Marker interface for .GenericLicence.GenericLicence
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

class ILayer(Interface):
    """Marker interface for .Layer.Layer
    """

class IDeclaration(Interface):
    """Marker interface for .Declaration.Declaration
    """

class IUrbanCertificateBase(Interface):
    """Marker interface for .UrbanCertificateBase.UrbanCertificateBase
    """

class IUrbanCertificateTwo(Interface):
    """Marker interface for .UrbanCertificateTwo.UrbanCertificateTwo
    """

class IDivision(Interface):
    """Marker interface for .Division.Division
    """

class IMiscDemand(Interface):
    """Marker interface for .MiscDemand.MiscDemand
    """

class IEnvironmentBase(Interface):
    """Marker interface for .EnvironmentBase.EnvironmentBase
    """

class IEnvironmentLicence(Interface):
    """Marker interface for .EnvironmentLicence.EnvironmentLicence
    """

##code-section FOOT
class ILicenceContainer(Interface):
    """
    Marker interface for a folder containing Licences
    """


class IEventTypeType(IInterface):
    """
    Basic event type
    """


class ITechnicalServiceOpinionRequestEvent(Interface):
    __doc__ = _("""ITechnicalServiceOpinionRequest type marker interface""")


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


class ICommunalCouncilEvent(Interface):
    __doc__ = _("""ICommunalCouncil type marker interface""")


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


class ILicenceDeliveryEvent(Interface):
    __doc__ = _("""ILicenceDelivery type marker interface""")


class ILicenceExpirationEvent(Interface):
    __doc__ = _("""ILicenceExpiration type marker interface""")


class ICollegeReportEvent(Interface):
    __doc__ = _("""ICollegeReport type marker interface""")


class ITheLicenceEvent(Interface):
    __doc__ = _("""ITheLicence type marker interface""")


class IWorkBeginningEvent(Interface):
    __doc__ = _("""IWorkBeginning type marker interface""")


class IProrogationEvent(Interface):
    __doc__ = _("""IProrogation type marker interface""")


class IUrbanBase(Interface):
    """Marker interface for .Base.UrbanBase
    """


class IUrbanCertificateOne(Interface):
    """Marker interface for UrbanCertificateOne
    """


class INotaryLetter(Interface):
    """Marker interface for EnvClassThree
    """


class IEnvClassThree(Interface):
    """Marker interface for EnvClassThree
    """

class IEnvCLassOne(Interface):
    """Marker interface for .EnvClassOne
    """


class IContactFolder(Interface):
    """Marker interface for folders containing contacts
    """

##/code-section FOOT