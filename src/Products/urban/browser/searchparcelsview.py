from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.urban.UrbanTool import DB_QUERY_ERROR

class SearchParcelsView(BrowserView):
    """
      This manage the search parcels view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.tool = getToolByName(context, 'portal_urban')
        #this way, if portal_urban.findDivisions display a portal message
        #it will be displayed on the page
        self.divisions = self.tool.findDivisions()
        #if the search was launched with no criteria, add a message
        if not self.searchHasCriteria(self.request):
            #we still not launched the search, everything is ok ;-)
            if request.has_key('division') \
               or request.has_key('location') \
               or request.has_key('prcOwner'):
                plone_utils = getToolByName(context, 'plone_utils')
                plone_utils.addPortalMessage(translate('warning_enter_search_criteria'), type="warning")

    def getDivisions(self):
        """
          Returns the existing divisions
          If we had a problem getting the divisions, we return nothing so the
          search form is not displayed
        """
        #check that we correctly received divisions
        if DB_QUERY_ERROR in str(self.divisions):
            return None
        return self.divisions

    def searchHasCriteria(self, request):
        """
        """
        division = request.get('division', '')
        section = request.get('section', '')
        radical = request.get('radical', '')
        bis = request.get('bis', '')
        exposant = request.get('exposant', '')
        puissance = request.get('puissance', '')
        location = request.get('location', '')
        prcOwner = request.get('prcOwner', '')
        #the division is not enough
        if (not division or (not section and not radical and not bis and not exposant and not puissance and not location and not prcOwner)) \
           and not location and not prcOwner:
            return False
        else:
            return True

    def browseOldParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None):
        """
           Return the concerned parcels
        """
        section=section.upper()
        exposant=exposant.upper()
        query_string = "SELECT distinct prca as prc, pas.da, divname, sectionavant as section, radicalavant as radical, bisavant as bis, exposantavant as exposant, puissanceavant as puissance FROM pas left join da on pas.da=da.da "
        condition = ["WHERE prca is not null and "]
        if division != '':  #precise division selected
            condition.append('pas.da = %s' % division)
        if section:
            condition.append("sectionavant = '%s'" % section)
        if radical:
            condition.append("radicalavant = "+radical)
        if bis:
            condition.append("bisavant = "+bis)
        if exposant:
            condition.append("exposantavant = '%s'" %exposant)
        if puissance:
            condition.append("puissanceavant = "+puissance)
        if len(condition) > 1:
            query_string += condition[0]
            query_string += ' and '.join(condition[1:])
            result = self.tool.queryDB(query_string)
            for res in result:
                res['old'] = True
        return result


    def findParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, location=None, prcOwner=None, prcHistory=None, browseOldParcels=None):
        """
           Return the concerned parcels
        """
        if not self.searchHasCriteria(self.context.REQUEST):
            return []
        if prcHistory:
            return []
        result = []
        if browseOldParcels and not prcHistory and not prcOwner:
           result = self.browseOldParcel(division, section, radical, bis, exposant, puissance)
        section=section.upper()
        exposant=exposant.upper()
        query_string = "SELECT capa.da, divname, prc, section, radical, exposant, bis, puissance, sl1, na1,pe FROM map left join capa on map.capakey=capa.capakey left join da on capa.da = da.da "
        condition = ["WHERE "]
        if division != '':  #precise division selected
            condition.append('capa.da = %s' % division)
        if section:
            condition.append("section = '%s'" % section)
        if radical:
            condition.append("radical = "+radical)
        if bis:
            condition.append("bis = "+bis)
        if exposant:
            condition.append("exposant = '%s'" %exposant)
        if puissance:
            condition.append("puissance = "+puissance)
        if prcOwner:
            condition.append("pe ILIKE '%%%s%%'" % prcOwner)
        if location:
            condition.append("sl1 ILIKE '%%%s%%'" % location)
        if len(condition) > 1:
            query_string += condition[0]
            query_string += ' and '.join(condition[1:])
            result.extend(self.tool.queryDB(query_string))
        return result

    def findOldParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, prcHistory=None, divname=None, prca=None):
        """
        Return the concerned parcels
        """
        if prcHistory:
            toreturn=[{'da':division,'divname':divname,'prca':prca,'sectionavant':section,'radicalavant':radical,'bisavant':bis,'exposantavant':exposant,'puissanceavant':puissance,'level':0}]
            def getOldPrc(div, sect, rad, exp, puis, bis, level):
                query_string = "SELECT distinct prca,pas.da,divname,sectionavant,radicalavant,bisavant,exposantavant,puissanceavant FROM pas left join da on pas.da=da.da WHERE pas.da=%s and section = '%s' AND radical = %s AND exposant = '%s' AND puissance = %s AND bis = %s AND prca is not null AND (section != sectionavant or radical != radicalavant or bis != bisavant or exposant != exposantavant or puissance != puissanceavant)"%(div, sect, rad, exp, puis, bis)
                result = self.tool.queryDB(query_string)
                for dic in result:
                    dic['level'] = level+1
                    toreturn.append(dic)
                    getOldPrc(div, dic['sectionavant'], dic['radicalavant'], dic['exposantavant'], dic['puissanceavant'], dic['bisavant'], level+1)
            getOldPrc(division, section, radical, exposant, puissance, bis, 0)
            return toreturn
        else:
            query_string = "SELECT distinct prca,pas.da,divname,sectionavant,radicalavant,bisavant,exposantavant,puissanceavant FROM pas left join da on pas.da=da.da "
            condition = ["WHERE "]
            if division != '0':  #precise division selected
                condition.append('pas.da = %s'%division)
            if section:
                condition.append("sectionavant = '%s'"%section)
            if radical:
                condition.append("radicalavant = "+radical)
            if bis:
                condition.append("bisavant = "+bis)
            if exposant:
                condition.append("exposantavant = '%s'"%exposant)
            if puissance:
                condition.append("puissanceavant = "+puissance)
            if len(condition) > 1:
                query_string += condition[0]
                query_string += ' and '.join(condition[1:])
            return self.tool.queryDB(query_string)
