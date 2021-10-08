# -*- coding: utf-8 -*-

from Products.urban.events import licenceEvents
from imio.schedule import utils
from imio.schedule.events.zope_registration import unsubscribe_task_configs_for_content_type

import logging

logger = logging.getLogger(__name__)


def disabled(*args, **kwargs):
    pass


original_methods = {}


def _disable(module, to_patch=[]):
    for method in to_patch:
        if method not in original_methods:
            method_key = '{}.{}'.format(module.__name__, method)
            original_methods[method_key] = getattr(module, method)
        setattr(module, method, disabled)
        logger.info('disable {} method'.format(method))


def _restore(module, to_patch=[]):
    for method in to_patch:
        method_key = '{}.{}'.format(module.__name__, method)
        setattr(licenceEvents, method, original_methods.pop(method_key))
        logger.info('disable {} method'.format(method))


def disable_licence_default_values():
    to_patch = [
        '_setDefaultReference',
        '_setDefaultTextValues',
        '_setDefaultSelectValues',
        '_setDefaultFolderManagers',
    ]
    _disable(licenceEvents, to_patch)


def restore_licence_default_values():
    to_patch = [
        '_setDefaultReference',
        '_setDefaultTextValues',
        '_setDefaultSelectValues',
        '_setDefaultFolderManagers',
    ]
    _restore(licenceEvents, to_patch)


def disable_schedule():
    for schedule_cfg in utils.get_all_schedule_configs():
        for task_cfg in schedule_cfg.get_all_task_configs():
            unsubscribe_task_configs_for_content_type(task_cfg, None)
