# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager

from Products.Five import BrowserView

from plone import api


class UrbanRedirectsView(BrowserView):
    """
      This manage the default redirection of urban view
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def __call__(self):
        user = api.user.get_current()
        sm = getSecurityManager()
        portal = api.portal.get()
        can_view = sm.checkPermission('View', getattr(portal, 'urban'))

        if can_view:
            self.context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/urban')
        else:
            user_groups = api.group.get_groups(user=user)
            group_ids = [g.id for g in user_groups]
            if 'survey_editors' in group_ids:
                self.context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/urban/survey_schedule')
            if 'opinions_editors' in group_ids:
                self.context.REQUEST.RESPONSE.redirect(portal.absolute_url() + '/urban/opinions_schedule')

        return self.index()
