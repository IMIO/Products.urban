# -*- coding: utf-8 -*-
#
# File: BaseBuildLicence.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
from zope.i18n import translate
from Products.urban import interfaces
from Products.urban.content.Inquiry import Inquiry
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from plone import api

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from dateutil.relativedelta import relativedelta
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

optional_fields = [
    "implantation",
    "roadAdaptation",
    "pebDetails",
    "requirementFromFD",
    "roadTechnicalAdvice",
    "locationTechnicalAdvice",
    "locationTechnicalConditions",
    "pebTechnicalAdvice",
    "locationDgrneUnderground",
    "roadDgrneUnderground",
    "workType",
    "townshipCouncilFolder",
    "roadMiscDescription",
    "procedureChoice",
    "water",
    "electricity",
    "shouldNumerotateBuildings",
    "habitationsAfterLicence",
    "habitationsBeforeLicence",
    "additionalHabitationsAsked",
    "additionalHabitationsGiven",
    "mayNeedLocationLicence",
    "impactStudy",
    "exemptFDArticle",
    "availableParkings",
    "missingParkings",
    "parkingDetails",
]

slave_fields_habitation = (
    {
        "name": "shouldNumerotateBuildings",
        "action": "hide",
        "hide_values": (True,),
    },
    {
        "name": "habitationsBeforeLicence",
        "action": "hide",
        "hide_values": (True,),
    },
    {
        "name": "habitationsAfterLicence",
        "action": "hide",
        "hide_values": (True,),
    },
    {
        "name": "additionalHabitationsAsked",
        "action": "hide",
        "hide_values": (True,),
    },
    {
        "name": "additionalHabitationsGiven",
        "action": "hide",
        "hide_values": (True,),
    },
    {
        "name": "mayNeedLocationLicence",
        "action": "hide",
        "hide_values": (True,),
    },
    {
        "name": "habitationsBeforeLicence",
        "action": "hide",
        "hide_values": (True,),
    },
)

slave_fields_procedurechoice = (
    {
        "name": "annoncedDelay",
        "action": "value",
        "vocab_method": "getProcedureDelays",
        "control_param": "values",
    },
    {
        "name": "exemptFDArticle",
        "action": "show",
        "toggle_method": "showExemptFDArticle",
        "control_param": "values",
    },
    {
        "name": "requirementFromFD",
        "action": "show",
        "toggle_method": "showRequirementFromFD",
        "control_param": "values",
    },
)

slave_fields_modified_blueprints = (
    {
        "name": "delayAfterModifiedBlueprints",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "delayAfterModifiedBlueprintsDetails",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "procedureChoiceModifiedBlueprints",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "prorogationModifiedBp",
        "action": "show",
        "hide_values": (True,),
    },
)

slave_fields_composition = (
    {
        "name": "missingParts",
        "action": "vocabulary",
        "vocab_method": "getCompositionMissingParts",
        "control_param": "composition",
    },
)

slave_fields_impact_study = (
    {
        "name": "investigation_radius",
        "action": "value",
        "vocab_method": "get_impact_study_radius",
        "control_param": "has_impact_study",
    },
)
##/code-section module-header

