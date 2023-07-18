from plone import api
from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import createVocabularies
from Products.urban.setuphandlers import createVocabularyFolders

import logging


def add_couple_to_preliminary_notice(context):
    """
    """
    logger = logging.getLogger('urban: add Couple to Preliminary Notice')
    logger = logging.getLogger('urban: add Couple to Project Meeting')
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'workflow')
    logger.info("upgrade step done!")


def add_vocabularies_to_preliminary_notice_foldercategories(context):
    portal_urban = api.portal.get_tool('portal_urban')
    config_folder = getattr(portal_urban, 'preliminarynotice')
    preliminary_notice_vocabularies = default_values['PreliminaryNotice']
    createVocabularyFolders(
        container=config_folder, vocabularies=preliminary_notice_vocabularies, site=None
    )
    createVocabularies(
        container=config_folder, vocabularies=preliminary_notice_vocabularies
    )
