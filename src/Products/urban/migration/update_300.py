# -*- coding: utf-8 -*-

from Products.urban.utils import set_default_optional_field
from plone import api
from plone.registry import Record
from plone.registry.field import Choice
from plone.registry.field import List
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging


logger = logging.getLogger("urban: migrations")


def set_additional_reference_as_default(context):
    logger = logging.getLogger(
        "urban: Activate additionalReference for all licences types"
    )
    logger.info("starting upgrade steps")
    updated_types = set_default_optional_field("additionalReference")
    logger.info("Licences updated: {0}".format(", ".join(updated_types)))
    logger.info("migration step done!")


def install_urban_core(context):
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-imio.urban.core:default')


def add_missing_registry_record(context):
    logger = logging.getLogger("urban: add offdays settings")
    logger.info("starting migration steps")

    from collective.z3cform.datagridfield.registry import DictRow
    from Products.urban.browser.offdays_settings import IOffDay
    from Products.urban.browser.offdays_settings import IOffDayPeriod

    registry = getUtility(IRegistry)

    key = "Products.urban.browser.offdays_settings.IOffDays.week_offdays"
    registry_field = List(
        title=u"Week off days",
        description=u"",
        value_type=Choice(
            title=u"weekdays", vocabulary=u"urban.vocabularies.weekdays"
        ),
    )
    registry_record = Record(registry_field)
    registry_record.value = []
    registry.records[key] = registry_record

    key = "Products.urban.browser.offdays_settings.IOffDays.periods"
    registry_field = List(
        title=u"Off days period",
        description=u"",
        value_type=DictRow(title=u"Period", schema=IOffDayPeriod, required=False),
    )
    registry_record = Record(registry_field)
    registry_record.value = []
    registry.records[key] = registry_record

    key = "Products.urban.browser.offdays_settings.IOffDays.offdays"
    registry_field = List(
        title=u"Off days",
        description=u"",
        value_type=DictRow(title=u"Day", schema=IOffDay, required=False),
    )
    registry_record = Record(registry_field)
    registry_record.value = []
    registry.records[key] = registry_record

    logger.info("migration done!")
