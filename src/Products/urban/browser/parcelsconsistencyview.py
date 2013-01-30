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
        urban_tool = getToolByName(context, 'portal_urban')
        portal_workflow = getToolByName(context, 'portal_workflow')
        parcelbrains = catalog(portal_type='PortionOut')
        result = {
                    'critical_outdated_parcels' :[],
                    'outdated_parcels' :[],
                }
        ref_names = ['division', 'section', 'radical', 'bis', 'exposant', 'puissance']
        for brain in parcelbrains:
            parcel = brain.getObject()
            if parcel.getIsOfficialParcel() and parcel.getDivisionCode() and parcel.getSection():
                references = dict([(name, getattr(parcel,'get%s' % name.capitalize())()) for name in ref_names])
                outdated = not urban_tool.queryParcels(fuzzy=False, **references)
            else:
                outdated = False
            parcel.setOutdated(outdated)
            licence = parcel.aq_inner.aq_parent
            infos = {'parcel':brain.Title, 'licence title':licence.Title(), 'licence path': licence.absolute_url()}
            if outdated or not parcel.getIsOfficialParcel():
                if portal_workflow.getInfoFor(licence, 'review_state') == 'in_progress':
                    result['critical_outdated_parcels'].append(infos)
                else:
                    result['outdated_parcels'].append(infos)
        return result
