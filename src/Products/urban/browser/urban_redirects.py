# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager

from Products.Five import BrowserView

from Products.urban.interfaces import IUrbanRootRedirects

from plone import api

from zope.component import queryAdapter


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

        path = None

        if can_view:
            path = 'urban'

        if user.getId() is not None:
            user_groups = api.group.get_groups(user=user)
            group_ids = [g.id for g in user_groups]
            if 'opinions_editors' in group_ids:
                path = 'urban/opinions_schedule'

        redirects_adapter = queryAdapter(user, IUrbanRootRedirects)
        if redirects_adapter:
            path = redirects_adapter.get_redirection_path()

        if path is not None:
            return self.context.REQUEST.RESPONSE.redirect('{}/{}'.format(portal.absolute_url(), path))

        return self.index()
