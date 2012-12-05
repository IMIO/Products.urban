# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')

def migrateToUrban116(context):
    """
     Launch every migration steps for the version 1.1.6
    """
    # the environment declaration config has changed
    # the portal_type used has changed as well
    migrateEnvironmentDeclaration(context)

    # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:tests', 'urban-addTestObjects')

def migrateEnvironmentDeclaration(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')

    # rename the licence folder and config 'environmentaldeclaration' into 'envclassthree'
    site.urban.manage_delObjects('environmentaldeclarations')
    urban_tool.manage_renameObject(id='environmentaldeclaration',  new_id='envclassthree')
