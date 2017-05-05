# encoding: utf-8

from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IInquiry
from plone import api
from zope.component import createObject

import logging

logger = logging.getLogger('urban: migrations')


def migrate_inquiry_date_fields():
    logger = logging.getLogger('urban: migrate Inquiry into EventInquiry ->')
    logger.info("starting migration step")
    cat = api.portal.get_tool('portal_catalog')
    licence_brains = cat(object_provides=IInquiry.__identifier__)
    licences = [l.getObject() for l in licence_brains if IGenericLicence.providedBy(l.getObject())]
    for licence in licences:
        start_date = getattr(licence, 'investigationStart', None)
        if not start_date:
            continue
        event_inquiries = [o for o in licence.objectValues() if o.portal_type == 'UrbanEventInquiry']
        if not event_inquiries:
            event_inquiries = [createObject('UrbanEventInquiry', 'enquete-publique', licence)]
        for event_inquiry in event_inquiries:
            inquiry = event_inquiry.getLinkedInquiry()
            if hasattr(inquiry, 'investigationStart'):
                event_inquiry.investigationStart = inquiry.investigationStart
                delattr(inquiry, 'investigationStart')
            if hasattr(inquiry, 'investigationEnd'):
                event_inquiry.investigationEnd = inquiry.investigationEnd
                delattr(inquiry, 'investigationEnd')
    logger.info("migration step done!")


def migrateform_tabbing():
    logger = logging.getLogger('urban: migrate form_tabbing.js expression ->')
    logger.info("starting migration step")
    api.portal.get_tool('portal_javascripts').getResource('form_tabbing.js').setExpression('')
    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.1')
    logger.info("starting migration steps")
    migrate_inquiry_date_fields()
    migrateform_tabbing()
    logger.info("migration done!")
