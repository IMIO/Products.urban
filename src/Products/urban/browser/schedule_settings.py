# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from imio.schedule.interfaces import IDueDateSettings
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from z3c.form import button
from z3c.form import field


class ScheduleEditForm(RegistryEditForm):
    """ """

    schema = IDueDateSettings
    label = _(u"Schedule alerts")
    description = _(u"""""")

    fields = field.Fields(IDueDateSettings)

    @button.buttonAndHandler(_("Save"), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view)
        )


class ScheduleControlPanel(ControlPanelFormWrapper):
    form = ScheduleEditForm
