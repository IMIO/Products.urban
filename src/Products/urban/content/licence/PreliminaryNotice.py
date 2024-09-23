# -*- coding: utf-8 -*-
#
# File: PreliminaryNotice.py
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
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.MiscDemand import finalizeSchema as firstBaseFinalizeSchema
from Products.urban.content.licence.MiscDemand import MiscDemand
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from collective.archetypes.select2.select2widget import MultiSelect2Widget

from Products.urban import UrbanMessage as _
from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

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

schema = Schema((
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
            label=_("urban_label_regional_inventory_building", default="Regional_inventory_building"),
        ),
        schemata="urban_patrimony",
    ),
    BooleanField(
        name="small_popular_patrimony",
        default=False,
        widget=BooleanField._properties["widget"](
            label=_("urban_label_small_popular_patrimony", default="Small_popular_patrimony"),
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
            label=_("urban_label_patrimony_architectural_complex", default="Patrimony_architectural_complex"),
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
            label=_("urban_label_patrimony_archaeological_map", default="Patrimony_archaeological_map"),
        ),
        schemata="urban_patrimony",
    ),
    BooleanField(
        name="patrimony_project_gtoret_1ha",
        default=False,
        widget=BooleanField._properties["widget"](
            label=_("urban_label_patrimony_project_gtoret_1ha", default="Patrimony_project_gtoret_1ha"),
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
            label=_("urban_label_patrimony_observation", default="Patrimony_observation"),
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
            label=_("urban_label_classification_order_scope", default="Classification_order_scope"),
        ),
        schemata="urban_patrimony",
        multiValued=1,
        vocabulary=UrbanVocabulary("classification_order_scope", inUrbanConfig=False),
        default_method="getDefaultValue",
    ),
    StringField(
        name="general_disposition",
        widget=SelectionWidget(
            label=_("urban_label_general_disposition", default="General_disposition"),
        ),
        schemata="urban_patrimony",
        vocabulary=UrbanVocabulary("general_disposition", inUrbanConfig=False, with_empty_value=True),
    ),
    LinesField(
        name="protectedBuilding",
        widget=MultiSelect2Widget(
            format="checkbox",
            label=_("urban_label_protectedBuilding",
                    default="Protectedbuilding"),
        ),
        schemata="urban_patrimony",
        multiValued=1,
        vocabulary_factory="urban.vocabulary.ProtectedBuilding",
        default_method="getDefaultValue",
    ),
    TextField(
        name="protectedBuildingDetails",
        allowable_content_types=("text/html",),
        widget=RichWidget(
            label=_("urban_label_protectedBuildingDetails",
                    default="Protectedbuildingdetails"),
        ),
        default_content_type="text/html",
        default_method="getDefaultText",
        schemata="urban_patrimony",
        default_output_type="text/x-html-safe",
    ),
))

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PreliminaryNotice_schema = (
    BaseFolderSchema.copy()
    + getattr(MiscDemand, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
PreliminaryNotice_schema.delField("referenceDGATLP")
##/code-section after-schema


class PreliminaryNotice(BaseFolder, MiscDemand, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IPreliminaryNotice)

    meta_type = "PreliminaryNotice"
    _at_rename_after_creation = True

    schema = PreliminaryNotice_schema

    # Methods

    def list_patrimony_types(self):
        """
        """
        vocabulary = (
            ("none", "aucune incidence"),
            ("patrimonial", "incidence patrimoniale"),
            ("classified", "bien classé"),
        )
        return DisplayList(vocabulary)


registerType(PreliminaryNotice, PROJECTNAME)
# end of class PreliminaryNotice


##code-section module-footer #fill in your manual code here
# finalizeSchema come from MiscDemand as its the same changes

def finalizeSchema(schema):
    schema.moveField("patrimony", pos="top")
    schema.moveField("regional_inventory_building", after="patrimony")
    schema.moveField("patrimony_archaeological_map", after="regional_inventory_building")
    schema.moveField("patrimony_architectural_complex", after="patrimony_archaeological_map")
    schema.moveField("communal_inventory", after="patrimony_architectural_complex")
    schema.moveField("regional_inventory", after="communal_inventory")
    schema.moveField("patrimony_monument", after="regional_inventory")
    schema.moveField("small_popular_patrimony", after="patrimony_monument")
    schema.moveField("patrimony_project_gtoret_1ha", after="small_popular_patrimony")
    schema.moveField("patrimony_site", after="patrimony_project_gtoret_1ha")
    schema.moveField("archeological_site", after="patrimony_site")
    schema.moveField("protection_zone", after="archeological_site")
    schema.moveField("classification_order_scope", after="protection_zone")
    schema.moveField("general_disposition", after="classification_order_scope")
    schema.moveField("protectedBuilding", after="general_disposition")
    schema.moveField("protectedBuildingDetails", after="protectedBuilding")
    schema.moveField("patrimony_analysis", after="protectedBuildingDetails")
    schema.moveField("patrimony_observation", after="patrimony_analysis")
    return schema

firstBaseFinalizeSchema(PreliminaryNotice_schema)
finalizeSchema(PreliminaryNotice_schema)
##/code-section module-footer
