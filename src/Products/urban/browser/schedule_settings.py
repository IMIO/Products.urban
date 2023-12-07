# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from zope import schema
from zope.interface import invariant
from zope.interface import Interface
from zope.interface import Invalid
from z3c.form import button
from z3c.form import field


class ISchedule(Interface):
    """ """

    color_orange_x_days_before_due_date = schema.Int(
        title=_("Color due date in orange if it comes close to X days"),
        description=_("Leave empty to disable"),
        required=False,
        default=10,
        min=0,
    )

    color_red_x_days_before_due_date = schema.Int(
        title=_("Color due date in red if it comes close to X days"),
        description=_("Overrides orange color, leave empty to disable"),
        required=False,
        default=5,
        min=0,
    )

    @invariant
    def orange_is_before_red_invariant(data):
        if data.color_orange_x_days_before_due_date is None or data.color_red_x_days_before_due_date is None:
            return
        if data.color_orange_x_days_before_due_date < data.color_red_x_days_before_due_date:
            raise Invalid(_(u"The orange value should be higher than the red one, as it is used as a first warning."))


class ScheduleEditForm(RegistryEditForm):
    """"""
    schema = ISchedule
    label = _(u"Schedule alerts")
    description = _(u"""""")

    fields = field.Fields(ISchedule)

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Edit cancelled"),
            "info"
        )
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view)
        )


class ScheduleControlPanel(ControlPanelFormWrapper):
    form = ScheduleEditForm
