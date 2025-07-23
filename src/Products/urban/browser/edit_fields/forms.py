# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from imio.pm.wsclient.interfaces import IRedirect
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.z3cform.layout import wrap_form
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from zope.interface import Interface


class IEditFieldsForm(Interface):
    description = RichText(title=u"Obervations", required=False)


class EditFieldsForm(Form):
    fields = field.Fields(IEditFieldsForm)
    _finishedSent = False
    _displayErrorsInOverlay = False
    ignoreContext = True

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @button.buttonAndHandler(_("Send"), name="edit_fields")
    def handleSend(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        description = self.request.form.get("form.widgets.description", "")
        if self.context.get_description_edit_permission():
            with api.env.adopt_roles(["Manager"]):
                self.context.setDescription(description)
        self._finishedSent = True

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        self._finishedSent = True

    def render(self):
        if not self.context.get_description_edit_permission():
            IStatusMessage(self.request).addStatusMessage(
                u"You're not authorized to edit this field", "error"
            )
            return ""
        if self._finishedSent:
            IRedirect(self.request).redirect(self.context.absolute_url())
            return ""
        return super(EditFieldsForm, self).render()

    def updateWidgets(self, prefix=None):
        super(EditFieldsForm, self).updateWidgets(prefix=prefix)

        # Confirm the widget exists
        if "description" in self.widgets:
            self.widgets["description"].value = RichTextValue(
                self.context.getRawDescription(), "text/html", "text/x-html-safe"
            )


SendMailActionWrapper = wrap_form(EditFieldsForm)