schema = Schema(
    (
        LinesField(
            name="workType",
            widget=MultiSelect2Widget(
                label=_("urban_label_workType", default="Worktype"),
            ),
            schemata="urban_description",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                path="folderbuildworktypes", sort_on="sortable_title"
            ),
            default_method="getDefaultValue",
        ),
        StringField(
            name="usage",
            widget=SelectionWidget(
                label=_("urban_label_usage", default="Usage"),
            ),
            required=True,
            schemata="urban_description",
            vocabulary="listUsages",
        ),
        StringField(
            name="annoncedDelay",
            widget=SelectionWidget(
                label=_("urban_label_annoncedDelay", default="Annonceddelay"),
            ),
            schemata="urban_analysis",
            vocabulary=UrbanVocabulary(
                "folderdelays", vocType="UrbanDelay", with_empty_value=True
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="annoncedDelayDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_annoncedDelayDetails", default="Annonceddelaydetails"
                ),
            ),
            schemata="urban_analysis",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="townshipCouncilFolder",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_townshipCouncilFolder", default="Townshipcouncilfolder"
                ),
                description_msgid="urban_help_townshipCouncilFolder",
            ),
            schemata="urban_road",
        ),
        BooleanField(
            name="impactStudy",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_impact_study,
                label=_("urban_label_impactStudy", default="Impactstudy"),
            ),
            schemata="urban_description",
        ),
        BooleanField(
            name="implantation",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_implantation", default="Implantation"),
            ),
            schemata="urban_analysis",
        ),
        StringField(
            name="pebType",
            widget=SelectionWidget(
                label=_("urban_label_pebType", default="Pebtype"),
            ),
            enforceVocabulary=True,
            schemata="urban_peb",
            vocabulary=UrbanVocabulary(path="pebcategories"),
            default_method="getDefaultValue",
        ),
        TextField(
            name="pebDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pebDetails", default="Pebdetails"),
            ),
            schemata="urban_peb",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="pebStudy",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_pebStudy", default="Pebstudy"),
            ),
            schemata="urban_peb",
        ),
        BooleanField(
            name="noApplication",
            default=True,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_habitation,
                label=_("urban_label_noApplication", default="Noapplication"),
            ),
            schemata="urban_habitation",
        ),
        BooleanField(
            name="shouldNumerotateBuildings",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_shouldNumerotateBuilding",
                    default="Shouldnumerotatebuildings",
                ),
            ),
            schemata="urban_habitation",
        ),
        IntegerField(
            name="habitationsBeforeLicence",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_habitationsBeforeLicence",
                    default="Habitationsbeforelicence",
                ),
            ),
            schemata="urban_habitation",
        ),
        IntegerField(
            name="additionalHabitationsAsked",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_additionalHabitationsAsked",
                    default="Additionalhabitationsasked",
                ),
            ),
            schemata="urban_habitation",
        ),
        IntegerField(
            name="additionalHabitationsGiven",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_additionalHabitationsGiven",
                    default="Additionalhabitationsgiven",
                ),
            ),
            schemata="urban_habitation",
        ),
        IntegerField(
            name="habitationsAfterLicence",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_habitationsAfterLicence",
                    default="Habitationsafterlicence",
                ),
            ),
            schemata="urban_habitation",
        ),
        BooleanField(
            name="mayNeedLocationLicence",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_mayNeedLocationLicence",
                    default="Mayneedlocationlicence",
                ),
            ),
            schemata="urban_habitation",
        ),
        StringField(
            name="roadAdaptation",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_roadAdaptation", default="Roadadaptation"),
            ),
            schemata="urban_road",
            vocabulary="listRoadAdaptations",
        ),
        IntegerField(
            name="availableParkings",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_("urban_label_availableParkings", default="Availableparkings"),
            ),
            schemata="urban_road",
        ),
        IntegerField(
            name="missingParkings",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_("urban_label_missingParkings", default="Missingparkings"),
            ),
            schemata="urban_road",
        ),
        TextField(
            name="parkingDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_parkingDetails", default="Parkingdetails"),
            ),
            default_method="getDefaultText",
            schemata="urban_road",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="roadMiscDescription",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_roadMiscDescription", default="Roadmiscdescription"
                ),
            ),
            default_method="getDefaultText",
            schemata="urban_road",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="roadDgrneUnderground",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_roadDgrneUnderground", default="Roaddgrneunderground"
                ),
                description_msgid="urban_help_roadDgrneUnderground",
            ),
            schemata="urban_road",
        ),
        TextField(
            name="roadTechnicalAdvice",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_roadTechnicalAdvice", default="Roadtechnicaladvice"
                ),
            ),
            default_method="getDefaultText",
            schemata="urban_road",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="locationDgrneUnderground",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_locationDgrneUnderground",
                    default="Locationdgrneunderground",
                ),
                description_msgid="urban_help_locationDgrneUnderground",
            ),
            schemata="urban_location",
        ),
        TextField(
            name="locationTechnicalAdvice",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_locationTechnicalAdvice",
                    default="Locationtechnicaladvice",
                ),
            ),
            default_method="getDefaultText",
            schemata="urban_analysis",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="locationTechnicalConditions",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_locationTechnicalConditions",
                    default="Locationtechnicalconditions",
                ),
            ),
            default_method="getDefaultText",
            schemata="urban_analysis",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="pebTechnicalAdvice",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pebTechnicalAdvice", default="Pebtechnicaladvice"),
            ),
            default_method="getDefaultText",
            schemata="urban_peb",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        ReferenceField(
            name="architects",
            widget=ReferenceBrowserWidget(
                force_close_on_insert=1,
                allow_search=1,
                only_for_review_states="enabled",
                allow_browse=1,
                show_indexes=1,
                show_index_selector=1,
                available_indexes={"Title": "Nom"},
                startup_directory="urban/architects",
                wild_card_search=True,
                restrict_browsing_to_startup_directory=1,
                label=_("urban_label_architects", default="Architect(s)"),
                popup_name="contact_reference_popup",
                visible=False,
            ),
            allowed_types=("Architect",),
            schemata="urban_description",
            multiValued=1,
            relationship="licenceArchitects",
        ),
        ReferenceField(
            name="representativeContacts",
            widget=ReferenceBrowserWidget(
                force_close_on_insert=1,
                allow_search=1,
                only_for_review_states="enabled",
                allow_browse=0,
                show_indexes=1,
                available_indexes={"Title": "Nom"},
                startup_directory="urban",
                wild_card_search=True,
                show_results_without_query=True,
                restrict_browsing_to_startup_directory=False,
                label=_(
                    "urban_label_representative_contacts",
                    default="RepresentativeContact(s)",
                ),
                popup_name="contact_reference_popup",
            ),
            schemata="urban_description",
            multiValued=1,
            relationship="basebuildlicenceRepresentativeContacts",
            allowed_types=(
                "Geometrician",
                "Architect",
            ),
        ),
        LinesField(
            name="procedureChoice",
            default="ukn",
            widget=MasterMultiSelectWidget(
                format="checkbox",
                slave_fields=slave_fields_procedurechoice,
                label=_("urban_label_procedureChoice", default="Procedurechoice"),
            ),
            schemata="urban_analysis",
            validators=("isValidProcedureChoice",),
            multiValued=1,
            vocabulary="listProcedureChoices",
        ),
        LinesField(
            name="requirementFromFD",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_requirementFromFD", default="Requirementfromfd"),
            ),
            schemata="urban_analysis",
            multiValued=1,
            vocabulary="listRequirementsFromFD",
        ),
        StringField(
            name="exemptFDArticle",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_exemptFDArticle", default="Exemptfdarticle"),
            ),
            schemata="urban_analysis",
            vocabulary=UrbanVocabulary("exemptfdarticle", with_empty_value=True),
            default_method="getDefaultValue",
        ),
        BooleanField(
            name="hasModifiedBlueprints",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_modified_blueprints,
                label=_(
                    "urban_label_hasModifiedBlueprints", default="Hasmodifiedblueprints"
                ),
            ),
            schemata="urban_analysis",
        ),
        StringField(
            name="delayAfterModifiedBlueprints",
            widget=SelectionWidget(
                label=_(
                    "urban_label_delayAfterModifiedBlueprints",
                    default="Delayaftermodifiedblueprints",
                ),
            ),
            schemata="urban_analysis",
            vocabulary=UrbanVocabulary(
                "folderdelays", vocType="UrbanDelay", with_empty_value=True
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="delayAfterModifiedBlueprintsDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_delayAfterModifiedBlueprintsDetails",
                    default="Delayaftermodifiedblueprintsdetails",
                ),
            ),
            schemata="urban_analysis",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="water",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_water", default="Water"),
            ),
            schemata="urban_road",
        ),
        BooleanField(
            name="electricity",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_electricity", default="Electricity"),
            ),
            schemata="urban_road",
        ),
        StringField(
            name="composition",
            widget=MasterSelectWidget(
                slave_fields=slave_fields_composition,
                label=_("urban_label_composition", default="Composition"),
            ),
            schemata="urban_analysis",
            vocabulary="listCompositions",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

BaseBuildLicence_schema = (
    BaseFolderSchema.copy()
    + getattr(Inquiry, "schema", Schema(())).copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
BaseBuildLicence_schema["title"].required = False
# put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(BaseBuildLicence_schema)
##/code-section after-schema


class BaseBuildLicence(BaseFolder, Inquiry, GenericLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IBaseBuildLicence)

    _at_rename_after_creation = True

    schema = BaseBuildLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic("listRoadAdaptations")

    def listRoadAdaptations(self):
        """
        This vocabulary for field roadAdaptation returns a list of
        road adaptations : no, yes modify, yes create
        """
        vocab = (
            ("modify", translate(_("road_adaptation_modify"), context=self.REQUEST)),
            ("create", translate(_("road_adaptation_create"), context=self.REQUEST)),
            ("supress", translate(_("road_adaptation_supress"), context=self.REQUEST)),
        )
        return DisplayList(vocab)

    security.declarePublic("listUsages")

    def listUsages(self):
        """
        This vocabulary for field usage returns a list of
        building usage : for habitation, not for habitation
        """
        vocab = (
            ("for_habitation", _("usage_for_habitation")),
            ("not_for_habitation", _("usage_not_for_habitation")),
            ("not_applicable", _("usage_not_applicable")),
        )
        return DisplayList(vocab)

    # Manually created methods

    security.declarePublic("getRepresentatives")

    def getRepresentatives(self):
        """ """
        return self.getRepresentativeContacts()

    security.declarePublic("getArchitects")

    def getArchitects(self):
        """ """
        return [
            contact
            for contact in self.getRepresentativeContacts()
            if contact.portal_type == "Architect"
        ]

    security.declarePublic("getGeometricians")

    def getGeometricians(self):
        """ """
        return [
            contact
            for contact in self.getRepresentativeContacts()
            if contact.portal_type == "Geometrician"
        ]

    security.declarePublic("listRequirementsFromFD")

    def listRequirementsFromFD(self):
        """
        This vocabulary for field requirementsFromFD returns this list: decision, opinion
        """
        vocab = (
            ("opinion", "Avis simple"),
            ("decision", "Avis conforme"),
        )
        return DisplayList(vocab)

    security.declarePublic("askFD")

    def askFD(self):
        """ """
        return "FD" in self.getProcedureChoice()

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastMissingPart(self):
        return self.getLastEvent(interfaces.IMissingPartEvent)

    def getAllMissingPart(self):
        return self.getAllEvents(interfaces.IMissingPartEvent)

    def getLastMissingPartDeposit(self):
        return self.getLastEvent(interfaces.IMissingPartDepositEvent)

    def getLastWalloonRegionPrimo(self):
        return self.getLastEvent(interfaces.IWalloonRegionPrimoEvent)

    def getLastWalloonRegionOpinionRequest(self):
        return self.getLastEvent(interfaces.IWalloonRegionOpinionRequestEvent)

    def getFirstAcknowledgment(self):
        return self.getFirstEvent(interfaces.IAcknowledgmentEvent)

    def getLastAcknowledgment(self, state=None):
        return self.getLastEvent(interfaces.IAcknowledgmentEvent, state)

    def getLastAnnouncement(self):
        return self.getLastEvent(interfaces.IAnnouncementEvent)

    def getLastCommunalCouncil(self):
        return self.getLastEvent(interfaces.ICommunalCouncilEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastModificationDeposit(self):
        return self.getLastEvent(interfaces.IModificationDepositEvent)

    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)

    def getLastLicenceNotification(self):
        return self.getLastEvent(interfaces.ILicenceNotificationEvent)

    def getLastWorkBeginning(self):
        return self.getLastEvent(interfaces.IWorkBeginningEvent)

    def getLastWorkEnd(self):
        return self.getLastEvent(interfaces.IWorkEndEvent)

    def getLastRecourse(self):
        return self.getLastEvent(interfaces.IRecourseEvent)

    def getLastProrogation(self):
        return self.getLastEvent(interfaces.IProrogationEvent)

    def getLastRefusedNotification(self):
        return self.getLastEvent(interfaces.IRefusedIncompletenessEvent)

    def getAllMissingPartDeposits(self):
        return self.getAllEvents(interfaces.IMissingPartDepositEvent)

    def getAllTechnicalServiceOpinionRequests(self):
        return self.getAllEvents(interfaces.ITechnicalServiceOpinionRequestEvent)

    def getProrogatedToDate(self):
        """
        This method will calculate the 'prorogated to' date
        """
        lastTheLicenceDecisionDate = self.getLastTheLicence().getDecisionDate()
        if not lastTheLicenceDecisionDate:
            return ""
        else:
            # the prorogation gives one year more to the applicant
            tool = getToolByName(self, "portal_urban")
            # relativedelta does not work with DateTime so use datetime
            return tool.formatDate(
                lastTheLicenceDecisionDate.asdatetime() + relativedelta(years=+3)
            )

    def listProcedureChoices(self):
        vocabulary = (
            ("ukn", "Non determiné"),
            ("opinions", "Sollicitation d'avis (instance ou service interne/externe)"),
            ("inquiry", "Enquête publique"),
            ("FD", "Sollicitation du fonctionnaire délégué"),
        )
        return DisplayList(vocabulary)

    def getProcedureDelays(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        unknown = "ukn" in selection
        opinions = "opinions" in selection
        inquiry = "inquiry" in selection
        FD = "FD" in selection

        if unknown:
            return ""
        elif (opinions or inquiry) and FD:
            return "115j"
        elif opinions and inquiry and not FD:
            return "70j"
        elif opinions and not (inquiry or FD):
            return "70j"
        elif inquiry and not (opinions or FD):
            return "70j"
        elif FD and not (opinions or inquiry):
            return "75j"
        else:
            return "30j"

    def listCompositions(self):
        vocabulary = (
            ("", "Non déterminée"),
            ("285", "Art. 285 - complet avec architecte"),
            ("288", "Art. 288 - simplifié avec architecte"),
            ("291", "Art. 291 - simplifié sans architecte"),
        )
        return DisplayList(vocabulary)

    def showExemptFDArticle(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        show = "FD" not in selection and "ukn" not in selection
        return show

    def showRequirementFromFD(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        show = "FD" in selection and "ukn" not in selection
        return show

    def getCompositionMissingParts(self, composition):
        """ """
        urban_voc = self.schema["missingParts"].vocabulary
        all_terms = urban_voc.listAllVocTerms(self)

        display_values = [
            (term.id, term.Title().decode("utf-8"))
            for term in all_terms
            if str(composition) in term.getExtraValue()
        ]

        return DisplayList(display_values)

    def costCalculation(
        self, base_price=0, FD_price=0, inquiry_price=0, opinions_price=0
    ):
        cost = base_price
        if "opinions" in self.getProcedureChoice():
            cost += opinions_price
        if "inquiry" in self.getProcedureChoice():
            cost += inquiry_price
        if "FD" in self.getProcedureChoice():
            cost += FD_price
        return cost


# end of class BaseBuildLicence

##code-section module-footer #fill in your manual code here
# Make sure the schema is correctly finalized


def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("roadAdaptation", before="roadTechnicalAdvice")
    schema.moveField("representativeContacts", after="workLocations")
    schema.moveField("foldermanagers", after="representativeContacts")
    schema.moveField("workType", after="folderCategory")
    schema.moveField("parcellings", after="isInSubdivision")
    schema.moveField("description", after="usage")
    schema.moveField("roadMiscDescription", after="roadEquipments")
    schema.moveField("locationTechnicalRemarks", after="locationTechnicalConditions")
    schema.moveField("areParcelsVerified", after="folderCategoryTownship")
    schema.moveField("requirementFromFD", before="annoncedDelay")
    schema.moveField("townshipCouncilFolder", after="futureRoadCoating")
    schema.moveField("annoncedDelayDetails", after="annoncedDelay")
    schema.moveField("hasModifiedBlueprints", after="annoncedDelayDetails")
    schema.moveField("delayAfterModifiedBlueprints", after="hasModifiedBlueprints")
    schema.moveField(
        "delayAfterModifiedBlueprintsDetails", after="delayAfterModifiedBlueprints"
    )
    schema.moveField("impactStudy", after="delayAfterModifiedBlueprintsDetails")
    schema.moveField("procedureChoice", before="description")
    schema.moveField("exemptFDArticle", after="procedureChoice")
    schema.moveField("water", after="futureRoadCoating")
    schema.moveField("electricity", before="water")
    schema.moveField("composition", before="missingParts")
    schema.moveField("availableParkings", after="roadType")
    schema.moveField("missingParkings", after="availableParkings")
    schema.moveField("parkingDetails", after="missingParkings")
    schema["missingParts"].widget.format = None
    return schema


finalizeSchema(BaseBuildLicence_schema)
##/code-section module-footer
