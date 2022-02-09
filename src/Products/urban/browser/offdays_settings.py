# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from datetime import date

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.autoform import directives as form

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _

from z3c.form import button
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope.interface import Interface
from zope import schema


class IOffDayPeriod(Interface):
    """ """

    period_type = schema.Choice(
        title=_(u"Type"),
        required=True,
        vocabulary=u'urban.vocabularies.offdays_period_types'
    )

    start_date = schema.Date(
        title=_(u"Suspension period start date"),
        default=date.today(),
        required=True,
    )

    end_date = schema.Date(
        title=_(u"Suspension period end date"),
        default=date.today(),
    )


class IOffDay(Interface):
    """ """

    day_type = schema.Choice(
        title=_(u"Type"),
        required=True,
        vocabulary=u'urban.vocabularies.offdays_types'
    )

    date = schema.Date(
        title=_(u"Date"),
        default=date.today(),
        required=True,
    )


class IOffDays(Interface):
    """ """

    form.widget(week_offdays=CheckBoxFieldWidget)
    week_offdays = schema.List(
        title=_(u"Week off days"),
        required=False,
        value_type=schema.Choice(
            title=_('weekdays'),
            vocabulary=u'urban.vocabularies.weekdays'
        )
    )

    periods = schema.List(
        title=_("Off days period"),
        description=_(""),
        value_type=DictRow(
            title=_("Period"),
            schema=IOffDayPeriod,
            required=False
        ),
        default=[],
        required=False,
    )

    offdays = schema.List(
        title=_("Off days"),
        description=_(""),
        value_type=DictRow(
            title=_("Day"),
            schema=IOffDay,
            required=False
        ),
        default=[],
        required=False,
    )


class OffDaysEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IOffDays
    label = _(u"Off days")
    description = _(u"""""")

    fields = field.Fields(IOffDays)
    fields['offdays'].widgetFactory = DataGridFieldFactory
    fields['periods'].widgetFactory = DataGridFieldFactory

    def updateWidgets(self):
        super(OffDaysEditForm, self).updateWidgets()

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


class OffDaysControlPanel(ControlPanelFormWrapper):
    form = OffDaysEditForm
