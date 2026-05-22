# -*- coding: utf-8 -*-
from datetime import datetime
from z3c.form import button
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.form import Form
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from Products.urban.notice.exceptions import NoMatchingEventFoundException
from Products.urban.notice.exceptions import NoPreviousEventFoundException
from Products.urban.notice.response import clean_accents
from Products.urban.utils import get_ws_meetingitem_infos
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.z3cform.layout import wrap_form


def possible_outgoing_notice_notifications(licence):
    result = []
    all_incomings = []
    all_outgoings = []

    all_licence_events = sorted(
        licence.getAllEvents(), key=lambda e: e.created(), reverse=True
    )
    for event in all_licence_events:
        annotations = IAnnotations(event)
        key = "notice_notification"
        notice = annotations.get(key, {})
        incoming = notice.get("incoming", {})
        if incoming:
            all_incomings.append((event, incoming))
        outgoings = notice.get("outgoing", [])
        all_outgoings.extend(outgoings)

    for event, incoming in all_incomings:
        linked_outgoings = [
            outgoing
            for outgoing in all_outgoings
            if outgoing["incoming_notice_id"] == incoming["notice_id"]
        ]

        incoming_already_final = any(
            [outgoing["partial_or_final"] == "FINAL" for outgoing in linked_outgoings]
        )

        linked_outgoing_notice_types = [
            outgoing["outgoing_notice_type"] for outgoing in linked_outgoings
        ]

        if not incoming_already_final:
            result.append(
                {
                    "incoming_notice_id": incoming["notice_id"],
                    "incoming_notice_type": incoming["notice_type"],
                    "incoming_event": event,
                    "linked_outgoing_notice_types": linked_outgoing_notice_types,
                }
            )

    return result


@implementer(IContextSourceBinder)
class OpenIncomingNotifications(object):
    def __init__(self, accepted_incoming_types, avoided_outgoing_notice_types=None):
        self.accepted_incoming_types = accepted_incoming_types
        self.avoided_outgoing_notice_types = (
            []
            if avoided_outgoing_notice_types is None
            else avoided_outgoing_notice_types
        )

    def __call__(self, context):
        terms = []
        licence = context.aq_parent
        possible_notifs = possible_outgoing_notice_notifications(licence)
        for possible_notif in possible_notifs:
            # remove those not concerning our incoming type
            if (
                self.accepted_incoming_types
                and possible_notif["incoming_notice_type"]
                not in self.accepted_incoming_types
            ):
                continue

            # remove those where the concerned outgoings already exist
            if self.avoided_outgoing_notice_types and set(
                self.avoided_outgoing_notice_types
            ).intersection(possible_notif["linked_outgoing_notice_types"]):
                continue

            incoming_id = possible_notif["incoming_notice_id"]
            incoming_notice_type = possible_notif["incoming_notice_type"]
            incoming_event = possible_notif["incoming_event"]
            description = u"{} - {} - {}".format(
                incoming_event.title,
                incoming_event.getFormattedDate().decode("utf8"),
                translate(incoming_notice_type, "urban", context=context.REQUEST),
            )
            terms.append(
                SimpleVocabulary.createTerm(
                    unicode(incoming_id), str(incoming_id), description
                )
            )
        return SimpleVocabulary(terms)


class ITransferBaseActionForm(Interface):
    file_paths = schema.List(
        title=_(u"Licence Files"),
        description=_(
            u"Select files from this event or the parent licence you want to send (PDF, XLSX or PNG)."
        ),
        required=False,
        value_type=schema.Choice(
            vocabulary="urban.vocabularies.valid_notice_licence_documents"
        ),
    )


