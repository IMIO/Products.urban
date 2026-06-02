# -*- coding: utf-8 -*-

import base64

from Acquisition import aq_parent
from Products.urban.interfaces import IInquiryEvent
from Products.urban.interfaces import ITheLicenceEvent
from Products.urban.notice.base import NoticeElement
from plone import api


def clean_accents(raw_string):
    return raw_string.decode("utf8").encode("ascii", "xmlcharrefreplace")


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


class NoticeOutgoingFileNotification(NoticeElement):
    def __init__(self, file_path):
        self._file = api.content.get(path=file_path)

    @property
    def file(self):
        return {
            "name": self._file.id,
            "mime": self._file.content_type,
            "content": base64.encodestring(self._file.data),
        }

    @property
    def type(self):
        return {
            "code": "PIECE_JOINTE_URBAN",
            "label": u"Pièce jointe venant d'iA.Urban",
        }

    @property
    def language(self):
        return "FR"

    @property
    def description(self):
        return self._file.title

# TWICE

class NoticeOutgoingNotification(NoticeResponse):
    state = "FINAL"
    type = "tns:TwiceDefaultResponse"

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def specific(self):
        return {
            "tns:municipalityReference": self._reference,
        }


class NoticeOutgoingPublicSurveyNotification(NoticeResponse):
    def __init__(self, event, inquiry_event=None, college_opinion=None):
        super(NoticeOutgoingPublicSurveyNotification, self).__init__(event)
        self._inquiry_event = inquiry_event
        self._college_opinion = college_opinion

    type = "tns:PublicSurveyResponse"

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def state(self):
        raise NotImplementedError

    @property
    def _minute(self):
        return (
            clean_accents(self._inquiry_event.getReportText())
            if self._inquiry_event
            else None
        )

    @property
    def _observations(self):
        return (
            clean_accents(self._inquiry_event.getClaimsText())
            if self._inquiry_event
            else None
        )

    @property
    def _notice_college(self):
        return self._college_opinion

    @property
    def _display_start_date(self):
        return self._inquiry_event.getDisplayDate() if self._inquiry_event else None

    @property
    def _display_end_date(self):
        return self._inquiry_event.getDisplayDateEnd() if self._inquiry_event else None

    @property
    def _organisation_start_date(self):
        return (
            self._inquiry_event.getInvestigationStart() if self._inquiry_event else None
        )

    @property
    def _organisation_end_date(self):
        return (
            self._inquiry_event.getInvestigationEnd() if self._inquiry_event else None
        )

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


class NoticeOutgoingPublicSurveyDatesNotification(
    NoticeOutgoingPublicSurveyNotification
):
    state = "PARTIAL"

    def __init__(self, event):
        super(NoticeOutgoingPublicSurveyDatesNotification, self).__init__(
            event, inquiry_event=event
        )


class NoticeOutgoingPublicSurveyPVNotification(NoticeOutgoingPublicSurveyNotification):
    state = "PARTIAL"

    def __init__(self, event):
        super(NoticeOutgoingPublicSurveyPVNotification, self).__init__(
            event, inquiry_event=event
        )


class NoticeOutgoingPublicSurveyOpinionNotification(
    NoticeOutgoingPublicSurveyNotification
):
    state = "FINAL"

    def __init__(self, event, inquiry_event, college_opinion):
        super(NoticeOutgoingPublicSurveyOpinionNotification, self).__init__(
            event, inquiry_event=inquiry_event, college_opinion=college_opinion
        )


class NoticeOutgoingPublicSurveyFinalWithoutOpinionNotification(
    NoticeOutgoingPublicSurveyNotification
):
    state = "FINAL"

    def __init__(self, event):
        super(NoticeOutgoingPublicSurveyFinalWithoutOpinionNotification, self).__init__(
            event, inquiry_event=event
        )


