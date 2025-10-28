# encoding: utf-8

from Products.urban import UrbanMessage as _
from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import add_new_urban_licence_type
from Products.urban.setuphandlers import createFolderDefaultValues
from Products.urban.setuphandlers import createVocabularyFolder
from plone import api

import logging


def add_building_procedure(context):
    logger = logging.getLogger("urban: Add housing procedure")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    setup_tool.runImportStepFromProfile("profile-Products.urban:urbantypes", "typeinfo")

    add_new_urban_licence_type("Housing")

    # Add vocabularies
    portal_urban = api.portal.get_tool("portal_urban")
    dimension_type_vocabularies_config = default_values["global"]["dimensiontypes"]
    allowedtypes = dimension_type_vocabularies_config[0]
    dimension_type_vocabularies_config = createVocabularyFolder(
        portal_urban, "dimensiontypes", context, allowedtypes
    )
    createFolderDefaultValues(
        dimension_type_vocabularies_config,
        default_values["global"]["dimensiontypes"][1:],
        default_values["global"]["dimensiontypes"][0],
    )
    units_vocabularies_config = default_values["global"]["units"]
    allowedtypes = units_vocabularies_config[0]
    units_vocabularies_config = createVocabularyFolder(
        portal_urban, "units", context, allowedtypes
    )
    createFolderDefaultValues(
        units_vocabularies_config,
        default_values["global"]["units"][1:],
        default_values["global"]["units"][0],
    )
    observation_items_vocabularies_config = default_values["Housing"][
        "observationitems"
    ]
    observation_items_vocabularies_config = createVocabularyFolder(
        portal_urban.housing, "observationitems", context, allowedtypes
    )
    createFolderDefaultValues(
        observation_items_vocabularies_config,
        default_values["Housing"]["observationitems"][1:],
        default_values["Housing"]["observationitems"][0],
    )

    logger.info("migration step done!")
