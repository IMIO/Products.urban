## -*- coding: utf-8 -*-

from zope.i18n import translate
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
        return {key_to_match:request.get(key_to_match, '')}

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
            args_name = ['division','section', 'radical', 'bis', 'exposant', 'puissance']
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
                        'street':self.getArgument('street'),
                        'name':self.getArgument(['name', 'contacttypes']),
                        'parcel':self.getArgument(['division','section', 'radical', 'bis', 'exposant', 'puissance', 'partie', 'browseoldparcels']),
                    }
        if search_by == 'street':
            res = self.searchByStreet(foldertypes, **arguments.get(search_by, []))
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
        res = catalogTool(portal_type=foldertypes, StreetsUID=street_uids)
        return res

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
        parcels_historic = self.queryParcels(division, section, radical, bis, exposant, puissance, browseoldparcels)
        for parcel in parcels_historic:
            for ref in parcel.getAllSearchRefs():
                parcel_infos.add(ref)
        res = catalogTool(portal_type=foldertypes, parcelInfosIndex=list(parcel_infos))
        return res

    def queryParcels(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, browseold=False):
        """
        Return the concerned parcels
        """
        query_string = browseold and \
                       "SELECT distinct prca, prcc, prcb1 as prc, da.divname, pas.da as division, section, radical, exposant, bis, puissance \
                        FROM pas left join da on da.da = pas.da" or \
                       "SELECT capa.da as division, divname, prc, section, radical, exposant, bis, puissance \
                        FROM map left join capa on map.capakey=capa.capakey left join da on capa.da = da.da "
        conditions = []
        division != 0 and conditions.append("%s.da= %s" % (browseold and 'pas' or 'capa', division))
        section       and conditions.append("section= '%s'" % section)
        radical       and conditions.append("radical= %s" % radical)
        bis           and conditions.append("bis= %s" % bis)
        exposant      and conditions.append("exposant= '%s'" % exposant)
        puissance     and conditions.append("puissance= %s" % puissance)
        if conditions:
            query_string = '%s WHERE %s' % (query_string, ' and '.join(conditions))
        records = self.tool.queryDB(query_string)
        parcels = [ParcelHistoric(highlight=True, **r) for r in records]
        parcels = ParcelHistoric.mergeDuplicate(parcels)
        if browseold:
            for i, parcel in enumerate(parcels):
                parcel.buildRelativesChain(self.tool, 'parents')
                parcel.buildRelativesChain(self.tool, 'childs')
        return parcels


class ParcelHistoric:

    @staticmethod
    def mergeDuplicate(parcel_historics):
        checked = {}
        for i, historic in enumerate(parcel_historics):
            key = historic.key()
            if key in checked.keys():
                parcel_historics[checked[key]].mergeRelatives(historic)
                parcel_historics[i] = None
            else:
                checked[key] = i
        return [parcel for parcel in parcel_historics if parcel]


    def __init__(self, highlight=False, prc='', prca='', prcc='', **refs):
        self.highlight = highlight
        self.parents = self.diffPrc(prca, prc) and [prca] or []
        self.childs = self.diffPrc(prcc, prc) and [prcc] or []
        self.divname = self.division = self.section = self.radical = self.bis =  self.exposant =  self.puissance = ''
        self.refs = ['divname', 'division', 'section', 'radical', 'bis', 'exposant', 'puissance']
        self.setRefs(**refs)

    def __str__(self):
        return ' '.join([getattr(self, attr, '') for attr in self.refs])

    def __hash__(self):
        return self.__str__()

    def key(self):
        return self.__str__()

    def buildRelativesChain(self, urban_tool, link_name):
        o_link_name  = link_name == 'parents' and 'childs' or 'parents'
        link = link_name == 'parents' and 'prca' or 'prcc'
        o_link = link == 'prca' and 'prcc' or 'prca'
        division = self.division
        relatives_chain = []
        for prc in getattr(self, link_name):
            section = prc[0]
            prcb1 = prc[1:]
            prcb1 = '%s%s%s' % (prcb1[:-3], ' '.join(['' for i in range(12-len(prcb1))]), prcb1[-3:])
            query_string = "SELECT distinct %s, prcb1 as prc, da.divname, pas.da as division, section, radical, exposant, bis, puissance \
                            FROM pas left join da on da.da = pas.da \
                            WHERE pas.da = %s and section = '%s' and pas.prcb1 = '%s' and pas.%s IS NOT NULL" % (link, division, section, prcb1, o_link)
            records = urban_tool.queryDB(query_string)
            relatives = [ParcelHistoric(**r) for r in records]
            if not relatives:
                continue
            relative = ParcelHistoric.mergeDuplicate(relatives)[0]
            relative.buildRelativesChain(urban_tool, link_name)
            relative.addRelative(o_link_name, [self])
            relatives_chain.append(relative)
        setattr(self, link_name, relatives_chain)

    def getSearchRef(self):
        return ','.join([val and str(val) or '' for val in [self.division, self.section, self.radical, self.bis, self.exposant, self.puissance, '0']])

    def getAllSearchRefs(self):
        all_nodes = {}
        all_nodes = [n['node'] for n in self.getAllNodes(nodes=all_nodes).values()]
        return [node.getSearchRef() for node in all_nodes]

    def getAllNodes(self, directions=['childs', 'parents'], nodes={}, distance=0):
        nodes[self.key()] = {'node':self, 'distance':distance}
        for direction in directions:
            dist = direction == 'childs' and distance + 1 or distance - 1
            for relative in self.getRelatives(direction):
                if str(relative) not in nodes.keys():
                    relative.getAllNodes(directions, nodes, dist)
        return nodes

    def mergeRelatives(self, other, merge_points=['parents', 'childs']):
        for merge_point in merge_points:
            existing_relatives= [str(p) for p in getattr(self, merge_point)]
            relatives = [relative for relative in getattr(other, merge_point) if str(relative) not in existing_relatives]
            self.addRelative(merge_point, relatives)

    def diffPrc(self, prc_ac, prc):
        return prc_ac and prc_ac.replace(' ','')[1:] != prc.replace(' ','') or False

    def setRefs(self, **kwargs):
        for ref in self.refs:
            val = kwargs.get(ref, '') and str(kwargs[ref]) or ''
            setattr(self, ref, val)

    def getRelatives(self, name):
        return getattr(self, '%s' % name, [])

    def addRelative(self, name, relative):
        adder = getattr(self, 'add%s' % name.capitalize(), None)
        if adder:
            adder(relative)

    def addParents(self, parents):
        self.parents.extend(parents)

    def addChilds(self, childs):
        self.childs.extend(childs)

class UrbanSearchMacros(BrowserView):
    """
      This manage the macros of UrbanSearch
    """
