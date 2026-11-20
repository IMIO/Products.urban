# -*- coding: utf-8 -*-
"""Required values validation of the SPW notices.

NoticeRequiredValues selects the rules of an event config from its licence
config and its notice event type; the rules are INoticeRules adapters named
'<notice type>.<notice event type>' (see configure.zcml).
"""
from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.CMFPlone.utils import safe_unicode
from Products.urban import UrbanMessage as _
from Products.urban.interfaces import IAcknowledgmentEvent
from Products.urban.interfaces import IAmendedPlansAcknowledgmentEvent
from Products.urban.interfaces import IAnnouncementEvent
from Products.urban.interfaces import ICollegeOpinionEvent
from Products.urban.interfaces import IDecisionProjectFromSPWEvent
from Products.urban.interfaces import IDepositEvent
from Products.urban.interfaces import IDisplayingTheDecisionEvent
from Products.urban.interfaces import IInquiryEvent
from Products.urban.interfaces import ILicenceConfig
from Products.urban.interfaces import ILicenceDeliveryEvent
from Products.urban.interfaces import IMissingPartEvent
from Products.urban.interfaces import INoticeRules
from Products.urban.interfaces import IProrogationEvent
from Products.urban.interfaces import IRefusedIncompletenessEvent
from Products.urban.interfaces import ITheLicenceEvent
from Products.urban.interfaces import ITransmitToSPWEvent
from Products.urban.interfaces import IWalloonRegionDecisionEvent
from imio.urban.core.contents.eventconfig.content import IEventConfig
from imio.urban.core.contents.utils import get_field_value
from imio.urban.core.interfaces import IRequiredValues
from plone import api
from zope.component import adapter
from zope.component import queryAdapter
from zope.interface import implementer


NOTICE_EVENT_TYPE_FIELD = "notice_event_type"

# notice types (SPW procedures) and the urban procedures they cover
NOTICE_TYPES = {
    "TLPE": ["CODT_Article127"],
    "ARNE": ["CODT_UniqueLicence", "EnvClassOne", "EnvClassTwo"],
}


@implementer(IRequiredValues)
@adapter(IEventConfig)
class NoticeRequiredValues(object):
    """Select the notice rules from the licence config and the notice event type.

    The rules are named INoticeRules adapters on the licence config:
    '<notice type>.<notice event type>'.
    """

    def __init__(self, context):
        self.context = context

    @property
    def url(self):
        url = api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.url", default=None
        )
        if not url:
            return False
        return url

    @property
    def instance_code(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id",
            default=None,
        )

    @property
    def sent_on_behalf_of(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.sent_on_behalf_of_municipality_id",
            default=None,
        )

    def is_enabled(self, data):
        return bool(self.url and self.instance_code and self.sent_on_behalf_of)

    def get_rules(self, data):
        event_type = get_field_value(data, NOTICE_EVENT_TYPE_FIELD)
        context = getattr(data, "__context__", None)
        if not event_type or context is None:
            return {}
        licence_config = get_licence_config(context)
        if licence_config is None:
            return {}

        notice_type = get_notice_type(licence_config)
        if notice_type is None:
            return {}

        name = u"{0}.{1}".format(notice_type, safe_unicode(event_type))
        rules = queryAdapter(licence_config, INoticeRules, name=name)
        if rules is None:
            return {}
        return rules()


def get_licence_config(context):
    """First licence config found in the context acquisition chain."""
    for obj in aq_chain(aq_inner(context)):
        if ILicenceConfig.providedBy(obj):
            return obj
    return None


def get_notice_type(licence_config):
    """Notice type covering the procedure of the licence config."""
    licence_type = licence_config.getId().lower()
    for notice_type, procedures in NOTICE_TYPES.items():
        if licence_type in [procedure.lower() for procedure in procedures]:
            return notice_type
    return None


# rules


def event_type(interface):
    return {"value": interface.__identifier__, "label": interface.__doc__}


URBAN_EVENT = {"value": "UrbanEvent", "label": PMF("UrbanEvent")}
URBAN_EVENT_INQUIRY = {"value": "UrbanEventInquiry", "label": PMF("UrbanEventInquiry")}
URBAN_EVENT_ANNOUNCEMENT = {
    "value": "UrbanEventAnnouncement",
    "label": PMF("UrbanEventAnnouncement"),
}
URBAN_EVENT_COLLEGE = {"value": "UrbanEventCollege", "label": PMF("UrbanEventCollege")}
URBAN_EVENT_NOTICE = {"value": "UrbanEventNotice", "label": PMF("UrbanEventNotice")}

