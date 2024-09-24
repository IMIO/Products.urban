# encoding: utf-8

from plone import api
import logging


def rename_patrimony_certificate(context):
    """ """
    logger = logging.getLogger("urban: rename Patrimony certificate")
    logger.info("starting upgrade steps")
    portal = api.portal.get()

    patrimony_folder = portal.urban.patrimonycertificates
    patrimony_folder.setTitle(u"Patrimoines")
    patrimony_folder.reindexObject(["Title"])

    patrimony_collection = portal.urban.patrimonycertificates.collection_patrimonycertificate
    patrimony_collection.setTitle(u"Patrimoines")
    patrimony_collection.reindexObject(["Title"])

    patrimony_config_folder = portal.portal_urban.patrimonycertificate
    patrimony_config_folder.setTitle(u"Paramètres des patrimoines")
    patrimony_config_folder.reindexObject(["Title"])

    logger.info("upgrade step done!")


def allow_corporate_tenant_in_inspections(context):
    """ """
    logger = logging.getLogger("urban: Allow corporate tenant in inspections")
    logger.info("starting upgrade steps")

    portal_types_tool = api.portal.get_tool("portal_types")
    isp_tool = portal_types_tool.get("Inspection")
    if "CorporationTenant" not in isp_tool.allowed_content_types:
        new_allowed_types = list(isp_tool.allowed_content_types) + ["CorporationTenant"]
        isp_tool.allowed_content_types = tuple(new_allowed_types)

    logger.info("upgrade step done!")