class NoticeResponseActionForm(Form):
    ignoreContext = True

    success_message = None

    def _get_incoming_type(self, incoming_id):
        licence = self.context.aq_parent
        for event in licence.getAllEvents():
            annotations = IAnnotations(event)
            key = "notice_notification"
            notice = annotations.get(key, {})
            incoming = notice.get("incoming", [])
            if incoming.get("notice_id") == incoming_id:
                return incoming.get("notice_type")
        return None

    def _fetch_iadelib_opinion(self, field_to_fill):
        motivation = self._get_iadelib_field(self.context, "motivation") or ""
        decision = self._get_iadelib_field(self.context, "decision") or ""
        if motivation or decision:
            full_text = (
                "<h1>Motivation:</h1>\r\n{}\r\n<h1>Décision:</h1>\r\n{}\r\n".format(
                    motivation, decision
                )
            )
            full_text = clean_accents(full_text)
            self.widgets[field_to_fill].value = RichTextValue(
                full_text,
                "text/html",
                "text/html",
            )

    def _get_iadelib_field(self, event, field_name):
        linked_item = get_ws_meetingitem_infos(
            event,
            query_hook=lambda q: q.update({"metadata_fields": field_name}),
            first=True,
        )
        if linked_item and field_name in linked_item:
            field = linked_item[field_name]
            return field.get("data", "") if isinstance(field, dict) else field

    def transfer_response(self, data):
        raise NotImplementedError()

    def store_sent_data(
        self,
        incoming_notice_id,
        reception_date=None,
        field_values=None,
    ):
        self.context.store_outgoing_notice(
            incoming_notice_id,
            self.action_code,
            self.partial_or_final,
            reception_date if reception_date else datetime.now(),
            api.user.get_current().id,
            field_values,
        )

    def updateWidgets(self):
        super(NoticeResponseActionForm, self).updateWidgets()

        # disable portlets
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)

        self.widgets["file_paths"].value = []

    @button.buttonAndHandler(_("Send"), name="send_response")
    def handleSendResponse(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        incoming_notice_id = data["incoming_notification"]

        self.field_values_to_store = {}
        response_result = self.transfer_response(data)
        if type(response_result) == dict and response_result.get("error") is True:
            IStatusMessage(self.request).addStatusMessage(
                response_result.get("message"), "error"
            )
            return
        else:
            IStatusMessage(self.request).addStatusMessage(self.success_message, "info")

        file_paths = data.get("file_paths", [])
        for file_path in file_paths:
            file_obj = api.content.get(path=file_path)
            if not file_obj:
                IStatusMessage(self.request).addStatusMessage(
                    _("One file is not available anymore, and couldn't be sent."),
                    "error",
                )
                continue
            document_title = file_obj.Title().decode("utf8")
            sent_documents = self.field_values_to_store.get("documents", [])
            sent_documents.append(
                {
                    "path": file_path,
                    "title": document_title,
                }
            )
            self.field_values_to_store["documents"] = sent_documents

            file_result = self.context.transfer_notice_file(incoming_notice_id, file_path)

        reception_date_str = response_result["body"]["result"]["receptionDate"]
        reception_date = datetime.strptime(reception_date_str[:19], "%Y-%m-%dT%H:%M:%S")

        self.store_sent_data(
            incoming_notice_id,
            reception_date=reception_date,
            field_values=self.field_values_to_store,
        )

        self.request.response.redirect(self.context.absolute_url())


class ITransferFolderToDPAActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "TRANSFERT_DOSSIER",
            ],
            ["transfer_folder_to_dpa"]
        ),
    )


class TransferFolderToDPAActionForm(NoticeResponseActionForm):
    label = _("Transfer folder to DPA")
    fields = field.Fields(ITransferFolderToDPAActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_folder_to_dpa"
    partial_or_final = "FINAL"
    success_message = _(u"The folder transfer to DPA is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        result = self.context.transfer_folder_to_dpa(incoming_id)
        return result


TransferFolderToDPAActionWrapper = wrap_form(TransferFolderToDPAActionForm)


class ITransferDatesTicketActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_EP",
                "DEMANDE_EP_DOSSIER_PRECEDENT",
                "DEMANDE_EP_EXTRA",
            ],
            ["transfer_dates"]
        ),
    )


class TransferDatesActionForm(NoticeResponseActionForm):
    label = _("Transfer dates to the SPW")
    fields = field.Fields(ITransferDatesTicketActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_dates"
    partial_or_final = "PARTIAL"
    success_message = _(u"The transfer of dates is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        result = self.context.transfer_dates(incoming_id)
        return result


TransferDatesActionWrapper = wrap_form(TransferDatesActionForm)


class ITransferTicketActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_EP",
                "DEMANDE_EP_DOSSIER_PRECEDENT",
                "DEMANDE_EP_EXTRA",
            ],
            ["transfer_ticket", "transfer_ticket_final"]
        ),
    )

    partial_or_final = schema.Choice(
        title=_(u"Preliminary Opinion"),
        description=_(u"This action cannot be reversed."),
        required=True,
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    value=u"PARTIAL", title=_(u"I will create a college opinion")
                ),
                SimpleTerm(
                    value=u"FINAL",
                    title=_(
                        u"I will not send a college opinion and I am finalizing the response to the SPW now"
                    ),
                ),
            ]
        ),
    )


