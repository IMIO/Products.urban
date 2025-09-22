# encoding: utf-8

from Acquisition import aq_parent
from eea.facetednavigation.interfaces import ICriteria
from OFS.interfaces import IOrderedContainer
from Products.urban import UrbanMessage as _
from Products.urban.config import URBAN_TYPES
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import IGenericLicence
from Products.urban.migration.utils import refresh_workflow_permissions
from Products.urban.setuphandlers import createFolderDefaultValues
from Products.urban.setuphandlers import createVocabularyFolder
from imio.schedule.content.object_factories import MacroCreationConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject
from imio.schedule.content.object_factories import MacroFreezeConditionObject
from imio.schedule.content.object_factories import MacroRecurrenceConditionObject
from imio.schedule.content.object_factories import MacroStartConditionObject
from imio.schedule.content.object_factories import MacroThawConditionObject
from imio.schedule.events.zope_registration import (
    register_schedule_collection_criterion,
)
from imio.schedule.events.zope_registration import register_task_collection_criterion
from imio.schedule.events.zope_registration import (
    subscribe_task_configs_for_content_type,
)
from imio.schedule.events.zope_registration import (
    unregister_schedule_collection_criterion,
)
from imio.schedule.events.zope_registration import unregister_task_collection_criterion
from imio.schedule.events.zope_registration import (
    unsubscribe_task_configs_for_content_type,
)
from plone import api
from plone.registry import Record
from plone.registry.field import Dict
from plone.registry.field import TextLine
from plone.registry.field import List
from plone.registry.interfaces import IRegistry
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter
from zope.component import getUtility

import logging


def rename_patrimony_certificate(context):
    """ """
    logger = logging.getLogger("urban: rename Patrimony certificate")
    logger.info("starting upgrade steps")
    portal = api.portal.get()

    patrimony_folder = portal.urban.patrimonycertificates
    patrimony_folder.setTitle(u"Patrimoines")
    patrimony_folder.reindexObject(["Title"])

    patrimony_collection = (
        portal.urban.patrimonycertificates.collection_patrimonycertificate
    )
    patrimony_collection.setTitle(u"Patrimoines")
    patrimony_collection.reindexObject(["Title"])

    patrimony_config_folder = portal.portal_urban.patrimonycertificate
    patrimony_config_folder.setTitle(u"Paramètres des patrimoines")
    patrimony_config_folder.reindexObject(["Title"])

    logger.info("upgrade step done!")


def rename_content_rule(context):
    """ """
    logger = logging.getLogger("urban: Rename a content rules")
    logger.info("starting upgrade steps")

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:default", "contentrules"
    )

    logger.info("upgrade step done!")


def fix_supended_state_licence(context):
    logger = logging.getLogger("urban: Fix supended state licence")
    logger.info("starting upgrade steps")
    portal = api.portal.get()
    urban_path = "/".join(portal["urban"].getPhysicalPath())
    refresh_workflow_permissions(
        "codt_buildlicence_workflow",
        folder_path=urban_path,
        for_states=["suspension", "frozen_suspension"],
    )
    logger.info("upgrade done!")


def log_info(logger, msg):
    if logger:
        logger.info(msg)


