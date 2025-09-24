# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.urban.notice.base import NoticeElement


class NoticeResponse(NoticeElement):
    _excluded_keys = (
        "notice_id",
        "event",
    )

    def __init__(self, event):
        self.event = event

    @property
    def _licence(self):
        return aq_parent(self.event)

    @property
    def notice_id(self):
        """Notification ID from event parent"""
        return self._licence.noticeId

    @property
    def type(self):
        """Response type"""
        raise NotImplementedError

    @property
    def state(self):
        """Response state (PARTIAL or FINAL)"""
        raise NotImplementedError

    @property
    def specific(self):
        """Response specific data"""
        raise NotImplementedError


class NoticeOutgoingNotification(NoticeResponse):
    state = "FINAL"
    type = "TwiceDefaultResponse"

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def specific(self):
        return {
            "tns:municipalityReference": self._reference,
        }

class NoticeOutgoingSummaryReportNotification(NoticeResponse):
    state = "FINAL"
    type = "SummaryReportResponse"

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def specific(self):
        return {
            "tns:municipalityReference": self._reference,
            "tns:caracteristicsComment":,
            "tns:decisionDate": self._display_decision_date,
            "tns:displayDecisionStartDate": self._decision,
            "tns:displayDecisionEndDate"
            
        }
        
    @property
    def _display_decision_date(self):
        return self.event.getDisplayDate()
    #return self._licence.getDecisionDate()
    @property
    def _decision(self):
        return self.event.getDecision()