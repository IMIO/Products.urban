# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')

def migrateToUrban116(context):
    """
     Launch every migration steps for the version 1.1.5
    """
    # the environment declaration config has changed
    # the portal_type used has changed as well
    migrateEnvironmentDeclaration(context)

def migrateEnvironmentConfig(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')
