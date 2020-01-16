# -*- coding: utf-8 -*-

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


class CODT_NotaryLetterMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanCertificateBase"
    src_portal_type = "CODT_NotaryLetter"
    dst_meta_type = "CODT_UrbanCertificateBase"
    dst_portal_type = "CODT_NotaryLetter"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrate_CODT_NotaryLetter_to_CODT_UrbanCertificateBase(context):
    """
    Base class of CODT_NotaryLetter is now CODT_UrbanCertificateBase
    """
    logger = logging.getLogger('urban: migrate CODT_NotaryLetter meta type to CODT_UrbanCertificateBase ->')
    logger.info("starting migration step")

    migrator = CODT_NotaryLetterMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    # Run the migrations
    folder_path = '/'.join(portal.urban.codt_notaryletters.getPhysicalPath())
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
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


class CODT_UrbanCertificateOneMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanCertificateBase"
    src_portal_type = "CODT_UrbanCertificateOne"
    dst_meta_type = "CODT_UrbanCertificateBase"
    dst_portal_type = "CODT_UrbanCertificateOne"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrate_CODT_UrbanCertificateOne_to_CODT_UrbanCertificateBase(context):
    """
    Base class of CODT_NotaryLetter is now CODT_UrbanCertificateBase
    """
    logger = logging.getLogger('urban: migrate CODT_UrbanCertificateOne meta type to CODT_UrbanCertificateBase ->')
    logger.info("starting migration step")

    migrator = CODT_UrbanCertificateOneMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    # Run the migrations
    folder_path = '/'.join(portal.urban.codt_urbancertificateones.getPhysicalPath())
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
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.5')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-update-rubrics')
    migrate_CODT_NotaryLetter_to_CODT_UrbanCertificateBase(context)
    migrate_CODT_UrbanCertificateOne_to_CODT_UrbanCertificateBase(context)
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    logger.info("migration done!")
