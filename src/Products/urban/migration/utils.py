# -*- coding: utf-8 -*-

from Products.urban.events import licenceEvents
from plone import api
from imio.schedule import utils
from imio.schedule.events.zope_registration import (
    unsubscribe_task_configs_for_content_type,
)

import logging

logger = logging.getLogger(__name__)


def disabled(*args, **kwargs):
    pass


original_methods = {}


def _disable(module, to_patch=[]):
    for method in to_patch:
        if method not in original_methods:
            method_key = "{}.{}".format(module.__name__, method)
            original_methods[method_key] = getattr(module, method)
        setattr(module, method, disabled)
        logger.info("disable {} method".format(method))


def _restore(module, to_patch=[]):
    for method in to_patch:
        method_key = "{}.{}".format(module.__name__, method)
        setattr(licenceEvents, method, original_methods.pop(method_key))
        logger.info("disable {} method".format(method))


def disable_licence_default_values():
    to_patch = [
        "_setDefaultReference",
        "_setDefaultTextValues",
        "_setDefaultSelectValues",
        "_setDefaultFolderManagers",
    ]
    _disable(licenceEvents, to_patch)


def restore_licence_default_values():
    to_patch = [
        "_setDefaultReference",
        "_setDefaultTextValues",
        "_setDefaultSelectValues",
        "_setDefaultFolderManagers",
    ]
    _restore(licenceEvents, to_patch)


def disable_schedule():
    for schedule_cfg in utils.get_all_schedule_configs():
        for task_cfg in schedule_cfg.get_all_task_configs():
            unsubscribe_task_configs_for_content_type(task_cfg, None)


def refresh_workflow_permissions(workflow_id, folder_path=None, for_states=None):
    if not folder_path:
        folder_path = '/'.join(api.portal.get().getPhysicalPath())
    portal_workflow = api.portal.get_tool('portal_workflow')
    portal_catalog = api.portal.get_tool('portal_catalog')

    for at_type, wf_ids in portal_workflow._chains_by_type.items():
        if len(wf_ids) < 1:
            continue
        if wf_ids[0] == workflow_id:
            workflow = portal_workflow.getWorkflowById(wf_ids[0])
            query = {
                'path': {'query': folder_path},
                'portal_type': at_type,
            }
            if for_states is not None:
                query["review_state"] = for_states
            results = portal_catalog.unrestrictedSearchResults(query)
            for brain in results:
                obj = brain.getObject()
                workflow.updateRoleMappingsFor(obj)
                obj.reindexObjectSecurity()
                obj.reindexObject(idxs=['allowedRolesAndUsers'])
