# encoding: utf-8

from Acquisition import aq_parent
from OFS.interfaces import IOrderedContainer
from Products.urban.migration.utils import refresh_workflow_permissions
from imio.schedule.content.object_factories import MacroCreationConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject
from imio.schedule.content.object_factories import MacroFreezeConditionObject
from imio.schedule.content.object_factories import MacroRecurrenceConditionObject
from imio.schedule.content.object_factories import MacroStartConditionObject
from imio.schedule.content.object_factories import MacroThawConditionObject
from imio.schedule.events.zope_registration import (
    register_schedule_collection_criterion,
)
from imio.schedule.events.zope_registration import register_task_collection_criterion
from imio.schedule.events.zope_registration import (
    subscribe_task_configs_for_content_type,
)
from imio.schedule.events.zope_registration import (
    unregister_schedule_collection_criterion,
)
from imio.schedule.events.zope_registration import unregister_task_collection_criterion
from imio.schedule.events.zope_registration import (
    unsubscribe_task_configs_for_content_type,
)
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter

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


def rename_content_rule(context):
    """ """
    logger = logging.getLogger("urban: Rename a content rules")
    logger.info("starting upgrade steps")

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "contentrules")

    logger.info("upgrade step done!")


def fix_supended_state_licence(context):
    logger = logging.getLogger("urban: Fix supended state licence")
    logger.info("starting upgrade steps")
    portal = api.portal.get()
    urban_path = "/".join(portal["urban"].getPhysicalPath())
    refresh_workflow_permissions(
        "codt_buildlicence_workflow",
        folder_path=urban_path,
        for_states=["suspension", "frozen_suspension"]
    )
    logger.info("upgrade done!")


def log_info(logger, msg):
    if logger:
        logger.info(msg)


def _replace_object(obj, new_type, condition=None, logger=None):
    portal = api.portal.get()
    request = portal.REQUEST
    container = aq_parent(obj)

    ordered = IOrderedContainer(container, None)
    if ordered is not None:
        order = ordered.getObjectPosition(obj.getId())

    serializer = getMultiAdapter((obj, request), ISerializeToJson)
    old_obj_data = serializer()
    collection_uid = obj["dashboard_collection"].UID()
    log_info(logger, "{} deleted".format("/".join(obj.getPhysicalPath())))
    api.content.delete(obj)

    new_obj = api.content.create(
        container=container,
        type=new_type,
        id=old_obj_data["id"],
        title=old_obj_data["title"],
        start_date=old_obj_data["start_date"]["token"],
        enabled=old_obj_data["enabled"],
        default_assigned_group=old_obj_data["default_assigned_group"]["token"],
        default_assigned_user=old_obj_data["default_assigned_user"]["token"],
        warning_delay=old_obj_data["warning_delay"],
        additional_delay=old_obj_data["additional_delay"],
        additional_delay_type=old_obj_data["additional_delay_type"],
        round_to_day=old_obj_data["round_to_day"]["token"],
        activate_recurrency=old_obj_data["activate_recurrency"],
    )
    log_info(logger, "{} created".format("/".join(obj.getPhysicalPath())))

    state_keys = [
        "calculation_delay",
        "marker_interfaces",
        "creation_state",
        "starting_states",
        "ending_states",
        "freeze_states",
        "thaw_states",
        "recurrence_states",
    ]

    for key in state_keys:
        if key in old_obj_data and old_obj_data[key]:
            setattr(
                new_obj,
                key,
                [item["token"] for item in old_obj_data["calculation_delay"]],
            )

    conditions = {
        "creation_conditions": MacroCreationConditionObject,
        "start_conditions": MacroStartConditionObject,
        "end_conditions": MacroEndConditionObject,
        "freeze_conditions": MacroFreezeConditionObject,
        "thaw_conditions": MacroThawConditionObject,
        "recurrence_conditions": MacroRecurrenceConditionObject,
    }

    for key, value in conditions.items():
        if key in old_obj_data and old_obj_data[key]:
            setattr(
                new_obj,
                key,
                set(
                    [
                    value(
                        condition=item["condition"],
                        operator=item["operator"],
                            display_status=item["display_status"],
                    )
                    for item in old_obj_data[key]
                    ]
                ),
            )

    unsubscribe_task_configs_for_content_type(new_obj, None)
    unregister_task_collection_criterion(new_obj, None)

    setattr(new_obj, "_plone.uuid", old_obj_data["UID"])
    new_obj.reindexObject(idxs=["UID"])

    if ordered:
        ordered.moveObjectToPosition(new_obj.getId(), order)
        new_obj.reindexObject(idxs=["getObjPositionInParent"])

    subscribe_task_configs_for_content_type(new_obj, None)
    register_task_collection_criterion(new_obj, None)

    dashboard_collection = new_obj["dashboard_collection"]

    setattr(dashboard_collection, "_plone.uuid", collection_uid)
    dashboard_collection.reindexObject(idxs=["UID"])

    dashboard_collection.showNumberOfItems = True

    query = [
        {"i": filter["i"], "o": filter["o"], "v": old_obj_data["UID"]}
        if filter["i"] == "CompoundCriterion"
        else filter
        for filter in dashboard_collection.query
    ]

    dashboard_collection.setQuery(query)


def fix_config_wrong_class(context):
    """ """
    logger = logging.getLogger("migrate announcement schedule config")
    logger.info("starting upgrade steps")
    portal_urban = api.portal.get_tool("portal_urban")
    for licence_config in portal_urban.objectValues("LicenceConfig"):
        schedule_cfg = getattr(licence_config, "schedule", None)

        if schedule_cfg and hasattr(schedule_cfg, "announcement-preparation"):
            data = schedule_cfg.REQUEST.form
            data["force_dashboard_creation"] = True
            schedule_cfg.REQUEST.form = data

            unregister_schedule_collection_criterion(schedule_cfg, None)

            announcement_prep_task = getattr(schedule_cfg, "announcement-preparation")
            _replace_object(announcement_prep_task, "MacroTaskConfig", logger)

            announcement_done_task = getattr(schedule_cfg, "announcement")
            _replace_object(announcement_done_task, "MacroTaskConfig", logger)

            register_schedule_collection_criterion(schedule_cfg, None)
            data["force_dashboard_creation"] = False
            schedule_cfg.REQUEST.form = data

    logger.info("Upgrade step done!")
