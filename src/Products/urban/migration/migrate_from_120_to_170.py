# -*- coding: utf-8 -*-

import logging

from plone import api

from Products.urban.migration import migrate_to_1110
from Products.urban.migration.migrate_to_130 import migrateToUrban130
from Products.urban.migration.migrate_to_160 import migrateToUrban160
from Products.urban.migration.migrate_to_170 import migrateToUrban170

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrate(context):
    """
     Launch every migration steps for the version 1.11.0 from 1.2.0
    """
    logger = logging.getLogger('urban: migrate to 1.6.0')
    logger.info("starting global migration steps")
    migrateToUrban130(context)
    migrateToUrban160(context)
    migrateToUrban170(context)  # 1h
    # migrate_to_1110.migrate(context)  # 1h 50m
    catalog = api.portal.get_tool('portal_catalog')
    catalog.refreshCatalog(clear=True)  # 20m
    logger.info("global migration done!")
