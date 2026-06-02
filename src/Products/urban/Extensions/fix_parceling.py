# -*- coding: utf-8 -*-

from plone import api
from plone.app.textfield.value import RichTextValue

import logging

logger = logging.getLogger("External method - fix parceling : ")

SUBDIVIDER_NAME_PLACEHOLDER = "n/a"


def fix_subdividerName_field():
    parcellings = api.content.find(portal_type="Parcelling")
    for parcelling in parcellings:
        parcelling_obj = parcelling.getObject()
        parcelling_obj.subdividerName = SUBDIVIDER_NAME_PLACEHOLDER


def fix_changesDescription_field():
    logger.info("Start fix changesDescription field")
    brains = api.content.find(portal_type="Parcelling")
    for brain in brains:
        parcelling = brain.getObject()
        if hasattr(parcelling.changesDescription, "raw"):
            continue
        description = parcelling.changesDescription
        if description is None:
            description = u"<p></p>"
        if not isinstance(description, (str, unicode)):
            raise ValueError("{} not a string".format(description))
        parcelling.changesDescription = RichTextValue(
            description,
            "text/html",
            "text/html",
        )
    logger.info("Finish External method")
