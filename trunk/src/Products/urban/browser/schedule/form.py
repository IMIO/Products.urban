# -*- coding: utf-8 -*-

from Products.urban import UrbanMessage as _
from Products.urban.browser.schedule.interfaces import IScheduleEventField
from Products.urban.utils import getCurrentFolderManager

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import IValue

from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.interface import implements


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


class IEnvClassOneEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.envclassone_schedulable_events',
    )


class IEnvClassTwoEventsRow(Interface):
    event = schema.Choice(
        required=False,
        vocabulary='urban.envclasstwo_schedulable_events',
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
    no_duplicated_licences = schema.Bool(
        title=_(u"Display each licence only once"),
        required=False,
    )
    sort_by_licence = schema.Bool(
        title=_(u"Sort by licence type"),
        required=False,
    )
    events_buildlicence = schema.List(
        title=_(u"BuildLicence"),
        required=False,
        value_type=DictRow(
            schema=IBuildlicenceEventsRow,
            required=False
        ),
    )
    alsoProvides(events_buildlicence, IScheduleEventField)
    events_parceloutlicence = schema.List(
        title=_(u"ParcelOutLicence"),
        required=False,
        value_type=DictRow(
            schema=IParcelOutLicenceEventsRow,
            required=False
        ),
    )
    alsoProvides(events_parceloutlicence, IScheduleEventField)
    events_declaration = schema.List(
        title=_(u"Declaration"),
        required=False,
        value_type=DictRow(
            schema=IDeclarationEventsRow,
            required=False
        ),
    )
    alsoProvides(events_declaration, IScheduleEventField)
    events_division = schema.List(
        title=_(u"Division"),
        required=False,
        value_type=DictRow(
            schema=IDivisionEventsRow,
            required=False
        ),
    )
    alsoProvides(events_division, IScheduleEventField)
    events_urbancertificateone = schema.List(
        title=_(u"UrbanCertificateOne"),
        required=False,
        value_type=DictRow(
            schema=IUrbanCertificateOneEventsRow,
            required=False
        ),
    )
    alsoProvides(events_urbancertificateone, IScheduleEventField)
    events_urbancertificatetwo = schema.List(
        title=_(u"UrbanCertificateTwo"),
        required=False,
        value_type=DictRow(
            schema=IUrbanCertificateTwoEventsRow,
            required=False
        ),
    )
    alsoProvides(events_urbancertificatetwo, IScheduleEventField)
    events_notaryletter = schema.List(
        title=_(u"NotaryLetter"),
        required=False,
        value_type=DictRow(
            schema=INotaryLetterEventsRow,
            required=False
        ),
    )
    alsoProvides(events_notaryletter, IScheduleEventField)
    events_envclassone = schema.List(
        title=_(u"EnvClassOne"),
        required=False,
        value_type=DictRow(
            schema=IEnvClassOneEventsRow,
            required=False
        ),
    )
    alsoProvides(events_envclassone, IScheduleEventField)
    events_envclasstwo = schema.List(
        title=_(u"EnvClassTwo"),
        required=False,
        value_type=DictRow(
            schema=IEnvClassTwoEventsRow,
            required=False
        ),
    )
    alsoProvides(events_envclasstwo, IScheduleEventField)
    events_envclassthree = schema.List(
        title=_(u"EnvClassThree"),
        required=False,
        value_type=DictRow(
            schema=IEnvClassThreeEventsRow,
            required=False
        ),
    )
    alsoProvides(events_envclassthree, IScheduleEventField)


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
        'events_urbancertificatetwo', 'events_envclassone',
        'events_envclasstwo', 'events_envclassthree'
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


class defaultValueForLicenceEventField:
    implements(IValue)

    def __init__(self, context, request, form, field, widget):
        """ """

    def get(self):
        default = [{'event': None}]

        if getCurrentFolderManager():
            default = [{'event': 'all'}]

        return default
