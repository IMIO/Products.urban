# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from z3c.form import button
from z3c.form.interfaces import DISPLAY_MODE
from zope import schema
from zope.interface import Interface


class INoticeSettings(Interface):
    url = schema.URI(
        title=_("Webservice URL"),
        required=True,
        default="https://api-staging.imio.be/spw/notice/v1/",
    )

    municipality_id = schema.TextLine(
        title=_("Municipality ID in Notice"),
        required=True,
    )

    last_import_date = schema.Datetime(
        title=_("Last import date from Notice Webservice"),
        required=False,
    )


class NoticeSettingsEditForm(RegistryEditForm):
    schema = INoticeSettings
    label = _("Notice settings")
    description = ""

    def updateWidgets(self):
        super(NoticeSettingsEditForm, self).updateWidgets()
        self.widgets["last_import_date"].mode = DISPLAY_MODE

    @button.buttonAndHandler(_("Save"), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if "url" in data and not isinstance(data["url"], unicode):
            data["url"] = unicode(data["url"])
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_("Changes saved"), "info")

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_("Edit cancelled"), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view)
        )


class NoticeSettingsControlPanel(ControlPanelFormWrapper):
    form = NoticeSettingsEditForm
