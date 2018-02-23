# -*- coding: utf-8 -*-

from imio.schedule.content.object_factories import EndConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject

from Products.urban.config import LICENCE_FINAL_STATES

from plone import api


def add_licence_ended_condition():
    """
    """
    portal_urban = api.portal.get_tool('portal_urban')
    for licence_config in portal_urban.objectValues('LicenceConfig'):
        schedule_cfg = licence_config.schedule

        for task_cfg in schedule_cfg.get_all_task_configs():

            # add 'licence_ended' to the end conditions
            ending_states = task_cfg.ending_states
            end_conditions = task_cfg.end_conditions or []
            end_condition_ids = end_conditions and [c.condition for c in end_conditions]
            condition_id = 'urban.schedule.licence_ended'
            if (end_condition_ids or not ending_states) and condition_id not in end_condition_ids:
                if task_cfg.portal_type == 'MacroTaskConfig':
                    condition = MacroEndConditionObject(
                        condition=condition_id,
                        operator='OR',
                        display_status=False
                    )
                else:
                    condition = EndConditionObject(
                        condition=condition_id,
                        operator='OR',
                        display_status=False
                    )
                task_cfg.end_conditions = (condition,) + tuple(end_conditions)
            elif ending_states:
                old_ending_states = list(task_cfg.ending_states)
                new_ending_states = list(set(old_ending_states + LICENCE_FINAL_STATES))
                task_cfg.ending_states = new_ending_states
