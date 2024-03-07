# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger("urban: migrations")


def contentmigrationLogger(oldObject, **kwargs):
    """Generic logger method to be used with CustomQueryWalker"""
    kwargs["logger"].info("/".join(kwargs["purl"].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban120(context):
    """
    Launch every migration steps for the version 1.2.0
    """
    logger = logging.getLogger("urban: migrate to 1.2.0")
    logger.info("starting migration steps")
    # delete rubrics and conditions folders with test values so they can be
    # reinstalled without any "id already in use" conflict
    deleteRubricsAndConditionsTestFolder(context)

    logger.info(
        "starting to reinstall urban..."
    )  # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile("profile-Products.urban:default")
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


def deleteRubricsAndConditionsTestFolder(context):
    """ """
    logger = logging.getLogger(
        "urban: delete rurbrics and conditions folders from the config->"
    )
    logger.info("starting migration step")

    portal_urban = getToolByName(context, "portal_urban")

    conditionfolder = getattr(portal_urban, "exploitationconditions", None)
    if conditionfolder and len(conditionfolder.objectValues()) == 3:

        portal_urban.manage_delObjects(["exploitationconditions"])
        logger.info("Deleted 'exloitation conditions' folder")

    rubricsfolder = getattr(portal_urban.envclassthree, "rubrics", None)
    if rubricsfolder and len(rubricsfolder.objectValues()) == 10:
        portal_urban.envclassthree.manage_delObjects(["rubrics"])
        logger.info("Deleted 'rubrics' folder")

    logger.info("migration step done!")
