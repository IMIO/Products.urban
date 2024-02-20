# -*- coding: utf-8 -*-

from plone import api
from datetime import datetime

import logging

logger = logging.getLogger("urban: migrations")


def migrate_vocabulary_validity_date(context):
    logger.info("starting : Update vocabulary term validity end date")
    portal_urban = api.portal.get()["portal_urban"]
    brains = api.content.find(
        portal_type="UrbanVocabularyTerm",
        review_state="disabled",
        context=portal_urban,
    )
    for brain in brains:
        term = brain.getObject()
        if term.getEndValidity() is None:
            term.setEndValidity(datetime.now())
    logger.info("upgrade done!")
