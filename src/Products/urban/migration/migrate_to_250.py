# -*- coding: utf-8 -*-

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from Products.urban.config import URBAN_TYPES
from Products.urban.migration.to_DX.migration_utils import (
    clean_obsolete_portal_type,
    delete_plone_objects,
)
from Products.urban.utils import getLicenceFolderId

from plone import api

import logging

logger = logging.getLogger("urban: migrations")


def migrate_codt_buildlicences_schedule(context):
    """
    Disbale recurrency for task 'deposit'
    """
    logger = logging.getLogger("urban: migrate codt buildlicences schedule")
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool("portal_urban")
    schedule = portal_urban.codt_buildlicence.schedule
    schedule.reception.deposit.ending_states = ()
    schedule.incomplet2.notify_refused.ending_states = ()
    schedule.reception.deposit.recurrence_states = ()
    schedule.reception.deposit.activate_recurrency = False
    if "deposit" not in (schedule.incomplet.attente_complements.ending_states or ()):
        old_states = schedule.incomplet.attente_complements.ending_states or ()
        new_states = tuple(old_states) + ("deposit",)
        schedule.incomplet.attente_complements.ending_states = new_states
    if "complete" not in (schedule.reception.ending_states or ()):
        old_states = schedule.reception.ending_states or ()
        new_states = tuple(old_states) + ("deposit",)
        schedule.reception.ending_states = new_states
    if "incomplete" not in (schedule.reception.ending_states or ()):
        old_states = schedule.reception.ending_states or ()
        new_states = tuple(old_states) + ("incomplete",)
        schedule.reception.ending_states = new_states

    logger.info("migration step done!")


def contentmigrationLogger(oldObject, **kwargs):
    """Generic logger method to be used with CustomQueryWalker"""
    kwargs["logger"].info("/".join(kwargs["purl"].getRelativeContentPath(oldObject)))
    return True


class CODT_NotaryLetterMigrator(InplaceATFolderMigrator):
    """ """

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
    logger = logging.getLogger(
        "urban: migrate CODT_NotaryLetter meta type to CODT_UrbanCertificateBase ->"
    )
    logger.info("starting migration step")

    migrator = CODT_NotaryLetterMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    # Run the migrations
    folder_path = "/".join(portal.urban.codt_notaryletters.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={"path": folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url,
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


class CODT_UrbanCertificateOneMigrator(InplaceATFolderMigrator):
    """ """

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
    logger = logging.getLogger(
        "urban: migrate CODT_UrbanCertificateOne meta type to CODT_UrbanCertificateBase ->"
    )
    logger.info("starting migration step")

    migrator = CODT_UrbanCertificateOneMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    # Run the migrations
    folder_path = "/".join(portal.urban.codt_urbancertificateones.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={"path": folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url,
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


def migrate_CODT_UrbanCertificateBase_add_permissions(context):
    """ """
    logger = logging.getLogger(
        "urban: migrate CODT_UrbanCertificateBase add permission"
    )
    logger.info("starting migration step")

    portal = api.portal.get()
    for urban_type in URBAN_TYPES:
        licence_folder_id = getLicenceFolderId(urban_type)
        licence_folder = getattr(portal.urban, licence_folder_id)
        if urban_type in [
            "CODT_UrbanCertificateOne",
            "CODT_NotaryLetter",
        ]:
            licence_folder.manage_permission(
                "urban: Add CODT_UrbanCertificateBase",
                [
                    "Manager",
                    "Contributor",
                ],
                acquire=0,
            )

    logger.info("migration step done!")


def migrate_opinion_request_TAL_expression(context):
    """ """
    logger = logging.getLogger("urban: migrate opinion request TAL expression")
    logger.info("starting migration step")

    catalog = api.portal.get_tool("portal_catalog")
    opinion_request_eventtypes = [
        b.getObject() for b in catalog(portal_type="OpinionRequestEventType")
    ]
    for opinion_request_eventtype in opinion_request_eventtypes:
        if opinion_request_eventtype.getTALCondition().strip():
            opinion_request_eventtype.setTALCondition(
                "python: event.mayAddOpinionRequestEvent(here)"
            )
            logger.info(
                "migrated TAL condition of {}".format(opinion_request_eventtype)
            )

    logger.info("migration step done!")


def migrate_report_and_remove_urbandelay_portal_type(context):
    """ """
    logger = logging.getLogger("urban: report_and_remove_urbandelay_portal_type")
    logger.info("starting migration step")
    clean_obsolete_portal_type(portal_type_to_remove="UrbanDelay")
    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger("urban: migrate to 2.5")
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    # setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-update-rubrics')
    migrate_codt_buildlicences_schedule(context)
    migrate_CODT_NotaryLetter_to_CODT_UrbanCertificateBase(context)
    migrate_CODT_UrbanCertificateOne_to_CODT_UrbanCertificateBase(context)
    migrate_CODT_UrbanCertificateBase_add_permissions(context)
    migrate_opinion_request_TAL_expression(context)
    migrate_report_and_remove_urbandelay_portal_type(context)
    catalog = api.portal.get_tool("portal_catalog")
    catalog.clearFindAndRebuild()
    logger.info("migration done!")