class TransferTicketActionForm(NoticeResponseActionForm):
    label = _("Transfer ticket to the SPW")
    fields = field.Fields(ITransferTicketActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    fields["partial_or_final"].widgetFactory = RadioFieldWidget
    action_code = (
        None  # will be set in self.transfer_response, before it's actually needed
    )
    success_message = _(u"The ticket transfer is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        self.partial_or_final = data.get("partial_or_final")
        if self.partial_or_final == "PARTIAL":
            self.action_code = "transfer_ticket"
            return self.context.transfer_ticket(incoming_id)
        if self.partial_or_final == "FINAL":
            self.action_code = "transfer_ticket_final"
            return self.context.finalize_inquiry_without_opinion(incoming_id)


TransferTicketActionWrapper = wrap_form(TransferTicketActionForm)


class ITransferOpinionActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_EP",
                "DEMANDE_EP_DOSSIER_PRECEDENT",
                "DEMANDE_EP_EXTRA",
            ],
            ["transfer_opinion", "transfer_ticket_final"]
        ),
    )

    college_opinion = RichText(
        title=_(u"College opinion"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferOpinionActionForm(NoticeResponseActionForm):
    label = _("Transfer opinion to the SPW")
    fields = field.Fields(ITransferOpinionActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_opinion"
    partial_or_final = "FINAL"
    success_message = _(u"The opinion transfer is done.")

    def _get_inquiry_event(self, incoming_id):
        licence = self.context.aq_parent
        all_licence_events = sorted(
            licence.getAllEvents(), key=lambda e: e.created(), reverse=True
        )
        for event in all_licence_events:
            if event.portal_type != "UrbanEventInquiry":
                continue
            annotations = IAnnotations(event)
            key = "notice_notification"
            notice = annotations.get(key, {})
            outgoings = notice.get("outgoing", [])
            for outgoing in outgoings:
                matching_notice_id = outgoing["incoming_notice_id"] == incoming_id
                matching_action_code = outgoing["outgoing_notice_type"] in (
                    "transfer_dates",
                    "transfer_ticket",
                )
                if matching_notice_id and matching_action_code:
                    return event

        raise NoMatchingEventFoundException("Inquiry")

    def _get_college_opinion_text(self, data):
        college_opinion = data.get("college_opinion", "")
        output = college_opinion.output if college_opinion else ""
        self.field_values_to_store["college_opinion"] = output
        return output

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        inquiry_event = self._get_inquiry_event(incoming_id)
        college_opinion = self._get_college_opinion_text(data)
        result = self.context.transfer_opinion(incoming_id, inquiry_event, college_opinion)
        return result

    def updateWidgets(self):
        super(TransferOpinionActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_opinion")


TransferOpinionActionWrapper = wrap_form(TransferOpinionActionForm)


class ITransferDecisionActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "NOTIFICATION_RS_COMMUNE",
                "NOTIFICATION_RS_COMMUNE_RETARD",
                "NOTIFICATION_RS_COMMUNE_RETARD_SFD",
                "NOTIFICATION_PAS_ENVOI_RS",
                "NOTIFICATION_PAS_ENVOI_RS_SFD",
            ],
            ["transfer_decision"]
        ),
    )

    college_decision = RichText(
        title=_(u"College decision"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferDecisionActionForm(NoticeResponseActionForm):
    label = _("Transfer decision to the SPW")
    fields = field.Fields(ITransferDecisionActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_decision"
    partial_or_final = "PARTIAL"
    success_message = _(u"The decision transfer is done.")

    def _get_college_decision_text(self, data):
        college_decision = data.get("college_decision", "")
        output = college_decision.output if college_decision else ""
        self.field_values_to_store["college_decision"] = output
        return output

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        college_decision = self._get_college_decision_text(data)
        result = self.context.transfer_decision(incoming_id, college_decision)
        return result

    def updateWidgets(self):
        super(TransferDecisionActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_decision")


TransferDecisionActionWrapper = wrap_form(TransferDecisionActionForm)


class ITransferDecisionDisplayActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "NOTIFICATION_RS_COMMUNE",
                "NOTIFICATION_RS_COMMUNE_RETARD",
                "NOTIFICATION_RS_COMMUNE_RETARD_SFD",
                "NOTIFICATION_PAS_ENVOI_RS",
                "NOTIFICATION_PAS_ENVOI_RS_SFD",
                "NOTIFICATION_DECISION_COMMUNE",
                "NOTIFICATION_DEC_RS_COMMUNE",
                "NOTIFICATION_DECRS_REFUS_TACITE_COMMUNE",
            ],
            ["transfer_decision_display"]
        ),
    )


class TransferDecisionDisplayActionForm(NoticeResponseActionForm):
    label = _(u"Transfer decision display to the SPW")
    fields = field.Fields(ITransferDecisionDisplayActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_decision_display"
    partial_or_final = "FINAL"
    success_message = _(u"The transfer of decision display dates is done.")

    def _get_decision_data(self, incoming_id):
        licence = self.context.aq_parent
        all_licence_events = sorted(
            licence.getAllEvents(), key=lambda e: e.created(), reverse=True
        )
        for event in all_licence_events:
            annotations = IAnnotations(event)
            key = "notice_notification"
            notice = annotations.get(key, {})
            outgoings = notice.get("outgoing", [])
            for outgoing in outgoings:
                matching_notice_id = outgoing["incoming_notice_id"] == incoming_id
                matching_action_code = outgoing["outgoing_notice_type"] == "transfer_decision"
                if matching_notice_id and matching_action_code:
                    college_decision = outgoing["field_values"]["college_decision"]
                    return event, college_decision
        return None, None

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        incoming_type = self._get_incoming_type(incoming_id)
        if incoming_type in (
            "NOTIFICATION_RS_COMMUNE",
            "NOTIFICATION_RS_COMMUNE_RETARD",
            "NOTIFICATION_RS_COMMUNE_RETARD_SFD",
            "NOTIFICATION_PAS_ENVOI_RS",
            "NOTIFICATION_PAS_ENVOI_RS_SFD",
        ):
            decision_event, college_decision = self._get_decision_data(incoming_id)
            if not decision_event:
                raise NoPreviousEventFoundException(
                    "transfer of decision", "this summary report"
                )
            result = self.context.transfer_decision_display(
                incoming_id,
                decision_event=decision_event,
                college_decision=college_decision,
            )
        if incoming_type in (
            "NOTIFICATION_DECISION_COMMUNE",
            "NOTIFICATION_DEC_RS_COMMUNE",
            "NOTIFICATION_DECRS_REFUS_TACITE_COMMUNE",
        ):
            result = self.context.transfer_decision_display(incoming_id)
        return result


TransferDecisionDisplayActionWrapper = wrap_form(TransferDecisionDisplayActionForm)


class ITransferDatesGesperEPActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_dates_gesper_ep"]
        ),
    )


class TransferDatesGesperEPActionForm(NoticeResponseActionForm):
    label = _("Transfer dates to the SPW")
    fields = field.Fields(ITransferDatesGesperEPActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_dates_gesper_ep"
    partial_or_final = "PARTIAL"
    success_message = _(u"The transfer of dates is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        return self.context.transfer_dates_gesper_ep(incoming_id)


TransferDatesGesperEPActionWrapper = wrap_form(TransferDatesGesperEPActionForm)


class ITransferTicketGesperEPActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_ticket_gesper_ep", "transfer_ticket_final_gesper_ep"]
        ),
    )

    partial_or_final = schema.Choice(
        title=_(u"Preliminary Opinion"),
        description=_(u"This action cannot be reversed."),
        required=True,
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    value=u"PARTIAL", title=_(u"I will create a college opinion")
                ),
                SimpleTerm(
                    value=u"FINAL",
                    title=_(
                        u"I will not send a college opinion and I am finalizing the response to the SPW now"
                    ),
                ),
            ]
        ),
    )


