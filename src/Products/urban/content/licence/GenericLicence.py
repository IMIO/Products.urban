# -*- coding: utf-8 -*-
#
# File: GenericLicence.py
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
from zope.annotation import IAnnotations
from datetime import datetime

from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from collective.faceted.task.interfaces import IFacetedTaskContainer

from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable

from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.utils import is_attachment
from Products.urban import utils

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from collective.plonefinder.browser.interfaces import IFinderUploadCapable
from collective.quickupload.interfaces import IQuickUploadCapable
from Products.urban.config import *
from Products.urban import UrbanMessage as _

# code-section module-header #fill in your manual code here
from zope.i18n import translate
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from Products.ATContentTypes.configuration import zconf
from Products.Archetypes.Widget import RichWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.content.licence.base import UrbanBase
from Products.urban.interfaces import IOpinionRequestEvent
from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import get_interface_by_path
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from zope.globalrequest import getRequest

from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from plone import api

slave_fields_subdivision = (
    # if in subdivision, display a textarea the fill some details
    {
        "name": "subdivisionDetails",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "parcellings",
        "action": "show",
        "hide_values": (True,),
    },
)

slave_fields_watercourse = (
    # if a watercourse is select , display a select field with watercourse categories
    {
        "name": "watercourseCategories",
        "action": "show",
        "toggle_method": "showWatercourseCategories",
        "control_param": "values",
    },
)
slave_fields_pca = (
    # if in a pca, display a selectbox
    {
        "name": "pca",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "pcaDetails",
        "action": "show",
        "hide_values": (True,),
    },
    {
        "name": "pcaZone",
        "action": "show",
        "hide_values": (True,),
    },
)

slave_fields_tax = (
    # if other selected, show taxdetails field.
    {
        "name": "taxDetails",
        "action": "show",
        "hide_values": ("none", "other"),
    },
)

optional_fields = [
    "subdivisionDetails",
    "missingParts",
    "missingPartsDetails",
    "folderZoneDetails",
    "folderZone",
    "isInPCA",
    "roadType",
    "roadCoating",
    "roadEquipments",
    "pcaZone",
    "isInSubdivision",
    "solicitLocationOpinionsTo",
    "technicalRemarks",
    "locationTechnicalRemarks",
    "folderCategoryTownship",
    "protectedBuilding",
    "protectedBuildingDetails",
    "folderCategory",
    "pash",
    "pashDetails",
    "catchmentArea",
    "catchmentAreaDetails",
    "equipmentAndRoadRequirements",
    "SSC",
    "sscDetails",
    "RCU",
    "rcuDetails",
    "floodingLevel",
    "floodingLevelDetails",
    "solicitRoadOpinionsTo",
    "areParcelsVerified",
    "locationFloodingLevel",
    "licenceSubject",
    "referenceDGATLP",
    "roadMissingParts",
    "roadMissingPartsDetails",
    "locationMissingParts",
    "locationMissingPartsDetails",
    "PRevU",
    "prevuDetails",
    "PRenU",
    "prenuDetails",
    "airportNoiseZone",
    "airportNoiseZoneDetails",
    "description",
    "rgbsr",
    "rgbsrDetails",
    "karstConstraints",
    "karstConstraintsDetails",
    "concentratedRunoffSRisk",
    "concentratedRunoffSRiskDetails",
    "sevesoSite",
    "natura_2000",
    "sewers",
    "sewersDetails",
    "roadAnalysis",
    "futureRoadCoating",
    "expropriation",
    "expropriationDetails",
    "preemption",
    "preemptionDetails",
    "SAR",
    "sarDetails",
    "enoughRoadEquipment",
    "enoughRoadEquipmentDetails",
    "reparcelling",
    "reparcellingDetails",
    "noteworthyTrees",
    "pipelines",
    "pipelinesDetails",
    "tax",
    "groundStateStatus",
    "groundstatestatusDetails",
    "covid",
    "watercourse",
    "watercourseCategories",
    "trail",
    "trailDetails",
    "tax",
    "taxDetails",
    "photo",
    "dgrim",
    "publicHealthRecord",
    "setbackArea",
    "infrabel",
    "deadEndBuilding",
    "zoning",
]
# /code-section module-header

