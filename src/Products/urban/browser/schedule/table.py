# -*- coding: utf-8 -*-
from DateTime import DateTime

from Products.urban import UrbanMessage as _
from Products.urban.browser.schedule.interfaces import IScheduleListingTable
from Products.urban.browser.schedule.interfaces import ITimeDelayColumn
from Products.urban.browser.table.column import TitleColumn
from Products.urban.browser.table.column import TitleColumnHeader
from Products.urban.browser.table.column import UrbanColumn
from Products.urban.browser.table.tablevalue import BrainForUrbanTable
from Products.urban.browser.table.tablevalue import ObjectForUrbanTable
from Products.urban.browser.table.tablevalue import ValuesForUrbanListing
from Products.urban.browser.table.urbantable import UrbanTable

from Products.urban.interfaces import IUrbanEvent
from Products.urban.interfaces import IGenericLicence
from Products.urban.utils import getLicenceFolderId

from plone import api

from zope.i18n import translate
from zope.interface import implements


class ScheduleListingTable(UrbanTable):
    """
    Licence listing for schedule
    """
    implements(IScheduleListingTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    batchSize = 20
    sortOn = None


class ScheduleLicenceTitleColumnHeader(TitleColumnHeader):
    """ return the right label to display in Title Column header """

    def update(self):
        self.label = 'label_colname_licence'


class TimeDelayColumn(UrbanColumn):
    """ Display the time delay of an urban event """
    implements(ITimeDelayColumn)

    header = u'label_colname_time_delay'
    weight = -10

    def renderCell(self, schedule_item):
        delay = schedule_item.getEventTimeDelay()
        if delay == 9999:
            cell = u'<div style="font-size:200%; text-align:center">\u221e</div>'
        else:
            cell = u'<div style="text-align:center">{delay}</div>'.format(delay=delay)
        return cell


class ScheduleEventTitleColumn(TitleColumn):
    """ """

    header = u'label_colname_event_title'
    weight = -5

    def renderCell(self, schedule_item):
        event = schedule_item.getEvent()
        title = self.renderTitleLink(event)
        return title.decode('utf-8')

    def renderHeadCell(self):
        return translate(self.header, 'urban', context=self.request)


class ScheduleEventDatesColumn(UrbanColumn):
    """ Used in schedule view to display all the dates of an event"""

    header = u'label_colname_event_dates'
    weight = -4

    def renderCell(self, schedule_item):
        dates = schedule_item.getEventDates()

        if len(dates) == 1:
            date = dates[0]
            if date['date_label'] == 'Date':
                return u'<div>{date}</div>'.format(**date)

        dateline = u'<div>{date_label}: {date}</div>'
        cell = u''.join([dateline.format(**date) for date in dates])

        return cell


class ValuesForScheduleListing(ValuesForUrbanListing):
    """
    Find events in progress matching form criterias.
    Compute their time delay values, wrap them and sort them
    so they can be rendered in the schedule result listing.
    """

    @property
    def values(self):
        events = self.getUrbanEventsToList()
        return events

    def getUrbanEventsToList(self, **kwargs):
        form_datas = self.context.form.extractData()[0]
        licences = form_datas.get('licences') or []
        sort_by_delay = not form_datas.get('sort_by_licence')

        sorted_events = []

        for licence in licences:
            event_brains = self.getUrbanEventsOfLicence(licence)
            events = [ItemForScheduleListing(event) for event in event_brains]
            events.sort(key=lambda event: -event.delay)
            sorted_events.extend(events)

        if sort_by_delay:
            sorted_events.sort(key=lambda event: -event.delay)

        return sorted_events

    def getUrbanEventsOfLicence(self, licence_type):
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


class ItemForScheduleListing(BrainForUrbanTable):
    """ wrapper for couple event/licence """

    def __init__(self, event):
        catalog = api.portal.get_tool('portal_catalog')
        licence_path = '/'.join(event.getPath().split('/')[:-1])
        licence_brains = catalog(
            path={'query': licence_path},
            object_provides=IGenericLicence.__identifier__,
        )
        self.licence = licence_brains[0]
        self.value = self.licence
        self.event = ObjectForUrbanTable(event.getObject())
        self.delay = self._computeDelay(event)

    def _computeDelay(self, event):
        event = self.event
        event_type = event.getUrbaneventtypes()
        deadline_delay = event_type.getDeadLineDelay()
        event_date = event.getEventDate()
        if event_date is None:
            return 9999
        delay = DateTime() - (event_date + deadline_delay)
        return int(delay)

    def getEvent(self):
        return self.event

    def getLicence(self):
        return self.licence

    def getEventTimeDelay(self):
        return self.delay

    def getEventDates(self):
        def formatDate(date):
            if date is None:
                return '<span class="discreet">N.C.</span>'
            return date.strftime('%d/%m/%Y')

        event = self.event
        event_date = formatDate(event.getEventDate())
        event_type = event.getUrbaneventtypes()
        request = api.portal.getRequest()

        dates = [{'date_label': event_type.getEventDateLabel(), 'date': event_date}]

        for fieldname in event_type.getActivatedFields():
            field = event.getField(fieldname)
            if field.type == 'datetime':
                date = formatDate(field.get(event))
                date_label = translate(_(field.widget.label_msgid), 'urban', context=request)
                dates.append({'date_label': date_label, 'date': date})

        return dates
