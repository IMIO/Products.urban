# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger('urban: migrations')

def migrateToUrban117(context):
    """
     Launch every migration steps for the version 1.1.7
    """
    logger = logging.getLogger('urban: migrate to 1.1.7')
    logger.info("starting migration steps")

    # finish with reinstalling urban and adding the templates
    logger.info("starting to reinstall urban...")
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:tests', 'urban-addTestObjects')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


