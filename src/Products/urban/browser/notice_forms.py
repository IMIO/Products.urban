# -*- coding: utf-8 -*-
from z3c.form import button
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.form import Form
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from Products.urban.notice.response import clean_accents
from Products.urban.utils import get_ws_meetingitem_infos
from imio.pm.wsclient.interfaces import IRedirect
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.z3cform.layout import wrap_form


class NoticeResponseActionForm(Form):
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


class ITransferTicketActionForm(Interface):
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
    fields["partial_or_final"].widgetFactory = RadioFieldWidget
    _finishedSent = False
    _displayErrorsInOverlay = False
    ignoreContext = True
    @button.buttonAndHandler(_("Send"), name="send_response")
    def handleSendResponse(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if data.get("partial_or_final") == "PARTIAL":
            result = self.context.transfer_ticket()

        if data.get("partial_or_final") == "FINAL":
            result = self.context.finalize_inquiry_without_opinion()

        if result["error"] is True:
            IStatusMessage(self.request).addStatusMessage(result["message"], "error")
        else:
            IStatusMessage(self.request).addStatusMessage(
                _(u"The ticket transfer is done."), "info"
            )

        self._finishedSent = True

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        self._finishedSent = True

    def render(self):
        if self._finishedSent:
            IRedirect(self.request).redirect(self.context.absolute_url())
            return ""
        return super(TransferTicketActionForm, self).render()


TransferTicketActionWrapper = wrap_form(TransferTicketActionForm)


class ITransferOpinionActionForm(Interface):

    college_opinion = RichText(
        title=_(u"College opinion"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferOpinionActionForm(NoticeResponseActionForm):
    label = _("Transfer opinion to the SPW")
    fields = field.Fields(ITransferOpinionActionForm)
    _finishedSent = False
    _displayErrorsInOverlay = False
    ignoreContext = True

    def updateWidgets(self):
        super(TransferOpinionActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_opinion")

    @button.buttonAndHandler(_("Send"), name="send_response")
    def handleSendResponse(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        college_opinion = data.get("college_opinion", "")

        result = self.context.transfer_opinion(college_opinion.output)

        if result["error"] is True:
            IStatusMessage(self.request).addStatusMessage(result["message"], "error")
        else:
            IStatusMessage(self.request).addStatusMessage(
                _(u"The opinion transfer is done."), "info"
            )
        self._finishedSent = True

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        self._finishedSent = True

    def render(self):
        if self._finishedSent:
            IRedirect(self.request).redirect(self.context.absolute_url())
            return ""
        return super(TransferOpinionActionForm, self).render()


TransferOpinionActionWrapper = wrap_form(TransferOpinionActionForm)


class ITransferDecisionActionForm(Interface):

    college_decision = RichText(
        title=_(u"College decision"),
        default=u"<h1>Motivation:</h1>\r\n\r\n<h1>Décision:</h1>\r\n\r\n",
        required=False,
    )


class TransferDecisionActionForm(NoticeResponseActionForm):
    label = _("Transfer decision to the SPW")
    fields = field.Fields(ITransferDecisionActionForm)
    _finishedSent = False
    _displayErrorsInOverlay = False
    ignoreContext = True

    def updateWidgets(self):
        super(TransferDecisionActionForm, self).updateWidgets()
        self._fetch_iadelib_opinion("college_decision")

    @button.buttonAndHandler(_("Send"), name="send_response")
    def handleSendResponse(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        college_decision = data.get("college_decision", "")

        result = self.context.transfer_decision(college_decision.output)

        notice_id = self.context.aq_parent.get_notice_id(self.response_id_code)
        if not notice_id:
            raise ValueError(
                _(
                    u"Can't send response to event '{}': no Notice ID found for '{}'".format(
                        self.context.absolute_url, self.response_id_code
                    )
                )
            )

        self._finishedSent = True

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        self._finishedSent = True

    def render(self):
        if self._finishedSent:
            IRedirect(self.request).redirect(self.context.absolute_url())
            return ""
        return super(TransferDecisionActionForm, self).render()


TransferDecisionActionWrapper = wrap_form(TransferDecisionActionForm)
