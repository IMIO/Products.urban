# encoding: utf-8

from Products.urban.migration.utils import refresh_workflow_permissions
from plone import api
import logging


def rename_patrimony_certificate(context):
    """ """
    logger = logging.getLogger("urban: rename Patrimony certificate")
    logger.info("starting upgrade steps")
    portal = api.portal.get()

    patrimony_folder = portal.urban.patrimonycertificates
    patrimony_folder.setTitle(u"Patrimoines")
    patrimony_folder.reindexObject(["Title"])

    patrimony_collection = portal.urban.patrimonycertificates.collection_patrimonycertificate
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
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "contentrules")

    logger.info("upgrade step done!")


def fix_supended_state_licence(context):
    logger = logging.getLogger("urban: Fix supended state licence")
    logger.info("starting upgrade steps")
    portal = api.portal.get()
    urban_path = "/".join(portal["urban"].getPhysicalPath())
    refresh_workflow_permissions(
        "codt_buildlicence_workflow",
        folder_path=urban_path,
        for_states=["suspension", "frozen_suspension"]
    )
    logger.info("upgrade done!")
