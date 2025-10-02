from eea.facetednavigation.interfaces import ICriteria
from imio.helpers.catalog import reindexIndexes
from plone import api
from Products.urban.config import URBAN_TYPES

import logging


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


def _update_collection_assigned_user(context, logger):
    dashboard_collection = getattr(context, "dashboard_collection", None)
    if "assigned_user_column" in dashboard_collection.customViewFields:
        customViewFields = list(dashboard_collection.customViewFields)
        customViewFields = [
            "assigned_user" if field == "assigned_user_column" else field
            for field in customViewFields
        ]
        dashboard_collection.customViewFields = tuple(customViewFields)
        logger.info("{0} updated".format(dashboard_collection.absolute_url()))


def _update_tasks_collection_assigned_user(context, logger):
    _update_collection_assigned_user(context, logger)
    for task_id in context.keys():
        if task_id == "dashboard_collection":
            continue
        task_context = getattr(context, task_id)
        _update_tasks_collection_assigned_user(task_context, logger)


def fix_opinion_schedule_column(context):
    logger = logging.getLogger("urban: Update Opinion Schedule Collection Column")
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get_tool("portal_urban")
    if "opinions_schedule" in portal_urban:
        schedule = getattr(portal_urban, "opinions_schedule")
        _update_tasks_collection_assigned_user(schedule, logger)

    logger.info("upgrade step done!")


def update_collection_column(context):
    logger = logging.getLogger("urban: Update Collection Column")
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get_tool("portal_urban")
    for urban_type in URBAN_TYPES:
        config_folder = getattr(portal_urban, urban_type.lower())
        schedule_config = getattr(config_folder, "schedule")
        _update_tasks_collection_assigned_user(schedule_config, logger)

    logger.info("upgrade step done!")


def add_additional_reference_index(context):
    logger = logging.getLogger("urban: Add additionnal reference index")
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "catalog"
    )
    catalog = api.portal.get_tool("portal_catalog")
    reindexIndexes(None, ["getAdditionalReference"])
    logger.info("upgrade step done!")


def update_faceted_dashboard(context):
    """ """
    from Products.urban.dashboard.utils import switch_config_folder
    logger = logging.getLogger(
        "urban: update faceted dashboard"
    )
    logger.info("starting upgrade steps")
    site = api.portal.getSite()
    urban_folder = getattr(site, "urban")
    for urban_type in URBAN_TYPES:
        config_path = switch_config_folder("{0}s.xml".format(urban_type.lower()))
        folder = getattr(urban_folder, urban_type.lower() + "s", None)
        if not folder:
            continue
        folder.unrestrictedTraverse("@@faceted_exportimport").import_xml(
            import_file=open(config_path)
        )
    logger.info("upgrade step done!")