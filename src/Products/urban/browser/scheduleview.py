# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban import UrbanMessage as _
from Products.urban.browser.table.tablevalue import ValuesForUrbanListing
from Products.urban.browser.table.urbantable import ScheduleListingTable
from Products.urban.config import ORDERED_URBAN_TYPES
from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import getLicenceFolderId

from plone import api

from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope import schema
from zope.interface import Interface
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


class ValuesForScheduleListing(ValuesForUrbanListing):
    """ return licence values from the context  """

    def getItems(self):
        licence_brains = self.getLateUrbanEvents()
        return licence_brains

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
        self.status = "Thank you very much!"
