# encoding: utf-8

from plone import api

from Products.urban.profiles.extra.schedule_config import schedule_config

import logging

logger = logging.getLogger("urban: migrations")


def migrate(context):
    logger = logging.getLogger("urban: update to 2.2")
    logger.info("starting migration steps")

    portal_urban = api.portal.get_tool("portal_urban")
    for config_id in schedule_config.keys():
        schedule = getattr(portal_urban, config_id).schedule
        schedule.manage_delObjects(ids=schedule.objectIds())

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:extra", "urban-extra")
    catalog = api.portal.get_tool("portal_catalog")
    catalog.refreshCatalog(clear=True)
    logger.info("migration done!")
