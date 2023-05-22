# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

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


class IGenericLicence(Interface):
    """Marker interface for .GenericLicence.GenericLicence
    """


class IBaseAllBuildLicence(IGenericLicence):
    """Marker interface for all the buildilicence likes procedures (cwatup and CODT).
    """


class IBaseBuildLicence (IBaseAllBuildLicence):
    """Marker interface for all buildlicence procedures (cwatup)
    """


class ICODT_BaseBuildLicence (IBaseAllBuildLicence):
    """Marker interface for all buildlicence procedures (codt)
    """


class ICODT_UrbanCertificateBase (IGenericLicence):
    """Marker interface for all notaryletter/urbancertifcateone procedures (codt)
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


class IUrbanEventInspectionReport(Interface):
    """Marker interface for UrbanEventInspectionReport
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


class ICODT_BuildLicence(ICODT_BaseBuildLicence):
    """Marker interface for CODT_BuildLicence
    """


class ICODT_CommercialLicence(ICODT_BaseBuildLicence):
    """Marker interface for CODT_CommercialLicence
    """


class IParcelOutLicence(IBaseBuildLicence):
    """Marker interface for .ParcelOutLicence.ParcelOutLicence
    """


class ICODT_ParcelOutLicence(IBaseBuildLicence):
    """Marker interface for CODT_ParcelOutLicence
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


class ICODT_UrbanCertificateTwo(ICODT_BaseBuildLicence):
    """Marker interface for CODT_ UrbanCertificateTwo
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


class ICODT_Inquiry(IInquiry):
    """Marker interface for .Inquiry.Inquiry
    """


class ICODT_UniqueLicenceInquiry(IInquiry):
    """Marker interface for CODT_uniqueLicence inquiry
    """


class IUrbanEventBaseInquiry(Interface):
    """base arker interface for inquiry events
    """


class IUrbanEventInquiry(IUrbanEventBaseInquiry):
    """Marker interface for .UrbanEventInquiry.UrbanEventInquiry
    """


class IUrbanEventAnnouncement(IUrbanEventBaseInquiry):
    """Marker interface for .UrbanEventAnnouncement.UrbanEventAnnouncement
    """


class IUrbanEventOpinionRequest(Interface):
    """Marker interface for .UrbanEventOpinionRequest.UrbanEventOpinionRequest
    """


class IUrbanEventFollowUp(Interface):
    __doc__ = _("""IUrbanEventFollowUp type marker interface""")


class IOrganisationTerm(Interface):
    """Marker interface for .OrganisationTerm.OrganisationTerm
    """


class IMiscDemand(Interface):
    """Marker interface for .MiscDemand.MiscDemand
    """


class IPreliminaryNotice(IGenericLicence):
    """Marker interface for .PreliminaryNotice.PreliminaryNotice
    """


class IProjectMeeting(IGenericLicence):
    """Marker interface for .ProjectMeeting.ProjectMeeting
    """


class IPatrimonyCertificate(IGenericLicence):
    """Marker interface for .PatrimonyCertificate.PatrimonyCertificate
    """


class IUrbanConfigurationValue(Interface):
    """Marker interface for .UrbanConfigurationValue.UrbanConfigurationValue
    """


class IUrbanConfigurationFolder(Interface):
    """Marker interface for .UrbanConfigurationValue.UrbanConfigurationValue
    """


class IEnvironmentBase(IGenericLicence):
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


class IFollowUpEventType(Interface):
    """Marker interface for .FollowUpEventType.FollowUpEventType
    """


class IEnvironmentLicence(IEnvironmentBase):
    """Marker interface for .EnvironmentLicence.EnvironmentLicence
    """


class IEnvClassThree(IEnvironmentBase):
    """Marker interface for .EnvClassThree.EnvClassThree
    """


class ICorporation(Interface):
    """Marker interface for .Corporation.Corporation
    """


class ICouple(Interface):
    """Marker interface for .Couple.Couple
    """


class IClaimant(Interface):
    """Marker interface for .Claimant.Claimant
    """


class IApplicant(Interface):
    """Marker interface for .Applicant.Applicant
    """


class IEnvClassTwo(IEnvironmentLicence):
    """Marker interface for .EnvClassTwo.EnvClassTwo
    """


class IEnvClassOne(IEnvironmentLicence):
    """Marker interface for .EnvClassOne.EnvClassOne
    """


class IEnvClassBordering(IEnvironmentLicence):
    """Marker interface for EnvClassBordering
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


class ICODT_Article127(ICODT_BaseBuildLicence):
    """Marker interface for CODT_ Article127
    """


class ICODT_UniqueLicence(ICODT_BaseBuildLicence):
    """Marker interface for CODT_ UniqueLicence
    """


class ICODT_IntegratedLicence(ICODT_BaseBuildLicence):
    """Marker interface for  CODT_ IntegratedLicence
    """


class ILicenceContainer(Interface):
    """
    Marker interface for a folder containing Licences
    """


class IEventTypeType(IInterface):
    """
    Basic event type
    """


class IExplosivesPossession(IGenericLicence):
    """
    Marker interface for explosives possession
    """


class IInspection(IGenericLicence):
    """
    Marker interface for inspection
    """


class ITicket(IGenericLicence):
    """
    Marker interface for inspection
    """


class IRoadDecree(ICODT_BaseBuildLicence):
    """
    Marker interface for road degree
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


