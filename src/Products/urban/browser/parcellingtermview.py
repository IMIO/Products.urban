# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class ParcellingTermView(BrowserView):
    """
      This manage methods of ParcellingTerm view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
