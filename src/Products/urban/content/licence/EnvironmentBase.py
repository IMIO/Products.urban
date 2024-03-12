# -*- coding: utf-8 -*-
#
# File: EnvironmentBase.py
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
from Products.urban import interfaces
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.CODT_UniqueLicenceInquiry import CODT_UniqueLicenceInquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from collective.delaycalculator import workday
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from datetime import date
from Products.urban.utils import (
    setOptionalAttributes,
    setSchemataForCODT_UniqueLicenceInquiry,
)
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.widget.historizereferencewidget import (
    HistorizeReferenceBrowserWidget,
)
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget

from plone import api

optional_fields = [
    "roadTechnicalAdvice",
    "locationTechnicalAdvice",
    "additionalLegalConditions",
    "businessOldLocation",
    "applicationReasons",
    "validityDelay",
    "environmentTechnicalRemarks",
    "rubricsDetails",
    "referenceFT",
    "divergences",
    "divergenceDetails",
    "prorogation",
]

slave_fields_natura2000 = (
    {
        "name": "natura2000Details",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "natura2000location",
        "action": "show",
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
)

slave_fields_prorogation = (
    {
        "name": "annoncedDelay",
        "action": "value",
        "vocab_method": "getProrogationDelays",
        "control_param": "values",
    },
)

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="referenceFT",
            widget=StringField._properties["widget"](
                size=30,
                label=_("urban_label_referenceFT", default="Referenceft"),
            ),
            schemata="urban_description",
        ),
        ReferenceField(
            name="rubrics",
            widget=HistorizeReferenceBrowserWidget(
                allow_search=True,
                allow_browse=True,
                force_close_on_insert=True,
                startup_directory="portal_urban/rubrics",
                show_indexes=False,
                wild_card_search=True,
                restrict_browsing_to_startup_directory=True,
                base_query="rubrics_base_query",
                label=_("urban_label_rubrics", default="Rubrics"),
            ),
            allowed_types=("EnvironmentRubricTerm",),
            schemata="urban_description",
            multiValued=True,
            relationship="rubric",
        ),
        TextField(
            name="rubricsDetails",
            widget=RichWidget(
                label=_("urban_label_rubricsDetails", default="Rubricsdetails"),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_environment",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
        ),
        ReferenceField(
            name="minimumLegalConditions",
            widget=ReferenceBrowserWidget(
                label=_(
                    "urban_label_minimumLegalConditions",
                    default="Minimumlegalconditions",
                ),
            ),
            schemata="urban_description",
            multiValued=True,
            relationship="minimumconditions",
        ),
        ReferenceField(
            name="additionalLegalConditions",
            widget=HistorizeReferenceBrowserWidget(
                allow_browse=True,
                allow_search=True,
                default_search_index="Title",
                startup_directory="portal_urban/exploitationconditions",
                restrict_browsing_to_startup_directory=True,
                wild_card_search=True,
                base_query="legalconditions_base_query",
                label=_(
                    "urban_label_additionalLegalConditions",
                    default="Additionallegalconditions",
                ),
            ),
            allowed_types=("UrbanVocabularyTerm",),
            schemata="urban_description",
            multiValued=True,
            relationship="additionalconditions",
        ),
        LinesField(
            name="applicationReasons",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_applicationReasons", default="Applicationreasons"),
            ),
            schemata="urban_description",
            multiValued=True,
            vocabulary=UrbanVocabulary(
                path="applicationreasons", sort_on="getObjPositionInParent"
            ),
            default_method="getDefaultValue",
        ),
        DataGridField(
            name="businessOldLocation",
            schemata="urban_description",
            widget=DataGridWidget(
                columns={
                    "number": Column("Number"),
                    "street": ReferenceColumn(
                        "Street",
                        surf_site=False,
                        object_provides=(
                            "Products.urban.interfaces.IStreet",
                            "Products.urban.interfaces.ILocality",
                        ),
                    ),
                },
                helper_js=("datagridwidget.js", "datagridautocomplete.js"),
                label=_(
                    "urban_label_businessOldLocation", default="Old business location"
                ),
            ),
            allow_oddeven=True,
            columns=("number", "street"),
            validators=("isValidStreetName",),
        ),
        TextField(
            name="businessDescription",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_businessDescription", default="Businessdescription"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_description",
            default_output_type="text/x-html-safe",
        ),
        StringField(
            name="procedureChoice",
            default="ukn",
            widget=MasterSelectWidget(
                slave_fields=slave_fields_procedurechoice,
                label=_("urban_label_procedureChoice", default="Procedurechoice"),
            ),
            schemata="urban_description",
            validators=("isValidProcedureChoice",),
            multiValued=1,
            vocabulary="listProcedureChoices",
        ),
        StringField(
            name="annoncedDelay",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_annoncedDelay", default="Annonceddelay"),
            ),
            schemata="urban_description",
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
            name="natura2000",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_natura2000,
                label=_("urban_label_natura2000", default="Natura2000"),
            ),
            schemata="urban_description",
        ),
        StringField(
            name="natura2000location",
            widget=SelectionWidget(
                label=_("urban_label_location", default="Natura2000location"),
            ),
            schemata="urban_description",
            vocabulary="listNatura2000Locations",
        ),
        TextField(
            name="natura2000Details",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_natura2000Details", default="Natura2000details"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_description",
            default_output_type="text/x-html-safe",
        ),
        IntegerField(
            name="validityDelay",
            default=20,
            widget=IntegerField._properties["widget"](
                label=_("urban_label_validityDelay", default="Validitydelay"),
            ),
            schemata="urban_description",
        ),
        TextField(
            name="roadTechnicalAdvice",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_roadTechnicalAdvice", default="Roadtechnicaladvice"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
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
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="description",
            widget=RichWidget(
                label=_("urban_label_description", default="Description"),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_description",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            accessor="Description",
        ),
        TextField(
            name="environmentTechnicalRemarks",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_environmentTechnicalRemarks",
                    default="Environmenttechnicalremarks",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_environment",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="isTransferOfLicence",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_istransferoflicence", default="IsTransferOfLicence"
                ),
            ),
            schemata="urban_description",
        ),
        BooleanField(
            name="prorogation",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_prorogation,
                label=_("urban_label_prorogation", default="Prorogation"),
            ),
            schemata="urban_description",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentBase_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(CODT_UniqueLicenceInquiry, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
EnvironmentBase_schema["title"].required = False
EnvironmentBase_schema["title"].widget.visible = False
setSchemataForCODT_UniqueLicenceInquiry(EnvironmentBase_schema)
# hide Inquiry fields but 'solicitOpinionsTo'
for field in EnvironmentBase_schema.filterFields(isMetadata=False):
    if field.schemata == "urban_investigation_and_advices" and field.getName() not in [
        "solicitOpinionsTo",
        "solicitOpinionsToOptional",
    ]:
        field.widget.visible = False

# change translation of some fields
EnvironmentBase_schema["referenceDGATLP"].widget.label = _("urban_label_referenceDGO3")
EnvironmentBase_schema["workLocations"].widget.label = _(
    "urban_label_situation", default="Situation"
)

##/code-section after-schema


class EnvironmentBase(
    BaseFolder, GenericLicence, CODT_UniqueLicenceInquiry, BrowserDefaultMixin
):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IEnvironmentBase)

    meta_type = "EnvironmentBase"
    _at_rename_after_creation = True

    schema = EnvironmentBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = [
        "urban_description",
        "urban_road",
        "urban_location",
        "urban_investigation_and_advices",
    ]
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("listNatura2000Locations")

    def listNatura2000Locations(self):
        """
        This vocabulary for field location returns a list of
        Natura2000 locations
        """
        vocab = (
            ("inside", "location_inside"),
            ("near", "location_near"),
        )
        return DisplayList(vocab)

    def rubrics_base_query(self):
        """to be overriden"""
        return {"review_state": ["enabled", "private"]}

    def legalconditions_base_query(self):
        return {"review_state": ["enabled", "private"]}

    def listProcedureChoices(self):
        vocabulary = (
            ("ukn", "Non determiné"),
            ("simple", "Classique"),
            ("temporary", "Temporaire"),
        )
        return DisplayList(vocabulary)

    def getProcedureDelays(self, *values):
        """
        To implements in subclasses
        """

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastCollegeOpinion(self):
        return self.getLastEvent(interfaces.ICollegeOpinionEvent)

    def getLastLicenceNotification(self):
        return self.getLastEvent(interfaces.ILicenceNotificationEvent)

    def getLastDisplayingTheDecision(self):
        return self.getLastEvent(interfaces.IDisplayingTheDecisionEvent)

    def getLastLicenceDelivery(self):
        return self.getLastEvent(interfaces.ILicenceDeliveryEvent)

    def getLastProvocation(self):
        return self.getLastEvent(interfaces.IProvocationEvent)

    def getLastRecourse(self):
        return self.getLastEvent(interfaces.IRecourseEvent)

    def getLastLicenceEffectiveStart(self):
        return self.getLastEvent(interfaces.ILicenceEffectiveStartEvent)

    def getLastLicenceExpiration(self):
        return self.getLastEvent(interfaces.ILicenceExpirationEvent)

    def getLastIILEPrescription(self):
        return self.getLastEvent(interfaces.IIILEPrescriptionEvent)

    def getLastActivityEnded(self):
        return self.getLastEvent(interfaces.IActivityEndedEvent)

    def getLastForcedEnd(self):
        return self.getLastEvent(interfaces.IForcedEndEvent)

    def getLastModificationRegistry(self):
        return self.getLastEvent(interfaces.IModificationRegistryEvent)

    def getLastSentToArchives(self):
        return self.getLastEvent(interfaces.ISentToArchivesEvent)

    def getLastWalloonRegionDecisionEvent(self):
        return self.getLastEvent(interfaces.IWalloonRegionDecisionEvent)

    def getLastDecisionProjectFromSPWEvent(self):
        return self.getLastEvent(interfaces.IDecisionProjectFromSPWEvent)

    def getLastProprietaryChangeEvent(self):
        return self.getLastEvent(interfaces.IProprietaryChangeEvent)

    security.declarePublic("getLastTransferOfLicence")

    def getLastTransferOfLicence(self):
        return self.getLastEvent(interfaces.ITransferOfLicenceEvent)

    security.declarePublic("getAllTransferOfLicence")

    def getAllTransfersOfLicence(self):
        return self.getAllEvents(interfaces.ITransferOfLicenceEvent)

    security.declarePublic("mayAddTransferOfLicenceEvent")

    def mayAddTransferOfLicenceEvent(self):
        """
        May add TransferOfLicenceEvent if isTransferOfLicence is true
        """
        if not self.getIsTransferOfLicence():
            return False
        return True

    security.declarePublic("getAdditionalLayers")

    def getAdditionalLayers(self):
        """
        Return a list of additional layers that will be used
        when generating the mapfile
        """
        try:
            additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
            return additionalLayersFolder.objectValues("Layer")
        except AttributeError:
            return None

    def getRubricsConfigPath(self):
        config_path = "/".join(self.getLicenceConfig().rubrics.getPhysicalPath())[1:]
        return config_path

    security.declarePrivate("_getConditions")

    def _getConditions(self, restrict=["CI/CS", "CI", "CS", "CS-Eau", "Ville"]):
        all_conditions = self.getMinimumLegalConditions()
        all_conditions.extend(self.getAdditionalLegalConditions())
        return [cond for cond in all_conditions if cond.getExtraValue() in restrict]

    security.declarePublic("getIntegralConditions")

    def getIntegralConditions(self):
        """
        Return all the integral conditions,
        """
        return self._getConditions(restrict=["CI"])

    security.declarePublic("getSectorialConditions")

    def getSectorialConditions(self):
        """
        Return all the sectorial conditions,
        """
        return self._getConditions(restrict=["CS"])

    security.declarePublic("getIandSConditions")

    def getIandSConditions(self):
        """
        Return all the integral & sectorial conditions,
        """
        return self._getConditions(restrict=["CI/CS"])

    def getWaterConditions(self):
        """
        Return all the water conditions,
        """
        return self._getConditions(restrict=["CS-Eau"])

    def getTownshipConditions(self):
        """
        Return all the water conditions,
        """
        return self._getConditions(restrict=["Ville"])

    security.declarePublic("getLicenceSEnforceableDate")

    def getLicenceSEnforceableDate(self, displayDay, periodForAppeal):
        return workday(
            date(displayDay.year(), displayDay.month(), displayDay.day()),
            periodForAppeal,
        )

    security.declarePublic("showBoundLicenceIfArticle65")

    def showBoundLicenceIfArticle65(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        show = "article65" in selection
        return show

    def getProrogationDelays(self, *values):
        procedure_choice = [{"val": self.getProcedureChoice(), "selected": True}]
        base_delay = self.getProcedureDelays(*procedure_choice)
        if self.prorogation:
            base_delay = "{}j".format(str(int(base_delay[:-1]) - 30))

        return self._getProrogationDelays(base_delay, values)

    def _getProrogationDelays(self, base_delay, values):
        if False in values:
            return base_delay

        prorogated_delay = ""
        if base_delay:
            prorogated_delay = "{}j".format(str(int(base_delay[:-1]) + 30))

        return prorogated_delay


registerType(EnvironmentBase, PROJECTNAME)


# end of class EnvironmentBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("businessOldLocation", after="workLocations")
    schema.moveField("foldermanagers", after="businessOldLocation")
    #    schema.moveField('bound_licences', after='isTransferOfLicence')
    schema.moveField("rubrics", after="folderCategory")
    schema.moveField("description", after="additionalLegalConditions")
    schema.moveField("referenceFT", after="referenceDGATLP")
    schema.moveField("isTransferOfLicence", after="referenceFT")

    return schema


finalizeSchema(EnvironmentBase_schema)
##/code-section module-footer
