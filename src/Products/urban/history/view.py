# -*- coding: utf-8 -*-

from imio.history.browser.views import IHContentHistoryView


class HistoryView(IHContentHistoryView):
    histories_to_handle = (
        u'revision',
        u'workflow',
        u'update_rubrics',
        u'rubrics_history',
        u'update_additionalLegalCondition',
        u'additionalLegalConditions_history',
    )
