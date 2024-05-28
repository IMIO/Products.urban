# -*- coding: utf-8 -*-

from imio.pm.wsclient import WS4PMClientMessageFactory as _
from imio.pm.wsclient.interfaces import IRedirect
from plone.z3cform.layout import wrap_form
from z3c.form import button
from z3c.form.form import Form
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import Interface
from zope import schema
from zope.event import notify
from .event import SendMailAction

class ISendMailActionForm(Interface):
    files = schema.List(
        title=u"Licence Files",
        description=u"Select all files from the parent licence you whant to send",
        required=False,
        value_type=schema.Choice(
            vocabulary="urban.vocabularies.licence_documents"
        )
    )

class SendMailActionForm(Form):
    fields = field.Fields(ISendMailActionForm)
    fields['files'].widgetFactory = CheckBoxFieldWidget
    _finishedSent = False
    _displayErrorsInOverlay = False
    ignoreContext = True

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.label = "Send"

    @button.buttonAndHandler(_('Send'), name='send_mail_action')
    def handleSendToPloneMeeting(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        files = self.request.form.get('form.widgets.files', [])
        notify(SendMailAction(self.context, files))
        self._finishedSent = True

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        self._finishedSent = True

    def render(self):
        if self._finishedSent:
            IRedirect(self.request).redirect(self.context.absolute_url())
            return ""
        return super(SendMailActionForm, self).render()

SendMailActionWrapper = wrap_form(SendMailActionForm)