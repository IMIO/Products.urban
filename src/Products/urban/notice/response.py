# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.urban.interfaces import ICollegeOpinionEvent
from Products.urban.interfaces import IInquiryEvent
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

    def notice_id(self, notification_type):
        """Notification ID from event parent"""
        return self._licence.get_notice_id(notification_type)

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


class NoticeOutgoingPublicSurveyNotification(NoticeResponse):
    def __init__(self, event):
        super(NoticeOutgoingPublicSurveyNotification, self).__init__(event)
        self._inquiry_event = self._licence.getLastEvent(IInquiryEvent)
        self._college_opinion_event = self._licence.getLastEvent(ICollegeOpinionEvent)

    type = "PublicSurveyResponse"

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def state(self):
        raise NotImplementedError

    @property
    def _minute(self):
        return self._inquiry_event.getReportText() if self._inquiry_event else None

    @property
    def _observations(self):
        return self._inquiry_event.getClaimsText() if self._inquiry_event else None

    @property
    def _notice_college(self):
        return "<p>TEST DATA FOR tns:noticeCollege</p><p><b>BOLD TEXT</b></p>"  # TODO: compose from DELIB data

    @property
    def _display_start_date(self):
        return self._inquiry_event.getDisplayDate() if self._inquiry_event else None

    @property
    def _display_end_date(self):
        return self._inquiry_event.getDisplayDateEnd() if self._inquiry_event else None

    @property
    def _organisation_start_date(self):
        return self._inquiry_event.getInvestigationStart() if self._inquiry_event else None

    @property
    def _organisation_end_date(self):
        return self._inquiry_event.getInvestigationEnd() if self._inquiry_event else None

    @property
    def _suspension_start_date(self):
        return None

    @property
    def _suspension_end_date(self):
        return None

    @property
    def specific(self):
        return {
            "tns:municipalityReference": self._reference,
            "tns:minute": self._minute,
            "tns:observations": self._observations,
            "tns:noticeCollege": self._notice_college,
            "tns:displayStartDate": self._display_start_date,
            "tns:displayEndDate": self._display_end_date,
            "tns:organisationStartDate": self._organisation_start_date,
            "tns:organisationEndDate": self._organisation_end_date,
            "tns:suspensionStartDate": self._suspension_start_date,
            "tns:suspensionEndDate": self._suspension_end_date,
        }


class NoticeOutgoingPublicSurveyDatesNotification(NoticeOutgoingPublicSurveyNotification):
    state = "PARTIAL"


class NoticeOutgoingPublicSurveyPVNotification(NoticeOutgoingPublicSurveyNotification):
    state = "PARTIAL"


class NoticeOutgoingPublicSurveyOpinionNotification(NoticeOutgoingPublicSurveyNotification):
    state = "FINAL"


class NoticeOutgoingPublicSurveyFinalWithoutOpinionNotification(NoticeOutgoingPublicSurveyNotification):
    state = "FINAL"

    @property
    def _notice_college(self):
        return None

