## -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner

from Products.urban.interfaces import ITheLicenceEvent, ICommunalCouncilEvent


class PMWSClientView(BrowserView):
    """adpats an urban event to provides all the methodis needed by pm.wsclient"""

    def __init__(self, context, request):
        super(PMWSClientView, self).__init__(context, request)
        self.context = context
        self.request = request

    def isDecisionCollegeEvent(self):
        context = aq_inner(self.context)
        return ITheLicenceEvent.providedBy(context)

    def isCollegeCouncilEvent(self):
        context = aq_inner(self.context)
        return ICommunalCouncilEvent.providedBy(context)
