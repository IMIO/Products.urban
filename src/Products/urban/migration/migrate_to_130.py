# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone import api

import logging

logger = logging.getLogger("urban: migrations")


def contentmigrationLogger(oldObject, **kwargs):
    """Generic logger method to be used with CustomQueryWalker"""
    kwargs["logger"].info("/".join(kwargs["purl"].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban130(context):
    """
    Launch every migration steps for the version 1.2.0
    """
    logger = logging.getLogger("urban: migrate to 1.2.0")
    logger.info("starting migration steps")
    # migrate default view of urban root folder
    migrateUrbanRootView(context)

    logger.info(
        "starting to reinstall urban..."
    )  # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile("profile-Products.urban:default")
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


def migrateUrbanRootView(context):
    """ """
    logger = logging.getLogger(
        "urban: delete rurbrics and conditions folders from the config->"
    )
    logger.info("starting migration step")

    portal = api.portal.getSite()

    portal.setLayout("redirectto_urban_root_view")

    urban_root = portal.urban
    urban_root.setLayout("urban_root_view")