class NoticeOutgoingSummaryReportNotification(NoticeResponse):

    def __init__(self, event, decision_event=None, decision_display_event=None, college_decision=None):
        super(NoticeOutgoingSummaryReportNotification, self).__init__(event)
        self._decision_event = decision_event
        self._decision_display_event = decision_display_event
        self._college_decision = college_decision

    type = "tns:SummaryReportResponse"

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def _display_decision_start_date(self):
        return self._decision_display_event.getDisplayDate() if self._decision_display_event else None

    @property
    def _display_decision_end_date(self):
        return self._decision_display_event.getDisplayDateEnd() if self._decision_display_event else None

    @property
    def _decision_code(self):
        if self._decision_event:
            decision_codes = {
                "favorable": "OCTROI",
                "defavorable": "REFUS",
                "octroi": "OCTROI",
                "refus": "REFUS",
            }
            return {"cod:code": decision_codes.get(self._decision_event.getDecision())}
        else:
            return None

    @property
    def _motivation(self):
        return self._college_decision

    @property
    def _decision_date(self):
        return self._decision_event.getDecisionDate()

    @property
    def specific(self):
        return {
            "not:notice": self._decision_code,
            "not:motivation": self._motivation,
            "tns:municipalityReference": self._reference,
            "tns:decisionDate": self._decision_date,
            "tns:displayDecisionStartDate": self._display_decision_start_date,
            "tns:displayDecisionEndDate": self._display_decision_end_date,
        }


class NoticeOutgoingSummaryReportDecisionNotification(
    NoticeOutgoingSummaryReportNotification
):
    state = "PARTIAL"

    def __init__(self, event, college_decision=None):
        super(NoticeOutgoingSummaryReportDecisionNotification, self).__init__(
            event, decision_event=event, college_decision=college_decision
        )


class NoticeOutgoingSummaryReportDatesNotification(
    NoticeOutgoingSummaryReportNotification
):
    def __init__(self, event, decision_event=None, college_decision=None):
        super(NoticeOutgoingSummaryReportDatesNotification, self).__init__(
            event,
            decision_event=decision_event,
            decision_display_event=event,
            college_decision=college_decision,
        )

    state = "FINAL"


class NoticeOutgoingDecisionNotification(NoticeResponse):

    type = "tns:DecisionResponse"
    state = "FINAL"

    @property
    def _motivation(self):
        return None

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def _decision_date(self):
        return None

    @property
    def _display_decision_start_date(self):
        return self.event.getDisplayDate()

    @property
    def _display_decision_end_date(self):
        return self.event.getDisplayDateEnd()

    @property
    def specific(self):
        return {
            "not:motivation": self._motivation,
            "tns:municipalityReference": self._reference,
            "tns:decisionDate": self._decision_date,
            "tns:displayDecisionStartDate": self._display_decision_start_date,
            "tns:displayDecisionEndDate": self._display_decision_end_date,
        }


# GESPER

class NoticeOutgoingGesperPublicSurveyNotification(NoticeResponse):

    type = "gns:GesperPublicSurveyResponse"

    def __init__(self, event, inquiry_event=None, college_opinion=None):
        super(NoticeOutgoingGesperPublicSurveyNotification, self).__init__(event)
        self._inquiry_event = inquiry_event
        self._college_opinion = college_opinion

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def state(self):
        raise NotImplementedError

    @property
    def _minute(self):
        return (
            clean_accents(self._inquiry_event.getReportText())
            if self._inquiry_event
            else None
        )

    @property
    def _observations(self):
        return (
            clean_accents(self._inquiry_event.getClaimsText())
            if self._inquiry_event
            else None
        )

    @property
    def _notice_college(self):
        return self._college_opinion

    @property
    def _display_start_date(self):
        return self._inquiry_event.getDisplayDate() if self._inquiry_event else None

    @property
    def _display_end_date(self):
        return self._inquiry_event.getDisplayDateEnd() if self._inquiry_event else None

    @property
    def _organisation_start_date(self):
        return (
            self._inquiry_event.getInvestigationStart() if self._inquiry_event else None
        )

    @property
    def _organisation_end_date(self):
        return (
            self._inquiry_event.getInvestigationEnd() if self._inquiry_event else None
        )

    @property
    def _suspension_start_date(self):
        return None

    @property
    def _suspension_end_date(self):
        return None

    @property
    def specific(self):
        return {
            "gns:iaReference": self._reference,
            "gns:minute": self._minute,
            "gns:observations": self._observations,
            "gns:noticeCollege": self._notice_college,
            "gns:displayStartDate": self._display_start_date,
            "gns:displayEndDate": self._display_end_date,
            "gns:organisationStartDate": self._organisation_start_date,
            "gns:organisationEndDate": self._organisation_end_date,
            "gns:suspensionStartDate": self._suspension_start_date,
            "gns:suspensionEndDate": self._suspension_end_date,
        }


