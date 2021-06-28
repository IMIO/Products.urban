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


def copy_MiscLicence_cfg_to_Inspection(context):
    """
    """
    logger = logging.getLogger('urban: add new default personTitle')
    logger.info("starting upgrade steps")
    portal_urban = api.portal.get_tool('portal_urban')
    logger.info("duplicate event configs")
    for eventconfig in portal_urban.miscdemand.eventconfigs.objectValues():
        api.content.copy(eventconfig, portal_urban.inspection.eventconfigs)
    logger.info("upgrade done!")
