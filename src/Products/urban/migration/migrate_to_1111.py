# -*- coding: utf-8 -*-

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate(context):
    """
     Launch every migration steps for the version 1.11.1
    """
    logger = logging.getLogger('urban: migrate to 1.11.1')
    logger.info("starting migration steps")

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")
