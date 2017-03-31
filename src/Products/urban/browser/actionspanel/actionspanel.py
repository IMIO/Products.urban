# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

from imio.actionspanel.browser.views import ActionsPanelView


class UrbanDefaultActionsPanelView(ActionsPanelView):
    """
    By default only show workflow, edit, and delete actions
    on urban objects.
    """
    def __init__(self, context, request):
        super(UrbanDefaultActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = ('renderTransitions', 'renderEdit', 'renderOwnDelete',)
        self.IGNORABLE_ACTIONS = ('cut', 'paste', 'rename', 'copy')


class EventActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Urban Events.
    """
    def __init__(self, context, request):
        super(EventActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderEdit', 'renderActions')
        self.ACCEPTABLE_ACTIONS = ('plonemeeting_wsclient_action_1',)


class LicenceActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(LicenceActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = ('renderEdit',)
        self.IGNORABLE_ACTIONS = ('cut', 'paste', 'rename', 'copy')


class TransitionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(TransitionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = ('renderTransitions', 'renderHistory',)

    def __call__(self,
                 **kwargs):
        return super(TransitionsPanelView, self).__call__(
            showHistory=True,
            **kwargs
        )

    def _transitionsToConfirm(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow = portal_workflow.getWorkflowsFor(self.context)[0]
        transitions = workflow.transitions.objectIds()

        to_confirm = dict([('%s.%s' % (self.context.portal_type, tr), 'simpleconfirm_view') for tr in transitions])

        return to_confirm


class ConfigValueActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(ConfigValueActionsPanelView, self).__init__(context, request)
        self.ACCEPTABLE_ACTIONS = ('rename', )


class AutomatedTaskActionsPanelView(ActionsPanelView):
    """Actions pannel view of tasks"""

    def __init__(self, context, request):
        super(AutomatedTaskActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderChangeOwner',)

    def __call__(self,
                 useIcons=False,
                 showTransitions=False,
                 appendTypeNameToTransitionLabel=False,
                 showEdit=False,
                 showOwnDelete=False,
                 showActions=False,
                 showAddContent=False,
                 showHistory=False,
                 showHistoryLastEventHasComments=False,
                 showChangeOwner=True,
                 **kwargs):

        self.showChangeOwner = showChangeOwner

        return super(AutomatedTaskActionsPanelView, self).__call__(
            useIcons=useIcons,
            showTransitions=showTransitions,
            appendTypeNameToTransitionLabel=False,
            showEdit=showEdit,
            showOwnDelete=showOwnDelete,
            showActions=showActions,
            showAddContent=showAddContent,
            showHistory=showHistory,
            showHistoryLastEventHasComments=showHistoryLastEventHasComments,
            **kwargs
        )

    def renderChangeOwner(self):
        """Render a link for the change owner view"""
        if self.showChangeOwner:
            return ViewPageTemplateFile('actions_panel_change_owner.pt')(self)


class SimpleTaskActionsPanelView(ActionsPanelView):
    """Actions pannel view of tasks"""

    def __init__(self, context, request):
        super(SimpleTaskActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = (
            'renderTransitions',
            'renderEdit',
            'renderOwnDelete',
            'renderActions',
        )

    def __call__(self,
                 useIcons=True,
                 showTransitions=True,
                 appendTypeNameToTransitionLabel=False,
                 showEdit=True,
                 showOwnDelete=True,
                 showActions=False,
                 showAddContent=False,
                 showHistory=False,
                 showHistoryLastEventHasComments=False,
                 **kwargs):

        return super(SimpleTaskActionsPanelView, self).__call__(
            useIcons=useIcons,
            showTransitions=showTransitions,
            appendTypeNameToTransitionLabel=False,
            showEdit=showEdit,
            showOwnDelete=showOwnDelete,
            showActions=showActions,
            showAddContent=showAddContent,
            showHistory=showHistory,
            showHistoryLastEventHasComments=showHistoryLastEventHasComments,
            **kwargs
        )


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
            useIcons=useIcons,
            showTransitions=showTransitions,
            appendTypeNameToTransitionLabel=appendTypeNameToTransitionLabel,
            showEdit=showEdit,
            showOwnDelete=showOwnDelete,
            showActions=showActions,
            showAddContent=showAddContent,
            showHistory=showHistory,
            showHistoryLastEventHasComments=showHistoryLastEventHasComments,
            **kwargs
        )