def _replace_object(obj, new_type, condition=None, logger=None):
    portal = api.portal.get()
    request = portal.REQUEST
    container = aq_parent(obj)

    ordered = IOrderedContainer(container, None)
    if ordered is not None:
        order = ordered.getObjectPosition(obj.getId())

    serializer = getMultiAdapter((obj, request), ISerializeToJson)
    old_obj_data = serializer()
    collection_uid = obj["dashboard_collection"].UID()
    log_info(logger, "{} deleted".format("/".join(obj.getPhysicalPath())))
    api.content.delete(obj)

    start_date = old_obj_data.get("start_date", None)
    if isinstance(start_date, dict):
        start_date = start_date.get("token", None)
    default_assigned_group = old_obj_data.get("default_assigned_group", None)
    if isinstance(default_assigned_group, dict):
        default_assigned_group = default_assigned_group.get("token", None)
    default_assigned_user = old_obj_data.get("default_assigned_user", None)
    if isinstance(default_assigned_user, dict):
        default_assigned_user = default_assigned_user.get("token", None)
    round_to_day = old_obj_data.get("round_to_day", None)
    if isinstance(round_to_day, dict):
        round_to_day = round_to_day.get("token", None)

    new_obj = api.content.create(
        container=container,
        type=new_type,
        id=old_obj_data["id"],
        title=old_obj_data["title"],
        start_date=start_date,
        enabled=old_obj_data.get("enabled", None),
        default_assigned_group=default_assigned_group,
        default_assigned_user=default_assigned_user,
        warning_delay=old_obj_data.get("warning_delay", None),
        additional_delay=old_obj_data.get("additional_delay", None),
        additional_delay_type=old_obj_data.get("additional_delay_type", None),
        round_to_day=round_to_day,
        activate_recurrency=old_obj_data.get("activate_recurrency", None),
    )
    log_info(logger, "{} created".format("/".join(obj.getPhysicalPath())))

    state_keys = [
        "calculation_delay",
        "marker_interfaces",
        "creation_state",
        "starting_states",
        "ending_states",
        "freeze_states",
        "thaw_states",
        "recurrence_states",
    ]

    for key in state_keys:
        if key in old_obj_data and old_obj_data[key]:
            setattr(
                new_obj,
                key,
                [item["token"] for item in old_obj_data["calculation_delay"]],
            )

    conditions = {
        "creation_conditions": MacroCreationConditionObject,
        "start_conditions": MacroStartConditionObject,
        "end_conditions": MacroEndConditionObject,
        "freeze_conditions": MacroFreezeConditionObject,
        "thaw_conditions": MacroThawConditionObject,
        "recurrence_conditions": MacroRecurrenceConditionObject,
    }

    for key, value in conditions.items():
        if key in old_obj_data and old_obj_data[key]:
            setattr(
                new_obj,
                key,
                set(
                    [
                        value(
                            condition=item.get("condition", None),
                            operator=item.get("operator", None),
                            display_status=item.get("display_status", None),
                        )
                        for item in old_obj_data[key]
                    ]
                ),
            )

    unsubscribe_task_configs_for_content_type(new_obj, None)
    unregister_task_collection_criterion(new_obj, None)

    setattr(new_obj, "_plone.uuid", old_obj_data["UID"])
    new_obj.reindexObject(idxs=["UID"])

    if ordered:
        ordered.moveObjectToPosition(new_obj.getId(), order)
        new_obj.reindexObject(idxs=["getObjPositionInParent"])

    subscribe_task_configs_for_content_type(new_obj, None)
    register_task_collection_criterion(new_obj, None)

    dashboard_collection = new_obj["dashboard_collection"]

    setattr(dashboard_collection, "_plone.uuid", collection_uid)
    dashboard_collection.reindexObject(idxs=["UID"])

    dashboard_collection.showNumberOfItems = True

    query = [
        (
            {"i": filter["i"], "o": filter["o"], "v": old_obj_data["UID"]}
            if filter["i"] == "CompoundCriterion"
            else filter
        )
        for filter in dashboard_collection.query
    ]

    dashboard_collection.setQuery(query)


def fix_config_wrong_class(context):
    """ """
    logger = logging.getLogger("migrate announcement schedule config")
    logger.info("starting upgrade steps")
    portal_urban = api.portal.get_tool("portal_urban")
    for licence_config in portal_urban.objectValues("LicenceConfig"):
        schedule_cfg = getattr(licence_config, "schedule", None)

        if schedule_cfg and hasattr(schedule_cfg, "announcement-preparation"):
            data = schedule_cfg.REQUEST.form
            data["force_dashboard_creation"] = True
            schedule_cfg.REQUEST.form = data

            unregister_schedule_collection_criterion(schedule_cfg, None)

            announcement_prep_task = getattr(schedule_cfg, "announcement-preparation")
            _replace_object(announcement_prep_task, "MacroTaskConfig", logger)

            announcement_done_task = getattr(schedule_cfg, "announcement")
            _replace_object(announcement_done_task, "MacroTaskConfig", logger)

            register_schedule_collection_criterion(schedule_cfg, None)
            data["force_dashboard_creation"] = False
            schedule_cfg.REQUEST.form = data

    logger.info("Upgrade step done!")


def add_new_voc_terms_for_form_composition(context):
    logger = logging.getLogger(
        "urban: Add new vocabularies to portal_urban/form_composition"
    )
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get()["portal_urban"]
    form_composition_folder = portal_urban.form_composition

    # Those are the new vocabulary terms that will be added
    # Refer to profiles/extra/config_default_values.py
    # for the existing vocabulary terms
    # that will be initiated in each new instance
    form_composition_new_vocabulary_terms_to_add = [
        {"id": "10", "title": "1/1 Formulaire général permis environnement et unique"},
        {"id": "11", "title": "1/2 Élevage et détention d'animaux"},
        {
            "id": "12",
            "title": "Annexe V/1 - Implantation d'un commerce",
        },
        {
            "id": "13",
            "title": "Annexe IX - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
        },
        {
            "id": "14",
            "title": "Annexe X - Demande de permis d'urbanisation ou de modification de permis d'urbanisation",
        },
        {
            "id": "15",
            "title": "Annexe XI - Demande de permis d'urbanisation ou de modification de permis d'urbanisation avec contenu simplifié",
        },
        {"id": "16", "title": "Annexe XV - Demande de certificat d'urbanisme n°2"},
    ]

    createFolderDefaultValues(
        form_composition_folder,
        form_composition_new_vocabulary_terms_to_add,
        portal_type="UrbanVocabularyTerm",
    )

    logger.info("upgrade done!")


