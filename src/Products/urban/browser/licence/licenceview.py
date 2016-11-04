# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five import BrowserView

from Products.urban import utils
from Products.urban.UrbanEventInquiry import UrbanEventInquiry_schema
from Products.urban.browser.table.urbantable import ApplicantTable
from Products.urban.browser.table.urbantable import AttachmentsTable
from Products.urban.browser.table.urbantable import EventsTable
from Products.urban.browser.table.urbantable import NestedAttachmentsTable
from Products.urban.browser.table.urbantable import ParcelsTable
from Products.urban.browser.table.urbantable import ProprietaryTable
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IUrbanDoc
from Products.urban.interfaces import IUrbanEvent

from plone import api
from plone.memoize import view


class LicenceView(BrowserView):
    """
    Base class for licences browser views.
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

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
        portal_urban = api.portal.get_tool('portal_urban')

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

    def mayAddAttachment(self):
        context = aq_inner(self.context)
        member = api.portal.get_tool('portal_membership').getAuthenticatedMember()
        if member.has_permission('ATContentTypes: Add File', context):
            return True
        return False

    def getInquiryReclamationNumbers(self):

        inquiryReclamationNumbers = []
        context = aq_inner(self.context)
        totalOral = 0
        totalWrite = 0
        if context.getClaimants():
            for claimant in context.getClaimants():
                if claimant.getClaimType() == 'oralClaim':
                    totalOral += 1
                elif claimant.getClaimType() == 'writedClaim':
                    totalWrite += 1

        inquiryReclamationNumbers.append(totalOral)
        inquiryReclamationNumbers.append(totalWrite)
        return inquiryReclamationNumbers

    def renderAttachmentsListing(self):
        licence = aq_inner(self.context)
        queryString = {
            'portal_type': 'File',
            'path': {
                'query': '/'.join(licence.getPhysicalPath()),
                'depth': 1,
            },
            'sort_on': 'created'
        }
        catalog = api.portal.get_tool('portal_catalog')
        attachments = catalog(queryString)
        if not attachments:
            return ''
        table = AttachmentsTable(attachments, self.request)
        return self.renderListing(table)

    def renderNestedAttachmentsListing(self):
        licence = aq_inner(self.context)
        path = '/'.join(licence.getPhysicalPath())
        queryString = {
            'portal_type': 'File',
            'path': {
                'query': path,
                'depth': 2,
            },
            'sort_on': 'created'
        }
        catalog = api.portal.get_tool('portal_catalog')
        attachments = catalog(queryString)
        path_len = len(path.split('/'))
        nested_attachments = []
        for brain in attachments:
            attachment = brain.getObject()
            is_not_doc = not IUrbanDoc.providedBy(attachment)
            is_nested = len(brain.getPath().split('/')) > path_len + 1
            if is_nested and is_not_doc:
                nested_attachments.append(attachment)

        if not nested_attachments:
            return ''
        table = NestedAttachmentsTable(nested_attachments, self.request)
        return self.renderListing(table)

    def getAdviceTitles(self):
        licence = aq_inner(self.context)
        all_advices = licence.getAllAdvices()
        advice_titles = [advice.Title() for advice in all_advices]
        advice_titles = ', '.join(advice_titles)
        return advice_titles

    def renderListing(self, table):
        table.update()
        return table.render()

    def renderApplicantListing(self):
        if not self.context.getApplicants():
            return ''
        contacttable = ApplicantTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderProprietaryListing(self):
        if not self.context.getProprietaries():
            return ''
        contacttable = ProprietaryTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ''
        parceltable = ParcelsTable(parcels, self.request)
        return self.renderListing(parceltable)

    def renderEventsListing(self):
        catalog = api.portal.get_tool('portal_catalog')
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
        if api.content.get_state(self.context) in ['accepted', 'refused']:
            return False
        return any([not parcel.getIsOfficialParcel for parcel in context.listFolderContents(contentFilter={"portal_type": "PortionOut"})])

    def getKeyDates(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool('portal_catalog')
        urban_tool = api.portal.get_tool('portal_urban')
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
        urban_tool = api.portal.get_tool('portal_urban')
        inquirydates = []
        for inquiry in context.getInquiries():
            event = [inq_event for inq_event in context.objectValues('UrbanEventInquiry') if inq_event.getLinkedInquiry() == inquiry]
            event = event and event[0] or None
            start_date = event and event.getInvestigationStart() or None
            end_date = event and event.getInvestigationEnd() or None
            inquirydates.append({
                'start_date': start_date and urban_tool.formatDate(start_date, translatemonth=False) or None,
                'end_date': end_date and urban_tool.formatDate(end_date, translatemonth=False) or None,
                'url': event and event.absolute_url() or None,
            })
        return inquirydates

    def getSchemataFields(self, schemata='', exclude=[]):
        displayed_fields = self.getUsedAttributes()
        return utils.getSchemataFields(self.context, displayed_fields, schemata, exclude)

    def getDescriptionFields(self, exclude=[]):
        return self.getSchemataFields('urban_description', exclude)

    def getAnalysisFields(self, exclude=[]):
        return self.getSchemataFields('urban_analysis', exclude)

    def getRoadFields(self, exclude=[]):
        return self.getSchemataFields('urban_road', exclude)

    def getLocationFields(self, exclude=[]):
        return self.getSchemataFields('urban_location', exclude)

    def getAdviceFields(self, exclude=[]):
        return self.getSchemataFields('urban_advices', exclude)

    def getInquiryFields(self, exclude=[]):
        return self.getSchemataFields('urban_inquiry', exclude)

    def get_state(self):
        return api.content.get_state(self.context)


class UrbanCertificateBaseView(LicenceView):
    """
      This manage the view of UrbanCertificate and NotaryLetter Classes
    """
    def __init__(self, context, request):
        super(UrbanCertificateBaseView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getSpecificFeatures(self, subtype=''):
        context = aq_inner(self.context)
        accessor = getattr(context, 'get%sSpecificFeatures' % subtype.capitalize())
        specific_features = accessor()
        return [spf.get('value', spf['text']) for spf in specific_features if not 'check' in spf or spf['check']]


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
        catalog = api.portal.get_tool('portal_catalog')
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
            sorted_conditions[val].append(
                {
                    'type': val,
                    'url': cond.absolute_url() + '/description/getRaw',
                    'title': cond.Title()
                }
            )
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


class ShowEditTabbing(BrowserView):
    """ call this view to see if a licence should display the tabbing with edit icons """

    def __call__(self):

        # this view is registered for any kind of content (because fuck you thats why)
        # we do the check if we are a licence inside the call
        if not IGenericLicence.providedBy(self.context):
            return

        member = api.user.get_current()
        licence = self.context
        show_tabbing = member.has_permission('Modify portal content', licence)
        return show_tabbing
