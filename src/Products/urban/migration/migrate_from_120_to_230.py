# -*- coding: utf-8 -*-

import logging

from plone import api

from Products.urban.migration import migrate_to_1110, migrate_to_1111, migrate_to_200, migrate_to_210, migrate_to_220, \
    migrate_to_230
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
     Launch every migration steps for the version 2.3 from 1.2.0
    """
    logger = logging.getLogger('urban: migrate to 2.3.0')
    logger.info("starting global migration steps")
    catalog = api.portal.get_tool('portal_catalog')
    migrateToUrban130(context) # 18m 130+160
    migrateToUrban160(context)
    migrateToUrban170(context)  # 1h
    catalog.refreshCatalog(clear=True)  # 20m
    migrate_to_1110.migrate(context)  # 1h 50m
    catalog.refreshCatalog(clear=True)  # 20m
    migrate_to_1111.migrate(context)  # 1m
    migrate_to_200.migrate(context)  # 1m
    migrate_to_210.migrate(context)  # 5m
    migrate_to_220.migrate(context)  # 5m
    migrate_to_230.migrate(context)  # 5m
    catalog.refreshCatalog(clear=True)  # 20m

    logger.info("global migration done!")
