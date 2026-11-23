# -*- coding: utf-8 -*-
"""Required values validation of the SPW notices.

NoticeRequiredValues selects the schema of an event config from its licence
config and its notice event type; the schema are INoticeSchema adapters named
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
from Products.urban.interfaces import INoticeSchema
from Products.urban.interfaces import IProrogationEvent
from Products.urban.interfaces import IRefusedIncompletenessEvent
from Products.urban.interfaces import ITheLicenceEvent
from Products.urban.interfaces import ITransmitToSPWEvent
from Products.urban.interfaces import IWalloonRegionDecisionEvent
from Products.urban.utils import cache_key_5min
from plone.memoize import ram
from imio.urban.core.contents.eventconfig.content import IEventConfig
from imio.urban.core.interfaces import IRequiredValues
from plone import api
from z3c.form.interfaces import IData
from zope.component import adapter
from zope.component import queryAdapter
from zope.interface import implementer
from zope.interface import Interface
from imio.urban.core.schema_validation.schema import All
from imio.urban.core.schema_validation.schema import Any
from imio.urban.core.schema_validation.schema import Composite
from imio.urban.core.schema_validation.schema import MustBe

NOTICE_EVENT_TYPE_FIELD = "notice_event_type"

# notice types (SPW procedures) and the urban procedures they cover
NOTICE_TYPES = {
    "TLPE": ["CODT_Article127"],
    "ARNE": ["CODT_UniqueLicence", "EnvClassOne", "EnvClassTwo"],
}

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
# INVESTIGATION_START = {
#     "value": "investigationStart",
#     "label": _("urban_label_investigationStart"),
# }
# INVESTIGATION_END = {
#     "value": "investigationEnd",
#     "label": _("urban_label_investigationEnd"),
# }
CLAIMS_TEXT = {"value": "claimsText", "label": _("urban_label_claimsText")}
INQUIRY_REPORT = {"value": "reportText", "label": _("urban_label_reportText")}


def event_type_dict(interface):
    doc = (interface.__doc__ or "").strip()
    label = doc.splitlines()[0].strip() if doc else interface.__identifier__
    return {"value": interface.__identifier__, "label": _(label)}


@implementer(IRequiredValues)
@adapter(IEventConfig)
class NoticeRequiredValues(object):
    """Select the notice schema from the licence config and the notice event type.

    The schema are named INoticeSchema adapters on the licence config:
    '<notice type>.<notice event type>'.
    """

    def __init__(self, data):
        self.data = data

    @property
    def context(self):
        if not IData.providedBy(self.data):
            raise TypeError("Adapter must be call on a z3c.form.validator.Data")
        return getattr(self.data, "__context__", None)

    @property
    @ram.cache(cache_key_5min)
    def url(self):
        url = api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.url", default=None
        )
        if not url:
            return None
        return url

    @property
    @ram.cache(cache_key_5min)
    def instance_code(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id",
            default=None,
        )

    @property
    @ram.cache(cache_key_5min)
    def sent_on_behalf_of(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.sent_on_behalf_of_municipality_id",
            default=None,
        )

    def is_enabled(self):
        return "Manager" not in api.user.get_roles() and bool(
            self.url and self.instance_code and self.sent_on_behalf_of
        )

    @property
    def get_error_order(self):
        return ["eventPortalType", "activatedFields", "eventType"]

    def get_field_value(self, data, field_name):
        if isinstance(data, dict):
            return data.get(field_name)
        return getattr(data, field_name, None)

    def get_schema(self):
        event_type = self.get_field_value(self.data, NOTICE_EVENT_TYPE_FIELD)
        if not event_type or self.context is None:
            return None
        licence_config = self.get_licence_config()
        if licence_config is None:
            return None

        notice_type = self.get_notice_type(licence_config)
        if notice_type is None:
            return None

        name = u"{0}.{1}".format(notice_type, safe_unicode(event_type))
        schemas_provider = queryAdapter(licence_config, INoticeSchema, name=name)
        if schemas_provider is None:
            return None
        return schemas_provider()

    def get_licence_config(self):
        """First licence config found in the context acquisition chain."""
        for obj in aq_chain(aq_inner(self.context)):
            if ILicenceConfig.providedBy(obj):
                return obj
        return None

    def get_notice_type(self, licence_config):
        """Notice type covering the procedure of the licence config."""
        licence_type = licence_config.getId().lower()
        for notice_type, procedures in NOTICE_TYPES.items():
            if licence_type in [procedure.lower() for procedure in procedures]:
                return notice_type
        return None


# schemas


@implementer(INoticeSchema)
@adapter(ILicenceConfig)
class NoticeSchema(object):

    schema_class = None

    def __init__(self, context):
        self.context = context

    def schema(self):
        return self.schema_class

    def __call__(self):
        return self.schema()


# ARNE


class IARNEDepositSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IDepositEvent)])


class ARNEDepositSchema(NoticeSchema):
    schema_class = IARNEDepositSchema


class IARNESendFTSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT_NOTICE)
    eventType = All(constraint_values=[event_type_dict(ITransmitToSPWEvent)])


class ARNESendFTSchema(NoticeSchema):
    schema_class = IARNESendFTSchema


class IARNEInacceptableSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IRefusedIncompletenessEvent)])


class ARNEInacceptableSchema(NoticeSchema):
    schema_class = IARNEInacceptableSchema


class IARNEIncompleteSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IMissingPartEvent)])


class ARNEIncompleteSchema(NoticeSchema):
    schema_class = IARNEIncompleteSchema


class IARNECompleteFolderSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IAcknowledgmentEvent)])


class ARNECompleteFolderSchema(NoticeSchema):
    schema_class = IARNECompleteFolderSchema


class IARNEInquirySchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT_INQUIRY)
    activatedFields = All(
        constraint_values=[
            INQUIRY_REPORT,
            CLAIMS_TEXT,
            DISPLAY_DATE,
            DISPLAY_DATE_END,
            # INVESTIGATION_START, implicitly add with UrbanEventInquiry
            # INVESTIGATION_END, implicitly add with UrbanEventInquiry
        ]
    )
    eventType = All(
        constraint_values=[
            event_type_dict(IInquiryEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class ARNEInquirySchema(NoticeSchema):
    schema_class = IARNEInquirySchema


class IARNECollegePreliminaryOpinionSchema(Interface):
    eventPortalType = Any(constraint_values=[URBAN_EVENT_COLLEGE, URBAN_EVENT])
    eventType = All(
        constraint_values=[
            event_type_dict(ICollegeOpinionEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class ARNECollegePreliminaryOpinionSchema(NoticeSchema):
    schema_class = IARNECollegePreliminaryOpinionSchema


class IARNEProrogationSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IProrogationEvent)])


class ARNEProrogationSchema(NoticeSchema):
    schema_class = IARNEProrogationSchema


class IARNEFTOpinionSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IDecisionProjectFromSPWEvent)])


class ARNEFTOpinionSchema(NoticeSchema):
    schema_class = IARNEFTOpinionSchema


class IARNECollegeDecisionSchema(Interface):
    eventPortalType = Any(constraint_values=[URBAN_EVENT_COLLEGE, URBAN_EVENT])
    activatedFields = All(
        constraint_values=[
            DECISION_DATE,
            DECISION,
        ]
    )
    eventType = Composite(
        fields=[
            All(constraint_values=[event_type_dict(ITransmitToSPWEvent)]),
            Any(
                constraint_values=[
                    event_type_dict(ILicenceDeliveryEvent),
                    event_type_dict(ITheLicenceEvent),
                ]
            ),
        ]
    )


class ARNECollegeDecisionSchema(NoticeSchema):
    schema_class = IARNECollegeDecisionSchema


class IARNESPWDecisionSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    activatedFields = All(constraint_values=[DECISION])
    eventType = All(
        constraint_values=[
            event_type_dict(IWalloonRegionDecisionEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class ARNESPWDecisionSchema(NoticeSchema):
    schema_class = IARNESPWDecisionSchema


class IARNEDisplayCollegeDecisionSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    activatedFields = All(
        constraint_values=[
            DISPLAY_DATE,
            DISPLAY_DATE_END,
        ]
    )
    eventType = All(
        constraint_values=[
            event_type_dict(IDisplayingTheDecisionEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class ARNEDisplayCollegeDecisionSchema(NoticeSchema):
    schema_class = IARNEDisplayCollegeDecisionSchema


# TLPE


class ITLPECompleteFolderSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(constraint_values=[event_type_dict(IAcknowledgmentEvent)])


class TLPECompleteFolderSchema(NoticeSchema):
    schema_class = ITLPECompleteFolderSchema


class ITLPECompleteFolderModifiedPlanSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    eventType = All(
        constraint_values=[event_type_dict(IAmendedPlansAcknowledgmentEvent)]
    )


class TLPECompleteFolderModifiedPlanSchema(NoticeSchema):
    schema_class = ITLPECompleteFolderModifiedPlanSchema


class ITLPEInquirySchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT_INQUIRY)
    activatedFields = All(
        constraint_values=[
            INQUIRY_REPORT,
            CLAIMS_TEXT,
            DISPLAY_DATE,
            DISPLAY_DATE_END,
            # INVESTIGATION_START, implicitly add with UrbanEventInquiry
            # INVESTIGATION_END, implicitly add with UrbanEventInquiry
        ]
    )
    eventType = All(
        constraint_values=[
            event_type_dict(IInquiryEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class TLPEInquirySchema(NoticeSchema):
    schema_class = ITLPEInquirySchema


class ITLPEAnnouncementSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT_ANNOUNCEMENT)
    activatedFields = All(
        constraint_values=[
            INQUIRY_REPORT,
            CLAIMS_TEXT,
            DISPLAY_DATE,
            DISPLAY_DATE_END,
            # INVESTIGATION_START, implicitly add with UrbanEventAnnouncement
            # INVESTIGATION_END, implicitly add with UrbanEventAnnouncement
        ]
    )
    eventType = All(
        constraint_values=[
            event_type_dict(IAnnouncementEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class TLPEAnnouncementSchema(NoticeSchema):
    schema_class = ITLPEAnnouncementSchema


class ITLPECollegeOpinionSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT_COLLEGE)
    eventType = All(
        constraint_values=[
            event_type_dict(ICollegeOpinionEvent),
            event_type_dict(ITransmitToSPWEvent),
        ]
    )


class TLPECollegeOpinionSchema(NoticeSchema):
    schema_class = ITLPECollegeOpinionSchema


class ITLPESPWDecisionSchema(Interface):
    eventPortalType = MustBe(unique_value=URBAN_EVENT)
    activatedFields = All(constraint_values=[DECISION])
    eventType = All(constraint_values=[event_type_dict(IWalloonRegionDecisionEvent)])


class TLPESPWDecisionSchema(NoticeSchema):
    schema_class = ITLPESPWDecisionSchema
