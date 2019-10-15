# -*- coding: utf-8 -*-

from collective.wfadaptations.interfaces import IWorkflowAdaptation

from Persistence import PersistentMapping

from plone import api

from zope.interface import implements


class SuspensionWorkflowAdaptation(object):
    """
    Suspension workflow adaptation adding a suspension state.
    """

    implements(IWorkflowAdaptation)

    def patch_workflow(self, workflow_name, **parameters):

        wtool = api.portal.get_tool('portal_workflow')
        workflow = wtool[workflow_name]

        self.create_suspend_transition(workflow, **parameters)
        self.set_suspend_transition(workflow, **parameters)
        self.create_resume_transition(workflow, **parameters)
        self.create_suspension_state(workflow, **parameters)
        self.create_frozen_suspension_state(workflow, **parameters)

        message = "patched '{}' workflow with suspension loop".format(workflow_name)
        return True, message

    def create_resume_transition(self, workflow, **parameters):
        """
         create a transition 'resume'
        """
        if 'resume' not in workflow.transitions:
            workflow.transitions.addTransition('resume')

        resume_transition = workflow.transitions['resume']
        props = parameters.get('resume_transition_guard', None)
        resume_transition.setProperties(
            title=resume_transition.id,
            new_state_id=parameters['resuming_state'],
            actbox_name=resume_transition.id,
            props=props,
        )

    def create_suspension_state(self, workflow, **parameters):
        """
        create a 'suspension' state
        """
        if 'suspension' not in workflow.states:
            workflow.states.addState('suspension')

        suspension_state = workflow.states['suspension']
        default_mapping = workflow.states.objectValues()[0].permission_roles.copy()
        suspension_state.title = 'suspension'
        suspension_state.permission_roles = default_mapping
        suspension_state.group_roles = PersistentMapping()
        suspension_state.var_values = PersistentMapping()
        suspension_state.transitions = ('resume',)

    def create_frozen_suspension_state(self, workflow, **parameters):
        """
        create a 'frozen_suspension' state
        """
        if 'frozen_suspension' not in workflow.states:
            workflow.states.addState('frozen_suspension')

        frozen_suspension_state = workflow.states['frozen_suspension']
        default_mapping = workflow.states['suspension'].permission_roles.copy()
        frozen_suspension_state.title = 'frozen_suspension'
        frozen_suspension_state.permission_roles = default_mapping
        frozen_suspension_state.group_roles = PersistentMapping()
        frozen_suspension_state.var_values = PersistentMapping()

    def create_suspend_transition(self, workflow, **parameters):
        """
        create a 'suspend' transition
        """
        if 'suspend' not in workflow.transitions:
            workflow.transitions.addTransition('suspend')
        suspend_transition = workflow.transitions['suspend']
        props = parameters.get('suspend_transition_guard', None)

        # update transition settings
        suspend_transition.setProperties(
            title=suspend_transition.id,
            new_state_id='suspension',
            actbox_name=suspend_transition.id,
            props=props
        )

    def set_suspend_transition(self, workflow, **parameters):
        """
        Set transition suspend on each state of the workflow but suspension
        """
        for state_name, state in workflow.states.objectItems():
            transitions = state.transitions
            if state_name != 'suspension' and 'suspend' not in transitions:
                new_transitions = transitions and transitions + ('suspend',) or ()
                state.transitions = new_transitions