class IMayorCollegeEvent(ICollegeEvent):
    __doc__ = _("""IMayorCollegeEvent type marker interface""")


class IEnvironmentSimpleCollegeEvent(ICollegeEvent):
    __doc__ = _("""IEnvironmentSimpleCollegeEvent type marker interface""")


class ITransmitToSPWEvent(Interface):
    __doc__ = _("""ITransmitToSPWEvent type marker interface""")


class IAcknowledgmentEvent(Interface):
    __doc__ = _("""IAcknowledgment type marker interface""")


class IDefaultCODTAcknowledgmentEvent(IAcknowledgmentEvent):
    __doc__ = _("""IDefaultCODTAcknowledgmentEvent type marker interface""")


class ICommunalCouncilEvent(Interface):
    __doc__ = _("""ICommunalCouncil type marker interface""")


class IDepositEvent(Interface):
    __doc__ = _("""IDeposit type marker interface""")


class IMissingPartDepositEvent(IDepositEvent):
    __doc__ = _("""IMissingPartDeposit type marker interface""")


class IMissingPartTransmitToSPWEvent(IDepositEvent):
    __doc__ = _("""IMissingPartTransmitToSPWEvent type marker interface""")


class IModificationDepositEvent(IDepositEvent):
    __doc__ = _("""IModificationDeposit type marker interface""")


class IMissingPartEvent(Interface):
    __doc__ = _("""IMissingPart type marker interface""")


class ICODTProcedureChoiceNotified(Interface):
    __doc__ = _("""ICODTProcedureChoiceNotified type marker interface""")


class IInquiryEvent(Interface):
    __doc__ = _("""IInquiry type marker interface""")


class IAnnouncementEvent(Interface):
    __doc__ = _("""IAnnouncement type marker interface""")


class ICollegeOpinionTransmitToSPWEvent(Interface):
    __doc__ = _("""ICollegeOpinionTransmitToSPWEvent type marker interface""")


class ICollegeOpinionEvent(Interface):
    __doc__ = _("""ICollegeOpinionEvent type marker interface""")


class IDecisionProjectFromSPWEvent(Interface):
    __doc__ = _("""IDecisionProjectFromSPWEvent type marker interface""")


class ILicenceDeliveryEvent(Interface):
    __doc__ = _("""ILicenceDelivery type marker interface""")


class ILicenceEffectiveStartEvent(Interface):
    __doc__ = _("""ILicenceEffectiveStart type marker interface""")


class ILicenceExpirationEvent(Interface):
    __doc__ = _("""ILicenceExpiration type marker interface""")


class ICollegeReportEvent(Interface):
    __doc__ = _("""ICollegeReport type marker interface""")


class ITheLicenceEvent(Interface):
    __doc__ = _("""ITheLicence type marker interface""")


class ITheTicketEvent(Interface):
    __doc__ = _("""ITheTicket type marker interface""")


class ITechnicalAnalysis(Interface):
    __doc__ = _("""ITechnicalAnalysis type marker interface""")


class ITheLicenceCollegeEvent(Interface):
    __doc__ = _("""ITheLicence type marker interface""")


class ILicenceNotificationEvent(Interface):
    __doc__ = _("""ILicenceNotification type marker interface""")


class IDisplayingTheDecisionEvent(Interface):
    __doc__ = _("""IDisplayingTheDecisionEvent type marker interface""")


class IRecourseEvent(Interface):
    __doc__ = _("""IRecourseEvent type marker interface""")


class IWorkBeginningEvent(Interface):
    __doc__ = _("""IWorkBeginning type marker interface""")


class IWorkEndEvent(Interface):
    __doc__ = _("""IWorkEnd type marker interface""")


class IProrogationEvent(Interface):
    __doc__ = _("""IProrogation type marker interface""")


class IProvocationEvent(Interface):
    __doc__ = _("""IProvocationEvent type marker interface""")


class IRefusedIncompletenessEvent(Interface):
    __doc__ = _("""IRefusedIncompleteness type marker interface""")


class IIILEPrescriptionEvent(Interface):
    __doc__ = _("""IIILEPrescriptionEvent type marker interface""")


class IActivityEndedEvent(Interface):
    __doc__ = _("""IActivityEndedEvent type marker interface""")


class IForcedEndEvent(Interface):
    __doc__ = _("""IForcedEndEvent type marker interface""")


class IModificationRegistryEvent(Interface):
    __doc__ = _("""IModificationRegistryEvent type marker interface""")