class TransferTicketGesperEPActionForm(NoticeResponseActionForm):
    label = _("Transfer ticket to the SPW")
    fields = field.Fields(ITransferTicketGesperEPActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    fields["partial_or_final"].widgetFactory = RadioFieldWidget
    success_message = _(u"The ticket transfer is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        self.partial_or_final = data.get("partial_or_final")
        if self.partial_or_final == "PARTIAL":
            self.action_code = "transfer_ticket_gesper_ep"
            return self.context.transfer_ticket_gesper_ep(incoming_id)

        if self.partial_or_final == "FINAL":
            self.action_code = "transfer_ticket_final_gesper_ep"
            return self.context.finalize_inquiry_without_opinion_gesper_ep(incoming_id)


TransferTicketGesperEPActionWrapper = wrap_form(TransferTicketGesperEPActionForm)


class ITransferOpinionGesperEPActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_opinion_gesper_ep", "transfer_ticket_final_gesper_ep"]
        ),
    )

    college_opinion = RichText(
        title=_(u"College opinion"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferOpinionGesperEPActionForm(NoticeResponseActionForm):
    label = _("Transfer opinion to the SPW")
    fields = field.Fields(ITransferOpinionGesperEPActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_opinion_gesper_ep"
    partial_or_final = "FINAL"
    success_message = _(u"The opinion transfer is done.")

    def updateWidgets(self):
        super(TransferOpinionGesperEPActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_opinion")

    def _get_inquiry_event(self, incoming_id):
        licence = self.context.aq_parent
        all_licence_events = sorted(
            licence.getAllEvents(), key=lambda e: e.created(), reverse=True
        )
        for event in all_licence_events:
            if event.portal_type != "UrbanEventInquiry":
                continue
            annotations = IAnnotations(event)
            key = "notice_notification"
            notice = annotations.get(key, {})
            outgoings = notice.get("outgoing", [])
            for outgoing in outgoings:
                matching_notice_id = outgoing["incoming_notice_id"] == incoming_id
                matching_action_code = outgoing["outgoing_notice_type"] in (
                    "transfer_dates_gesper_ep",
                    "transfer_ticket_gesper_ep",
                )
                if matching_notice_id and matching_action_code:
                    return event

        raise NoMatchingEventFoundException("Inquiry")

    def _get_college_opinion_text(self, data):
        college_opinion = data.get("college_opinion", "")
        output = college_opinion.output if college_opinion else ""
        self.field_values_to_store["college_opinion"] = output
        return output

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        inquiry_event = self._get_inquiry_event(incoming_id)
        college_opinion = self._get_college_opinion_text(data)
        return self.context.transfer_opinion_gesper_ep(incoming_id, inquiry_event, college_opinion)


TransferOpinionGesperEPActionWrapper = wrap_form(TransferOpinionGesperEPActionForm)


class ITransferDatesGesperAPActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_ANNONCE PROJET_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_ANNONCE_PROJET_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_dates_gesper_ap"]
        ),
    )


class TransferDatesGesperAPActionForm(NoticeResponseActionForm):
    label = _("Transfer dates to the SPW")
    fields = field.Fields(ITransferDatesGesperAPActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_dates_gesper_ap"
    partial_or_final = "PARTIAL"
    success_message = _(u"The transfer of dates is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        return self.context.transfer_dates_gesper_ap(incoming_id)


TransferDatesGesperAPActionWrapper = wrap_form(TransferDatesGesperAPActionForm)


class ITransferTicketGesperAPActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_ANNONCE PROJET_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_ANNONCE_PROJET_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_ticket_gesper_ap", "transfer_ticket_final_gesper_ap"],
        ),
    )

    partial_or_final = schema.Choice(
        title=_(u"Preliminary Opinion"),
        description=_(u"This action cannot be reversed."),
        required=True,
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    value=u"PARTIAL", title=_(u"I will create a college opinion")
                ),
                SimpleTerm(
                    value=u"FINAL",
                    title=_(
                        u"I will not send a college opinion and I am finalizing the response to the SPW now"
                    ),
                ),
            ]
        ),
    )


