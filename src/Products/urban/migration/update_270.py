# -*- coding: utf-8 -*-

from plone.registry import Record
from plone.registry import field
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging


logger = logging.getLogger('urban: migrations')


def initialize_notice_settings(context):
    from Products.urban.browser.notice_settings import INoticeSettings

    logger = logging.getLogger("urban: Initialize Notice Settings")
    registry = getUtility(IRegistry)
    base = "Products.urban.browser.notice_settings.INoticeSettings"
    if "{0}.url".format(base) not in registry.records:
        registry_field = field.TextLine(title=INoticeSettings["url"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.url".format(base)] = registry_record
    if "{0}.municipality_id".format(base) not in registry.records:
        registry_field = field.TextLine(title=INoticeSettings["municipality_id"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.municipality_id".format(base)] = registry_record
    if "{0}.last_import_date".format(base) not in registry.records:
        registry_field = field.Datetime(title=INoticeSettings["last_import_date"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.last_import_date".format(base)] = registry_record
    logger.info("Upgrade done!")
