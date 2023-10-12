# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement
from Acquisition import aq_parent


class NoticeResponse(NoticeElement):
    _excluded_keys = ("notice_id",)

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
