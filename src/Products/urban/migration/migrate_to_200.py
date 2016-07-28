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
    logger.info("migration done!")


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
