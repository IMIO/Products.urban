# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner

from Products.urban import services

from plone import api


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
        request = aq_inner(self.request)
        if request.get("check") != "yes":
            return

        catalog = api.portal.get_tool("portal_catalog")
        parcelbrains = catalog(portal_type="PortionOut")
        result = {
            "critical_outdated_parcels": [],
            "outdated_parcels": [],
        }
        cadastre = services.cadastre.new_session()
        for brain in parcelbrains:
            outdated = False
            parcel = brain.getObject()
            if (
                parcel.getIsOfficialParcel()
                and parcel.getDivisionCode()
                and parcel.getSection()
            ):
                references = parcel.reference_as_dict()
                outdated = cadastre.is_outdated_parcel(**references)
            parcel.setOutdated(outdated)
            licence = parcel.aq_inner.aq_parent
            infos = {
                "parcel": brain.Title,
                "licence title": licence.Title(),
                "licence path": licence.absolute_url(),
            }
            if outdated or not parcel.getIsOfficialParcel():
                if api.content.get_state(licence) == "in_progress":
                    result["critical_outdated_parcels"].append(infos)
                else:
                    result["outdated_parcels"].append(infos)
        cadastre.close()
        return result
