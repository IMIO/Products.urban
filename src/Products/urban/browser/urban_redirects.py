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

        redirects_adapter = queryAdapter(user, IUrbanRootRedirects)
        if redirects_adapter:
            path = redirects_adapter.get_redirection_path()

        if path is not None:
            return self.context.REQUEST.RESPONSE.redirect('{}/{}'.format(portal.absolute_url(), path))

        return self.index()