schema = Schema(
    (
        StringField(
            name="title",
            widget=StringField._properties["widget"](
                label=_("urban_label_title", default="Title"),
            ),
            required=True,
            schemata="urban_description",
            accessor="Title",
        ),
        StringField(
            name="licenceSubject",
            widget=StringField._properties["widget"](
                size=120,
                maxlength=500,
                label=_("urban_label_licenceSubject", default="Licencesubject"),
            ),
            schemata="urban_description",
        ),
        StringField(
            name="reference",
            widget=StringField._properties["widget"](
                size=60,
                label=_("urban_label_reference", default="Reference"),
            ),
            schemata="urban_description",
            validators=("isNotDuplicatedReference",),
        ),
        StringField(
            name="referenceDGATLP",
            widget=StringField._properties["widget"](
                size=60,
                label=_("urban_label_referenceDGATLP", default="Referencedgatlp"),
            ),
            schemata="urban_description",
        ),
        StringField(
            name="additionalReference",
            widget=StringField._properties["widget"](
                size=60,
                label=_(
                    "urban_label_additionalReference", default="Additionalreference"
                ),
            ),
            schemata="urban_description",
        ),
        DataGridField(
            name="workLocations",
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
                        workflow_states=("enabled",),
                    ),
                },
                helper_js=("datagridwidget.js", "datagridautocomplete.js"),
                label=_("urban_label_workLocations", default="Work locations"),
            ),
            allow_oddeven=True,
            columns=("number", "street"),
            validators=("isValidStreetName",),
        ),
        StringField(
            name="folderCategory",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_folderCategory", default="Foldercategory"),
            ),
            enforceVocabulary=True,
            schemata="urban_description",
            vocabulary=UrbanVocabulary("foldercategories", with_empty_value=True),
            default_method="getDefaultValue",
        ),
        StringField(
            name="tax",
            widget=MasterSelectWidget(
                slave_fields=slave_fields_tax,
                label=_("urban_label_tax", default="Tax"),
            ),
            enforceVocabulary=True,
            schemata="urban_description",
            vocabulary=UrbanVocabulary(
                "tax", with_empty_value=True, sort_on="sortable_title"
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="taxDetails",
            default_content_type="text/plain",
            allowable_content_types=("text/plain",),
            schemata="urban_description",
            default_method="getDefaultText",
            default_output_type="text/plain",
            accessor="Taxdetails",
            widget=TextAreaWidget(
                label=_("urban_label_taxDetails", default="Taxdetails"),
            ),
        ),
        LinesField(
            name="missingParts",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_missingParts", default="Missingparts"),
            ),
            schemata="urban_analysis",
            multiValued=True,
            vocabulary=UrbanVocabulary("missingparts"),
            default_method="getDefaultValue",
        ),
        TextField(
            name="missingPartsDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_missingPartsDetails", default="Missingpartsdetails"
                ),
            ),
            schemata="urban_analysis",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        ImageField(
            name="photo",
            max_size=zconf.ATImage.max_image_dimension,
            pil_resize_algo=zconf.pil_config.resize_algo,
            sizes={
                "large": (768, 768),
                "preview": (400, 400),
                "mini": (200, 200),
                "thumb": (128, 128),
                "tile": (64, 64),
                "icon": (32, 32),
                "listing": (16, 16),
            },
            widget=ImageWidget(
                label=_("urban_label_photos", default="Photos"),
            ),
            schemata="urban_description",
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
        LinesField(
            name="roadMissingParts",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_roadMissingParts", default="Roadmissingparts"),
            ),
            schemata="urban_road",
            multiValued=True,
            vocabulary=UrbanVocabulary("roadmissingparts"),
            default_method="getDefaultValue",
        ),
        TextField(
            name="roadMissingPartsDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_roadMissingPartsDetails",
                    default="Roadmissingpartsdetails",
                ),
            ),
            schemata="urban_road",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="roadType",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_roadType", default="Roadtype"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "folderroadtypes", inUrbanConfig=False, with_empty_value=False
            ),
            default_method="getDefaultValue",
        ),
        LinesField(
            name="roadAnalysis",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_roadAnalysis", default="Roadanalysis"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary("roadanalysis"),
            default_method="getDefaultValue",
        ),
        StringField(
            name="roadCoating",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_roadCoating", default="Roadcoating"),
            ),
            schemata="urban_road",
            vocabulary=UrbanVocabulary(
                "folderroadcoatings", inUrbanConfig=False, with_empty_value=True
            ),
            default_method="getDefaultValue",
        ),
        StringField(
            name="futureRoadCoating",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_futureRoadCoating", default="Futureroadcoating"),
            ),
            schemata="urban_road",
            vocabulary=UrbanVocabulary(
                "folderroadcoatings", inUrbanConfig=False, with_empty_value=True
            ),
            default_method="getDefaultValue",
        ),
        DataGridField(
            name="roadEquipments",
            schemata="urban_road",
            widget=DataGridWidget(
                columns={
                    "road_equipment": SelectColumn(
                        "Road equipments",
                        UrbanVocabulary("folderroadequipments", inUrbanConfig=False),
                    ),
                    "road_equipment_details": Column("Road equipment details"),
                },
                label=_("urban_label_roadEquipments", default="Roadequipments"),
            ),
            allow_oddeven=True,
            columns=("road_equipment", "road_equipment_details"),
        ),
        StringField(
            name="sewers",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_sewers", default="Sewers"),
            ),
            schemata="urban_road",
            vocabulary=UrbanVocabulary(
                "sewers", inUrbanConfig=False, with_empty_value=True
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="sewersDetails",
            widget=RichWidget(
                label=_("urban_label_sewersDetails", default="Sewersdetails"),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_road",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="pash",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_pash", default="Pash"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary("pashs", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="pashDetails",
            widget=RichWidget(
                label=_("urban_label_pashDetails", default="Pashdetails"),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_road",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="catchmentArea",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_catchmentArea", default="Catchmentarea"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary_factory="urban.vocabulary.CatchmentArea",
        ),
        TextField(
            name="catchmentAreaDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_catchmentAreaDetails", default="Catchmentareadetails"
                ),
            ),
            schemata="urban_road",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="karstConstraints",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_karstConstraints", default="Karstconstraints"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary("karst_constraints", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="karstConstraintsDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_karstConstraintsDetails",
                    default="Karstconstraintsdetails",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="concentratedRunoffSRisk",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_concentratedRunoffSRisk",
                    default="concentratedrunoffsrisk",
                ),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "concentrated_runoff_s_risk", inUrbanConfig=False
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="concentratedRunoffSRiskDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_concentratedRunoffSRiskDetails",
                    default="concentratedrunoffsriskdetails",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="sevesoSite",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_sevesoSite", default="sevesosite"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary("seveso_site", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        LinesField(
            name="pipelines",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_pipelines", default="pipelines"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary("pipelines", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="pipelinesDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pipelinesDetails", default="Pipelinesdetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="natura_2000",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_natura_2000", default="natura_2000"),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary_factory="urban.vocabulary.Natura2000",
            default_method="getDefaultValue",
        ),
        LinesField(
            name="floodingLevel",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_floodingLevel", default="Floodinglevel"),
            ),
            multiValued=True,
            schemata="urban_road",
            vocabulary="listFloodingLevels",
        ),
        TextField(
            name="floodingLevelDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_floodingLevelDetails", default="Floodingleveldetails"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="equipmentAndRoadRequirements",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_equipmentAndRoadRequirements",
                    default="Equipmentandroadrequirements",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="technicalRemarks",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_technicalRemarks", default="Technicalremarks"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_road",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="groundStateStatus",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_groundStateStatus", default="Groundstatestatus"),
            ),
            schemata="urban_road",
            vocabulary=UrbanVocabulary("groundstatestatus", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="groundstatestatusDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_groundStateStatusDetails",
                    default="Groundstatestatusdetails",
                ),
            ),
            schemata="urban_road",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="locationMissingParts",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_locationMissingParts", default="Locationmissingparts"
                ),
            ),
            schemata="urban_location",
            multiValued=True,
            vocabulary=UrbanVocabulary("locationmissingparts"),
            default_method="getDefaultValue",
        ),
        TextField(
            name="locationMissingPartsDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_locationMissingPartsDetails",
                    default="Locationmissingpartsdetails",
                ),
            ),
            schemata="urban_location",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="folderZone",
            widget=MultiSelect2Widget(
                size=10,
                label=_("urban_label_folderZone", default="Folderzone"),
            ),
            schemata="urban_location",
            multiValued=True,
            vocabulary_factory="urban.vocabulary.AreaPlan",
            default_method="getDefaultValue",
        ),
        TextField(
            name="folderZoneDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_folderZoneDetails", default="Folderzonedetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="isInPCA",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_pca,
                label=_("urban_label_isInPCA", default="Isinpca"),
            ),
            schemata="urban_location",
        ),
        StringField(
            name="pca",
            widget=SelectionWidget(
                label=_("urban_label_pca", default="Pca"),
            ),
            schemata="urban_location",
            vocabulary=UrbanVocabulary("pcas", vocType="PcaTerm", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="pcaDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pcaDetails", default="Pcadetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="pcaZone",
            widget=MultiSelect2Widget(
                size=10,
                label=_("urban_label_pcaZone", default="Pcazone"),
            ),
            schemata="urban_location",
            multiValued=True,
            vocabulary_factory="urban.vocabulary.PCAZones",
            default_method="getDefaultValue",
        ),
        BooleanField(
            name="isInSubdivision",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_subdivision,
                label=_("urban_label_isInSubdivision", default="Isinsubdivision"),
            ),
            schemata="urban_location",
        ),
        TextField(
            name="subdivisionDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                description=_(
                    "urban_descr_subdivisionDetails", default="Number of the lots, ..."
                ),
                label=_("urban_label_subdivisionDetails", default="Subdivisiondetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="locationFloodingLevel",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_locationFloodingLevel", default="Locationfloodinglevel"
                ),
            ),
            multiValued=True,
            schemata="urban_location",
            vocabulary="listFloodingLevels",
        ),
        BooleanField(
            name="expropriation",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_expropriation", default="expropriation"),
            ),
            schemata="urban_location",
        ),
        TextField(
            name="expropriationDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_expropriationDetails", default="Expropriationdetails"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="preemption",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_preemption", default="preemption"),
            ),
            schemata="urban_location",
        ),
        TextField(
            name="preemptionDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_preemptionDetails", default="Preemptiondetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="SAR",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_SAR", default="sar"),
            ),
            schemata="urban_location",
        ),
        TextField(
            name="sarDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_sarDetails", default="Sardetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="enoughRoadEquipment",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_enoughRoadEquipment", default="enoughRoadEquipment"
                ),
            ),
            schemata="urban_location",
        ),
        TextField(
            name="enoughRoadEquipmentDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_enoughRoadEquipmentDetails",
                    default="Enoughroadequipmentdetails",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="locationTechnicalRemarks",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_locationTechnicalRemarks",
                    default="Locationtechnicalremarks",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_analysis",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="solicitRoadOpinionsTo",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_solicitRoadOpinionsTo", default="Solicitroadopinionsto"
                ),
            ),
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "eventconfigs",
                vocType="OpinionEventConfig",
                value_to_use="abbreviation",
            ),
            default_method="getDefaultValue",
        ),
        LinesField(
            name="protectedBuilding",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_protectedBuilding", default="Protectedbuilding"),
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
                label=_(
                    "urban_label_protectedBuildingDetails",
                    default="Protectedbuildingdetails",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_patrimony",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="SSC",
            widget=MultiSelect2Widget(
                size=15,
                label=_("urban_label_SSC", default="Ssc"),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary("ssc", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="sscDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_sscDetails", default="Sscdetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="RCU",
            widget=MultiSelect2Widget(
                size=10,
                label=_("urban_label_RCU", default="Rcu"),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary("rcu", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="rcuDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_rcuDetails", default="Rcudetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="PRenU",
            widget=MultiSelect2Widget(
                size=5,
                label=_("urban_label_PRenU", default="Prenu"),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary("prenu", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="prenuDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_prenuDetails", default="Prenudetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="PRevU",
            widget=MultiSelect2Widget(
                size=5,
                label=_("urban_label_PRevU", default="Prevu"),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary("prevu", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="prevuDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_prevuDetails", default="Prevudetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="reparcelling",
            widget=MultiSelect2Widget(
                size=5,
                label=_("urban_label_reparcelling", default="Prevu"),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary("reparcelling", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="reparcellingDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_reparcellingDetails", default="Reparcellingdetails"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        StringField(
            name="rgbsr",
            widget=SelectionWidget(
                label=_("urban_label_rgbsr", default="Rgbsr"),
            ),
            schemata="urban_location",
            vocabulary=UrbanVocabulary(
                "rgbsr", inUrbanConfig=False, with_empty_value=True
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="rgbsrDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_rgbsrDetails", default="Rgbsrdetails"),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="airportNoiseZone",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_airportNoiseZone", default="Airportnoisezone"),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary("airportnoisezone", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="airportNoiseZoneDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_airportNoiseZoneDetails",
                    default="Airportnoisezonedetails",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            schemata="urban_location",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="solicitLocationOpinionsTo",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_solicitLocationOpinionsTo",
                    default="Solicitlocationopinionsto",
                ),
            ),
            schemata="urban_location",
            multiValued=True,
            vocabulary=UrbanVocabulary(
                "eventconfigs",
                vocType="OpinionEventConfig",
                value_to_use="abbreviation",
            ),
            default_method="getDefaultValue",
        ),
        StringField(
            name="folderCategoryTownship",
            widget=SelectionWidget(
                label=_(
                    "urban_label_folderCategoryTownship",
                    default="Foldercategorytownship",
                ),
            ),
            enforceVocabulary=True,
            schemata="urban_location",
            vocabulary=UrbanVocabulary(
                "townshipfoldercategories",
                with_empty_value=True,
                sort_on="sortable_title",
            ),
            default_method="getDefaultValue",
        ),
        BooleanField(
            name="areParcelsVerified",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_areParcelsVerified", default="Areparcelsverified"),
            ),
            schemata="urban_location",
        ),
        ReferenceField(
            name="foldermanagers",
            widget=ReferenceBrowserWidget(
                allow_browse=False,
                base_query="foldermanagersBaseQuery",
                only_for_review_states="enabled",
                show_results_without_query=True,
                wild_card_search=True,
                allow_search=False,
                label=_("urban_label_foldermanagers", default="Foldermanagers"),
            ),
            relationship="licenceFolderManagers",
            required=True,
            schemata="urban_description",
            multiValued=True,
            allowed_types=("FolderManager",),
        ),
        ReferenceField(
            name="parcellings",
            widget=ReferenceBrowserWidget(
                force_close_on_insert=True,
                allow_search=True,
                only_for_review_states="enabled",
                allow_browse=True,
                show_indexes=True,
                available_indexes={"Title": "Nom"},
                show_index_selector=True,
                wild_card_search=True,
                startup_directory="urban/parcellings",
                restrict_browsing_to_startup_directory=True,
                default_search_index="Title",
                label=_("urban_label_parcellings", default="Parcellings"),
            ),
            allowed_types=("Parcelling",),
            schemata="urban_location",
            multiValued=False,
            relationship="licenceParcelling",
        ),
        LinesField(
            name="noteworthyTrees",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_noteworthyTrees", default="Noteworthytrees"),
            ),
            schemata="urban_location",
            multiValued=True,
            vocabulary=UrbanVocabulary("noteworthytrees", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        BooleanField(
            name="dgrim",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_dgrim", default="dgrim"),
            ),
            schemata="urban_location",
        ),
        LinesField(
            name="zoning",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_zoning", default="Zoning"),
            ),
            schemata="urban_location",
            multiValued=True,
            vocabulary=UrbanVocabulary(path="zoning", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        BooleanField(
            name="publicHealthRecord",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_publicHealthRecord", default="PublicHealthRecord"),
            ),
            schemata="urban_location",
        ),
        BooleanField(
            name="setbackArea",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_setbackArea", default="SetbackArea"),
            ),
            schemata="urban_location",
        ),
        BooleanField(
            name="infrabel",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_infrabel", default="Infrabel"),
            ),
            schemata="urban_location",
        ),
        BooleanField(
            name="deadEndBuilding",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_deadEndBuilding", default="DeadEndBuilding"),
            ),
            schemata="urban_location",
        ),
        BooleanField(
            name="covid",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_covid", default="COVID19"),
            ),
            schemata="urban_description",
        ),
        LinesField(
            name="watercourse",
            widget=MasterMultiSelectWidget(
                format="checkbox",
                slave_fields=slave_fields_watercourse,
                label=_("urban_label_watercourse", default="Watercourse"),
            ),
            enforceVocabulary=True,
            schemata="urban_location",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "watercourses", with_empty_value=False, inUrbanConfig=False
            ),
            default_method="getDefaultValue",
        ),
        LinesField(
            name="watercourseCategories",
            widget=MasterMultiSelectWidget(
                format="checkbox",
                label=_(
                    "urban_label_watercourseCategories", default="WatercourseCategories"
                ),
            ),
            schemata="urban_location",
            multiValued=1,
            vocabulary="listWatercourseCategories",
        ),
        LinesField(
            name="trail",
            widget=MasterMultiSelectWidget(
                format="checkbox",
                label=_("urban_label_trail", default="Trail"),
            ),
            enforceVocabulary=True,
            schemata="urban_road",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "trails", with_empty_value=False, inUrbanConfig=False
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="trailDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_trailDetails", default="TrailDetails"),
            ),
            schemata="urban_road",
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
    ),
)

# code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
# /code-section after-local-schema

GenericLicence_schema = OrderedBaseFolderSchema.copy() + schema.copy()

# code-section after-schema #fill in your manual code here
GenericLicence_schema["title"].searchable = True
GenericLicence_schema["title"].widget.visible = False
# /code-section after-schema


class GenericLicence(OrderedBaseFolder, UrbanBase, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(
        interfaces.IGenericLicence,
        IFacetedTaskContainer,
        IPossibleFacetedNavigable,
        IFinderUploadCapable,
        IQuickUploadCapable,
    )

    meta_type = "GenericLicence"
    _at_rename_after_creation = True
    # block local roles acquisition and let the workflow handle that
    __ac_local_roles_block__ = True

    schema = GenericLicence_schema

    # code-section class-header #fill in your manual code here
    # /code-section class-header

    # Methods

    security.declarePublic("getDefaultReference")

    def getDefaultReference(self):
        """
        Returns the reference for the new element
        """
        return self.getLicenceConfig().generateReference(self)

    # Manually created methods

    security.declarePublic("getRepresentatives")

    def getRepresentatives(self):
        """
        To override per licence type
        """
        return []

    security.declarePublic("getDefaultValue")

    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return [""]

        empty_value = getattr(field, "multivalued", "") and [] or ""
        if hasattr(field, "vocabulary") and isinstance(
            field.vocabulary, UrbanVocabulary
        ):
            return field.vocabulary.get_default_values(context)
        return empty_value

    security.declarePublic("getDefaultText")

    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = api.portal.get_tool("portal_urban")
        return urban_tool.getTextDefaultValue(field.getName(), context, html)

    security.declarePublic("getLicenceConfig")

    def getLicenceConfig(self):
        portal_urban = api.portal.get_tool("portal_urban")

        config_folder = portal_urban.getLicenceConfig(self)

        return config_folder

    security.declarePublic("attributeIsUsed")

    def attributeIsUsed(self, name):
        """
        Is the attribute named as param name used in this LicenceConfig ?
        """
        licenceConfig = self.getLicenceConfig()
        return name in licenceConfig.getUsedAttributes()

    security.declarePublic("createUrbanEvent")

    def createUrbanEvent(self, urban_event_type, **kwargs):
        """
        urban_event_type can either be an id, an uid or the object
        """
        urban_event = createObject("UrbanEvent", self, urban_event_type, **kwargs)
        return urban_event

    def divideList(self, divider, list):
        res = []
        part = len(list) / divider
        remain = len(list) % divider
        for i in range(part):
            res.append(list[i * divider : (i + 1) * divider])
        if remain > 0:
            res.append(list[divider * part : divider * part + remain])
        return tuple(res)

    def templateRoadEquipments(self, tup):
        res = []
        for pair in tup:
            res.append(pair["road_equipment"])
        return tuple(res)

    def templateRoadEquipmentDetail(self, tup):
        res = {}
        for pair in tup:
            res[pair["road_equipment"]] = pair["road_equipment_details"]
        return res

    def templateAllOpinions(self):
        all_opinions = list(self.getSolicitRoadOpinionsTo())
        location_opinions = self.getSolicitLocationOpinionsTo()
        if hasattr(self, "getLastInquiry"):
            inquiry = self.getLastInquiry()
        else:
            inquiry = None
        inquiry_opinions = None
        if inquiry is not None:
            inquiry_opinions = inquiry.getLinkedInquiry().getSolicitOpinionsTo()
        opinion_tank_list = [location_opinions, inquiry_opinions]
        for opinion_tank in opinion_tank_list:
            if opinion_tank is not None:
                for opinion in opinion_tank:
                    if opinion not in all_opinions:
                        all_opinions.append(opinion)
        return tuple(all_opinions)

    security.declarePublic("listCatchmentAreas")

    def listCatchmentAreas(self):
        """
        This vocabulary for field catchmentArea returns a list of
        catchment areas : close prevention area, far prevention area,
        supervision area or outside catchment
        """
        vocab = (
            ("close", translate(_("close_prevention_area"), context=self.REQUEST)),
            ("far", translate(_("far_prevention_area"), context=self.REQUEST)),
            ("supervision", translate(_("supervision_area"), context=self.REQUEST)),
            ("ouside", translate(_("outside_catchment"), context=self.REQUEST)),
        )

        return DisplayList(vocab)

    security.declarePublic("listFloodingLevels")

    def listFloodingLevels(self):
        """
        This vocabulary for field floodingLevel returns a list of
        flooding levels : no risk, low risk, moderated risk, high risk
        """
        vocab = (
            ("no", translate(_("flooding_level_no"), context=self.REQUEST)),
            ("very low", translate(_("flooding_level_verylow"), context=self.REQUEST)),
            ("low", translate(_("flooding_level_low"), context=self.REQUEST)),
            (
                "low_to_moderate",
                translate(_("flooding_level_low_to_moderate"), context=self.REQUEST),
            ),
            (
                "low_to_high",
                translate(_("flooding_level_low_to_high"), context=self.REQUEST),
            ),
            ("moderate", translate(_("flooding_level_moderate"), context=self.REQUEST)),
            (
                "moderate_to_high",
                translate(_("flooding_level_moderate_to_high"), context=self.REQUEST),
            ),
            ("high", translate(_("flooding_level_high"), context=self.REQUEST)),
        )

        return DisplayList(vocab)

    security.declarePublic("foldermanagersBaseQuery")

    def foldermanagersBaseQuery(self):
        """ """
        portal = api.portal.get_tool("portal_url").getPortalObject()
        rootPath = "/".join(portal.getPhysicalPath())
        urban_tool = api.portal.get_tool("portal_urban")
        ids = []
        for foldermanager in urban_tool.foldermanagers.objectValues():
            if self.getPortalTypeName() in foldermanager.getManageableLicences():
                ids.append(foldermanager.getId())
        dict = {}
        dict["path"] = {"query": "%s/portal_urban/foldermanagers" % (rootPath)}
        dict["id"] = ids
        return dict

    security.declarePublic("getParcels")

    def getParcels(self):
        """
        Return the list of parcels (portionOut) for the Licence
        """
        return [obj for obj in self.objectValues() if obj.portal_type == "Parcel"]

    security.declarePublic("getOfficialParcels")

    def getOfficialParcels(self):
        """
        Return the list of parcels (portionOut) for the Licence
        """
        parcels = [prc for prc in self.getParcels() if prc.isOfficialParcel]
        return parcels

    security.declarePublic("updateTitle")

    def updateTitle(self):
        """
        Update the title to clearly identify the licence
        """
        if self.getApplicants():
            applicants_display = ", ".join(
                [app.Title() for app in self.getApplicants()]
            )
        else:
            applicants_display = translate(
                "no_applicant_defined", "urban", context=self.REQUEST
            ).encode("utf8")
        title = "%s - %s - %s" % (
            self.getReference(),
            self.getLicenceSubject(),
            applicants_display,
        )
        self.setTitle(title)
        self.reindexObject(
            idxs=(
                "Title",
                "applicantInfosIndex",
                "sortable_title",
            )
        )

    security.declarePublic("getAttachments")

    def getAttachments(self):
        """
        Return the attachments (File) of the UrbanEvent
        """
        attachments = [obj for obj in self.objectValues() if is_attachment(obj)]
        return attachments

    security.declarePublic("getAnnoncedDelay")

    def getAnnoncedDelay(self, theObject=False):
        """
        Returns the annonced delay value or the UrbanDelay if theObject=True
        """
        field = self.getField("annoncedDelay")
        if not field:
            return None
        res = field.get(self)
        if res and theObject:
            urbanConfig = self.getLicenceConfig()
            res = getattr(urbanConfig.folderdelays, res)
        return res

    security.declarePublic("getPca")

    def getPca(self, theObject=False):
        """
        Returns the pca value or the PcaTerm if theObject=True
        """
        res = self.getField("pca").get(self)
        if type(res) is str and theObject:
            portal_urban = api.portal.get_tool("portal_urban")
            res = getattr(portal_urban.pcas, res, None)
        return res

    security.declarePublic("getOpinionRequests")

    def getOpinionRequests(self, organisation=""):
        """
        Returns the existing opinion requests
        """
        opinionRequests = self.objectValues("UrbanEventOpinionRequest")
        if organisation == "":
            return opinionRequests
        res = []
        for opinionRequest in opinionRequests:
            if opinionRequest.getLinkedOrganisationTermId() == organisation:
                res.append(opinionRequest)
        return res

    security.declarePublic("createAllAdvices")

    def createAllAdvices(self):
        """
        Create all urbanEvent corresponding to advice on a licence
        """
        urban_tool = api.portal.get_tool("portal_urban")
        opinionevent_configs = self.getAllAdvices()
        for opinionevent_config in opinionevent_configs:
            opinionevent_config.checkCreationInLicence(self)
            portal_type = opinionevent_config.getEventPortalType() or "UrbanEvent"

            newUrbanEventId = self.invokeFactory(
                portal_type,
                id=urban_tool.generateUniqueId(portal_type),
                title=opinionevent_config.Title(),
                urbaneventtypes=(opinionevent_config,),
            )
            newUrbanEventObj = getattr(self, newUrbanEventId)
            if opinionevent_config.id in self.solicitOpinionsToOptional:
                newUrbanEventObj.isOptional = True
            newUrbanEventObj.processForm()

        notify(ObjectModifiedEvent(self))
        return self.REQUEST.RESPONSE.redirect(
            self.absolute_url() + "/view?#fieldsetlegend-urban_events"
        )

    security.declarePublic("getAllAdvices")

    def getAllAdvices(self):
        """
        Returns all UrbanEvents corresponding to advice on a licence
        """
        licence_config = self.getLicenceConfig()
        event_configs = licence_config.getEnabledEventConfigs()
        res = []
        for event_config in event_configs:
            if (
                event_config.portal_type == "OpinionEventConfig"
                and event_config.canBeCreatedInLicence(self)
            ):
                res.append(event_config)
        return res

    security.declarePublic("hasEventNamed")

    def hasEventNamed(self, title):
        """
        Tells if the licence contains an urbanEvent named 'title'
        """
        for obj in self.objectValues():
            if IUrbanEvent.providedBy(obj) and obj.Title() == title:
                return True
        return False

    security.declarePublic("hasNoEventNamed")

    def hasNoEventNamed(self, title):
        """
        Tells if the licence does not contain any urbanEvent named 'title'
        """
        return not self.hasEventNamed(title)

    security.declarePublic("listWatercourseCategories")

    def listWatercourseCategories(self):
        """
        list of watercourse categories
        """
        vocab = (
            ("watercourse_cat1", translate(_("category1"), context=self.REQUEST)),
            ("watercourse_cat2", translate(_("category2"), context=self.REQUEST)),
            ("watercourse_cat3", translate(_("category3"), context=self.REQUEST)),
        )
        return DisplayList(vocab)

    security.declarePublic("showWatercourseCategories")

    def showWatercourseCategories(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        show = len(selection) > 0
        return show

    security.declarePublic("getLicencesOfTheParcels")

    def getFirstDeposit(self):
        return self.getFirstEvent(interfaces.IDepositEvent)

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getFirstPatrimonyMeeting(self):
        return self.getFirstEvent(interfaces.IPatrimonyMeetingEvent)

    def getLastPatrimonyMeeting(self):
        return self.getLastEvent(interfaces.IPatrimonyMeetingEvent)

    def getAllPatrimonyMeeting(self):
        return self.getAllEvents(interfaces.IPatrimonyMeetingEvent)

    def getLastPreliminaryWarning(self):
        return self.getLastEvent(interfaces.IPreliminaryWarningEvent)

    def getLastSimpleCollege(self):
        return self.getLastEvent(interfaces.ISimpleCollegeEvent)

    def getLastMayorCollege(self):
        return self.getLastEvent(interfaces.IMayorCollegeEvent)

    def getAllMayorColleges(self):
        return self.getAllEvents(interfaces.IMayorCollegeEvent)

    def getLastSuspension(self):
        return self.getLastEvent(interfaces.ISuspensionEvent)

    def getAllSuspensionEvents(self):
        return self.getAllEvents(interfaces.ISuspensionEvent)

    def getIntentionToSubmitAmendedPlans(self):
        return self.getLastEvent(interfaces.IIntentionToSubmitAmendedPlans)

    def getAllEvents(self, eventInterface=IUrbanEvent, state=None):
        return self.getAllEventsByObjectValues(eventInterface, state=state)

    def getAllEventsByObjectValues(self, eventInterface, state=None):
        events = [
            evt
            for evt in self.objectValues()
            if not eventInterface or eventInterface.providedBy(evt)
        ]
        if state:
            events = [evt for evt in events if api.content.get_state(evt) == state]
        return events

    def getLastEvent(self, eventInterface=None, state=None):
        events = self.getAllEvents(eventInterface, state)
        if events:
            return events[-1]

    def getFirstEvent(self, eventInterface=None):
        events = self.getAllEvents(eventInterface)
        if events:
            return events[0]

    def getLastEventWithValidityDate(self):
        events = [
            event
            for event in self.getAllEvents()
            if getattr(event, "validityEndDate", None) is not None
        ]
        if len(events) == 0:
            return None
        return events[-1]

    def get_bound_roaddecrees(self):
        roaddecrees = []
        annotations = IAnnotations(self)
        roaddecree_UIDs = list(annotations.get("urban.bound_roaddecrees", []))
        if roaddecree_UIDs:
            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog(UID=roaddecree_UIDs)
            roaddecrees = [b.getObject() for b in brains]
            return roaddecrees
        return []

    def get_bound_inspections(self):
        inspections = []
        annotations = IAnnotations(self)
        roaddecree_UIDs = list(annotations.get("urban.bound_inspections", []))
        if roaddecree_UIDs:
            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog(UID=roaddecree_UIDs)
            inspections = [b.getObject() for b in brains]
            return inspections
        return []

    def get_bound_tickets(self):
        tickets = []
        annotations = IAnnotations(self)
        roaddecree_UIDs = list(annotations.get("urban.bound_tickets", []))
        if roaddecree_UIDs:
            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog(UID=roaddecree_UIDs)
            tickets = [b.getObject() for b in brains]
            return tickets
        return []

    def get_first_deposit_date(self):
        deposit = self.getFirstDeposit()
        if not deposit:
            return
        if not deposit.eventDate:
            return
        return deposit.eventDate

    security.declarePublic("is_CODT2024")

    def is_CODT2024(self):
        """Return if we are in the new reform of CODT"""
        now = utils.now()
        deposit = self.getFirstDeposit()
        if not deposit and now >= datetime(2024, 4, 1):
            return True
        if not deposit:
            return False
        if not deposit.eventDate:
            return False
        deposit_date = deposit.eventDate.asdatetime()
        return deposit_date >= datetime(2024, 4, 1, tzinfo=deposit_date.tzinfo)

    security.declarePublic("is_not_CODT2024")

    def is_not_CODT2024(self):
        """Return if we are in the new reform of CODT"""
        return not self.is_CODT2024()

    security.declarePublic("getProrogationDelay")

    def getProrogationDelay(self, text_format=True):
        """Return the delay in text (default) or in integer based on the CODT reform"""
        # Should filter on types as well
        request = getRequest()
        delay = 30
        if self.is_CODT2024() is True:
            delay = 20
        if text_format is True:
            return translate(_("${nbr} days", mapping={"nbr": delay}), context=request)
        return delay

    security.declarePublic("getCompletenessDelay")

    def getCompletenessDelay(self, text_format=True):
        """Return the delay in text (default) or in integer based on the CODT reform"""
        request = getRequest()
        delay = 20
        if self.is_CODT2024() is True:
            delay = 30
        if text_format is True:
            return translate(_("${nbr} days", mapping={"nbr": delay}), context=request)
        return delay

    security.declarePublic("getReferFDDelay")

    def getReferFDDelay(self, text_format=True):
        """Return the delay in text (default) or in integer based on the CODT reform"""
        request = getRequest()
        delay = 40
        if self.is_CODT2024() is True:
            delay = 30
        if text_format is True:
            return translate(_("${nbr} days", mapping={"nbr": delay}), context=request)
        return delay

    security.declarePublic("getFDAdviceDelay")

    def getFDAdviceDelay(self, text_format=True):
        """Return the delay in text (default) or in integer based on the CODT reform"""
        request = getRequest()
        delay = 35
        if self.is_CODT2024() is True:
            delay = 30
        if text_format is True:
            return translate(_("${nbr} days", mapping={"nbr": delay}), context=request)
        return delay


registerType(GenericLicence, PROJECTNAME)
# end of class GenericLicence

# code-section module-footer #fill in your manual code here
# /code-section module-footer
