# -*- coding: utf-8 -*-
from Products.urban import UrbanMessage as _
from Products.urban.config import ORDERED_URBAN_TYPES

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from plone import api

from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE

from zope import schema
from zope.interface import Interface
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def licenceTypesVocabulary():
    terms = [SimpleTerm(licence, licence, _(licence))
             for licence in ORDERED_URBAN_TYPES]

    vocabulary = SimpleVocabulary(terms)
    return vocabulary


def getSchedulableEventsVocabulary(context, licence_type):
    urban_config = api.portal.get_tool('portal_urban')
    licence_config = urban_config.get(licence_type, None)

    terms = [SimpleTerm('all', 'all', _(u'All'))]
    if licence_config:
        terms.append(SimpleTerm('all_opinions', 'all_opinions', _(u'All opinion requests')))
        for event_type in licence_config.urbaneventtypes.objectValues():
            if event_type.getDeadLineDelay() > 0:
                title = event_type.Title()
                title = len(title) > 40 and '{title}...'.format(title=title[:39]) or title
                terms.append(SimpleTerm(
                    event_type.id,
                    event_type.id,
                    title
                ))

    vocabulary = SimpleVocabulary(terms)
    return vocabulary


class buildlicenceEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'buildlicence')
buildlicenceEventsVocabularyFactory = buildlicenceEventsVocabulary()


class parceloutlicenceEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'parceloutlicence')
parceloutlicenceEventsVocabularyFactory = parceloutlicenceEventsVocabulary()


class declarationEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'declaration')
declarationEventsVocabularyFactory = declarationEventsVocabulary()


class divisionEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'division')
divisionEventsVocabularyFactory = divisionEventsVocabulary()


class urbancertificateoneEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'urbancertificateone')
urbancertificateoneEventsVocabularyFactory = urbancertificateoneEventsVocabulary()


class urbancertificatetwoEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'urbancertificatetwo')
urbancertificatetwoEventsVocabularyFactory = urbancertificatetwoEventsVocabulary()


class notaryletterEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'notaryletter')
notaryletterEventsVocabularyFactory = notaryletterEventsVocabulary()


class envclassthreeEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'envclassthree')
envclassthreeEventsVocabularyFactory = envclassthreeEventsVocabulary()


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
    sort_by_licence = schema.Bool(
        title=_(u"Sort by licence type"),
        # description=_(u"Sort results by licence type first, then by delay time"),
        required=False,
    )


datagrid_field_names = [
    'events_buildlicence', 'events_parceloutlicence', 'events_declaration', 'events_division',
    'events_notaryletter', 'events_urbancertificateone', 'events_urbancertificatetwo', 'events_envclassthree'
]


class ScheduleForm(form.Form):
    """
    """

    schema = IScheduleForm
    ignoreContext = True

    description = u"Schedule"

    #template = Zope3PageTemplateFile("custom-form-template.pt")

    fields = field.Fields(IScheduleForm)
    for field_name in datagrid_field_names:
        fields[field_name].widgetFactory = DataGridFieldFactory

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()

    def updateWidgets(self):
        super(ScheduleForm, self).updateWidgets()

        for field_name in datagrid_field_names:
            self.widgets[field_name].auto_append = False

        #self.hideDataGridWidget('buildlicence_events')

    def hideDataGridWidget(self, licence_type):
        data_grid = self.widgets[licence_type]
        data_grid.mode = HIDDEN_MODE
        add_line_widget = data_grid.widgets(-2)
        old_klass = add_line_widget.klass
        add_line_widget.klass = '{old_klass} schedule-hide-form-input'.format(old_klass)