class ISentToArchivesEvent(Interface):
    __doc__ = _("""ISentToArchivesEvent type marker interface""")


class IEnvironmentOnlyEvent(Interface):
    __doc__ = _("""IEnvironmentOnly type marker interface""")


class IUrbanOrEnvironmentEvent(Interface):
    __doc__ = _("""IUrbanOrEnvironment type marker interface""")


class IUrbanAndEnvironmentEvent(Interface):
    __doc__ = _("""IUrbanAndEnvironment type marker interface""")


class IImpactStudyEvent(Interface):
    __doc__ = _("""ImpactStudy event type marker interface""")


class IInternalPreliminaryAdviceEvent(Interface):
    __doc__ = _("""IInternalPrelimaryAdvice type marker interface""")


class IPreliminaryWarningEvent(Interface):
    __doc__ = _("""IPrelimaryWarning type marker interface""")


class IPatrimonyMeetingEvent(Interface):
    __doc__ = _("""IPatrimonyMeetingEvent type marker interface""")


class IInspectionReportEvent(Interface):
    __doc__ = _("""IInspectionReportEvent type marker interface""")


class IUrbanEventFollowUpWithDelay(Interface):
    __doc__ = _("""IUrbanEventFollowUpWithDelay type marker interface""")


class IProprietaryChangeEvent(Interface):
    __doc__ = _("""IProprietaryChangeEvent type marker interface""")


class ISuspensionEvent(Interface):
    __doc__ = _("""ISuspensionEvent type marker interface""")


class ISettlementEvent(Interface):
    __doc__ = _("""ISettlementEvent type marker interface""")


class ITransferOfLicenceEvent(Interface):
    __doc__ = _("""ITransferOfLicence type marker interface""")


class IUrbanBase(Interface):
    """Marker interface for .Base.UrbanBase
    """


class IUrbanCertificateOne(IGenericLicence):
    """Marker interface for UrbanCertificateOne
    """


class ICODT_UrbanCertificateOne(IGenericLicence):
    """Marker interface for CODT_ UrbanCertificateOne
    """


class INotaryLetter(IGenericLicence):
    """Marker interface for NotaryLetter
    """


class ICODT_NotaryLetter(IGenericLicence):
    """Marker interface for CODT_ NotaryLetter
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


# [DX] TO DELETE > 2.5 [DX]
class ILicencePortionOut(Interface):
    """Marker interface for portionOut in a licence.
    """


class IOptionalFields(Interface):
    """ """


class IUrbanRootRedirects(Interface):
    """ """


class IWorklocationSignaletic(Interface):
    """ Adapts a licence into a displayable address for documents"""

    def get_signaletic(self):
        """ """


class IToUrbain220Street(Interface):
    """
    Adapts an object into streets infos needed for urbain 220:
    street_number
    street_name
    street_code
    """


class IIsArchive(Interface):
    """ Adapts a licence into an archive"""

    def is_archive(self):
        """ """


class ITestConfig(Interface):
    """ Marker interface for TestConfig."""


class ICODT_UniqueLicence_spe_reference_config(Interface):
    """ """
    numerotation = schema.Int(
        title=u"Numérotation",
        default=0
    )
    tal_expression = schema.TextLine(
        title=u"Generation expression",
        default=u"python: 'PU/' + numerotation"
    )


class IInternalOpinionServices(Interface):
    """ """
    services = schema.Dict(
        title=_(u"Internal opinion services"),
        description=_(u"Services that can give their opinion directly through urban"),
        key_type=schema.ASCIILine(),
        value_type=schema.Dict(
            key_type=schema.ASCIILine(),
            value_type=schema.ASCIILine()
        )
    )


class IAsyncInquiryRadius(Interface):
    """ """
    inquiries_to_do = schema.Dict(
        title=_(u"Planned mailings"),
        description=_(u"mailings planned"),
        key_type=schema.ASCIILine(),
        value_type=schema.Int()
    )


class IAsyncMailing(Interface):
    """ """
    mailing_items_limit = schema.Int(
        title=_(u"Mailing limit"),
        description=_(u"Max items allowed for immediate mailing"),
    )

    mailings_to_do = schema.Dict(
        title=_(u"Planned mailings"),
        description=_(u"mailings planned for radius search"),
        key_type=schema.ASCIILine(),
        value_type=schema.ASCIILine()
    )


class IAsyncClaimantsImports(Interface):
    """ """
    claimants_to_import = schema.List(
        title=_(u"Planned claimants imports"),
        description=_(u"inquiries planned for claimants imports"),
        value_type=schema.ASCIILine()
    )


class IGlobalSuspensionPeriod(Interface):
    """ """
    start_date = schema.Date(
        title=_(u"Suspension period start date"),
    )

    end_date = schema.Date(
        title=_(u"Suspension period end date"),
    )


class IFacetedCollection(Interface):
    """ Adapts an object into a faceted collection """


class IUrbanWarningCondition(Interface):
    """ Adapts a licence into a warning message """


class IProductUrbanLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
