# -*- coding: utf-8 -*-

from imio.history.browser.views import IHContentHistoryView
from plone import api


class SpecificHistoryView(IHContentHistoryView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.site_url = api.portal.get().absolute_url()
        fieldname = self.request.get("item", "")
        self.histories_to_handle = (
            u"update_{0}".format(fieldname),
            u"{0}_history".format(fieldname),
        )
