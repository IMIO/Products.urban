# encoding: utf-8

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
