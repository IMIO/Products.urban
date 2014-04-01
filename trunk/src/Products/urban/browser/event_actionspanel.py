from imio.actionspanel.browser.views import ActionsPanelView


class EventActionsPanelView(ActionsPanelView):
    """
      This manage the view displaying actions on context
    """
    def __init__(self, context, request):
        super(EventActionsPanelView, self).__init__(context, request)
        # portal_actions.object_buttons action ids to keep
        # if you define some here, only these actions will be kept
        self.ACCEPTABLE_ACTIONS = (
            'delete',
            'plonemeeting_wsclient_action_1',
        )
