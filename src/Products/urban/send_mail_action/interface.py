# -*- coding: utf-8 -*-

from zope.interface import Interface


class ISendMailAction(Interface):
    """Interface for event to send inquiry mail"""


class IRedirect(Interface):
    """ """

    def redirect():
        """
        Redirect to the right place in case we use plone.app.jquerytools overlays
        """
