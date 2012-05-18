from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as msg
from Products.CMFPlone.PloneBatch import Batch
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import URBAN_TYPES
from Products.urban.UrbanTool import DB_QUERY_ERROR
from Products.ZCTextIndex.ParseTree import ParseError

class UrbanSearchView(BrowserView):
    """
      This manage the view of UrbanSearch
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def AvailableStreets(self):
        context = aq_inner(self.context)
        voc = UrbanVocabulary('streets', vocType=("Street", "Locality", ), id_to_use="UID", sort_on="sortable_title",
                              inUrbanConfig=False, allowedStates=['enabled', 'disabled'], with_empty_value=True)
        return voc.getDisplayList(context).items()

    def getLicenceTypes(self):
        return URBAN_TYPES

    def getContactTypes(self):
        return ['Architect', 'Notary', 'Geometrician']

    def getDivisions(self):
        """
          Returns the existing divisions
          If we had a problem getting the divisions, we return nothing so the
          search form is not displayed
        """
        context = aq_inner(self.context)
        tool = getToolByName(context, 'portal_urban')
        divisions = tool.findDivisions(all=False)
        #check that we correctly received divisions
        if DB_QUERY_ERROR in str(divisions):
            return None
        return divisions

    def getSearchArgument(self, key_to_match):
        request = aq_inner(self.request)
        if type(key_to_match) == list:
            return [request.get(key, '') for key in key_to_match]
        request = aq_inner(self.request)
        return request.get(key_to_match, '')

    def searchLicence(self):
        """
          Find licences with given paramaters
        """
        request = aq_inner(self.request)
        search_by = request.get('search_by', '')
        foldertypes = request.get('foldertypes', [])
        arguments = {
                        'street':self.getSearchArgument('street'),
                        'name':self.getSearchArgument(['name', 'contacttypes']),
                        'parcel':self.getSearchArgument(['division','section', 'radical', 'bis', 'exposant', 'puissance', 'partie']),
                    }
        if search_by == 'street':
            res = self.searchByStreet(foldertypes, arguments.get(search_by, []))
        elif search_by == 'name':
            res = self.searchByName(foldertypes, arguments.get(search_by, []))
        elif search_by == 'parcel':
            res = self.searchByParcel(foldertypes, arguments.get(search_by, []))
        else:
            return None
        batch = Batch(res, len(res), 0, orphan=0)
        return batch

    def searchByName(self, foldertypes, arguments):
        """
          Find licences by name and by contact categories
        """
        name = arguments[0]
        contact_types = arguments[1]
        if not type(contact_types) == list:
            contact_types = [contact_types]
        result_uids = set()
        result = []
        for contact_type in contact_types:
            if contact_type == 'Applicant':
                sub_result = self.searchByApplicantName(foldertypes, name)
            else:
                sub_result = self.searchByContactName(foldertypes, name, contact_type)
            for brain in sub_result:
                if brain.UID not in result_uids:
                    result_uids.add(brain.UID)
                    result.append(brain)
        return result

    def searchByContactName(self, foldertypes, name, contact_type):
        """
          Find licences by contact type and by name
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        contacts = licence_ids = []
        try:
            contacts = [brain.getObject() for brain in catalogTool(portal_type=contact_type, SearchableText=name)]
        except ParseError:
            #in case something like '*' is entered, ZCTextIndex raises an error...
            ptool = getToolByName(self, "plone_utils")
            ptool.addPortalMessage(msg(u"please_enter_more_letters"), type="info")
            pass
        for contact in contacts:
            licence_ids.extend([ref.getId() for ref in contact.getBRefs()])
        return catalogTool(portal_type=foldertypes, id=licence_ids)

    def searchByApplicantName(self, foldertypes, applicant_infos_index):
        """
          Find licences with applicant paramaters
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        res = []
        try:
            res = catalogTool(portal_type=foldertypes, applicantInfosIndex=applicant_infos_index)
            return res
        except ParseError:
            #in case something like '*' is entered, ZCTextIndex raises an error...
            ptool = getToolByName(self, "plone_utils")
            ptool.addPortalMessage(msg(u"please_enter_more_letters"), type="info")
            return res

    def searchByStreet(self, foldertypes, sreets_uid):
        """
          Find licences with location paramaters
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        res = catalogTool(portal_type=foldertypes, StreetsUID=sreets_uid)
        return res

    def searchByParcel(self, foldertypes, parcel_infos_index):
        """
          Find licences with parcel paramaters
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        res = []
        if parcel_infos_index[-1] == 'on':
            parcel_infos_index[-1] = '1'
        else:
            parcel_infos_index[-1] = '0'
        parcelInfos = [','.join(parcel_infos_index)]
        #boilerplate to handle the case where the parcels in the licences have no values for bis and exposant
        if parcel_infos_index[3] == '0':
            parcelInfos.append('%s,,%s' % (','.join(parcel_infos_index[:3]), ','.join(parcel_infos_index[4:])))
        if parcel_infos_index[5] == '0':
            parcelInfos.append('%s,,%s' % (','.join(parcel_infos_index[:5]), parcel_infos_index[6]))
        if parcel_infos_index[3] == '0' and parcel_infos_index[5] == '0':
            parcelInfos.append('%s,,%s,,%s' % (','.join(parcel_infos_index[:3]), parcel_infos_index[4], parcel_infos_index[6]))
        #boilerplate end
        res = catalogTool(portal_type=foldertypes, parcelInfosIndex= parcelInfos)
        return res

class UrbanSearchMacros(BrowserView):
    """
      This manage the macros of UrbanSearch
    """
