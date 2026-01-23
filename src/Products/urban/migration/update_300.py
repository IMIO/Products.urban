# -*- coding: utf-8 -*-

from Products.urban.utils import set_default_optional_field
from Products.urban.utils import set_eventconfig_optional_field
from plone import api
from plone.registry import Record
from plone.registry.field import Choice
from plone.registry.field import List
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from plone.app.textfield import RichTextValue
from Products.CMFPlone.utils import safe_unicode

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
    logger = logging.getLogger("urban: install imio.urban.core")
    logger.info("starting migration steps")
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-imio.urban.core:default')
    logger.info("migration done!")


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


def change_event_config_folder_allowed_types(context):
    from Products.urban.config import URBAN_TYPES
    from Products.urban.setuphandlers import setFolderAllowedTypes

    logger = logging.getLogger("urban: Change event config folder allowed types")
    logger.info("starting migration steps")

    portal_urban = api.portal.get_tool("portal_urban")
    for urban_type in URBAN_TYPES:
        type_config = getattr(portal_urban, urban_type.lower(), None)
        if type_config is None:
            logger.warning("Cannot find {} config folder".format(urban_type))
            continue
        event_configs_folder = getattr(type_config, "eventconfigs", None)
        if event_configs_folder is None:
            logger.warning("{} config has no eventconfigs folder")
            continue
        if urban_type in ["Inspection", "Ticket"]:
            setFolderAllowedTypes(
                event_configs_folder, ["EventConfig", "FollowUpEventConfig"]
            )
        else:
            setFolderAllowedTypes(
                event_configs_folder, ["EventConfig", "OpinionEventConfig"]
            )

    logger.info("migration done!")


def reimport_typeinfo(context):
    logger.info("starting migration steps : Import type profile")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:urbantypes', 'typeinfo')
    logger.info("migration done!")


def fix_parcelling_changesDescription_field(context):
    logger = logging.getLogger(
        "urban: Fix parcelling changesDirection"
    )
    logger.info("starting upgrade steps")
    brains = api.content.find(portal_type="Parcelling")
    for brain in brains:
        parcelling = brain.getObject()
        changesDescription = ""
        if hasattr(parcelling, "changesDescription"):
            changesDescription = parcelling.changesDescription
        if isinstance(changesDescription, RichTextValue):
            continue
        new_value = RichTextValue(safe_unicode(changesDescription))
        setattr(parcelling, "changesDescription", new_value)
    logger.info("migration step done!")


def set_eventconfig_optional_fields(context):
    logger = logging.getLogger(
        "urban: set event config default optional fields"
    )
    logger.info("starting upgrade steps")
    updated_event_configs = set_eventconfig_optional_field(
        "inspection",
        "UrbanEventInspectionReport",
        ["delay"],
    )
    logger.info("Config updated: {0}".format(", ".join(updated_event_configs)))
    logger.info("migration step done!")


def set_select_all_attachments_by_default_to_false(context):
    logger = logging.getLogger(
        "urban: Set select_all_attachments_by_default to false"
    )
    logger.info("starting upgrade steps")
    api.portal.set_registry_record(
        name=(
            "imio.pm.wsclient.browser.settings.IWS4PMClientSettings."
            "select_all_attachments_by_default"
        ),
        value=False
    )
    logger.info("migration step done!")


def _settransform(**kwargs):
    # Cannot pass a dict to set transform parameters, it has
    # to be separate keys and values
    # Also the transform requires all dictionary values to be set
    # at the same time: other values may be present but are not
    # required.
    transform = api.portal.get_tool("portal_transforms").safe_html
    for k in ('valid_tags', 'nasty_tags'):
        if k not in kwargs:
            kwargs[k] = transform.get_parameter_value(k)

    for k in list(kwargs):
        if isinstance(kwargs[k], dict):
            v = kwargs[k]
            kwargs[k + '_key'] = v.keys()
            kwargs[k + '_value'] = [str(s) for s in v.values()]
            del kwargs[k]
    transform.set_parameters(**kwargs)
    transform._p_changed = True
    transform.reload()


def add_tags_to_filter_html(context):
    logger = logging.getLogger(
        "urban: Add tags to filter html"
    )
    logger.info("starting upgrade steps")
    tag_to_add = "s"
    transforms = api.portal.get_tool("portal_transforms").safe_html
    valid_tags = transforms.get_parameter_value('valid_tags')
    if tag_to_add in valid_tags:
        return
    valid_tags["s"] = 1
    _settransform(valid_tags=valid_tags)
    logger.info("migration step done!")
