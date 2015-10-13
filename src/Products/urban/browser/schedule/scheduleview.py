# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.browser.schedule.form import ScheduleForm
from Products.urban.browser.schedule.table import ItemForScheduleListing
from Products.urban.browser.schedule.table import ScheduleListingTable
from Products.urban.browser.schedule.table import ScheduleListingTableForLicence

from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import getCurrentFolderManager
from Products.urban.utils import getLicenceFolderId

from five import grok

from plone import api

from plone.z3cform.z2 import switch_on

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import Interface

grok.templatedir('templates')


class ScheduleView(grok.View):
    """
      This manages urban schedule view
    """
    grok.context(Interface)
    grok.name('schedule')
    grok.require('zope2.View')

    template = ViewPageTemplateFile('templates/scheduleview.pt')

    def __init__(self, context, request):
        super(ScheduleView, self).__init__(context, request)
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def refreshBatch(self, batch_start):
        # switch_on(self)
        self.schedulelisting.batchStart = batch_start
        self.schedulelisting.update()

        super(ScheduleView, self).update()

    def update(self):
        switch_on(self)

        self.form = ScheduleForm(self.context, self.request)

        # Restrict the form inputs to the licences managed by the current
        # forder manager
        self._restrictFormFieldsToAllowedLicences()
        self.form.update()

        self.schedulelisting = ScheduleListingTable(self, self.request)
        self.schedulelisting.update()

        super(ScheduleView, self).update()

    def _restrictFormFieldsToAllowedLicences(self):
        foldermanager = getCurrentFolderManager()

        if not foldermanager:
            return

        managed_licences = foldermanager.getManageableLicences()
        fields = self.form.fields
        fields_name_to_display = ['events_{}'.format(licencetype.lower()) for licencetype in managed_licences]
        fields_name_to_hide = [
            field_name for field_name in fields.keys() if
            field_name.startswith('events_') and field_name not in fields_name_to_display
        ]

        displayed_fields = fields.omit(*fields_name_to_hide)

        self.form.fields = displayed_fields

    def isSearchFormSubmittted(self):
        form_inputs = self.form.extractData()[0]
        form_is_submitted = any(form_inputs.values())

        return form_is_submitted

    def values(self):
        if self.isSearchFormSubmittted():
            events = self.searchScheduledEvents()
        else:
            events = self.getDefaultScheduledEvents()
        return events

    def getDefaultScheduledEvents(self):
        foldermanager = getCurrentFolderManager()
        events = []

        if not foldermanager:
            return events

        licence_types = foldermanager.getManageableLicences()
        for licence_type in licence_types:
            event_brains = self.findSchedulableUrbanEvents(licence_type, ['all'], foldermanager.UID())
            events.extend([ItemForScheduleListing(event) for event in event_brains])

        events.sort(key=lambda event: -event.delay)

        return events

    def searchScheduledEvents(self):
        form_datas = self.form.extractData()[0]
        foldermanager_uid = form_datas.get('foldermanager')
        sort_by_delay = not form_datas.get('sort_by_licence')
        no_duplicated_licences = form_datas.get('no_duplicated_licences')

        sorted_events = []

        for licence, eventtype_uids in self.extractLicenceDatas(form_datas):
            event_brains = self.findSchedulableUrbanEvents(licence, eventtype_uids, foldermanager_uid)
            events = [ItemForScheduleListing(event) for event in event_brains]
            events.sort(key=lambda event: -event.delay)
            sorted_events.extend(events)

        if no_duplicated_licences:
            licences_found = set()
            tmp = []
            for event in sorted_events:
                if event.licence.UID not in licences_found:
                    tmp.append(event)
                    licences_found.add(event.licence.UID)
            sorted_events = tmp

        if sort_by_delay:
            sorted_events.sort(key=lambda event: -event.delay)

        return sorted_events

    def extractLicenceDatas(self, datas):
        licences = []
        for form_input, data in datas.iteritems():
            if form_input.startswith('events_'):
                if data[0]['event'] is not None:
                    licence_type = form_input.split('_')[1]
                    data = [row['event'] for row in data]
                    licences.append((licence_type, data))

        return licences

    def findSchedulableUrbanEvents(self, licence_type, eventtype_uids, foldermanager_uid='all'):
        """
         Input: a licence_type, eventtypes uids  and a foldermanager
         Returns all the UrbanEvent brains having their eventtype in eventtype_uids
         such as the parent licence portal_type is  'licence_type' and that licence
         foldermanager is 'foldermanager'.
        """
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

        if foldermanager_uid != 'all':
            if foldermanager_uid == 'me':
                foldermanager_uid = getCurrentFolderManager().UID()
            query_string['folder_manager'] = foldermanager_uid

        event_brains = catalog(query_string)

        to_return = []

        for brain in event_brains:
            relations = ref_catalog(sourceUID=brain.UID, relationship='UrbanEventType')
            if relations:
                eventtype_uid = relations[0].targetUID
                # eventtype 'schedulability' (means deadlinedelay > 0) is
                # indexed on the 'last_key_event' index
                schedulable = catalog(UID=eventtype_uid, last_key_event='schedulable')
                all_events = 'all' in eventtype_uids
                selected_event = eventtype_uid in eventtype_uids
                all_opinions_request = 'all_opinions' in eventtype_uids and brain.portal_type == 'UrbanEventOpinionRequest'
                if schedulable and (all_events or selected_event or all_opinions_request):
                    to_return.append(brain)

        return to_return


class EventsListingForLicenceView(BrowserView):
    """ """

    def __init__(self, context, request):
        super(EventsListingForLicenceView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderScheduledEventsListing(self):
        listing = ScheduleListingTableForLicence(self, self.request)
        listing.update()
        listing_html = u'{}'.format(listing.render())
        return listing_html

    def values(self):
        """ """
        catalog = api.portal.get_tool('portal_catalog')
        ref_catalog = api.portal.get_tool('reference_catalog')
        licence = self.context

        event_brains = catalog(
            object_provides=IUrbanEvent.__identifier__,
            review_state='in_progress',
            path={'query': '/'.join(licence.getPhysicalPath())},
        )

        to_return = []

        for brain in event_brains:
            relations = ref_catalog(sourceUID=brain.UID, relationship='UrbanEventType')
            if relations:
                eventtype_uid = relations[0].targetUID
                # eventtype 'schedulability' (means deadlinedelay > 0) is
                # indexed on the 'last_key_event' index
                schedulable = catalog(UID=eventtype_uid, last_key_event='schedulable')
                if schedulable:
                    to_return.append(brain)

        to_return = [ItemForScheduleListing(event) for event in to_return]

        return to_return
