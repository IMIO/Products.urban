# -*- coding: utf-8 -*-

from plone.memoize import view
from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import utranslate
from Products.urban.indexes import genericlicence_parcelinfoindex
from Products.urban.UrbanEventInquiry import UrbanEventInquiry_schema
from Products.urban.interfaces import IUrbanEvent

class LicenceView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
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

    def getLicenceConfig(self):
        context = aq_inner(self.context)
        return context.getLicenceConfig()

    def getMacro(self, tab):
        context = aq_inner(self.context)
        portal_type = context.portal_type.lower()
        if tab in ['description', 'road', 'location', 'peb']:
            return context.unrestrictedTraverse('@@%s-macros/%sMacro' % (portal_type, tab))
        else:
            url_tool = getToolByName(context, 'portal_url')
            site = url_tool.getPortalObject()
            urban_macros = site.urban_macros
            if tab == 'investigation_and_advices':
                return urban_macros.macros['urbanInquiriesMacro']
            else:
                return urban_macros.macros['urbanEventsMacro']

    def getTabs(self):
        return self.getLicenceConfig().getActiveTabs()

    def getEmptyTabs(self):
        tabnames = ['urban_location', 'urban_road']
        return [tabname for tabname in tabnames if self.isEmptyTab(tabname)]

    def isEmptyTab(self, tab_name):
        context = aq_inner(self.context)
        urban_tool = self.getPortalUrban()
        used_fields_names = set(getattr(urban_tool, context.getPortalTypeName().lower()).getUsedAttributes())
        if used_fields_names :
            for field in context.schema.getSchemataFields(tab_name):
                if field.getName() in used_fields_names:
                    return False
        return True

    def hasOutdatedParcels(self):
        context = aq_inner(self.context)
        portal_workflow = getToolByName(self, 'portal_workflow')
        if portal_workflow.getInfoFor(self.context, 'review_state') in ['accepted', 'refused',]:
            return False
        return any([not parcel.getIsOfficialParcel for parcel in context.listFolderContents(contentFilter={"portal_type" : "PortionOut"})])

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
                keydates = [(date, displaylist.getValue(date)) for  date in eventtype.getKeyDates()]
                ordered_dates.append((eventtype.UID(), eventtype.getKeyDates()))
                key_dates[eventtype.UID()] = keydates
                dates[eventtype.UID()] = dict([(date[0], {
                    'date':None,
                    'label': date[0] == 'eventDate' and eventtype.Title() or '%s (%s)' % (eventtype.Title().decode('utf8'), date[1])
                    }) for date in keydates])
        # now check each event to see if its a key Event, if yes, we gather the key date values found on this event
        linked_eventtype_field = UrbanEventInquiry_schema.get('urbaneventtypes')
        for event_brain in catalog(path={'query':'/'.join(context.getPhysicalPath())}, object_provides=IUrbanEvent.__identifier__, sort_on='created', sort_order='descending'):
            event = event_brain.getObject()
            eventtype_uid = linked_eventtype_field.getRaw(event)
            if eventtype_uid in dates.keys() and not dates[eventtype_uid].get('url', ''):
                for date in key_dates[eventtype_uid]:
                    date_value = getattr(event, date[0])
                    dates[eventtype_uid][date[0]].update({
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
                'start_date':start_date and urban_tool.formatDate(start_date, translatemonth=False) or None,
                'end_date':end_date and urban_tool.formatDate(end_date, translatemonth=False) or None,
                'url': inquiry_event and inquiry_event[0].absolute_url() or None,
                })
        return inquirydates


class LicenceMacros(BrowserView):
    """
      This manage the macros of BuildLicence
    """
