# -*- coding: utf-8 -*-

from imio.history.browser.views import IHContentHistoryView


class SpecificHistoryView(IHContentHistoryView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        fieldname = self.request.get('item', '')
        self.histories_to_handle = (
            u'update_{0}'.format(fieldname),
            u'{0}_history'.format(fieldname),
        )
