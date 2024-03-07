# -*- coding: utf-8 -*-

from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues
from plone import api

import logging

logger = logging.getLogger("urban: migrations")


def migrate(context):
    """
    Launch every migration steps for the version 1.11.1
    """
    logger = logging.getLogger("urban: migrate to 1.11.1")
    logger.info("starting migration steps")
    migrate_karst_constraints(context)
    migrate_concentrated_runoff_s_risk(context)
    logger.info("migration done!")


def migrate_karst_constraints(context):
    """ """
    logger = logging.getLogger("urban: migrate karst constraints")
    logger.info("starting migration step")

    container = api.portal.get_tool("portal_urban")
    karst_constraints_vocabularies_config = default_values["global"][
        "karst_constraints"
    ]
    allowedtypes = karst_constraints_vocabularies_config[0]
    karst_constraints_folder_config = createVocabularyFolder(
        container, "karst_constraints", context, allowedtypes
    )
    createFolderDefaultValues(
        karst_constraints_folder_config,
        default_values["global"]["karst_constraints"][1:],
        default_values["global"]["karst_constraints"][0],
    )

    logger.info("migration step done!")


def migrate_concentrated_runoff_s_risk(context):
    """ """
    logger = logging.getLogger("urban: migrate concentrated runoff's risk")
    logger.info("starting migration step")

    container = api.portal.get_tool("portal_urban")
    concentrated_runoff_s_risk_vocabularies_config = default_values["global"][
        "concentrated_runoff_s_risk"
    ]
    allowedtypes = concentrated_runoff_s_risk_vocabularies_config[0]
    concentrated_runoff_s_risk_folder_config = createVocabularyFolder(
        container, "concentrated_runoff_s_risk", context, allowedtypes
    )
    createFolderDefaultValues(
        concentrated_runoff_s_risk_folder_config,
        default_values["global"]["concentrated_runoff_s_risk"][1:],
        default_values["global"]["concentrated_runoff_s_risk"][0],
    )

    logger.info("migration step done!")
