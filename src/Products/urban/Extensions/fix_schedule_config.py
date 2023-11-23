# -*- coding: utf-8 -*-

from Products.urban.config import URBAN_TYPES
from importlib import import_module
from plone import api

import logging

logger = logging.getLogger('urban: fix schedule config')


def get_class(class_path):
    module_name, class_name = class_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, class_name)


def check_condition(condition, expected_class):
    cls = get_class(expected_class)
    return condition.__class__ == cls


def fix_class_schedule(container, result):
    for key, item in container.items():
        if key == "dashboard_collection":
            continue
        mapping = {
            "creation_conditions": "CreationConditionObject",
            "start_conditions": "StartConditionObject",
            "end_conditions": "EndConditionObject",
            "freeze_conditions": "FreezeConditionObject",
            "thaw_conditions": "ThawConditionObject",
            "recurrence_conditions": "RecurrenceConditionObject",
        }
        class_basepath = "imio.schedule.content.object_factories.{0}"
        for attrname, factoryname in mapping.items():
            if not hasattr(item, attrname) or not getattr(item, attrname):
                continue
            
            if item.__class__.__name__ == "TaskConfig":
                expected_class = class_basepath.format(factoryname)
            elif item.__class__.__name__ == "MacroTaskConfig":
                expected_class = class_basepath.format("Macro{0}".format(factoryname))
            conditions = getattr(item, attrname)
            condition_errors = []
            for condition in conditions:
                if not check_condition(condition, expected_class):
                    condition_errors.append(condition)
            if condition_errors and len(condition_errors) == len(conditions):
                new_conditions = ()
                for condition in condition_errors:
                    new_class = get_class(expected_class)
                    result.append(
                        "Condition {0} on item {1} migrated from {2} to {3}".format(
                            str(condition),
                            item.absolute_url(),
                            str(condition.__class__),
                            str(new_class),
                        )
                    )
                    condition.__class__ = new_class
                    new_conditions += (condition, )
                setattr(item, attrname, new_conditions)
            elif condition_errors:
                result.append("Can not migrate condition on {0}".format(item.absolute_url()))
        result = fix_class_schedule(item, result)
    return result


def fix_schedule_config():
    portal = api.portal.get()
    portal_urban = portal["portal_urban"]
    result = []
    for ptype in URBAN_TYPES:
        cfg_folder = portal_urban[ptype.lower()]
        if "schedule" not in cfg_folder:
            continue
        schedule_config = cfg_folder["schedule"]
        fix_class_schedule(schedule_config, result)
    return "\n".join(result)

"""
 'creation_conditions': (<imio.schedule.content.object_factories.MacroCreationConditionObject object at 0x7f806ae3ffd0>,),
 'creation_date': DateTime('2017/05/31 15:04:54.522570 GMT+2'),
 'creation_state': ('complete',),
 'creators': ('admin',),
 'default_assigned_group': 'urban_editors',
 'default_assigned_user': 'urban.assign_folder_manager',
 'description': '',
 'end_conditions': (<imio.schedule.content.object_factories.EndConditionObject object at 0x7f806ae3f450>,),
"""