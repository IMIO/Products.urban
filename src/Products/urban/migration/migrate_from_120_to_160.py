# -*- coding: utf-8 -*-

import logging

from Products.urban.migration.migrate_to_130 import migrateToUrban130
from Products.urban.migration.migrate_to_160 import migrateToUrban160

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrate(context):
    """
     Launch every migration steps for the version 1.6.0 from 1.2.0
    """
    logger = logging.getLogger('urban: migrate to 1.6.0')
    logger.info("starting global migration steps")
    migrateToUrban130(context)
    migrateToUrban160(context)
    logger.info("global migration done!")
