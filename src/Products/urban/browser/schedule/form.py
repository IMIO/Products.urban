# -*- coding: utf-8 -*-
from Products.urban import UrbanMessage as _
from Products.urban.config import ORDERED_URBAN_TYPES

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from plone import api

from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
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

    terms = []
    if licence_config:
        for event_type in licence_config.urbaneventtypes.objectValues():
            if event_type.getDeadLineDelay() > 0:
                terms.append(SimpleTerm(
                    event_type.id,
                    event_type.id,
                    event_type.Title()
                ))

    vocabulary = SimpleVocabulary(terms)
    return vocabulary


class buildlicenceEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'buildlicence')
buildlicenceEventsVocabularyFactory = buildlicenceEventsVocabulary()


class IBuildlicenceEventsRow(Interface):
    local_userid = schema.Choice(
        required=False,
        vocabulary='urban.buildlicence_schedulable_events',
    )


class IScheduleForm(Interface):
    """ Define form fields """

    licences = schema.List(
        title=_(u"Licence types"),
        required=False,
        value_type=schema.Choice(source=licenceTypesVocabulary()),
    )
    buildlicence_events = schema.List(
        title=_(u"Buildlicence"),
        required=False,
        value_type=DictRow(
            schema=IBuildlicenceEventsRow,
            required=False
        ),
    )
    sort_by_licence = schema.Bool(
        title=_(u"Sort by licence type"),
        description=_(u"Sort results by licence type first, then by delay time"),
        required=False,
    )


class ScheduleForm(form.Form):
    """
    """

    schema = IScheduleForm
    ignoreContext = True

    description = u"Schedule"

    fields = field.Fields(IScheduleForm)
    fields['licences'].widgetFactory = CheckBoxFieldWidget
    fields['buildlicence_events'].widgetFactory = DataGridFieldFactory

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()

    def updateWidgets(self):
        super(ScheduleForm, self).updateWidgets()
        #self.hideDataGridWidget('buildlicence_events')

    def hideDataGridWidget(self, licence_type):
        data_grid = self.widgets[licence_type]
        data_grid.mode = HIDDEN_MODE
        add_line_widget = data_grid.widgets(-2)
        old_klass = add_line_widget.klass
        add_line_widget.klass = '{old_klass} schedule-hide-form-input'.format(old_klass)
