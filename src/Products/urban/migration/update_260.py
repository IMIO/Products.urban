from Products.urban.setuphandlers import configureCKEditor
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


def configure_ckeditor(context):
    logger = logging.getLogger("urban: configure ckeditor")
    logger.info("starting upgrade steps")
    configureCKEditor(context)
    logger.info("upgrade step done!")


def create_plone_custom_css(context):
    logger = logging.getLogger("urban: create plone custom css")
    logger.info("starting upgrade steps")
    portal = context.portal_url.getPortalObject()
    if "custom" not in portal.portal_skins.objectIds():
        portal.portal_skins.manage_addProduct["OFSP"].manage_addFolder(
            "custom", "Custom Skins"
        )
    custom_folder = portal.portal_skins.custom
    css_content = """
    /*
     *  This is the file where you put your CSS changes.
     *  You should preferrably use this and override the
     *  relevant properties you want to change here instead
     *  of customizing plone.css to survive upgrades. Writing
     *  your own plone.css only makes sense for very heavy
     *  customizations. Useful variables from Plone are
     *  documented at the bottom of this file.
     */

    /* <dtml-with imioapps_properties> (do not remove this :) */
    /* <dtml-call "REQUEST.set('portal_url', portal_url())"> (not this either :) */

    /* ADD YOUR CUSTOMIZATIONS HERE, IT USE imioapps_properties */
    /* CKeditor styles */
    .red-text {color: red;}
    .blue-text {color: blue;}
    .green-text {color: green;}
    .highlight-rouge {background-color: #FF7F7F;}
    .highlight-vert-claire {background-color: #83f28f;}
    .highlight-orange {background-color:orange;}
    .highlight-bleu {background-color:#34CCFF;}


    /* </dtml-with> */
    """
    if "ploneCustom.css" not in custom_folder.objectIds():
        custom_folder.manage_addProduct["OFSP"].manage_addDTMLMethod(
            "ploneCustom.css", "", css_content
        )
    logger.info("upgrade step done!")
