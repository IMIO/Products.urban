# encoding: utf-8

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate(context):
    logger = logging.getLogger('urban: update to 2.2')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-collective.faceted.task:default', 'componentregistry')
    setup_tool.runAllImportStepsFromProfile('profile-collective.faceted.task:default')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')
    setup_tool.runAllImportStepsFromProfile('profile-imio.schedule:default')
    logger.info("migration done!")
