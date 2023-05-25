# -*- coding: utf-8 -*-

from imio.actionspanel.browser.views import ActionsPanelView
from imio.actionspanel.browser.views import DEFAULT_CONFIRM_VIEW
from imio.actionspanel import ActionsPanelMessageFactory as _actions
from imio.urban.core.contents.eventconfig.content import IEventConfig

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.CMFPlone import PloneMessageFactory as _plone
from Products.DCWorkflow.Transitions import TransitionDefinition
from Products.urban.interfaces import IGenericLicence

from zope.annotation import IAnnotations
from zope.i18n import translate


class UrbanDefaultActionsPanelView(ActionsPanelView):
    """
    By default only show workflow, edit, and delete actions
    on urban objects.
    """
    def __init__(self, context, request):
        super(UrbanDefaultActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = ('renderTransitions', 'renderEdit', 'renderOwnDelete')
        self.IGNORABLE_ACTIONS = ('cut', 'paste', 'rename', 'copy')


class EventActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Urban Events.
    """
    def __init__(self, context, request):
        super(EventActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderEdit', 'renderOwnDelete', 'renderActions')
        self.ACCEPTABLE_ACTIONS = ('plonemeeting_wsclient_action_1', 'plonemeeting_wsclient_action_2',)


class ReorderActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Urban Events.
    """
    def __init__(self, context, request):
        super(ReorderActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderArrows',)

    def __call__(self, **kwargs):
        kwargs['showArrows']  = False,
        kwargs['arrowsPortalTypeAware'] = False,

        return super(ReorderActionsPanelView, self).__call__(
            **kwargs
        )

    def _returnTo(self, ):
        """What URL should I return to after moving the element and page is refreshed."""
        url = self.request.getURL()
        if IGenericLicence.providedBy(self.context.aq_parent):
            url = '{}/{}'.format(url, '#fieldsetlegend-attachments')
        return url

class RecipientCadastreActionsPanelView(UrbanDefaultActionsPanelView):
    """
    Actions panel view of Urban Inquiry Events.
    """
    def __init__(self, context, request):
        super(RecipientCadastreActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderTransitions', 'renderActions', 'renderEdit', 'renderOwnDelete')
        self.ACCEPTABLE_ACTIONS = ('copy_to_claimant',)


class TransferOfLicenceActionsPanelView(UrbanDefaultActionsPanelView):
    """
    Actions panel view of Urban Transfer of licence event.
    """
    def __init__(self, context, request):
        super(TransferOfLicenceActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderTransitions', 'renderActions', 'renderEdit', 'renderOwnDelete')


class LicenceActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(LicenceActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = ('renderEdit', 'renderActions')
        self.IGNORABLE_ACTIONS = ('cut', 'paste', 'rename', 'copy')
        self.ACCEPTABLE_ACTIONS = ('urban_duplicate_licence',)

    def triggerTransition(self, transition, comment, redirect=True):
        freeze_transition = 'suspend_freeze'
        thaw_transition = 'resume_thaw'
        if transition not in [freeze_transition, thaw_transition]:
            return super(LicenceActionsPanelView, self).triggerTransition(transition, comment, redirect)
        else:
            licence = self.context
            annotations = IAnnotations(licence)
            freeze_infos = annotations.get('imio.schedule.freeze_task', {'previous_state': api.content.get_state(licence)})
            if transition == freeze_transition:
                new_state = 'frozen_suspension'
                title = 'Freeze suspend'
                freeze_infos['freeze_state'] = api.content.get_state(licence)
                annotations['imio.schedule.freeze_task'] = freeze_infos
            else:
                new_state = freeze_infos['freeze_state']
                title = 'Freeze suspend'

            # execute
            plone_utils = api.portal.get_tool('plone_utils')
            workflow_tool = api.portal.get_tool('portal_workflow')
            workflow_def = workflow_tool.getWorkflowsFor(licence)[0]
            transition = TransitionDefinition(transition)
            transition.setProperties(title, new_state)
            workflow_def._executeTransition(licence, transition)

            transition_title = freeze_transition.capitalize()
            # add a portal message, we try to translate a specific one or add 'Item state changed.' as default
            msg = _actions('%s_done_descr' % transition_title, default=_plone("Item state changed."))
            plone_utils.addPortalMessage(msg)

            if not self.member.has_permission('View', self.context):
                # After having triggered a wfchange, it the current user
                # can not access the obj anymore, try to find a place viewable by the user
                redirectToUrl = self._redirectToViewableUrl()
                # add a specific portal_message before redirecting the user
                msg = _actions(
                    'redirected_after_transition_not_viewable',
                    default="You have been redirected here because you do not have "
                            "access anymore to the element you just changed the state for."
                )
                plone_utils.addPortalMessage(msg, 'warning')
                return redirectToUrl
            else:
                # in some cases, redirection is managed at another level, by jQuery for example
                if not redirect:
                    return
                return self.request.get('HTTP_REFERER')


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
            forceRedirectAfterTransition=True,
            **kwargs
        )

    def getTransitions(self):
        transitions = super(TransitionsPanelView, self).getTransitions()
        workflow = self.request.get('imio.actionspanel_workflow_%s_cachekey' % self.context.portal_type, None)
        if 'frozen_suspension' in workflow.states:
            if api.content.get_state(self.context) == 'frozen_suspension':
                # add 'resume_thaw' fake transition
                transitions.append(
                    {
                        'id': 'resume_thaw',
                        # if the transition.id is not translated, use translated transition.title...
                        'title': translate('resume_thaw', domain="plone", context=self.request),
                        'description': '',
                        'name': 'Resume_thaw',
                        'may_trigger': True,
                        'confirm': True,
                        'confirmation_view': DEFAULT_CONFIRM_VIEW,
                        'url': '' % {'content_url': self.context.absolute_url(), 'portal_url': self.portal_url, 'folder_url': ''},
                        'icon': '' % {'content_url': self.context.absolute_url(), 'portal_url': self.portal_url, 'folder_url': ''},
                    }
                )
            else:
                # add 'suspend_freeze' fake transition
                transitions.append(
                    {
                        'id': 'suspend_freeze',
                        # if the transition.id is not translated, use translated transition.title...
                        'title': translate('suspend_freeze', domain="plone", context=self.request),
                        'description': '',
                        'name': 'Suspend_freeze',
                        'may_trigger': True,
                        'confirm': True,
                        'confirmation_view': DEFAULT_CONFIRM_VIEW,
                        'url': '' % {'content_url': self.context.absolute_url(), 'portal_url': self.portal_url, 'folder_url': ''},
                        'icon': '' % {'content_url': self.context.absolute_url(), 'portal_url': self.portal_url, 'folder_url': ''},
                    }
                )
        return transitions

    def sortTransitions(self, lst):
        """ Sort the list of transitions """
        super(TransitionsPanelView, self).sortTransitions(lst)
        end_transition_ids = ['abandon', 'suspend']
        to_move = []
        for transition in lst:
            if transition['id'] in end_transition_ids:
                to_move.append(lst.pop(lst.index(transition)))
        lst.extend(to_move)

    def _transitionsToConfirm(self):
        portal_workflow = api.portal.get_tool('portal_workflow')
        workflow = portal_workflow.getWorkflowsFor(self.context)[0]
        transitions = workflow.transitions.objectIds()

        to_confirm = dict([('%s.%s' % (self.context.portal_type, tr), 'simpleconfirm_view') for tr in transitions])

        return to_confirm

    def showHistoryForContext(self):
        # Ensure that self.content_history is initialized
        super(TransitionsPanelView, self).showHistoryForContext()
        return True


class ConfigValueActionsPanelView(ActionsPanelView):
    """
    Actions panel view of Licences.
    """
    def __init__(self, context, request):
        super(ConfigValueActionsPanelView, self).__init__(context, request)
        self.ACCEPTABLE_ACTIONS = ('rename', )

    def __call__(self,  **kwargs):
        kwargs['showOwnDelete'] = False
        # handle case where event config is ALSO an urban config value
        if IEventConfig.providedBy(self.context):
            kwargs['showAddContent'] = True
            kwargs['showTransitions'] = False
            kwargs['showActions'] = False
        return super(ConfigValueActionsPanelView, self).__call__(**kwargs)


class AutomatedTaskActionsPanelView(ActionsPanelView):
    """Actions pannel view of tasks"""

    def __init__(self, context, request):
        super(AutomatedTaskActionsPanelView, self).__init__(context, request)
        self.SECTIONS_TO_RENDER = ('renderChangeOwner', 'renderCloseTask')

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
                 showCloseTask=True,
                 **kwargs):

        self.showChangeOwner = showChangeOwner
        self.showCloseTask = showCloseTask

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
            self.saveHasActions()
            return ViewPageTemplateFile('actions_panel_change_owner.pt')(self)

    def renderCloseTask(self):
        """Render a link  to close the task manually"""
        if self.showCloseTask:
            self.saveHasActions()
            return ViewPageTemplateFile('actions_panel_close_task.pt')(self)


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
