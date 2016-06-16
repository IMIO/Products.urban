# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase

from plone import api

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class WorkflowState(ViewletBase):
    """This viewlet displays the workflow state."""

    def get_state(self):
        return api.content.get_state(self.context)

    index = ViewPageTemplateFile("templates/workflow_state.pt")
