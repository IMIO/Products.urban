# encoding: utf-8

from plone import api

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
