# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.layout.viewlets import ViewletBase


class WorkflowState(ViewletBase):
    """This viewlet displays the workflow state."""

    def get_state(self):
        return api.content.get_state(self.context)

    index = ViewPageTemplateFile("templates/workflow_state.pt")
