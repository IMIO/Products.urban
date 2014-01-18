# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.Five import BrowserView

from Products.urban import UrbanMessage as _
from Products.urban.browser.table.tablevalue import BrainForUrbanTable
from Products.urban.browser.table.tablevalue import ValuesForUrbanListing
from Products.urban.browser.table.urbantable import ScheduleListingTable
from Products.urban.config import ORDERED_URBAN_TYPES
from Products.urban.interfaces import IUrbanEvent
from Products.urban.interfaces import IGenericLicence
from Products.urban.utils import getLicenceFolderId

from plone import api

from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope import schema
from zope.interface import Interface
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ScheduleView(BrowserView):
    """
      This manages urban schedule view
    """
    def __init__(self, context, request):
        super(ScheduleView, self).__init__(context, request)
        self.context = context
        self.request = request

        self.form = ScheduleForm(self.context, self.request)
        self.form.update()

        self.schedulelisting = ScheduleListingTable(self, self.request)
        self.schedulelisting.update()

    def renderScheduleListing(self):
        self.schedulelisting.update()

        return u'{listing}{batch}'.format(
            listing=self.schedulelisting.render(),
            batch=self.schedulelisting.renderBatch(),
        )


class ItemForScheduleListing(BrainForUrbanTable):
    """ """

    def __init__(self, event):
        self.value = event.licence
        self.event = BrainForUrbanTable(event.event)

    def getEvent(self):
        return self.event

    def getLicence(self):
        return self.licence

    def getEventTimeDelay(self):
        event = self.getEvent().getObject()
        event_type = event.getUrbaneventtypes()
        deadline_delay = event_type.getDeadLineDelay()
        delay = DateTime() - (event.getEventDate() + deadline_delay)
        return int(delay)


class IEventAndLicenceWrapper(Interface):
    """ """


class EventAndLicenceWrapper(BrainForUrbanTable):
    """ wrapper for couple event/licence """
    implements(IEventAndLicenceWrapper)

    def __init__(self, event):
        catalog = api.portal.get_tool('portal_catalog')
        licence_path = '/'.join(event.getPath().split('/')[:-1])
        licence_brains = catalog(
            path={'query': licence_path},
            object_provides=IGenericLicence.__identifier__,
        )
        self.licence = licence_brains[0]
        self.event = event


class ValuesForScheduleListing(ValuesForUrbanListing):
    """ return late event/licence values from form query """

    def getItems(self):
        events = [EventAndLicenceWrapper(event) for event in self.getLateUrbanEvents()]
        return events

    def getLateUrbanEvents(self, **kwargs):
        form_datas = self.context.form.extractData()
        licences = form_datas[0].get('licences', []) or []

        events = {}

        for licence in licences:
            events[licence] = self.getLateEventsOfSpecificLicence(licence)

        event_brains = []
        for brains in events.values():
            event_brains.extend(brains)

        return event_brains

    def getLateEventsOfSpecificLicence(self, licence_type):
        """ """
        catalog = api.portal.get_tool('portal_catalog')
        site = api.portal.getSite()
        site_path = '/'.join(site.getPhysicalPath())
        folder = getLicenceFolderId(licence_type)

        path = '{site_path}/urban/{folder}'.format(site_path=site_path, folder=folder)

        query_string = {
            'object_provides': IUrbanEvent.__identifier__,
            'review_state': 'in_progress',
            'path': {'query': path},
        }

        event_brains = catalog(query_string)

        return event_brains


def licenceTypesVocabulary():
    terms = [SimpleTerm(licence, licence, _(licence))
             for licence in ORDERED_URBAN_TYPES]

    vocabulary = SimpleVocabulary(terms)
    return vocabulary


class IScheduleForm(Interface):
    """ Define form fields """

    licences = schema.List(
        title=u"Licence type",
        required=False,
        value_type=schema.Choice(source=licenceTypesVocabulary()),
    )


class ScheduleForm(form.Form):
    """
    """

    schema = IScheduleForm
    ignoreContext = True

    description = u"Schedule"

    fields = field.Fields(IScheduleForm)
    fields['licences'].widgetFactory = CheckBoxFieldWidget

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
