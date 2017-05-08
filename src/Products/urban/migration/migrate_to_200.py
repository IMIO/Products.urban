# -*- coding: utf-8 -*-
from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate(context):
    """
     Launch every migration steps for the version 2.0
    """
    logger = logging.getLogger('urban: migrate to 2.0')
    logger.info("starting migration steps")
    migrate_eventtype_mapping(context)
    migrate_deleted_permissions_workflow(context)
    logger.info("migration done!")


def migrate_deleted_permissions_workflow(context):
    """
    """
    logger = logging.getLogger('urban: set acquisition back on permissions deleted from urban_licence workflow')
    catalog = api.portal.get_tool('portal_catalog')
    wf_tool = api.portal.get_tool('portal_workflow')
    licence_types = []
    for portal_type, workflows in wf_tool._chains_by_type.iteritems():
        if 'urban_licence_workflow' in workflows:
            licence_types.append(portal_type)

    licence_brains = catalog(portal_type=licence_types)
    for brain in licence_brains:
        licence = brain.getObject()
        licence.manage_permission('urban: Add Contact', roles=[], acquire=1)
        licence.manage_permission('urban: Add PortionOut', roles=[], acquire=1)
        licence.manage_permission('urban: Add UrbanEvent', roles=[], acquire=1)
        licence.manage_permission('urban: Add Layer', roles=[], acquire=1)
        licence.manage_permission('urban: Add Inquiry', roles=[], acquire=1)
        logger.info("restored licence : %s" % licence.Title())
    logger.info("migration step done!")


def migrate_eventtype_mapping(context):
    """
    EventTypeType mapping to urban event portal_type is now
    on a persistent mapping on UrbanTool
    """
    logger = logging.getLogger('urban: migrate eventtype mapping')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    portal_urban.__init__()

    logger.info("migration step done!")
