# -*- coding: utf-8 -*-

from collective.wfadaptations.interfaces import IWorkflowAdaptation

from plone import api

from zope.interface import implements


class SimplifyWorkflowAdaptation(object):
    """
    Base class for workflow adaptation
    """

    implements(IWorkflowAdaptation)

    def patch_workflow(self, workflow_name, **parameters):

        wtool = api.portal.get_tool("portal_workflow")
        workflow = wtool[workflow_name]

        for transition_id in self.transitions_to_remove:
            if transition_id in workflow.transitions.objectIds():
                workflow.transitions.deleteTransitions([transition_id])

        for state_id in self.states_to_remove:
            if state_id in workflow.states.objectIds():
                workflow.states.deleteStates([state_id])

        for transition_id, new_target in self.transitions_new_target.iteritems():
            transition = getattr(workflow.transitions, transition_id)
            transition.new_state_id = new_target

        message = "simplified '{}' workflow".format(workflow_name)
        return True, message