class TransferTicketGesperAPActionForm(NoticeResponseActionForm):
    label = _("Transfer ticket to the SPW")
    fields = field.Fields(ITransferTicketGesperAPActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    fields["partial_or_final"].widgetFactory = RadioFieldWidget
    success_message = _(u"The ticket transfer is done.")

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        self.partial_or_final = data.get("partial_or_final")
        if self.partial_or_final == "PARTIAL":
            self.action_code = "transfer_ticket_gesper_ap"
            return self.context.transfer_ticket_gesper_ap(incoming_id)

        if self.partial_or_final == "FINAL":
            self.action_code = "transfer_ticket_final_gesper_ap"
            return self.context.finalize_inquiry_without_opinion_gesper_ap(incoming_id)


TransferTicketGesperAPActionWrapper = wrap_form(TransferTicketGesperAPActionForm)


class ITransferOpinionGesperAPActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_ANNONCE PROJET_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_ANNONCE_PROJET_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_opinion_gesper_ap", "transfer_ticket_final_gesper_ap"],
        ),
    )

    college_opinion = RichText(
        title=_(u"College opinion"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferOpinionGesperAPActionForm(NoticeResponseActionForm):
    label = _("Transfer opinion to the SPW")
    fields = field.Fields(ITransferOpinionGesperAPActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_opinion_gesper_ap"
    partial_or_final = "FINAL"
    success_message = _(u"The opinion transfer is done.")

    def updateWidgets(self):
        super(TransferOpinionGesperAPActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_opinion")

    def _get_announcement_event(self, incoming_id):
        licence = self.context.aq_parent
        all_licence_events = sorted(
            licence.getAllEvents(), key=lambda e: e.created(), reverse=True
        )
        for event in all_licence_events:
            if event.portal_type != "UrbanEventAnnouncement":
                continue
            annotations = IAnnotations(event)
            key = "notice_notification"
            notice = annotations.get(key, {})
            outgoings = notice.get("outgoing", [])
            for outgoing in outgoings:
                matching_notice_id = outgoing["incoming_notice_id"] == incoming_id
                matching_action_code = outgoing["outgoing_notice_type"] in (
                    "transfer_dates_gesper_ap",
                    "transfer_ticket_gesper_ap",
                )
                if matching_notice_id and matching_action_code:
                    return event

        raise NoMatchingEventFoundException("Announcement")

    def _get_college_opinion_text(self, data):
        college_opinion = data.get("college_opinion", "")
        output = college_opinion.output if college_opinion else ""
        self.field_values_to_store["college_opinion"] = output
        return output

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        announcement_event = self._get_announcement_event(incoming_id)
        college_opinion = self._get_college_opinion_text(data)
        return self.context.transfer_opinion_gesper_ap(incoming_id, announcement_event, college_opinion)


TransferOpinionGesperAPActionWrapper = wrap_form(TransferOpinionGesperAPActionForm)


class ITransferOpinionGesperOpinionRequestActionForm(ITransferBaseActionForm):
    incoming_notification = schema.Choice(
        title=_(u"Incoming notification to answer to"),
        source=OpenIncomingNotifications(
            [
                "DEMANDE_AVIS_OBLIGATOIRE_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_AVIS_OBLIGATOIRE_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_AVIS_OBLIGATOIRE_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_AVIS_OBLIGATOIRE_PLAN_MODIFIE_2_EME_INSTANCE",
                "DEMANDE_AVIS_FACULTATIF_PLAN_INITIAL_1_ERE_INSTANCE",
                "DEMANDE_AVIS_FACULTATIF_PLAN_MODIFIE_1_ERE_INSTANCE",
                "DEMANDE_AVIS_FACULTATIF_PLAN_INITIAL_2_EME_INSTANCE",
                "DEMANDE_AVIS_FACULTATIF_PLAN_MODIFIE_2_EME_INSTANCE",
            ],
            ["transfer_opinion_gesper_ap", "transfer_ticket_final_gesper_ap"],
        ),
    )

    college_opinion = RichText(
        title=_(u"College opinion"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferOpinionGesperOpinionRequestActionForm(NoticeResponseActionForm):
    label = _("Transfer opinion to the SPW")
    fields = field.Fields(ITransferOpinionGesperOpinionRequestActionForm)
    fields["file_paths"].widgetFactory = CheckBoxFieldWidget
    action_code = "transfer_opinion_gesper_opinion_request"
    partial_or_final = "FINAL"
    success_message = _(u"The opinion transfer is done.")

    def updateWidgets(self):
        super(TransferOpinionGesperOpinionRequestActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_opinion")

    def _get_college_opinion_text(self, data):
        college_opinion = data.get("college_opinion", "")
        output = college_opinion.output if college_opinion else ""
        self.field_values_to_store["college_opinion"] = output
        return output

    def transfer_response(self, data):
        incoming_id = data.get("incoming_notification")
        college_motivation = self._get_college_opinion_text(data)
        return self.context.transfer_opinion_gesper_opinion_request(incoming_id, college_motivation)


TransferOpinionGesperOpinionRequestActionWrapper = wrap_form(TransferOpinionGesperOpinionRequestActionForm)
