# -*- coding: utf-8 -*-
#
# File: EnvClassThree.py
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
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.EnvironmentBase import EnvironmentBase
from Products.urban.utils import (
    setOptionalAttributes,
    setSchemataForCODT_UniqueLicenceInquiry,
)
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban import UrbanMessage as _
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
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


slave_fields_additionalconditions = (
    {
        "name": "additionalConditions",
        "action": "show",
        "hide_values": (True,),
    },
)

optional_fields = [
    "depositType",
    "submissionNumber",
    "inadmissibilityReasons",
    "inadmissibilityreasonsDetails",
    "annoncedDelay",
    "annoncedDelayDetails",
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
]

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="depositType",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_depositType", default="Deposittype"),
            ),
            vocabulary=UrbanVocabulary("deposittype", inUrbanConfig=True),
            default_method="getDefaultValue",
            schemata="urban_description",
        ),
        StringField(
            name="submissionNumber",
            widget=StringField._properties["widget"](
                label=_("urban_label_submissionNumber", default="Submissionnumber"),
            ),
            schemata="urban_description",
        ),
        BooleanField(
            name="hasAdditionalConditions",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_additionalconditions,
                label=_(
                    "urban_label_hasAdditionalConditions",
                    default="Hasadditionalconditions",
                ),
            ),
            schemata="urban_description",
        ),
        FileField(
            name="additionalConditions",
            schemata="urban_description",
            widget=FileField._properties["widget"](
                label=_(
                    "urban_label_additionalConditions", default="Additionalconditions"
                ),
            ),
            storage=AnnotationStorage(),
        ),
        LinesField(
            name="inadmissibilityReasons",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_inadmissibilityReasons",
                    default="Inadmissibilityreasons",
                ),
            ),
            schemata="urban_description",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                path="inadmissibilityreasons", sort_on="getObjPositionInParent"
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="inadmissibilityreasonsDetails",
            widget=RichWidget(
                label=_(
                    "urban_label_inadmissibilityreasonsDetails",
                    default="Inadmissibilityreasonsdetails",
                ),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_description",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
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
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassThree_schema = (
    BaseFolderSchema.copy()
    + getattr(EnvironmentBase, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
# must be done after schema extension to be sure to make fields
# of parents schema optional
setOptionalAttributes(EnvClassThree_schema, optional_fields)
##/code-section after-schema


class EnvClassThree(BaseFolder, EnvironmentBase, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IEnvClassThree)

    meta_type = "EnvClassThree"
    _at_rename_after_creation = True

    schema = EnvClassThree_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getValidityDelay(self):
        return 10

    def rubrics_base_query(self):
        base_query = super(EnvClassThree, self).rubrics_base_query().copy()
        base_query["extraValue"] = ["0", "3"]
        return base_query

    def getProcedureDelays(self, *values):
        return "15j"

    def list_patrimony_types(self):
        """ """
        vocabulary = (
            ("none", "aucune incidence"),
            ("patrimonial", "incidence patrimoniale"),
            ("classified", "bien classé"),
        )
        return DisplayList(vocabulary)


registerType(EnvClassThree, PROJECTNAME)
# end of class EnvClassThree

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("businessOldLocation", after="workLocations")
    schema.moveField("foldermanagers", after="businessOldLocation")
    schema.moveField("depositType", after="folderCategory")
    schema.moveField("submissionNumber", after="depositType")
    schema.moveField("rubrics", after="submissionNumber")
    schema.moveField("description", after="additionalLegalConditions")
    schema.moveField("missingParts", after="inadmissibilityReasons")
    schema.moveField("missingPartsDetails", after="missingParts")
    schema.moveField("general_disposition", after="protectedBuilding")
    schema.moveField("patrimony", after="general_disposition")
    schema["validityDelay"].default = 10
    return schema


finalizeSchema(EnvClassThree_schema)
##/code-section module-footer
