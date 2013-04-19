# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import logging

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban118(context):
    """
     Launch every migration steps for the version 1.1.8
    """
    logger = logging.getLogger('urban: migrate to 1.1.8')
    logger.info("starting migration steps")
    # geometricians are now a portal_type of class Contact
    migrateGeometriciansMetaType(context)

    # finish with reinstalling urban and adding the templates
    logger.info("starting to reinstall urban...")
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


class GeometricianMetaTypeMigrator(object, InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "Geometrician"
    src_portal_type = "Geometrician"
    dst_meta_type = "Contact"
    dst_portal_type = "Geometrician"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrateGeometriciansMetaType(context):
    """
     The voc used for the specific features has now its own type : SpecificFeatureTerm
     We have to migrate the UrbanVocabularyTerm used for the specific features to this new Type
    """
    logger = logging.getLogger('urban: migrate Geometricians meta_type ->')
    logger.info("starting migration step")

    migrator = GeometricianMetaTypeMigrator
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    geometricians_folder = portal.urban.geometricians
    folder_path = '/'.join(geometricians_folder.getPhysicalPath())
    walker = migrator.walker(portal, migrator, query={'path': folder_path}, callBefore=contentmigrationLogger, logger=logger, purl=portal.portal_url)
    walker.go()

    # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")
