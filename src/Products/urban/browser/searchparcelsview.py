from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.urban.UrbanTool import DB_QUERY_ERROR
from Products.urban.browser.table.urbantable import ParcelsTable
from Products.urban.interfaces import IGenericLicence


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
            if 'division' in request or 'location' in request or 'prcOwner' in request:
                plone_utils = getToolByName(context, 'plone_utils')
                plone_utils.addPortalMessage(translate('warning_enter_search_criteria'), type="warning")

    def contextIsLicence(self):
        return IGenericLicence.providedBy(self.context)

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ''
        parcellisting = ParcelsTable(parcels, self.request)
        parcellisting.update()
        return parcellisting.render()

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
        if (not division or (not section and not radical and not bis and not exposant and not puissance and not location and not prcOwner)) and not location and not prcOwner:
            return False
        else:
            return True

    def findParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, location=None, prc_owner=None, prc_history=None, browseoldparcels=False):
        """
           Return the concerned parcels
        """
        if not self.searchHasCriteria(self.context.REQUEST):
            return []
        if prc_history:
            return []
        parcels = self.tool.queryParcels(division, section, radical, bis, exposant, puissance, location, prc_owner)
        result = [prc.getParcelAsDictionary() for prc in parcels]
        already_found = set([str(prc) for prc in parcels])
        if browseoldparcels and not prc_history and not prc_owner:
            old_parcels = self.tool.queryParcels(division, section, radical, bis, exposant, puissance, browseold=browseoldparcels)
            for parcel in old_parcels:
                if str(parcel) not in already_found:
                    dict_prc = parcel.getParcelAsDictionary()
                    dict_prc['old'] = True
                    result.append(dict_prc)
        return result

    def findOldParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, old=False):
        """
        Return the concerned parcels
        """
        parcel = self.tool.queryParcels(division, section, radical, bis, exposant, puissance, historic=True, browseold=True, fuzzy=False)[0]
        return parcel.getHistoricForDisplay()
