## -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from Products.urban.browser.urbansearchview import UrbanSearchView
from Products.urban.utils import ParcelHistoric
from Products.urban.interfaces import IGenericLicence


class ParcelsInfo(UrbanSearchView):
    """
      This manage parcelinfos method
    """

    def searchAllLicencesByParcel(self, division, section, radical, bis, exposant, puissance, partie):
        """
          Find licences with parcel paramaters
        """
        if not self.enoughSearchCriterias(self.context.REQUEST):
            return []
        catalogTool = getToolByName(self, 'portal_catalog')
        parcel_infos = set()
        arg_index = ParcelHistoric(division=division, section=section, radical=radical, bis=bis, exposant=exposant, puissance=puissance)
        parcel_infos.add(arg_index.getIndexableRef())
        parcels_historic = self.tool.queryParcels(division, section, radical, bis, exposant, puissance, historic=True, fuzzy=False, browseold=True)
        for parcel in parcels_historic:
            for ref in parcel.getAllIndexableRefs():
                parcel_infos.add(ref)
        return catalogTool(object_provides=IGenericLicence.__identifier__, parcelInfosIndex=list(parcel_infos))

    def getParcelInfos(self, capakey):
        parcelInfos = {}
        strsql = "select * from map where capakey = '" + capakey + "'"
        try:
            result = self.tool.queryDB(query_string=strsql)[0]
            divname = self.tool.queryDB("SELECT da,divname FROM da WHERE da = " + str(result['daa'])[0:5])[0]['divname']
            parcelInfos['name'] = divname + ' ' + result['prc']
            parcelInfos['ownername'] = result['pe']
            parcelInfos['ownerstreet'] = result['adr2']
            parcelInfos['ownercity'] = result['adr1']
            parcelInfos['type'] = result['na1']
            strsql = "select * from capa where capakey = '" + capakey + "'"
            result = self.tool.queryDB(query_string=strsql)[0]
            parcelInfos['division'] = str(result['da'])
            parcelInfos['section'] = result['section']
            parcelInfos['radical'] = str(result['radical'])
            if result['bis'] == 0:
                parcelInfos['bis'] = ''
            else:
                parcelInfos['bis'] = str(result['bis'])
            if result['exposant']:
                parcelInfos['exposant'] = result['exposant']
            else:
                parcelInfos['exposant'] = ''
            if result['puissance'] == 0:
                parcelInfos['puissance'] = ''
            else:
                parcelInfos['puissance'] = str(result['puissance'])
        except:
            pass
        return parcelInfos
