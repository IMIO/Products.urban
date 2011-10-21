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

    def getSearchArgumentByKey(self, key_to_match):
        request = aq_inner(self.request)
        try:
            keys = [request['search_arg'][i] for i in range(len(request['search_arg'])) if i % 2 == 0]
            values = [request['search_arg'][i] for i in range(len(request['search_arg'])) if i % 2 != 0]
            for i in range(len(keys)):
                if keys[i] == key_to_match: 
                    return values[i]
        except:
            pass
        return ''

    def searchLicence(self):
        """
          Find licences with given paramaters
        """
        request = aq_inner(self.request)
        search_by = request.get('search_by', '')
        foldertypes = request.get('foldertypes', [])
        criteria_name= [request['search_arg'][i] for i in range(len(request.get('search_arg', []))) if i % 2 == 0]
        criteria_values = [request['search_arg'][i] for i in range(len(request.get('search_arg', []))) if i % 2 != 0]
        arguments = {}  
        for i in range(len(criteria_name)):
            arguments[criteria_name[i]] = criteria_values[i]
        if search_by == 'street':
            return self.searchByStreet(foldertypes, arguments.get(search_by, []))
        elif search_by == 'applicant':
            return self.searchByApplicant(foldertypes, arguments.get(search_by, []))
        return None

    def searchByApplicant(self, foldertypes, applicant_infos_index):
        """
          Find licences with given paramaters
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

    def searchByStreet(self, foldertypes, workLocationUid):
        """
          Find licences with given paramaters
        """
        #we receive the street uid, look back references and returns the found licences
        catalogTool = getToolByName(self, 'portal_catalog')
        res = catalogTool(portal_type=foldertypes, StreetsUID=workLocationUid)
        return res

class UrbanSearchMacros(BrowserView):
    """
      This manage the macros of UrbanSearch
    """
