# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

from imio.actionspanel.browser.views import ActionsPanelView


class EventActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Urban Events.
    """
    def __init__(self, context, request):
        super(EventActionsPanelView, self).__init__(context, request)
        self.ACCEPTABLE_ACTIONS = ('plonemeeting_wsclient_action_1',)


class LicenceActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(LicenceActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = ('renderOwnDelete',)
        self.IGNORABLE_ACTIONS = ('cut', 'paste', 'rename', 'copy')


class ConfigValueActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(ConfigValueActionsPanelView, self).__init__(context, request)
        self.ACCEPTABLE_ACTIONS = ('rename', )


class TaskActionsPanelView(ActionsPanelView):
    """Actions pannel view of tasks"""

    def __init__(self, context, request):
        super(TaskActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderChangeOwner', )

    def __call__(self,
                 useIcons=True,
                 showTransitions=False,
                 appendTypeNameToTransitionLabel=False,
                 showEdit=False,
                 showOwnDelete=False,
                 showActions=False,
                 showAddContent=False,
                 showHistory=False,
                 showHistoryLastEventHasComments=False,
                 showChangeOwner=False,
                 **kwargs):

        self.showChangeOwner = showChangeOwner

        return super(TaskActionsPanelView, self).__call__(
            useIcons=True,
            showTransitions=False,
            appendTypeNameToTransitionLabel=False,
            showEdit=False,
            showOwnDelete=False,
            showActions=showActions,
            showAddContent=showAddContent,
            showHistory=False,
            showHistoryLastEventHasComments=False,
            **kwargs
        )

    def renderChangeOwner(self):
        """Render a link for the change owner view"""
        if self.showChangeOwner:
            return ViewPageTemplateFile('actions_panel_change_owner.pt')(self)


class FolderActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Folders.
    """

    def in_urban_config(self, folder):
        portal_urban = api.portal.get_tool('portal_urban')
        in_urban_config = portal_urban.contains(folder.UID())
        return in_urban_config

    def __call__(self,
                 useIcons=True,
                 showTransitions=False,
                 appendTypeNameToTransitionLabel=False,
                 showEdit=False,
                 showOwnDelete=False,
                 showActions=False,
                 showAddContent=False,
                 showHistory=False,
                 showHistoryLastEventHasComments=False,
                 **kwargs):

        folder = self.context
        if self.in_urban_config(folder):
            showAddContent = True

        return super(FolderActionsPanelView, self).__call__(
            useIcons=True,
            showTransitions=False,
            appendTypeNameToTransitionLabel=False,
            showEdit=False,
            showOwnDelete=False,
            showActions=showActions,
            showAddContent=showAddContent,
            showHistory=False,
            showHistoryLastEventHasComments=False,
            **kwargs
        )
