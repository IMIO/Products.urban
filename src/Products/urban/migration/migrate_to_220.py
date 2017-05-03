# encoding: utf-8

from plone import api
from plone.portlets.constants import CONTEXT_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor

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


def migrate_inquiry_eventtype():
    logger = logging.getLogger('urban: migrate inquiry event type')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues():
            if 'enquete-publique' in event_type.id:
                event_type.setEventPortalType('UrbanEventInquiry')
                old_fields = event_type.getActivatedFields()
                if 'investigationStart' not in old_fields:
                    new_fields = ['investigationStart', 'investigationEnd'] + list(old_fields)
                    event_type.setActivatedFields(new_fields)

    logger.info("migration step done!")


def block_urban_parent_portlets():
    logger = logging.getLogger('urban: block urban folder portlets')
    logger.info("starting migration step")
    portal = api.portal.get()
    urban_folder = portal.urban
    for manager_name, src_manager in getUtilitiesFor(IPortletManager, context=urban_folder):
        assignment_manager = getMultiAdapter(
            (urban_folder, src_manager),
            ILocalPortletAssignmentManager
        )
        assignment_manager.setBlacklistStatus(CONTEXT_CATEGORY, True)
        for category in (GROUP_CATEGORY, CONTENT_TYPE_CATEGORY):
            assignment_manager.setBlacklistStatus(
                category,
                assignment_manager.getBlacklistStatus(category)
            )
    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.1')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-imio.schedule:default')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    block_urban_parent_portlets()
    migrate_inquiry_tabs()
    migrate_inquiry_eventtype()
    logger.info("migration done!")
