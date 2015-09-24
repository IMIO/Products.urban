# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager

from Products.Five import BrowserView

from plone import api


class UrbanView(BrowserView):
    """
      This manage the view of urban
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request


class MayAccessUrban(BrowserView):
    """
    This view is is used in the python expresssion to evaluate
    the display of 'portal_tabs' actions (see profiles/default/actions.xml)
    """

    def __call__(self):
        """ Test if the current user can acess urban view."""
        portal = api.portal.get()
        sm = getSecurityManager()
        may_access = sm.checkPermission('View', getattr(portal, 'urban'))
        return may_access
