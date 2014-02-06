# -*- coding: utf-8 -*-

from plone.memoize import view
from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.urban.UrbanEventInquiry import UrbanEventInquiry_schema
from Products.urban.interfaces import IUrbanEvent
from Products.urban.browser.table.urbantable import ContactTable, ParcelsTable, EventsTable


class LicenceView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request

    @view.memoize
    def getCatalog(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_catalog')

    @view.memoize
    def getPortalUrban(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_urban')

    @view.memoize
    def getMember(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@plone_portal_state/member')()

    def getLicenceMainTemplateMacro(self):
        """
        """
        context = aq_inner(self.context)
        main_template_macro = context.unrestrictedTraverse('licencemainmacro/main')
        return main_template_macro

    def getUrbanEventTypes(self):
        licence = aq_inner(self.context)
        config_id = licence.portal_type.lower()
        portal_urban = self.getPortalUrban()

        eventtypes = portal_urban.listEventTypes(licence, urbanConfigId=config_id)
        return eventtypes

    def canAddUrbanEvent(self):
        licence = aq_inner(self.context)
        member = self.getMember()

        eventtypes = self.getUrbanEventTypes()
        has_permission = member.has_permission('urban: Add UrbanEvent', licence)
        return eventtypes and has_permission

    def canAddAllAdvices(self):
        licence = aq_inner(self.context)
        member = self.getMember()

        all_advices = licence.getAllAdvices()
        has_permission = member.has_permission('urban: Add UrbanEvent', licence)
        return all_advices and has_permission

    def getAdviceTitles(self):
        licence = aq_inner(self.context)
        all_advices = licence.getAllAdvices()
        advice_titles = [advice.Title() for advice in all_advices]
        advice_titles = ', '.join(advice_titles)
        return advice_titles

    def renderListing(self, table):
        table.update()
        return table.render()

    def renderContactListing(self):
        if not self.context.getApplicants():
            return ''
        contacttable = ContactTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ''
        parceltable = ParcelsTable(parcels, self.request)
        return self.renderListing(parceltable)

    def renderEventsListing(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        queryString = {
            'object_provides': 'Products.urban.interfaces.IUrbanEvent',
            'path': '/'.join(self.context.getPhysicalPath()),
            'sort_on': 'getObjPositionInParent',
            'sort_order': 'reverse',
        }
        events = catalog(queryString)
        if not events:
            return ''
        eventtable = EventsTable(events, self.request)
        return self.renderListing(eventtable)

    def getLicenceConfig(self):
        context = aq_inner(self.context)
        return context.getLicenceConfig()

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = '{}_macro'.format(tab)
        macros_view = self.getMacroViewName()
        macro = context.unrestrictedTraverse('{view}/{macro}'.format(view=macros_view, macro=macro_name))
        return macro

    def getMacroViewName(self):
        return 'licencetabs-macros'

    def getTabs(self):
        return self.getLicenceConfig().getActiveTabs()

    def getUseTabbing(self):
        return self.getLicenceConfig().getUseTabbingForDisplay()

    def getUsedAttributes(self):
        return self.getLicenceConfig().getUsedAttributes()

    def hasOutdatedParcels(self):
        context = aq_inner(self.context)
        portal_workflow = getToolByName(self, 'portal_workflow')
        if portal_workflow.getInfoFor(self.context, 'review_state') in ['accepted', 'refused']:
            return False
        return any([not parcel.getIsOfficialParcel for parcel in context.listFolderContents(contentFilter={"portal_type": "PortionOut"})])

    def getKeyDates(self):
        context = aq_inner(self.context)
        catalog = self.getCatalog()
        urban_tool = self.getPortalUrban()
        config = context.getLicenceConfig()
        ordered_dates = []
        key_dates = {}
        dates = {}

        # search in the config for all the Key urbaneventtypes and their key dates
        for eventtype in config.urbaneventtypes.objectValues():
            if eventtype.getIsKeyEvent():
                displaylist = eventtype.listActivatedDates()
                keydates = [(date, displaylist.getValue(date)) for date in eventtype.getKeyDates()]
                ordered_dates.append((eventtype.UID(), eventtype.getKeyDates()))
                key_dates[eventtype.UID()] = keydates
                dates[eventtype.UID()] = dict([(date[0], {
                    'dates': [],
                    'label': date[0] == 'eventDate' and eventtype.Title() or '%s (%s)' % (eventtype.Title().decode('utf8'), date[1])
                }) for date in keydates])

        # now check each event to see if its a key Event, if yes, we gather the key date values found on this event
        linked_eventtype_field = UrbanEventInquiry_schema.get('urbaneventtypes')
        event_brains = catalog(
            path={'query': '/'.join(context.getPhysicalPath())},
            object_provides=IUrbanEvent.__identifier__,
            sort_on='created',
            sort_order='ascending'
        )

        for event_brain in event_brains:
            event = event_brain.getObject()
            eventtype_uid = linked_eventtype_field.getRaw(event)
            if eventtype_uid in dates.keys() and not dates[eventtype_uid].get('url', ''):
                for date in key_dates[eventtype_uid]:
                    date_value = getattr(event, date[0])
                    dates[eventtype_uid][date[0]]['dates'].append({
                        'url': event_brain.getPath(),
                        'date':  date_value and urban_tool.formatDate(date_value, translatemonth=False) or None,
                    })

        # flatten the result to a list before returning it
        dates_list = []
        for uid, date_names in ordered_dates:
            for date in date_names:
                dates_list.append(dates[uid].get(date, None))
        return dates_list

    def getInquiryDates(self):
        """
          return the start/end dates of each inquiry and a link to its corresponding urbanEventInquiry (if it exists)
        """
        context = aq_inner(self.context)
        urban_tool = self.getPortalUrban()
        inquirydates = []
        for inquiry in context.getInquiries():
            start_date = inquiry.getInvestigationStart()
            end_date = inquiry.getInvestigationEnd()
            inquiry_event = [inq_event for inq_event in context.objectValues('UrbanEventInquiry') if inq_event.getLinkedInquiry() == inquiry]
            inquirydates.append({
                'start_date': start_date and urban_tool.formatDate(start_date, translatemonth=False) or None,
                'end_date': end_date and urban_tool.formatDate(end_date, translatemonth=False) or None,
                'url': inquiry_event and inquiry_event[0].absolute_url() or None,
            })
        return inquirydates

    def getSchemataFields(self, schemata='', exclude=[]):
        def isDisplayable(field):
            if hasattr(field, 'optional') and field.optional and field.getName() not in displayed_fields:
                return False
            if field.getName() in exclude:
                return False
            if not field.widget.visible:
                return False
            return True

        displayed_fields = self.getUsedAttributes()
        context = aq_inner(self.context)
        schema = context.__class__.schema
        fields = [field for field in schema.getSchemataFields(schemata) if isDisplayable(field)]

        return fields

    def getDescriptionFields(self, exclude=[]):
        return self.getSchemataFields('urban_description', exclude)

    def getRoadFields(self, exclude=[]):
        return self.getSchemataFields('urban_road', exclude)

    def getLocationFields(self, exclude=[]):
        return self.getSchemataFields('urban_location', exclude)

    def getInquiryFields(self, exclude=[]):
        return self.getSchemataFields('urban_investigation_and_advices', exclude)


class EnvironmentLicenceView(LicenceView):
    """
      This manage helper methods for all environment licences views
    """
    def __init__(self, context, request):
        super(EnvironmentLicenceView, self).__init__(context, request)

    def getInquiriesForDisplay(self):
        """
          Returns the inquiries to display on the buildlicence_view
          This will move to the buildlicenceview when it will exist...
        """
        context = aq_inner(self.context)
        inquiries = context.getInquiries()
        if not inquiries:
            #we want to display at least the informations about the inquiry
            #defined on the licence even if no data have been entered
            inquiries.append(context)
        return inquiries

    def getRubrics(self):
        """
        display the rubrics number, their class and then the text
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        rubric_uids = context.getField('rubrics').getRaw(context)
        rubric_brains = catalog(UID=rubric_uids)
        rubrics = [brain.getObject() for brain in rubric_brains]
        rubrics_display = ['<p>%s</p>%s' % (rub.getNumber(), rub.Description()) for rub in rubrics]
        return rubrics_display

    def _sortConditions(self, conditions):
        """
        sort exploitation conditions in this order: CI/CS, CI, CS
        """
        order = ['CI/CS', 'CI', 'CS', 'CS-Eau']
        sorted_conditions = dict([(val, [],) for val in order])
        for cond in conditions:
            val = cond.getExtraValue()
            sorted_conditions[val].append({'type': val, 'url': cond.absolute_url() + '/description/getRaw', 'title': cond.Title()})
        sort = []
        for val in order:
            sort.extend(sorted_conditions[val])
        return sort

    def getMinimumConditions(self):
        """
        sort the conditions from the field 'minimumLegalConditions'  by type (integral, sectorial, ...)
        """
        context = aq_inner(self.context)
        min_conditions = context.getMinimumLegalConditions()
        return self._sortConditions(min_conditions)

    def getAdditionalConditions(self):
        """
        sort the conditions from the field 'additionalLegalConditions'  by type (integral, sectorial, ...)
        """
        context = aq_inner(self.context)
        sup_conditions = context.getAdditionalLegalConditions()
        return self._sortConditions(sup_conditions)
