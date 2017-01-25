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


class IArchitect(Interface):
    """Marker interface for .Architect.Architect
    """


class IGeometrician(Interface):
    """Marker interface for .Geometrician.Geometrician
    """

CONTACT_INTERFACES = {
    'Architect': IArchitect,
    'Geometrician': IGeometrician,
    'Notary': INotary,  # to be taken into account if notary.py is removed
    'Proprietary': IProprietary,  # to be taken into account if proprietary.py is removed
}

##/code-section HEAD

class IGenericLicence(Interface):
    """Marker interface for .GenericLicence.GenericLicence
    """

class IBaseBuildLicence (IGenericLicence):
    """Marker interface for .Article127.Article127
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

class IBuildLicence(IBaseBuildLicence):
    """Marker interface for .BuildLicence.BuildLicence
    """

class IParcelOutLicence(IBaseBuildLicence):
    """Marker interface for .ParcelOutLicence.ParcelOutLicence
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

class IDeclaration(IGenericLicence):
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

class IUrbanCertificateTwo(IBaseBuildLicence):
    """Marker interface for .UrbanCertificateTwo.UrbanCertificateTwo
    """

class IDivision(Interface):
    """Marker interface for .Division.Division
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

class IUrbanEventOpinionRequest(Interface):
    """Marker interface for .UrbanEventOpinionRequest.UrbanEventOpinionRequest
    """

class IOrganisationTerm(Interface):
    """Marker interface for .OrganisationTerm.OrganisationTerm
    """

class IMiscDemand(Interface):
    """Marker interface for .MiscDemand.MiscDemand
    """

class IPreliminaryNotice(IGenericLicence):
    """Marker interface for .PreliminaryNotice.PreliminaryNotice
    """

class IPatrimonyCertificate(IGenericLicence):
    """Marker interface for .PatrimonyCertificate.PatrimonyCertificate
    """

class IUrbanConfigurationValue(Interface):
    """Marker interface for .UrbanConfigurationValue.UrbanConfigurationValue
    """

class IEnvironmentBase(Interface):
    """Marker interface for .EnvironmentBase.EnvironmentBase
    """

class IEnvironmentRubricTerm(Interface):
    """Marker interface for .EnvironmentRubricTerm.EnvironmentRubricTerm
    """

class ISpecificFeatureTerm(Interface):
    """Marker interface for .SpecificFeatureTerm.SpecificFeatureTerm
    """

class IOpinionRequestEventType(Interface):
    """Marker interface for .OpinionRequestEventType.OpinionRequestEventType
    """

class IEnvironmentLicence(Interface):
    """Marker interface for .EnvironmentLicence.EnvironmentLicence
    """

class IEnvClassThree(Interface):
    """Marker interface for .EnvClassThree.EnvClassThree
    """

class ICorporation(Interface):
    """Marker interface for .Corporation.Corporation
    """

class IClaimant(Interface):
    """Marker interface for .Claimant.Claimant
    """

class IApplicant(Interface):
    """Marker interface for .Applicant.Applicant
    """

class IEnvClassTwo(Interface):
    """Marker interface for .EnvClassTwo.EnvClassTwo
    """

class IEnvClassOne(Interface):
    """Marker interface for .EnvClassOne.EnvClassOne
    """

class IArticle127(IBaseBuildLicence):
    """Marker interface for .Article127.Article127
    """

class IUniqueLicence(IBaseBuildLicence):
    """Marker interface for .Article127.Article127
    """

class IIntegratedLicence(IBaseBuildLicence):
    """Marker interface for .Article127.Article127
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


class ICollegeEvent(Interface):
    __doc__ = _("""ICollege type marker interface""")

class ITechnicalServiceOpinionRequestEvent(Interface):
    __doc__ = _("""ITechnicalServiceOpinionRequest type marker interface""")


class IOpinionRequestEvent(Interface):
    __doc__ = _("""IOpinionRequest type marker interface""")


class IWalloonRegionPrimoEvent(Interface):
    __doc__ = _("""IWalloonRegionPrimo type marker interface""")


class IWalloonRegionOpinionRequestEvent(Interface):
    __doc__ = _("""IWalloonRegionOpinionRequest type marker interface""")


class IWalloonRegionDecisionEvent(Interface):
    __doc__ = _("""IWalloonRegionDecisionEvent type marker interface""")


class ISimpleCollegeEvent(ICollegeEvent):
    __doc__ = _("""ISimpleCollegeEvent type marker interface""")


class IAcknowledgmentEvent(Interface):
    __doc__ = _("""IAcknowledgment type marker interface""")


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


class ITheLicenceCollegeEvent(ICollegeEvent):
    __doc__ = _("""ITheLicenceCollege type marker interface""")


class ITheLicenceEvent(Interface):
    __doc__ = _("""ITheLicence type marker interface""")


class IDisplayingTheDecisionEvent(Interface):
    __doc__ = _("""IDisplayingTheDecisionEvent type marker interface""")


class IRecourseEvent(Interface):
    __doc__ = _("""IRecourseEvent type marker interface""")


class IWorkBeginningEvent(Interface):
    __doc__ = _("""IWorkBeginning type marker interface""")


class IProrogationEvent(Interface):
    __doc__ = _("""IProrogation type marker interface""")


class IUrbanBase(Interface):
    """Marker interface for .Base.UrbanBase
    """


class IUrbanCertificateOne(IGenericLicence):
    """Marker interface for UrbanCertificateOne
    """


class INotaryLetter(Interface):
    """Marker interface for EnvClassThree
    """


class IEnvClassThree(Interface):
    """Marker interface for EnvClassThree
    """


class IEnvCLassOne(Interface):
    """Marker interface for EnvClassOne
    """


class IContactFolder(Interface):
    """Marker interface for folders containing contacts
    """


class IUrbanDoc(Interface):
    """Marker interface for generated document.
    """


class ILicencePortionOut(Interface):
    """Marker interface for portionOut in a licence.
    """


class IOptionalFields(Interface):
    """ """


class IUrbanRootRedirects(Interface):
    """ """
##/code-section FOOT
