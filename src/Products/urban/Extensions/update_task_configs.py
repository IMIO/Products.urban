# -*- coding: utf-8 -*-

from imio.schedule.config import CREATION
from imio.schedule.config import STARTED
from imio.schedule.config import states_by_status
from imio.schedule.content.task import IAutomatedTask
from imio.schedule.content.object_factories import EndConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject

from Products.urban.config import LICENCE_FINAL_STATES
from Products.urban.interfaces import IGenericLicence

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from plone import api


def add_licence_ended_condition():
    """ """
    portal_urban = api.portal.get_tool("portal_urban")
    for licence_config in portal_urban.objectValues("LicenceConfig"):
        schedule_cfg = licence_config.schedule

        for task_cfg in schedule_cfg.get_all_task_configs():

            # add 'licence_ended' to the end conditions
            ending_states = task_cfg.ending_states
            end_conditions = task_cfg.end_conditions or []
            end_condition_ids = end_conditions and [c.condition for c in end_conditions]
            condition_id = "urban.schedule.licence_ended"
            if end_condition_ids and condition_id not in end_condition_ids:
                if task_cfg.portal_type == "MacroTaskConfig":
                    condition = MacroEndConditionObject(
                        condition=condition_id, operator="OR", display_status=False
                    )
                else:
                    condition = EndConditionObject(
                        condition=condition_id, operator="OR", display_status=False
                    )
                task_cfg.end_conditions = (condition,) + tuple(end_conditions)
            elif ending_states:
                old_ending_states = list(task_cfg.ending_states or [])
                new_ending_states = list(set(old_ending_states + LICENCE_FINAL_STATES))
                task_cfg.ending_states = new_ending_states


def close_old_tasks():
    catalog = api.portal.get_tool("portal_catalog")
    states = states_by_status[CREATION] = states_by_status[STARTED]
    task_brains = catalog(
        object_provides=IAutomatedTask.__identifier__, review_state=states
    )
    open_tasks = [b.getObject() for b in task_brains]
    licences = set(
        [
            t.aq_parent
            for t in open_tasks
            if IGenericLicence.providedBy(t.aq_parent)
            and api.content.get_state(t.aq_parent) in LICENCE_FINAL_STATES
        ]
    )
    for licence in licences:
        notify(ObjectModifiedEvent(licence))
        print "notified licence {}".format(licence)


def update_covid_tasks_deadline():
    catalog = api.portal.get_tool("portal_catalog")

    licences_to_update = set()

    for brain in catalog(portal_type=["TaskConfig", "MacroTaskConfig"]):
        task_cfg = brain.getObject()
        interface_1 = "Products.urban.schedule.interfaces.ITaskWithSuspensionDelay"
        interface_2 = "Products.urban.schedule.interfaces.ITaskWithWholeSuspensionDelay"
        if interface_1 in (task_cfg.marker_interfaces or []) or interface_2 in (
            task_cfg.marker_interfaces or []
        ):
            task_brains = catalog(
                object_provides=IAutomatedTask.__identifier__,
                task_config_UID=task_cfg.UID(),
                review_state=states_by_status[STARTED] + states_by_status[CREATION],
            )
            for brain in task_brains:
                task = brain.getObject()
                licences_to_update.add(task.get_container())

    for licence in licences_to_update:
        notify(ObjectModifiedEvent(licence))
        print "updated licence {}".format(licence.Title())


def update_task_delay():
    catalog = api.portal.get_tool("portal_catalog")

    licences_to_update = set()

    for brain in catalog(portal_type=["TaskConfig", "MacroTaskConfig"]):
        task_cfg = brain.getObject()
        task_brains = catalog(
            object_provides=IAutomatedTask.__identifier__,
            task_config_UID=task_cfg.UID(),
            review_state=states_by_status[STARTED] + states_by_status[CREATION],
        )
        for brain in task_brains:
            task = brain.getObject()
            licences_to_update.add(task.get_container())

    for licence in licences_to_update:
        notify(ObjectModifiedEvent(licence))
        print "updated licence {}".format(licence.Title())
