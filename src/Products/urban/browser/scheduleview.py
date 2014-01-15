# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner
#from Products.urban.browser.urbantable import ScheduleTable


class ScheduleView(BrowserView):
    """
      This manages urban schedule view
    """
    def __init__(self, context, request):
        super(ScheduleView, self).__init__(context, request)
        self.context = context
        self.request = request