DECISION_DATE = {"value": "decisionDate", "label": _("urban_label_decisionDate")}
DECISION = {"value": "decision", "label": _("urban_label_decision")}
DISPLAY_DATE = {"value": "displayDate", "label": _("urban_label_displayDate")}
DISPLAY_DATE_END = {"value": "displayDateEnd", "label": _("urban_label_displayDateEnd")}
INVESTIGATION_START = {
    "value": "investigationStart",
    "label": _("urban_label_investigationStart"),
}
INVESTIGATION_END = {
    "value": "investigationEnd",
    "label": _("urban_label_investigationEnd"),
}
CLAIMS_TEXT = {"value": "claimsText", "label": _("urban_label_claimsText")}
INQUIRY_REPORT = {"value": "reportText", "label": _("urban_label_reportText")}


@implementer(INoticeRules)
@adapter(ILicenceConfig)
class NoticeRules(object):

    rules = {}

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return self.rules


# ARNE


class ARNEDepositRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IDepositEvent),
            ],
        },
    }


class ARNESendFTRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT_NOTICE],
        },
        "eventType": {
            "all": [
                event_type(ITransmitToSPWEvent),
            ],
        },
    }


class ARNEInacceptableRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IRefusedIncompletenessEvent),
            ],
        },
    }


class ARNEIncompleteRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IMissingPartEvent),
            ],
        },
    }


class ARNECompleteFolderRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IAcknowledgmentEvent),
            ],
        },
    }


class ARNEInquiryRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT_INQUIRY],
        },
        "eventType": {
            "all": [
                event_type(IInquiryEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
        "activatedFields": {
            "all": [
                INQUIRY_REPORT,
                CLAIMS_TEXT,
                DISPLAY_DATE,
                DISPLAY_DATE_END,
                # INVESTIGATION_START, implicitly add with UrbanEventInquiry
                # INVESTIGATION_END, implicitly add with UrbanEventInquiry
            ],
        },
    }


class ARNECollegePreliminaryOpinionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "any": [
                [URBAN_EVENT_COLLEGE, URBAN_EVENT],
            ],
        },
        "eventType": {
            "all": [
                event_type(ICollegeOpinionEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
    }


class ARNEProrogationRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IProrogationEvent),
            ],
        },
    }


class ARNEFTOpinionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IDecisionProjectFromSPWEvent),
            ],
        },
    }


class ARNECollegeDecisionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "any": [
                [URBAN_EVENT_COLLEGE, URBAN_EVENT],
            ],
        },
        "eventType": {
            "all": [
                event_type(ITransmitToSPWEvent),
            ],
            "any": [
                [
                    event_type(ILicenceDeliveryEvent),
                    event_type(ITheLicenceEvent),
                ],
            ],
        },
        "activatedFields": {
            "all": [
                DECISION_DATE,
                DECISION,
            ],
        },
    }


class ARNESPWDecisionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IWalloonRegionDecisionEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
        "activatedFields": {
            "all": [
                DECISION,
            ],
        },
    }


class ARNEDisplayCollegeDecisionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IDisplayingTheDecisionEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
        "activatedFields": {
            "all": [
                DISPLAY_DATE,
                DISPLAY_DATE_END,
            ],
        },
    }


# TLPE


class TLPECompleteFolderRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IAcknowledgmentEvent),
            ],
        },
    }


class TLPECompleteFolderModifiedPlanRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IAmendedPlansAcknowledgmentEvent),
            ],
        },
    }


class TLPEInquiryRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT_INQUIRY],
        },
        "eventType": {
            "all": [
                event_type(IInquiryEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
        "activatedFields": {
            "all": [
                INQUIRY_REPORT,
                CLAIMS_TEXT,
                DISPLAY_DATE,
                DISPLAY_DATE_END,
                # INVESTIGATION_START, implicitly add with UrbanEventInquiry
                # INVESTIGATION_END, implicitly add with UrbanEventInquiry
            ],
        },
    }


class TLPEAnnouncementRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT_ANNOUNCEMENT],
        },
        "eventType": {
            "all": [
                event_type(IAnnouncementEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
        "activatedFields": {
            "all": [
                INQUIRY_REPORT,
                CLAIMS_TEXT,
                DISPLAY_DATE,
                DISPLAY_DATE_END,
                # INVESTIGATION_START, implicitly add with UrbanEventAnnouncement
                # INVESTIGATION_END, implicitly add with UrbanEventAnnouncement
            ],
        },
    }


class TLPECollegeOpinionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT_COLLEGE],
        },
        "eventType": {
            "all": [
                event_type(ICollegeOpinionEvent),
                event_type(ITransmitToSPWEvent),
            ],
        },
    }


class TLPESPWDecisionRules(NoticeRules):
    rules = {
        "eventPortalType": {
            "all": [URBAN_EVENT],
        },
        "eventType": {
            "all": [
                event_type(IWalloonRegionDecisionEvent),
            ],
        },
        "activatedFields": {
            "all": [
                DECISION,
            ],
        },
    }
