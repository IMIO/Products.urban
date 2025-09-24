# encoding: utf-8

from eea.facetednavigation.interfaces import ICriteria
from Products.urban.config import URBAN_TYPES
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues
from plone import api
from plone.registry import Record
from plone.registry.field import List
from plone.registry.field import TextLine
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from Products.urban.profiles.extra.schedule_config import (
    schedule_config as schedule_config_dict,
)

import logging


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
        licence.reindexObject()

    logger.info("upgrade step done!")


def add_new_registry_for_missing_capakey(context):
    logger = logging.getLogger("urban: Add new registry for missing capakey")
    logger.info("starting migration steps")

    registry = getUtility(IRegistry)
    key = "Products.urban.interfaces.IMissingCapakey"
    registry_field = List(
        title=u"Missing capakey",
        description=u"List of missing capakey",
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
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-liege.urban:default", "workflow")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "catalog")

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


def _update_collection(context):
    dashboard_collection = getattr(context, "dashboard_collection", None)
    if "assigned_user_column" in dashboard_collection.customViewFields:
        customViewFields = list(dashboard_collection.customViewFields)
        customViewFields = [
            "assigned_user" if field == "assigned_user_column" else field
            for field in customViewFields
        ]
        dashboard_collection.customViewFields = tuple(customViewFields)


def update_collection_column(context):
    logger = logging.getLogger("urban: Update Collection Column")
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get_tool("portal_urban")
    for urban_type in URBAN_TYPES:
        config_folder = getattr(portal_urban, urban_type.lower())
        schedule_config = getattr(config_folder, "schedule")
        _update_collection(schedule_config)

        for task in schedule_config_dict.get(urban_type.lower(), []):
            task_collection = getattr(schedule_config, task["id"])
            _update_collection(task_collection)

            for subtask in task.get("subtasks", []):
                subtask_collection = getattr(task_collection, subtask["id"])
                _update_collection(subtask_collection)

    logger.info("upgrade step done!")


def update_faceted_collection_widget(context):
    from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
    from eea.facetednavigation.interfaces import ICriteria

    logger = logging.getLogger("Urban: Update collection widget")
    logger.info("starting upgrade steps")

    brains = api.content.find(object_provides=IFacetedNavigable.__identifier__)
    for brain in brains:
        faceted = brain.getObject()
        criterion = ICriteria(faceted)
        for criteria in criterion.values():
            if criteria.widget == "collection-link":
                setattr(criteria, "hide_category", True)
                setattr(criteria, "hidealloption", True)
                criteria._p_changed = 1
                criterion.criteria._p_changed = 1

    logger.info("migration step done!")


def _update_collection_assigned_user(context):
    dashboard_collection = getattr(context, "dashboard_collection", None)
    if "assigned_user_column" in dashboard_collection.customViewFields:
        customViewFields = list(dashboard_collection.customViewFields)
        customViewFields = [
            "assigned_user" if field == "assigned_user_column" else field
            for field in customViewFields
        ]
        dashboard_collection.customViewFields = tuple(customViewFields)


def fix_opinion_schedule_column(context):
    logger = logging.getLogger("urban: Update Opinion Schedule Collection Column")
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get_tool("portal_urban")
    if "opinions_schedule" in portal_urban:
        schedule = getattr(portal_urban, "opinions_schedule")
        _update_collection_assigned_user(schedule)

        for task_id in schedule.keys():
            if task_id == "dashboard_collection":
                continue
            task = getattr(schedule, task_id)
            _update_collection_assigned_user(task)

            for subtask_id in task.keys():
                if subtask_id == "dashboard_collection":
                    continue
                subtask = getattr(schedule, subtask_id)
                _update_collection_assigned_user(subtask)

    logger.info("upgrade step done!")


def update_faceted_dashboard(context):
    """ """
    logger = logging.getLogger("urban: update faceted dashboard")
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "catalog"
    )
    catalog = api.portal.get_tool("portal_catalog")
    reindexIndexes(None, ["getAdditionalReference"])
    site = api.portal.getSite()
    urban_folder = getattr(site, "urban")
    for urban_type in URBAN_TYPES:
        folder = getattr(urban_folder, urban_type.lower() + "s")
        path = (
            os.path.dirname(__file__)[: -len("migration")]
            + "dashboard/config/%ss.xml" % urban_type.lower()
        )
        folder.unrestrictedTraverse("@@faceted_exportimport").import_xml(
            import_file=open(path)
        )
    logger.info("upgrade step done!")
