# -*- coding: utf-8 -*-

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from Products.urban.interfaces import IUrbanDoc

from plone import api

from zope.interface import alsoProvides

import logging

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban1110(context):
    """
     Launch every migration steps for the version 1.11.0
    """
    logger = logging.getLogger('urban: migrate to 1.11.0')
    logger.info("starting migration steps")
    #  migrate UrbanDoc to File type with an IUrbanDoc marker interface on it.
    migrateUrbanDocType(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


class UrbanDocTypeMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanDoc"
    src_portal_type = "UrbanDoc"
    dst_meta_type = "ATBlob"
    dst_portal_type = "File"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)

    def custom(self):
        """ set IUrbanDoc interface on migrated File"""
        alsoProvides(self.new, IUrbanDoc)


def migrateUrbanDocType(context):
    """
    UrbanDoc type is now File.
    """
    logger = logging.getLogger('urban: migrate UrbanDocs type ->')
    logger.info("starting migration step")

    migrator = UrbanDocTypeMigrator
    portal = api.portal.get()
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    folder_path = '/'.join(portal.urban.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={'path': folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")
