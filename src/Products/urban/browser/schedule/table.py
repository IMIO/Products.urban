# -*- coding: utf-8 -*-
from DateTime import DateTime

from Products.CMFCore.Expression import Expression
from Products.PageTemplates.Expressions import getEngine

from Products.urban import UrbanMessage as _
from Products.urban.browser.schedule.interfaces import IDelayTerm
from Products.urban.browser.schedule.interfaces import IScheduleListingTable
from Products.urban.browser.schedule.interfaces import ITimeDelayColumn
from Products.urban.browser.table.column import TitleColumn
from Products.urban.browser.table.column import TitleColumnHeader
from Products.urban.browser.table.column import UrbanColumn
from Products.urban.browser.table.tablevalue import BrainForUrbanTable
from Products.urban.browser.table.tablevalue import ObjectForUrbanTable
from Products.urban.browser.table.tablevalue import ValuesForUrbanListing

from Products.urban.interfaces import IUrbanEvent
from Products.urban.interfaces import IGenericLicence
from Products.urban.utils import getLicenceFolderId

import logging
logger = logging.getLogger('urban: Schedule')

from plone import api

from z3c.table.table import Table

from zope.i18n import translate
from zope.interface import implements


class ScheduleListingTable(Table):
    """
    Licence listing for schedule
    """
    implements(IScheduleListingTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    sortOn = None

    startBatchingAt = 15
    batchSize = 15
    batchProviderName = 'plonebatch'

    # add  __name__ to table to avoid traversal error
    # in OFS.absoluteurl. __str__
    __name__ = ''


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
        close_delay = schedule_item.isDelayGettingClose()
        css_class = 'ontime-event-delay'
        if delay < 0 and close_delay:
            css_class = 'warning-event-delay'
        if delay >= 0:
            css_class = 'late-event-delay'
        if delay == 9999:
            css_class = 'undefined-event-delay'
            cell = u'<div class="{css}" style="font-size:200%; text-align:center">\u221e</div>'.format(css=css_class)
        else:
            cell = u'<div class="{css}" style="text-align:center">{delay}</div>'.format(delay=delay, css=css_class)

        return cell


class DelayTerm(UrbanColumn):
    """ """
    implements(IDelayTerm)

    header = u'label_colname_delay_term'
    weight = -9

    def renderCell(self, schedule_item):
        delay_term = schedule_item.getDelayTerm()
        if delay_term is None:
            return '<div style="text-align:center" class="discreet">N.C.</div>'

        delay_term = delay_term.strftime('%d/%m/%Y')
        cell = u'<div style="text-align:center">{date}</div>'.format(date=delay_term)
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
        foldermanager = form_datas.get('foldermanager')
        sort_by_delay = not form_datas.get('sort_by_licence')

        sorted_events = []

        for licence, data in self.extractLicenceDatas(form_datas):
            event_brains = self.getUrbanEventsOfLicence(licence, data, foldermanager)
            events = [ItemForScheduleListing(event) for event in event_brains]
            events.sort(key=lambda event: -event.delay)
            sorted_events.extend(events)

        if sort_by_delay:
            sorted_events.sort(key=lambda event: -event.delay)

        return sorted_events

    def extractLicenceDatas(self, datas):
        licences = []
        for form_input, data in datas.iteritems():
            if form_input.startswith('events_'):
                null_value = data and len(data) == 1 and data[0]['event'] is None
                data = data is None and [{'event': 'all'}] or data
                if not null_value:
                    licence_type = form_input.split('_')[1]
                    data = [row['event'] for row in data]
                    licences.append((licence_type, data))

        return licences

    def getUrbanEventsOfLicence(self, licence_type, event_uids, foldermanager):
        catalog = api.portal.get_tool('portal_catalog')
        ref_catalog = api.portal.get_tool('reference_catalog')

        site = api.portal.getSite()
        site_path = '/'.join(site.getPhysicalPath())
        folder = getLicenceFolderId(licence_type)

        path = '{site_path}/urban/{folder}'.format(site_path=site_path, folder=folder)

        query_string = {
            'object_provides': IUrbanEvent.__identifier__,
            'review_state': 'in_progress',
            'path': {'query': path},
        }

        if foldermanager != 'all':
            if foldermanager == 'me' or not foldermanager:
                tool = api.portal.get_tool('portal_urban')
                current_fm = tool.getCurrentFolderManager(initials=False)
                foldermanager = current_fm and current_fm.UID() or None
            if foldermanager:
                query_string['folder_manager'] = foldermanager

        event_brains = catalog(query_string)

        to_return = []

        for brain in event_brains:
            relations = ref_catalog(sourceUID=brain.UID, relationship='UrbanEventType')
            if relations:
                eventtype_uid = relations[0].targetUID
                # eventtype 'schedulability' (means deadlinedelay > 0) is
                # indexed on the 'last_key_event' index
                schedulable = catalog(UID=eventtype_uid, last_key_event='schedulable')
                if schedulable and ('all' in event_uids or eventtype_uid in event_uids):
                    to_return.append(brain)

        return to_return


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
        self.delay, self.delay_term, self.close_delay = self._computeDelay(event)

    def _computeDelay(self, event):
        event = self.event
        event_type = event.getUrbaneventtypes()
        alert_delay = event_type.getAlertDelay()
        delay_term = self._computeDelayTerm(event, event_type)
        if delay_term is None:
            return 9999, None, False

        delay = DateTime() - delay_term
        close_delay = -alert_delay < delay < 0

        return int(delay), delay_term, close_delay

    def _computeDelayTerm(self, event, event_type):

        TALformula = event_type.getDelayComputation().strip()

        deadline_delay = event_type.getDeadLineDelay()
        event_date = event.getEventDate()

        if event_date:
            deadline = deadline_delay + event_date
        else:
            deadline = None

        if TALformula:
            data = {
                'self': event_type,
                'event': event,
                'licence': self.licence.getObject(),
            }
            ctx = getEngine().getContext(data)
            try:
                deadline = Expression(TALformula)(ctx)
            except Exception, e:
                logger.warn("The formula delay '%s' defined for event type '%s' is wrong!  Message is : %s" % (TALformula, event_type.absolute_url(), e))
                return None
        return deadline

    def getEvent(self):
        return self.event

    def getLicence(self):
        return self.licence

    def getEventTimeDelay(self):
        return self.delay

    def getDelayTerm(self):
        return self.delay_term

    def isDelayGettingClose(self):
        return self.close_delay

    def getEventDates(self):
        def formatDate(date):
            if date is None:
                return '<span class="discreet">N.C.</span>'
            return date.strftime('%d/%m/%Y')

        event = self.event
        event_date = formatDate(event.getEventDate())
        event_type = event.getUrbaneventtypes()
        request = api.portal.getRequest()

        dates = [{
            'date_label': event_type.getEventDateLabel().decode('utf-8'),
            'date': event_date
        }]

        for fieldname in event_type.getActivatedFields():
            field = event.getField(fieldname)
            if field and field.type == 'datetime':
                date = formatDate(field.get(event))
                date_label = translate(
                    _(field.widget.label_msgid),
                    'urban', context=request
                )
                dates.append({'date_label': date_label, 'date': date})

        return dates
