# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.Archetypes.atapi import *
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban import interfaces
from Products.urban import UrbanMessage as _
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import PROJECTNAME
from Products.urban.config import URBAN_TYPES
from Products.urban.content.Inquiry import Inquiry
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.licence.BaseInspection import BaseInspection
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import setSchemataForInquiry
from collective.archetypes.select2.select2widget import MultiSelect2Widget
from zope.interface import implements


optional_fields = [
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


slave_fields_bound_licence = (
    {
        "name": "workLocations",
        "action": "hide",
        "hide_values": (True,),
    },
)

schema = Schema(
    (
        StringField(
            name="referenceProsecution",
            widget=StringField._properties["widget"](
                size=60,
                label=_(
                    "urban_label_referenceProsecution", default="Referenceprosecution"
                ),
            ),
            schemata="urban_description",
        ),
        StringField(
            name="policeTicketReference",
            widget=StringField._properties["widget"](
                size=60,
                label=_(
                    "urban_label_policeTicketReference", default="Policeticketreference"
                ),
            ),
            schemata="urban_description",
        ),
        ReferenceField(
            name="bound_licences",
            widget=ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=False,
                force_close_on_insert=True,
                startup_directory="urban",
                show_indexes=False,
                wild_card_search=True,
                restrict_browsing_to_startup_directory=True,
                label=_("urban_label_bound_licences", default="Bound licences"),
            ),
            allowed_types=[
                t
                for t in URBAN_TYPES
                if t
                not in [
                    "Inspection",
                    "Ticket",
                    "ProjectMeeting",
                    "PatrimonyCertificate",
                    "CODT_UrbanCertificateOne",
                    "UrbanCertificateOne",
                ]
            ],
            schemata="urban_description",
            multiValued=True,
            relationship="bound_licences",
        ),
        BooleanField(
            name="use_bound_licence_infos",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_bound_licence,
                label=_(
                    "urban_label_use_bound_licence_infos",
                    default="Use_bound_licence_infos",
                ),
            ),
            schemata="urban_description",
        ),
        StringField(
            name="inspection_context",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_inspection_context", default="Inspection_context"),
            ),
            enforceVocabulary=True,
            schemata="urban_description",
            vocabulary=UrbanVocabulary("inspectioncontexts", with_empty_value=True),
            default_method="getDefaultValue",
        ),
        TextField(
            name="inspectionDescription",
            widget=RichWidget(
                label=_(
                    "urban_label_inspectionDescription", default="Inspectiondescription"
                ),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_inspection",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="observationItems",
            widget=MultiSelectionWidget(
                format="checkbox",
                label=_("urban_label_observationItems", default="ObservationItems"),
                i18n_domain="urban",
            ),
            multiValued=True,
            optional=True,
            schemata="urban_inspection",
            vocabulary=UrbanVocabulary("observationitems", inUrbanConfig=True),
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
setOptionalAttributes(schema, ["observationItems"])
Inspection_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(Inquiry, "schema", Schema(())).copy()
    + schema.copy()
)

setOptionalAttributes(Inspection_schema, optional_fields)
setSchemataForInquiry(Inspection_schema)


class Inspection(BaseInspection):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IInspection)

    meta_type = "Inspection"
    _at_rename_after_creation = True
    schema = Inspection_schema



registerType(Inspection, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema["folderCategory"].widget.visible = {"edit": "invisible", "view": "invisible"}
    schema.moveField("referenceProsecution", after="reference")
    schema.moveField("policeTicketReference", after="referenceProsecution")
    schema.moveField("description", after="inspection_context")
    schema.moveField("general_disposition", after="protectedBuilding")
    schema.moveField("patrimony", after="general_disposition")
    schema.moveField("bound_licences", before="workLocations")
    schema.moveField("use_bound_licence_infos", after="bound_licences")
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
    schema["complementary_delay"].schemata = "urban_description"
    return schema


finalize_schema(Inspection_schema)
