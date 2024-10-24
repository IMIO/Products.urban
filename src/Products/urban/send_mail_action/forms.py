# -*- coding: utf-8 -*-

from plone import api
from Products.urban import UrbanMessage as _
from imio.pm.wsclient.interfaces import IRedirect
from plone.z3cform.layout import wrap_form
from z3c.form import button, field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.form import Form
from zope import schema
from zope.event import notify
from zope.interface import Interface
from zope.i18n import translate
from datetime import datetime
from .event import SendMailAction
from plone.app.event.base import default_timezone
from zope.annotation.interfaces import IAnnotations


MAIL_ACTION_KEY = "Products.urban.send_mail_action"

class ISendMailActionForm(Interface):
    files = schema.List(
        title=_(u"Licence Files"),
        description=_(u"Select all files from this event or the parent licence you whant to send"),
        required=False,
        value_type=schema.Choice(vocabulary="urban.vocabularies.licence_documents"),
    )


class SendMailActionForm(Form):
    fields = field.Fields(ISendMailActionForm)
    fields["files"].widgetFactory = CheckBoxFieldWidget
    _finishedSent = False
    _displayErrorsInOverlay = False
    ignoreContext = True

    def __init__(self, context, request):
        self.context = context
        self.request = request

        rules = [rule.title for rule in self.context.get_all_rules_for_this_event()]
        last_rule = None
        if len(rules) > 1:
            last_rule = rules.pop()
        label = ", ".join(rules)
        if last_rule is not None:
            label += translate(
                _(" and ${last_rule}", mapping={"last_rule":last_rule}),
                context=request
            )
        self.label = label

    @button.buttonAndHandler(_("Send"), name="send_mail_action")
    def handleSendToPloneMeeting(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        files = self.request.form.get("form.widgets.files", [])
        notify(SendMailAction(self.context, files))
        self.add_notify_info_annotation()
        self._finishedSent = True

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        self._finishedSent = True

    def add_notify_info_annotation(self):
        user = api.user.get_current()
        tz = default_timezone(as_tzinfo=True)
        time = datetime.now(tz=tz)
        annotations = IAnnotations(self.context)
        notif = annotations.get(MAIL_ACTION_KEY, None)
        if notif is None:
            notif = []
        if not isinstance(notif, list):
            notif = [notif]
        user_id = user.id
        username = user.getProperty("fullname", None)
        notif.append({
            "title": self.label,
            "user": user_id,
            "username": username,
            "time": time
        })
        annotations[MAIL_ACTION_KEY] = notif

    def render(self):
        if self._finishedSent:
            IRedirect(self.request).redirect(self.context.absolute_url())
            return ""
        return super(SendMailActionForm, self).render()


SendMailActionWrapper = wrap_form(SendMailActionForm)
