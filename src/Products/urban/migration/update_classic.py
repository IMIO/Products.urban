from eea.facetednavigation.interfaces import ICriteria
from imio.helpers.catalog import reindexIndexes
from plone import api
from Products.urban.config import URBAN_TYPES
from Products.urban.profiles.extra.schedule_config import (
    schedule_config as schedule_config_dict,
)

import logging
import os


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