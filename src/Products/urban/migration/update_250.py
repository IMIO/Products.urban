# encoding: utf-8

from plone import api
import logging

logger = logging.getLogger('urban: migrations')


def add_new_default_personTitle(context):
    logger = logging.getLogger('urban: add new default personTitle')
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')
    logger.info("upgrade done!")