def remove_permission_to_create_integrated_licences(context):
    logger = logging.getLogger("urban: remove permission to create integrated licences")
    logger.info("starting upgrade step")

    portal = api.portal.get()
    codt_integratedlicences_folder = getattr(portal.urban, "codt_integratedlicences")
    if not codt_integratedlicences_folder:
        logger.error("couldn't find codt_integratedlicences folder, aborting!")
        return

    for principal_id, roles in codt_integratedlicences_folder.get_local_roles():
        if "Contributor" in roles:
            remaining_roles = tuple(set(roles).difference(["Contributor"]))
            codt_integratedlicences_folder.manage_delLocalRoles([principal_id])
            if remaining_roles:
                codt_integratedlicences_folder.manage_addLocalRoles(
                    principal_id, remaining_roles
                )

    codt_integratedlicences_folder.reindexObjectSecurity()
    logger.info("upgrade step done!")


def allow_corporate_tenant_in_inspections(context):
    """ """
    logger = logging.getLogger("urban: Allow corporate tenant in inspections")
    logger.info("starting upgrade steps")

    portal_types_tool = api.portal.get_tool("portal_types")
    isp_tool = portal_types_tool.get("Inspection")
    if "CorporationTenant" not in isp_tool.allowed_content_types:
        new_allowed_types = list(isp_tool.allowed_content_types) + ["CorporationTenant"]
        isp_tool.allowed_content_types = tuple(new_allowed_types)

    logger.info("upgrade step done!")


def fix_patrimony_certificate_class(context):
    from Products.urban.content.licence.PatrimonyCertificate import PatrimonyCertificate

    logger = logging.getLogger("urban: Fix patrimony certificate class")
    logger.info("starting upgrade steps")

    # fix FTI
    portal = api.portal.get()
    fti = portal.portal_types.PatrimonyCertificate
    fti.content_meta_type = "PatrimonyCertificate"
    fti.factory = "addPatrimonyCertificate"

    # migrate content
    catalog = api.portal.get_tool("portal_catalog")
    licence_brains = catalog(portal_type="PatrimonyCertificate")

    for licence_brain in licence_brains:
        licence = licence_brain.getObject()
        if licence.__class__ == PatrimonyCertificate:
            continue
        licence.__class__ = PatrimonyCertificate
        licence.meta_type = "PatrimonyCertificate"
        licence.schema = PatrimonyCertificate.schema
        licence._p_changed = 1
        licence.reindexObject()

    logger.info("upgrade step done!")


def fix_external_decision_values(context):
    logger = logging.getLogger("urban: Fix external decision values")
    logger.info("starting upgrade steps")

    catalog = api.portal.get_tool("portal_catalog")
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)

    for licence_brain in licence_brains:
        licence = licence_brain.getObject()
        for opinion in licence.objectValues("UrbanEventOpinionRequest"):
            external_decision = opinion.getField("externalDecision").get(opinion)
            if type(external_decision) is list and len(external_decision) == 1:
                opinion.setExternalDecision(external_decision[0])

    logger.info("upgrade step done!")


def add_new_registry_profil(context):
    logger = logging.getLogger("urban: reimport registry profil")
    logger.info("starting migration steps")

    registry = getUtility(IRegistry)
    attributes = {"title": _("Planned address"), "description": _("address planned")}
    key = "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_address_to_do"
    registry_field = Dict(**attributes)
    registry_record = Record(registry_field)
    registry_record.value = None
    registry.records[key] = registry_record

    logger.info("migration done!")


def hide_patrimony_tab_in_licence_config(context):
    logger = logging.getLogger("urban: Hiding patrimony tab where newly available")
    logger.info("starting upgrade steps")

    included = [
        "preliminarynotice",
        "envclassone",
        "envclasstwo",
        "envclassthree",
        "envclassbordering",
        "miscdemand",
        "projectmeeting",
        "explosivespossession",
        "inspection",
        "ticket",
    ]
    portal_urban = getToolByName(context, "portal_urban")
    for licence_config in portal_urban.objectValues("LicenceConfig"):
        if licence_config.id in included:
            # add hidden tab config (unless there is one already)
            if not [
                tab for tab in licence_config.tabsConfig if tab["value"] == "patrimony"
            ]:
                updated_config = licence_config.tabsConfig + (
                    {"display": "", "display_name": "Patrimoine", "value": "patrimony"},
                )
                licence_config.setTabsConfig(updated_config)

    logger.info("upgrade step done!")


