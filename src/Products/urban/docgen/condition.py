# -*- coding: utf-8 -*-

from collective.documentgenerator.content.condition import ConfigurablePODTemplateCondition

from plone import api


class UrbanTemplateCondition(ConfigurablePODTemplateCondition):
    """
    Check:
     - the permission
     - the TAL expression
     - the field 'activated'
     - the state 'enabled/disabled'
     of a PODTemplate on a context.
    """

    def evaluate(self):
        base_condition = super(UrbanTemplateCondition, self).evaluate()
        state_enabled = api.content.get_state(self.pod_template) == 'enabled'
        return base_condition and state_enabled
