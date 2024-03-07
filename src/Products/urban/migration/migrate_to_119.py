# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import logging

from zope import interface

from Products.urban.interfaces import IContactFolder

logger = logging.getLogger("urban: migrations")


def contentmigrationLogger(oldObject, **kwargs):
    """Generic logger method to be used with CustomQueryWalker"""
    kwargs["logger"].info("/".join(kwargs["purl"].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban119(context):
    """
    Launch every migration steps for the version 1.1.9
    """
    logger = logging.getLogger("urban: migrate to 1.1.9")
    logger.info("starting migration steps")
    # add a marker interface on urban contact folder (notaries, architects,
    # geometricians) to allow some view methods
    migrateContactFolders(context)

    logger.info(
        "starting to reinstall urban..."
    )  # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile("profile-Products.urban:default")
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


def migrateContactFolders(context):
    """ """
    logger = logging.getLogger(
        "urban: migrate organisationTerm into OpinionRequestEventType ->"
    )
    logger.info("starting migration step")

    portal_url = getToolByName(context, "portal_url")
    portal = portal_url.getPortalObject()
    urban_folder = portal.urban

    for foldername in ["architects", "geometricians", "notaries"]:
        contactfolder = getattr(urban_folder, foldername)
        interface.directlyProvides(contactfolder, IContactFolder)

    logger.info("migration step done!")
