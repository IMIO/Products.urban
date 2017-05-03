# encoding: utf-8

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate_inquiry_tabs():
    logger = logging.getLogger('urban: disable old investigation_and_advices tab from licence configs')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        old_tabs = licence_config.getTabsConfig()
        tab_ids = [t['value'] for t in old_tabs]
        if 'investigation_and_advices' in tab_ids:
            new_tabs = tuple([t for t in old_tabs if t['value'] != 'investigation_and_advices'])
            licence_config.setTabsConfig(new_tabs)

    logger.info("migration step done!")


def migrate_inquiry_eventtype_eventportaltype():
    logger = logging.getLogger('urban: set default eventPortalType of inquiries to UrbanEventInquiry')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues():
            if 'enquete-publique' in event_type.id:
                event_type.setEventPortalType('UrbanEventInquiry')

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.1')
    logger.info("starting migration steps")
    migrate_inquiry_tabs()
    migrate_inquiry_eventtype_eventportaltype()
    logger.info("migration done!")
