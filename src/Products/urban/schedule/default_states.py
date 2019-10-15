# -*- coding: utf-8 -*-

from imio.schedule.interfaces import IDefaultFreezeStates
from imio.schedule.interfaces import IDefaultThawStates

from plone import api

from zope.interface import implements


class LicencesDefaultFreezeStates(object):
    """
    """
    implements(IDefaultFreezeStates)

    def __init__(self, task_container):
        self.licence = task_container

    def __call__(self):
        return ['frozen_suspension']


class LicencesDefaultThawStates(object):
    """
    """
    implements(IDefaultThawStates)

    def __init__(self, task_container):
        self.licence = task_container

    def __call__(self):
        workflow_tool = api.portal.get_tool('portal_workflow')
        workflow_def = workflow_tool.getWorkflowsFor(self.licence)[0]
        states = [state_id for state_id in workflow_def.states.keys() if state_id != 'frozen_suspension']
        return states
