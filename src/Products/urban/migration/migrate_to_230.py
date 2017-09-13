# encoding: utf-8

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate_eventtypes_values():
    logger = logging.getLogger('urban: migrate urbaneventtype event type')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues():
            old_event_type = event_type.eventTypeType
            if type(old_event_type) == str or type(old_event_type) == unicode:
                event_type.setEventTypeType([event_type.eventTypeType])

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.3')
    logger.info("starting migration steps")
    migrate_eventtypes_values()
    logger.info("migration done!")
