# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

import logging

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban170(context):
    """
     Launch every migration steps for the version 1.7.0
    """
    logger = logging.getLogger('urban: migrate to 1.7.0')
    logger.info("starting migration steps")
    # migrate Applicant type has now Applicant meta type
    migrateApplicantMetaType(context)
    # migrate Proprietary type has now Applicant meta type
    migrateProprietaryMetaType(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


class ApplicantMetaTypeMigrator(object, InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "Contact"
    src_portal_type = "Applicant"
    dst_meta_type = "Applicant"
    dst_portal_type = "Applicant"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrateApplicantMetaType(context):
    """
    Applicant meta_type is now Applicant (instead of Contact).
    """
    logger = logging.getLogger('urban: migrate Applicants meta_type ->')
    logger.info("starting migration step")

    migrator = ApplicantMetaTypeMigrator
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
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


class ProprietaryMetaTypeMigrator(object, InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "Contact"
    src_portal_type = "Proprietary"
    dst_meta_type = "Applicant"
    dst_portal_type = "Proprietary"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrateProprietaryMetaType(context):
    """
    Proprietary meta_type is now Applicant (instead of Contact).
    """
    logger = logging.getLogger('urban: migrate Proprietarys meta_type ->')
    logger.info("starting migration step")

    migrator = ProprietaryMetaTypeMigrator
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
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