class NoticeOutgoingGesperPublicSurveyDatesNotification(
    NoticeOutgoingGesperPublicSurveyNotification
):
    def __init__(self, event):
        super(NoticeOutgoingGesperPublicSurveyDatesNotification, self).__init__(
            event, inquiry_event=event
        )

    state = "PARTIAL"


class NoticeOutgoingGesperPublicSurveyPVNotification(
    NoticeOutgoingGesperPublicSurveyNotification
):
    state = "PARTIAL"

    def __init__(self, event):
        super(NoticeOutgoingGesperPublicSurveyPVNotification, self).__init__(
            event, inquiry_event=event
        )


class NoticeOutgoingGesperPublicSurveyOpinionNotification(
    NoticeOutgoingGesperPublicSurveyNotification
):
    state = "FINAL"

    def __init__(self, event, inquiry_event, college_opinion):
        super(NoticeOutgoingGesperPublicSurveyOpinionNotification, self).__init__(
            event, inquiry_event=inquiry_event, college_opinion=college_opinion
        )


class NoticeOutgoingGesperPublicSurveyFinalWithoutOpinionNotification(
    NoticeOutgoingGesperPublicSurveyNotification
):
    state = "FINAL"

    def __init__(self, event):
        super(
            NoticeOutgoingGesperPublicSurveyFinalWithoutOpinionNotification, self
        ).__init__(event, inquiry_event=event)


class NoticeOutgoingGesperProjectAnnouncementDatesNotification(
    NoticeOutgoingGesperPublicSurveyDatesNotification
):
    type = "gns:GesperProjectAnnouncementResponse"


class NoticeOutgoingGesperProjectAnnouncementPVNotification(
    NoticeOutgoingGesperPublicSurveyPVNotification
):
    type = "gns:GesperProjectAnnouncementResponse"


class NoticeOutgoingGesperProjectAnnouncementOpinionNotification(
    NoticeOutgoingGesperPublicSurveyOpinionNotification
):
    type = "gns:GesperProjectAnnouncementResponse"


class NoticeOutgoingGesperProjectAnnouncementFinalWithoutOpinionNotification(
    NoticeOutgoingGesperPublicSurveyFinalWithoutOpinionNotification
):
    type = "gns:GesperProjectAnnouncementResponse"


class NoticeOutgoingGesperOpinionRequestNotification(NoticeResponse):
    type = "gns:GesperLicenceNoticeResponse"
    state = "FINAL"

    def __init__(self, event, college_motivation=None):
        super(
            NoticeOutgoingGesperOpinionRequestNotification, self
        ).__init__(event)
        self._college_motivation = college_motivation

    @property
    def _reference(self):
        return self._licence.getReference()

    @property
    def _opinion_code(self):
        opinion_codes = {
            "favorable": "FAVORABLE",
            "defavorable": "DEFAVORABLE",
            "favorable-cond": "FAVORABLE_CONDITIONNEL",
        }
        return {"cod:code": opinion_codes.get(self.event.getCollegeOpinion())}

    @property
    def _blocks(self):
        return None

    @property
    def _special_conditions(self):
        return None

    @property
    def specific(self):
        return {
            "not:notice": self._opinion_code,
            "not:motivation": self._college_motivation,
            "gns:iaReference": self._reference,
            "gns:blocks": self._blocks,
            "gns:specialConditions": self._special_conditions,
        }
