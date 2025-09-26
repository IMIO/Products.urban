# encoding: utf-8

from eea.facetednavigation.interfaces import ICriteria
from Products.urban.config import URBAN_TYPES
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues
from plone import api
from plone.registry import Record
from plone.registry.field import List
from plone.registry.field import TextLine
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging


def fix_patrimony_certificate_class(context):
    from Products.urban.content.licence.PatrimonyCertificate import PatrimonyCertificate

    logger = logging.getLogger("urban: Fix patrimony certificate class")
    logger.info("starting upgrade steps")

    # fix FTI
    portal = api.portal.get()
    fti = portal.portal_types.PatrimonyCertificate
    fti.content_meta_type = "PatrimonyCertificate"
    fti.factory = "addPatrimonyCertificate"

    # migrate content
    catalog = api.portal.get_tool("portal_catalog")
    licence_brains = catalog(portal_type="PatrimonyCertificate")

    for licence_brain in licence_brains:
        licence = licence_brain.getObject()
        if licence.__class__ == PatrimonyCertificate:
            continue
        licence.__class__ = PatrimonyCertificate
        licence.meta_type = "PatrimonyCertificate"
        licence.schema = PatrimonyCertificate.schema
        licence.reindexObject()

    logger.info("upgrade step done!")


def add_new_registry_for_missing_capakey(context):
    logger = logging.getLogger("urban: Add new registry for missing capakey")
    logger.info("starting migration steps")

    registry = getUtility(IRegistry)
    key = "Products.urban.interfaces.IMissingCapakey"
    registry_field = List(
        title=u"Missing capakey",
        description=u"List of missing capakey",
        value_type=TextLine(),
    )
    registry_record = Record(registry_field)
    registry_record.value = []
    registry.records[key] = registry_record

    logger.info("migration done!")


def add_additional_delay_option(context):
    logger = logging.getLogger("urban: Add complementary delay option")
    logger.info("starting upgrade steps")

    # Add new term type, workflow and index
    logger.info("Add new term type, workflow and index")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-liege.urban:default", "workflow")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "catalog")

    # Add vocabulary
    logger.info("Add vocabulary")
    portal_urban = api.portal.get_tool("portal_urban")
    complementary_delay_folder = createVocabularyFolder(
        container=portal_urban,
        folder_id="complementary_delay",
        site=None,
        allowedtypes="ComplementaryDelayTerm"
    )
    complementary_delay_term = [
        {
            "id": "cyberattaque_spw",
            "title": u"Cyberattaque SPW - avril 2025",
            "delay": 60
        }
    ]
    createFolderDefaultValues(
        complementary_delay_folder,
        complementary_delay_term,
        portal_type="ComplementaryDelayTerm"
    )

    # Add qery widget to 'all' folder 
    urban_folder = api.portal.get().urban
    data = {
        "_cid_": u"c97",
        "title": u"Prorogation complémentaire",
        "hidden": False,
        "index": u"getComplementary_delay",
        "vocabulary": u"urban.vocabularies.complementary_delay"
    }
    urban_folder_criterion = ICriteria(urban_folder)
    if urban_folder_criterion is not None:
        urban_folder_criterion.add(
            wid="select2",
            position="top",
            section="advanced",
            **data
        )

    # Add complementary_delay field to all default
    logger.info("Add complementary_delay field to all default")
    field = "complementary_delay"
    
    for urban_type in URBAN_TYPES:
        # Add complementary_delay field 
        licence_config = portal_urban.get(urban_type.lower(), None)
        if licence_config is None:
            continue
        if not hasattr(licence_config, "getUsedAttributes"):
            continue
        used_attributes = licence_config.getUsedAttributes()
        if field in used_attributes:
            continue
        licence_config.setUsedAttributes(used_attributes + (field, ))
        logger.info("Type {}, attribute add".format(urban_type))

        #Add query widget
        licence_folder = getattr(urban_folder, "{}s".format(urban_type.lower()), None)
        if licence_folder is None:
            continue
        criterion = ICriteria(licence_folder)
        if criterion is None:
            continue

        criterion.add(
            wid="select2",
            position="top",
            section="advanced",
            **data
        )
        logger.info("Type {}, query widget add".format(urban_type))
        

    logger.info("upgrade step done!")