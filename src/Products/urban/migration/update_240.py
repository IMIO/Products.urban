# encoding: utf-8

from imio.dashboard.utils import _updateDefaultCollectionFor
from plone import api
from Products.urban.config import URBAN_TYPES
import logging

logger = logging.getLogger('urban: migrations')


def fix_licences_breadcrumb(context):
    logger = logging.getLogger('urban: fix licence breadcrumb')
    logger.info("starting upgrade steps")

    portal = api.portal.get()
    urban_folder = portal.urban
    for urban_type in URBAN_TYPES:
        folder = getattr(urban_folder, urban_type.lower() + 's')
        collection_id = 'collection_%s' % urban_type.lower()
        collection = getattr(folder, collection_id)
        _updateDefaultCollectionFor(folder, collection.UID())
    logger.info("upgrade done!")
