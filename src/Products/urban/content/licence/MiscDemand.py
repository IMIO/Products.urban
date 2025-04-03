# -*- coding: utf-8 -*-
#
# File: MiscDemand.py
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
from Products.Archetypes.atapi import *
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget

from Products.urban import UrbanMessage as _
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import setSchemataForInquiry
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from collective.archetypes.select2.select2widget import MultiSelect2Widget


full_patrimony_slave_fields = (
    {
        "name": "patrimony_site",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "patrimony_architectural_complex",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "archeological_site",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "protection_zone",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "regional_inventory_building",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "small_popular_patrimony",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "communal_inventory",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "regional_inventory",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "patrimony_archaeological_map",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "patrimony_project_gtoret_1ha",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "observation",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "patrimony_monument",
        "action": "hide",
        "hide_values": ("none", "patrimonial"),
    },
    {
        "name": "classification_order_scope",
        "action": "hide",
        "hide_values": ("none", "patrimonial"),
    },
    {
        "name": "patrimony_analysis",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "patrimony_observation",
        "action": "hide",
        "hide_values": ("none",),
    },
)


optional_fields = [
    "architects",
    "patrimony",
    "archeological_site",
    "protection_zone",
    "regional_inventory_building",
    "small_popular_patrimony",
    "communal_inventory",
    "regional_inventory",
    "patrimony_analysis",
    "patrimony_architectural_complex",
    "patrimony_site",
    "patrimony_archaeological_map",
    "patrimony_project_gtoret_1ha",
    "patrimony_monument",
    "patrimony_observation",
    "classification_order_scope",
    "general_disposition",
    "noApplication",
    "shouldNumerotateBuildings",
    "habitationsBeforeLicence",
    "additionalHabitationsAsked",
    "additionalHabitationsGiven",
    "habitationsAfterLicence",
    "mayNeedLocationLicence",
]
##/code-section module-header


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
)


schema = Schema(
    (
        ReferenceField(
            name="architects",
            widget=ReferenceBrowserWidget(
                allow_search=True,
                only_for_review_states="enabled",
                allow_browse=True,
                force_close_on_insert=True,
                startup_directory="urban/architects",
                restrict_browsing_to_startup_directory=True,
                wild_card_search=True,
                show_index_selector=True,
                label=_("urban_label_architects", default="Architect(s)"),
                popup_name="contact_reference_popup",
            ),
            required=False,
            schemata="urban_description",
            multiValued=True,
            relationship="miscdemandarchitects",
            allowed_types="Architect",
        ),
        StringField(
            name="patrimony",
            default="none",
            widget=MasterSelectWidget(
                slave_fields=full_patrimony_slave_fields,
                label=_("urban_label_patrimony", default="Patrimony"),
            ),
            vocabulary="list_patrimony_types",
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="archeological_site",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_archeological_site", default="Archeological_site"),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="protection_zone",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_protection_zone", default="Protection_zone"),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="regional_inventory_building",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_regional_inventory_building",
                    default="Regional_inventory_building",
                ),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="small_popular_patrimony",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_small_popular_patrimony",
                    default="Small_popular_patrimony",
                ),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="communal_inventory",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_communal_inventory", default="Communal_inventory"),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="regional_inventory",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_regional_inventory", default="Regional_inventory"),
            ),
            schemata="urban_patrimony",
        ),
        TextField(
            name="patrimony_analysis",
            widget=RichWidget(
                label=_("urban_label_patrimony_analysis", default="Patrimony_analysis"),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_patrimony",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            accessor="PatrimonyAnalysis",
        ),
        BooleanField(
            name="patrimony_architectural_complex",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_patrimony_architectural_complex",
                    default="Patrimony_architectural_complex",
                ),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="patrimony_site",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_patrimony_site", default="Patrimony_site"),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="patrimony_archaeological_map",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_patrimony_archaeological_map",
                    default="Patrimony_archaeological_map",
                ),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="patrimony_project_gtoret_1ha",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_patrimony_project_gtoret_1ha",
                    default="Patrimony_project_gtoret_1ha",
                ),
            ),
            schemata="urban_patrimony",
        ),
        BooleanField(
            name="patrimony_monument",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_patrimony_monument", default="Patrimony_monument"),
            ),
            schemata="urban_patrimony",
        ),
        TextField(
            name="patrimony_observation",
            widget=RichWidget(
                label=_(
                    "urban_label_patrimony_observation", default="Patrimony_observation"
                ),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_patrimony",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            accessor="PatrimonyObservation",
        ),
        LinesField(
            name="classification_order_scope",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_classification_order_scope",
                    default="Classification_order_scope",
                ),
            ),
            schemata="urban_patrimony",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "classification_order_scope", inUrbanConfig=False
            ),
            default_method="getDefaultValue",
        ),
        StringField(
            name="general_disposition",
            widget=SelectionWidget(
                label=_(
                    "urban_label_general_disposition", default="General_disposition"
                ),
            ),
            schemata="urban_patrimony",
            vocabulary=UrbanVocabulary(
                "general_disposition", inUrbanConfig=False, with_empty_value=True
            ),
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
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

MiscDemand_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(Inquiry, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
# put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(MiscDemand_schema)
##/code-section after-schema


class MiscDemand(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IMiscDemand)

    meta_type = "MiscDemand"
    _at_rename_after_creation = True

    schema = MiscDemand_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ["urban_description", "urban_road", "urban_location"]
    ##/code-section class-header

    # Methods

    security.declarePublic("getRepresentatives")

    def getRepresentatives(self):
        """ """
        return self.getArchitects()

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)

    def list_patrimony_types(self):
        """ """
        vocabulary = (
            ("none", "aucune incidence"),
            ("patrimonial", "incidence patrimoniale"),
            ("classified", "bien classé"),
        )
        return DisplayList(vocabulary)


registerType(MiscDemand, PROJECTNAME)
# end of class MiscDemand


##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("description", after="architects")
    schema.moveField("general_disposition", after="protectedBuilding")
    schema.moveField("patrimony", after="general_disposition")
    schema["parcellings"].widget.label = _("urban_label_parceloutlicences")
    schema["isInSubdivision"].widget.label = _("urban_label_is_in_parceloutlicences")
    schema["subdivisionDetails"].widget.label = _(
        "urban_label_parceloutlicences_details"
    )
    schema["pca"].vocabulary = UrbanVocabulary(
        "sols", vocType="PcaTerm", inUrbanConfig=False
    )
    schema["pca"].widget.label = _("urban_label_sol")
    schema["pcaZone"].vocabulary_factory = "urban.vocabulary.SOLZones"
    schema["pcaZone"].widget.label = _("urban_label_solZone")
    schema["isInPCA"].widget.label = _("urban_label_is_in_sol")
    schema["pcaDetails"].widget.label = _("urban_label_sol_details")
    return schema


finalizeSchema(MiscDemand_schema)
##/code-section module-footer
