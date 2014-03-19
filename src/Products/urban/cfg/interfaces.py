# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
from zope.interface.interfaces import IInterface

from Products.urban import UrbanMessage as _
##/code-section HEAD

class IPersonTitleTerm(Interface):
    """Marker interface for .PersonTitleTerm.PersonTitleTerm
    """

class IUrbanEventType(Interface):
    """Marker interface for .UrbanEventType.UrbanEventType
    """

class IOpinionRequestEventType(Interface):
    """Marker interface for .OpinionRequestEventType.OpinionRequestEventType
    """

class IUrbanDelay(Interface):
    """Marker interface for .UrbanDelay.UrbanDelay
    """

class IUrbanVocabularyTerm(Interface):
    """Marker interface for .UrbanVocabularyTerm.UrbanVocabularyTerm
    """

class ISpecificFeatureTerm(Interface):
    """Marker interface for .SpecificFeatureTerm.SpecificFeatureTerm
    """

class IUrbanConfigurationValue(Interface):
    """Marker interface for .UrbanConfigurationValue.UrbanConfigurationValue
    """

class IOrganisationTerm(Interface):
    """Marker interface for .OrganisationTerm.OrganisationTerm
    """

class IPcaTerm(Interface):
    """Marker interface for .PcaTerm.PcaTerm
    """

class IFolderManager(Interface):
    """Marker interface for .FolderManager.FolderManager
    """

class ILicenceConfig(Interface):
    """Marker interface for .LicenceConfig.LicenceConfig
    """

class IUrbanTool(Interface):
    """Marker interface for .UrbanTool.UrbanTool
    """

class ICity(Interface):
    """Marker interface for .City.City
    """

class ILocality(Interface):
    """Marker interface for .Locality.Locality
    """

class IStreet(Interface):
    """Marker interface for .Street.Street
    """

class IEnvironmentRubricTerm(Interface):
    """Marker interface for .EnvironmentRubricTerm.EnvironmentRubricTerm
    """

##code-section FOOT


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


##/code-section FOOT