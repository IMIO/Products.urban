# -*- coding: utf-8 -*-

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

    def getReceiptDate(self):
        """
          Returns the receiptDate
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        lastDeposit = context.getLastDeposit()
        if not lastDeposit or not lastDeposit.getEventDate():
            return None
        dict = {
                'url': lastDeposit.absolute_url(),
                'date': tool.formatDate(lastDeposit.getEventDate(), translatemonth=False)
               }
        return dict

    def getTheLicenceDate(self):
        """
          Returns the last licence notification date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        theLicence = context.getLastTheLicence()
        if not theLicence or not theLicence.getEventDate():
            return None
        dict = {
                'url': theLicence.absolute_url(),
                'date': tool.formatDate(theLicence.getEventDate(), translatemonth=False)
               }
        return dict

    def getEmptyTabs(self):
        tabnames = ['urban_location', 'urban_road']
        return [tabname for tabname in tabnames if self.isEmptyTab(tabname)]

    def isEmptyTab(self, tab_name):
        context = aq_inner(self.context)
        urban_tool = getToolByName(context, 'portal_urban')
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
        return any([parcel.getOutdated() for parcel in context.listFolderContents(contentFilter={"portal_type" : "PortionOut"})])

    def getKeyDates(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        urban_tool = getToolByName(context, 'portal_urban')
        config = urban_tool.getUrbanConfig(context)
        ordered_dates = []
        key_dates = {}
        dates = {}
        # search in the config for all the Key urbaneventtypes and their key dates
        for eventtype in config.urbaneventtypes.listFolderContents():
            if eventtype.getIsKeyEvent():
                displaylist = eventtype.listActivatedDates()
                keydates = [(date, displaylist.getValue(date)) for  date in eventtype.getKeyDates()]
                ordered_dates.append((eventtype.UID(), eventtype.getKeyDates()))
                key_dates[eventtype.UID()] = keydates
                dates[eventtype.UID()] = {}
        # now check each event to see if its a key Event, if yes, we gather the key date values found on this event
        linked_eventtype_field = UrbanEventInquiry_schema.get('urbaneventtypes')
        for event_brain in catalog(path={'query':context.absolute_url_path()}, object_provides=IUrbanEvent.__identifier__, sort_on='created', sort_order='descending'):
            event = event_brain.getObject()
            eventtype_uid = linked_eventtype_field.getRaw(event)
            if eventtype_uid in dates.keys() and not dates[eventtype_uid]:
                for date in key_dates[eventtype_uid]:
                    date_value = getattr(event, date[0])
                    dates[eventtype_uid][date[0]] = {
                          'url': event_brain.getPath(),
                          'date':  date_value and urban_tool.formatDate(date_value, translatemonth=False) or None,
                          'label': date[1],
                          'event': event_brain.Title,
                          }
        # flatten the result to a list before returning it
        dates_list = []
        for uid, date_names in ordered_dates:
            for date in date_names:
                if dates[uid]:
                    dates_list.append(dates[uid][date])
                else:
                    dates_list.append(None)
        return dates_list



class LicenceMacros(BrowserView):
    """
      This manage the macros of BuildLicence
    """
