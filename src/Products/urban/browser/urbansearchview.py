from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as msg
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import URBAN_TYPES 
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
                              inUrbanConfig=False, allowedStates=['enabled', 'disabled'])
        return voc.getDisplayList(context).sortedByValue().items()

    def getLicenceTypes(self):
        return URBAN_TYPES

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
                        'applicant':self.getSearchArgument('applicant'),
                        'parcel':self.getSearchArgument(['section', 'radical', 'bis', 'exposant', 'puissance', 'partie']),
                    }  
        if search_by == 'street':
            return self.searchByStreet(foldertypes, arguments.get(search_by, []))
        elif search_by == 'applicant':
            return self.searchByApplicant(foldertypes, arguments.get(search_by, []))
        elif search_by == 'parcel':
            return self.searchByParcel(foldertypes, arguments.get(search_by, []))
        return None

    def searchByApplicant(self, foldertypes, applicant_infos_index):
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
        parcelInfos = ','.join(parcel_infos_index[:-1])
        if parcel_infos_index[-1] == 'on':
            parcelInfos = ',%s,1' %parcelInfos
        else:
            parcelInfos = ',%s,0' %parcelInfos
        res = catalogTool(portal_type=foldertypes, parcelInfosIndex= parcelInfos)
        return res

class UrbanSearchMacros(BrowserView):
    """
      This manage the macros of UrbanSearch
    """
