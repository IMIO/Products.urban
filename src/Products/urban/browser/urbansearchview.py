## -*- coding: utf-8 -*-

from zope.i18n import translate
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as msg
from Products.CMFPlone.PloneBatch import Batch
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import URBAN_TYPES
from Products.urban.utils import ParcelHistoric
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
        self.tool = getToolByName(context, 'portal_urban')
        if not self.enoughSearchCriterias(self.request):
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(translate('warning_enter_search_criteria'), type="warning")

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

    def getArgument(self, key_to_match):
        request = aq_inner(self.request)
        if type(key_to_match) == list:
            return dict([(key, request.get(key, '')) for key in key_to_match])
        request = aq_inner(self.request)
        return {key_to_match: request.get(key_to_match, '')}

    def getParcelRefArguments(self, arg_list):
        args = self.getArgument(arg_list)
        to_upper = ['section', 'radical', 'bis', 'exposant', 'puissance']
        return dict([(k, k in to_upper and v.upper() or v) for k, v in args.iteritems()])

    def getStreetInterfaces(self):
        interfaces = [
            'Products.urban.interfaces.IStreet',
            'Products.urban.interfaces.ILocality',
        ]
        return ','.join(interfaces)

    def enoughSearchCriterias(self, request):
        """
        """
        if request.get('search_by', '') == 'parcel':
            args_name = ['division', 'section', 'radical', 'bis', 'exposant', 'puissance']
            valid_args = [request.get(name) for name in args_name if request.get(name)]
            return len(valid_args) > 2
        return True

    def searchLicence(self):
        """
          Find licences with given paramaters
        """
        request = aq_inner(self.request)
        search_by = request.get('search_by', '')
        foldertypes = request.get('foldertypes', [])
        arguments = {
            'street': self.getArgument('street'),
            'folderref': self.getArgument('folderref'),
            'name': self.getArgument(['name', 'contacttypes']),
            'parcel': self.getParcelRefArguments(['division', 'section', 'radical', 'bis', 'exposant', 'puissance', 'partie', 'browseoldparcels']),
        }
        if search_by == 'street':
            res = self.searchByStreet(foldertypes, **arguments.get(search_by, []))
        elif search_by == 'folderref':
            res = self.searchByFolderReference(foldertypes, **arguments.get(search_by, []))
        elif search_by == 'name':
            res = self.searchByName(foldertypes, **arguments.get(search_by, []))
        elif search_by == 'parcel':
            res = self.searchByParcel(foldertypes, **arguments.get(search_by, []))
        else:
            return None
        batch = Batch(res, len(res), 0, orphan=0)
        return batch

    def searchByName(self, foldertypes, name, contacttypes):
        """
          Find licences by name and by contact categories
        """
        if not type(contacttypes) == list:
            contacttypes = [contacttypes]
        result_uids = set()
        result = []
        for contacttype in contacttypes:
            if contacttype == 'Applicant':
                sub_result = self.searchByApplicantName(foldertypes, name)
            else:
                sub_result = self.searchByContactName(foldertypes, name, contacttype)
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
        try:
            res = catalogTool(portal_type=foldertypes, applicantInfosIndex=applicant_infos_index)
            return res
        except ParseError:
            #in case something like '*' is entered, ZCTextIndex raises an error...
            ptool = getToolByName(self, "plone_utils")
            ptool.addPortalMessage(msg(u"please_enter_more_letters"), type="info")
            return res

    def searchByStreet(self, foldertypes, street):
        """
          Find licences with location paramaters
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        street = street.replace('(', ' ').replace(')', ' ')
        street_uids = [brain.UID for brain in catalogTool(portal_type='Street', Title=street)]
        return catalogTool(portal_type=foldertypes, StreetsUID=street_uids)

    def searchByFolderReference(self, foldertypes, folderref):
        """
          Find licences by name and by contact categories
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        return catalogTool(portal_type=foldertypes, getReference=folderref)

    def searchByParcel(self, foldertypes, division, section, radical, bis, exposant, puissance, partie, browseoldparcels=False):
        """
          Find licences with parcel paramaters
        """

        if not self.enoughSearchCriterias(self.context.REQUEST):
            return []
        catalogTool = getToolByName(self, 'portal_catalog')
        parcel_infos = set()
        arg_index = ParcelHistoric(division=division, section=section, radical=radical, bis=bis, exposant=exposant, puissance=puissance)
        parcel_infos.add(arg_index.getSearchRef())
        parcels_historic = self.tool.queryParcels(division, section, radical, bis, exposant, puissance, browseold=browseoldparcels, historic=True)
        for parcel in parcels_historic:
            for ref in parcel.getAllSearchRefs():
                parcel_infos.add(ref)
        return catalogTool(portal_type=foldertypes, parcelInfosIndex=list(parcel_infos))


class UrbanSearchMacros(BrowserView):
    """
      This manage the macros of UrbanSearch
    """
