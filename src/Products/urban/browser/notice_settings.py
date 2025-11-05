# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from z3c.form import button
from z3c.form.interfaces import DISPLAY_MODE
from zExceptions import Redirect
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

    sent_on_behalf_of_municipality_id = schema.TextLine(
        title=_("Sent On Behalf Of Municipality ID in Notice"),
        required=True,
    )

    last_import_date = schema.Datetime(
        title=_("Last import date from Notice Webservice"),
        required=False,
    )

    failed_notifications = schema.List(
        title=_("Failed notifications"),
        value_type=schema.ASCIILine(),
        required=False,
        default=[],
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

    def show_retry_button(self):
        failed_notifications = api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.failed_notifications",
            default=[],
        )
        return failed_notifications

    @button.buttonAndHandler(
        _("Retry failed notifications"),
        name="retry",
        condition=lambda form: form.show_retry_button(),
    )
    def handleRetry(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _("Retrying failed notifications"), "info"
        )
        raise Redirect(
            "%s/%s" % (api.portal.get().absolute_url(), "@@import-from-notice?retry=1")
        )


class NoticeSettingsControlPanel(ControlPanelFormWrapper):
    form = NoticeSettingsEditForm
