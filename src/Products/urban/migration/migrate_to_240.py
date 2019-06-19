# encoding: utf-8

from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues
from Products.urban.config import URBAN_TYPES

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrate_create_voc_classification_order_scope(context):
    """
    """
    logger = logging.getLogger('urban: migrate create_voc_classification_order_scope')
    logger.info("starting migration step")
    container = api.portal.get_tool('portal_urban')
    classification_order_scope_vocabularies_config = default_values['global']['classification_order_scope']
    allowedtypes = classification_order_scope_vocabularies_config[0]
    classification_order_scope_vocabularies_config = createVocabularyFolder(container, 'classification_order_scope',
                                                                            context, allowedtypes)
    createFolderDefaultValues(
        classification_order_scope_vocabularies_config,
        default_values['global']['classification_order_scope'][1:],
        default_values['global']['classification_order_scope'][0]
    )

    logger.info("migration step done!")


def migrate_create_voc_general_disposition(context):
    """
    """
    logger = logging.getLogger('urban: migrate create_voc_general_disposition')
    logger.info("starting migration step")
    container = api.portal.get_tool('portal_urban')
    general_disposition_vocabularies_config = default_values['global']['general_disposition']
    allowedtypes = general_disposition_vocabularies_config[0]
    general_disposition_vocabularies_config = createVocabularyFolder(container, 'general_disposition',
                                                                     context, allowedtypes)
    createFolderDefaultValues(
        general_disposition_vocabularies_config,
        default_values['global']['general_disposition'][1:],
        default_values['global']['general_disposition'][0]
    )

    logger.info("migration step done!")


def migrate_create_voc_tax(context):
    """
    """
    logger = logging.getLogger('urban: migrate create_voc_tax')
    logger.info("starting migration step")
    container = api.portal.get_tool('portal_urban')
    tax_vocabularies_config = default_values['shared_vocabularies']['tax']
    allowedtypes = tax_vocabularies_config[0]
    tax_vocabularies_config = createVocabularyFolder(container, 'tax',context, allowedtypes)

    createFolderDefaultValues(
        tax_vocabularies_config,
        default_values['shared_vocabularies']['tax'][1:],
        default_values['shared_vocabularies']['tax'][0]
    )

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.4')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runImportStepFromProfile('profile-Products.urban:default', 'plone.app.registry')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:preinstall')
    setup_tool.runAllImportStepsFromProfile('profile-urban.vocabulary:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')
    setup_tool.runAllImportStepsFromProfile('profile-collective.externaleditor:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'urban-postInstall')
    migrate_create_voc_classification_order_scope(context)
    migrate_create_voc_general_disposition(context)
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    logger.info("migration done!")
