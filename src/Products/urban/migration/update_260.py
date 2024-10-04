import os

from Products.urban import URBAN_TYPES
from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import (
    createVocabularyFolder,
    createFolderDefaultValues,
)
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from imio.helpers.catalog import reindexIndexes

from plone import api
import logging


def add_couple_to_preliminary_notice(context):
    """ """
    logger = logging.getLogger("urban: add Couple to Preliminary Notice")
    logger = logging.getLogger("urban: add Couple to Project Meeting")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    logger.info("upgrade step done!")


def remove_generation_link_viewlet(context):
    logger = logging.getLogger("urban: Remove generation-link viewlet")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "viewlets")
    logger.info("upgrade step done!")


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


def fix_opinion_workflow(context):
    logger = logging.getLogger("urban: update opinion workflow")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    logger.info("upgrade step done!")


def add_streetcode_to_catalog(context):
    logger = logging.getLogger("urban: add getStreetCode index")
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "catalog"
    )
    for brain in api.content.find(portal_type="Street"):
        street = brain.getObject()
        street.reindexObject(idxs=["getStreetCode"])
    logger.info("upgrade step done!")


def reindex_uid_catalog(context):
    logger = logging.getLogger("urban: reindex uid cataglog")
    logger.info("starting upgrade steps")
    uid_catalog = api.portal.get_tool("uid_catalog")
    reindexIndexes(None, idxs=uid_catalog.indexes(), catalog_id="uid_catalog")
    logger.info("upgrade step done!")


def update_delais_vocabularies_and_activate_prorogation_field(context):
    """ """
    logger = logging.getLogger(
        "urban: update delais vocabularies and activate prorogation field"
    )
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-update-vocabularies"
    )
    portal_urban = api.portal.get_tool("portal_urban")
    for config in portal_urban.objectValues("LicenceConfig"):
        if (
            "prorogation" in config.listUsedAttributes()
            and "prorogation" not in config.getUsedAttributes()
        ):
            to_set = ("prorogation",)
            config.setUsedAttributes(config.getUsedAttributes() + to_set)
    logger.info("upgrade step done!")


def add_new_vocabulary_for_investigation_radius_field(context):
    """ """
    logger = logging.getLogger(
        "urban: Add new vocabulary for investigation_radius field"
    )
    logger.info("starting upgrade steps")

    container = api.portal.get_tool("portal_urban")
    vocabulary_name = "investigations_radius"
    investigations_radius_vocabularies_config = default_values["global"][
        vocabulary_name
    ]
    allowedtypes = investigations_radius_vocabularies_config[0]
    investigations_radius_folder_config = createVocabularyFolder(
        container, vocabulary_name, context, allowedtypes
    )
    createFolderDefaultValues(
        investigations_radius_folder_config,
        default_values["global"][vocabulary_name][1:],
        default_values["global"][vocabulary_name][0],
    )

    logger.info("migration step done!")


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
