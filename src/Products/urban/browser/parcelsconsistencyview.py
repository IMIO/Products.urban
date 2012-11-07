# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

class ParcelsConsistencyView(BrowserView):
    """
      This manage methods of the view to check if urban PortionOut are consitent with the data
      in the cadastre database
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def checkParcelsConsistency(self):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        if request.get('check') != 'yes':
            return
        catalog = getToolByName(context, 'portal_catalog')
        portal_workflow = getToolByName(context, 'portal_workflow')
        parcelbrains = catalog(portal_type='PortionOut')
        result = {
                    'critical_outdated_parcels' :[],
                    'outdated_parcels' :[],
                }
        for brain in parcelbrains:
            parcel = brain.getObject()
            found = self.findParcel(
                    division = parcel.getDivisionCode(),
                    section = parcel.getSection(),
                    radical = parcel.getRadical(),
                    bis = parcel.getBis(),
                    exposant = parcel.getExposant(),
                    puissance = parcel.getPuissance()
                    )
            outdated = found == [] and True or False
            parcel.setOutdated(outdated)
            licence = parcel.aq_inner.aq_parent
            infos = {'parcel':brain.Title, 'licence title':licence.Title(), 'licence path': licence.absolute_url()}
            if outdated:
                if portal_workflow.getInfoFor(licence, 'review_state') == 'in_progress':
                    result['critical_outdated_parcels'].append(infos)
                else:
                    result['outdated_parcels'].append(infos)
        return result


    def findParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None):
        """
           Return the concerned parcels
        """
        context = aq_inner(self.context)
        urban_tool = getToolByName(context, 'portal_urban')
        result = []
        query_string = "SELECT capa.da, divname, prc, section, radical, exposant, bis, puissance, sl1, na1,pe FROM map left join capa on map.capakey=capa.capakey left join da on capa.da = da.da "
        condition = ["WHERE "]
        if division != '':  #precise division selected
            condition.append('capa.da = %s' % division)
        if section:
            section=section.upper()
            condition.append("section = '%s'" % section)
        if radical:
            condition.append("radical = "+radical)
        if bis:
            condition.append("bis = "+bis)
        if exposant:
            exposant=exposant.upper()
            condition.append("exposant = '%s'" %exposant)
        if puissance:
            condition.append("puissance = "+puissance)
        if len(condition) > 1:
            query_string += condition[0]
            query_string += ' and '.join(condition[1:])
            result.extend(urban_tool.queryDB(query_string))
        return result

