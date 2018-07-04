# -*- coding: utf-8 -*-

from imio.history.browser.views import IHContentHistoryView


class HistoryView(IHContentHistoryView):
    histories_to_handle = (
        u'revision',
        u'workflow',
        u'update_rubrics',
        u'rubrics_history',
        u'update_additionalLegalConditions',
        u'additionalLegalConditions_history',
    )


class SpecificHistoryView(IHContentHistoryView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.histories_to_handle = (u'update_{0}'.format(self.request.get('item')),
                                    u'{0}_history'.format(self.request.get('item')))