def hide_tab_in_licence_config(context):
    logger = logging.getLogger("urban: Hiding environment tab where newly available")
    logger.info("starting upgrade steps")

    # ignore types that already had the environment tab
    excluded = [
        "uniquelicence",
        "codt_uniquelicence",
        "codt_integratedlicence",
        "envclassthree",
        "envclassone",
        "envclasstwo",
        "envclassbordering",
        "explosivespossession",
    ]
    portal_urban = getToolByName(context, "portal_urban")
    for licence_config in portal_urban.objectValues("LicenceConfig"):
        if licence_config.id not in excluded:
            # add hidden tab config (unless there is one already)
            if not [
                tab
                for tab in licence_config.tabsConfig
                if tab["value"] == "environment"
            ]:
                updated_config = licence_config.tabsConfig + (
                    {
                        "display": "",
                        "display_name": "Analyse Environnement",
                        "value": "environment",
                    },
                )
                licence_config.setTabsConfig(updated_config)

    logger.info("upgrade step done!")


def hide_habitation_tab_in_licence_config(context):
    logger = logging.getLogger("urban: Hiding habitation tab where newly available")
    logger.info("starting upgrade steps")

    included = [
        "miscdemand",
        "preliminarynotice",
        "projectmeeting",
    ]
    portal_urban = getToolByName(context, "portal_urban")
    for licence_config in portal_urban.objectValues("LicenceConfig"):
        if licence_config.id in included:
            # add hidden tab config (unless there is one already)
            if not [
                tab for tab in licence_config.tabsConfig if tab["value"] == "habitation"
            ]:
                updated_config = licence_config.tabsConfig + (
                    {"display": "", "display_name": "Logement", "value": "habitation"},
                )
                licence_config.setTabsConfig(updated_config)

    logger.info("upgrade step done!")


def add_new_registry_for_missing_capakey(context):
    logger = logging.getLogger("urban: Add new registry for missing capakey")
    logger.info("starting migration steps")

    registry = getUtility(IRegistry)
    key = "Products.urban.interfaces.IMissingCapakey"
    registry_field = List(
        title="Missing capakey",
        description="List of missing capakey",
        value_type=TextLine(),
    )
    registry_record = Record(registry_field)
    registry_record.value = []
    registry.records[key] = registry_record

    logger.info("migration done!")


def add_additional_delay_option(context):
    logger = logging.getLogger("urban: Add complementary delay option")
    logger.info("starting upgrade steps")

    # Add new term type, workflow and index
    logger.info("Add new term type, workflow and index")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:urbantypes", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    setup_tool.runImportStepFromProfile("profile-Products.urban:urbantypes", "catalog")

    # Add vocabulary
    logger.info("Add vocabulary")
    portal_urban = api.portal.get_tool("portal_urban")
    complementary_delay_folder = createVocabularyFolder(
        container=portal_urban,
        folder_id="complementary_delay",
        site=None,
        allowedtypes="ComplementaryDelayTerm"
    )
    complementary_delay_term = [
        {
            "id": "cyberattaque_spw",
            "title": u"Cyberattaque SPW - avril 2025",
            "delay": 60
        }
    ]
    createFolderDefaultValues(
        complementary_delay_folder,
        complementary_delay_term,
        portal_type="ComplementaryDelayTerm"
    )

    # Add qery widget to 'all' folder 
    urban_folder = api.portal.get().urban
    data = {
        "_cid_": u"c97",
        "title": u"Prorogation complémentaire",
        "hidden": False,
        "index": u"getComplementary_delay",
        "vocabulary": u"urban.vocabularies.complementary_delay"
    }
    urban_folder_criterion = ICriteria(urban_folder)
    if urban_folder_criterion is not None:
        urban_folder_criterion.add(
            wid="select2",
            position="top",
            section="advanced",
            **data
        )

    # Add complementary_delay field to all default
    logger.info("Add complementary_delay field to all default")
    field = "complementary_delay"
    
    for urban_type in URBAN_TYPES:
        # Add complementary_delay field 
        licence_config = portal_urban.get(urban_type.lower(), None)
        if licence_config is None:
            continue
        if not hasattr(licence_config, "getUsedAttributes"):
            continue
        used_attributes = licence_config.getUsedAttributes()
        if field in used_attributes:
            continue
        licence_config.setUsedAttributes(used_attributes + (field, ))
        logger.info("Type {}, attribute add".format(urban_type))

        #Add query widget
        licence_folder = getattr(urban_folder, "{}s".format(urban_type.lower()), None)
        if licence_folder is None:
            continue
        criterion = ICriteria(licence_folder)
        if criterion is None:
            continue

        criterion.add(
            wid="select2",
            position="top",
            section="advanced",
            **data
        )
        logger.info("Type {}, query widget add".format(urban_type))
        

    logger.info("upgrade step done!")
