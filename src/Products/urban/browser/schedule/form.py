# -*- coding: utf-8 -*-
from Products.urban import UrbanMessage as _

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE

from zope import schema
from zope.interface import Interface


class IBuildlicenceEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.buildlicence_schedulable_events',
    )


class IParcelOutLicenceEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.parceloutlicence_schedulable_events',
    )


class IDeclarationEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.declaration_schedulable_events',
    )


class IDivisionEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.division_schedulable_events',
    )


class IUrbanCertificateOneEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.urbancertificateone_schedulable_events',
    )


class IUrbanCertificateTwoEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.urbancertificatetwo_schedulable_events',
    )


class INotaryLetterEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.notaryletter_schedulable_events',
    )


class IEnvClassThreeEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.envclassthree_schedulable_events',
    )


class IScheduleForm(Interface):
    """ Define form fields """

    foldermanager = schema.Choice(
        title=_(u"FolderManager"),
        required=False,
        default='me',
        vocabulary='urban.folder_managers',
    )
    sort_by_licence = schema.Bool(
        title=_(u"Sort by licence type"),
        required=False,
    )
    events_buildlicence = schema.List(
        title=_(u"BuildLicence"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IBuildlicenceEventsRow,
            required=False
        ),
    )
    events_parceloutlicence = schema.List(
        title=_(u"ParcelOutLicence"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IParcelOutLicenceEventsRow,
            required=False
        ),
    )
    events_declaration = schema.List(
        title=_(u"Declaration"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IDeclarationEventsRow,
            required=False
        ),
    )
    events_division = schema.List(
        title=_(u"Division"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IDivisionEventsRow,
            required=False
        ),
    )
    events_urbancertificateone = schema.List(
        title=_(u"UrbanCertificateOne"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IUrbanCertificateOneEventsRow,
            required=False
        ),
    )
    events_urbancertificatetwo = schema.List(
        title=_(u"UrbanCertificateTwo"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IUrbanCertificateTwoEventsRow,
            required=False
        ),
    )
    events_notaryletter = schema.List(
        title=_(u"NotaryLetter"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=INotaryLetterEventsRow,
            required=False
        ),
    )
    events_envclassthree = schema.List(
        title=_(u"EnvClassThree"),
        default=[{'event': 'all'}],
        required=False,
        value_type=DictRow(
            schema=IEnvClassThreeEventsRow,
            required=False
        ),
    )


class ScheduleForm(form.Form):
    """
    """

    schema = IScheduleForm
    ignoreContext = True
    method = "get"

    datagrid_field_names = [
        'events_buildlicence', 'events_parceloutlicence',
        'events_declaration', 'events_division',
        'events_notaryletter', 'events_urbancertificateone',
        'events_urbancertificatetwo', 'events_envclassthree'
    ]

    fields = field.Fields(IScheduleForm)
    for field_name in datagrid_field_names:
        fields[field_name].widgetFactory = DataGridFieldFactory

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()

    def updateWidgets(self):
        super(ScheduleForm, self).updateWidgets()

        for field_name in self.datagrid_field_names:
            if field_name in self.widgets:
                self.widgets[field_name].auto_append = False
