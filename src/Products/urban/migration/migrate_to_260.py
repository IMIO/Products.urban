# -*- coding: utf-8 -*-


from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.6')
    logger.info("starting migration steps")
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    logger.info("catalog rebuilt!")
    logger.info("refreshing reference catalog...")
    REQUEST = context.REQUEST
    ref_catalog = api.portal.get_tool('reference_catalog')
    ref_catalog.manage_catalogReindex(REQUEST, REQUEST.RESPONSE, REQUEST.URL)
    logger.info("migration done!")
