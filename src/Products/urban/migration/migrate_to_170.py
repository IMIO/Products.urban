# -*- coding: utf-8 -*-

from Acquisition import aq_base

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from plone import api

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
    # update EnvClassOne events
    migrateEnvClassOneEventTypes(context)
    # migrate decisions vocabulary
    migrateDecisionsVocabulary(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


class ApplicantMetaTypeMigrator(InplaceATFolderMigrator):
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


class ProprietaryMetaTypeMigrator(InplaceATFolderMigrator):
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


def migrateEnvClassOneEventTypes(context):
    """
    Update EnvClassOne UrbanEventTypes.
    """
    logger = logging.getLogger('urban: udpate EnvClassOne UrbanEventTypes ->')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')

    globaltemplates = portal_urban.globaltemplates
    ins_id = 'statsins.odt'
    if ins_id in globaltemplates.objectIds():
        api.content.delete(getattr(globaltemplates, ins_id))

    eventtypes_folder = portal_urban.envclassone.urbaneventtypes
    for obj in eventtypes_folder.objectValues():
        api.content.delete(obj)

    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runImportStepFromProfile('profile-Products.urban:extra', 'urban-updateAllUrbanTemplates')

    logger.info("migration step done!")


def migrateDecisionsVocabulary(context):
    """
    Decision vocabulary is now local for licence config.
    """
    logger = logging.getLogger('urban: migrate decision vocabulary ->')
    logger.info("starting migration step")

    #to avoid link integrity problems, disable checks
    portal_properties = api.portal.get_tool('portal_properties')
    portal_properties.site_properties.enable_link_integrity_checks = False

    portal_urban = api.portal.get_tool('portal_urban')
    decisions_global_folder = getattr(aq_base(portal_urban), 'decisions', None)

    if not decisions_global_folder:
        logger.info("migration step done!")
        return

    for licence_config in portal_urban.objectValues('LicenceConfig'):

        # ignore envclassone as it should have different 'decisions' values
        if licence_config.id == 'envclassone':
            continue

        if hasattr(aq_base(licence_config), 'decisions'):
            api.content.delete(obj=licence_config.decisions)
        api.content.copy(source=decisions_global_folder, target=licence_config)

    api.content.delete(obj=decisions_global_folder)

    #enable linkintegrity checks
    portal_properties.site_properties.enable_link_integrity_checks = True
    # this step will fill decisions values for envclassone config
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')

    logger.info("migration step done!")
