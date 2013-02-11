# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
import re

logger = logging.getLogger('urban: migrations')

def migrateToUrban117(context):
    """
     Launch every migration steps for the version 1.1.7
    """
    logger = logging.getLogger('urban: migrate to 1.1.7')
    logger.info("starting migration steps")
    #the method getCurrentFolderManager has changed
    # we have to migrate the tal expressions used for numerotation
    migrateNumerotationExpressions(context)

    # finish with reinstalling urban and adding the templates
    logger.info("starting to reinstall urban...")
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:tests', 'urban-addTestObjects')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")

def migrateNumerotationExpressions(context):
    """
     adapt the way to call getCurrentFolderManager method in numerotation expressions
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(context, 'portal_urban')
    logger = logging.getLogger('urban: migrate to environmental declarations ->')
    logger.info("starting migration step")

    configs = urban_tool.objectValues('LicenceConfig')
    regex = 'getCurrentFolderManager\\(.*?(obj\s*,?\s*).*?\\)'
    def adaptCall(matchobj):
        return matchobj.group(0).replace(matchobj.group(1), '')

    for config in configs:
        numerotation_expression = config.getReferenceTALExpression()
        new_expression = re.sub(regex, adaptCall, numerotation_expression)
        if new_expression != numerotation_expression:
            logger.info("Migrated tal expression of '%s' " % config.Title())
            config.setReferenceTALExpression(new_expression)

    logger.info("migration step done!")
