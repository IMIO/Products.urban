# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class LicenceEditView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(LicenceEditView, self).__init__(context, request)
        self.context = context
        self.request = request
