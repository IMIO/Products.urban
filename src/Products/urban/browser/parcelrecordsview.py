from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from Products.urban.interfaces import IGenericLicence


class ParcelRecordsView(BrowserView):
    """
      This manage the view of the popup showing the licences related to some parcels
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.parcel_id = self.request.get('id', None)
        if not self.parcel_id:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('Nothing to show !!!'), type="error")

    def getRelatedLicencesOfParcel(self):
        """
          Returns the licences related to a parcel
        """
        context = aq_inner(self.context)
        related_brains = self.searchRelatedLicences()
        related_items = []
        for brain in related_brains:
            if brain.id != context.id:
                item_infos = {
                    'title': brain.Title,
                    'url': brain.getURL(),
                    'class': 'state-%s contenttype-%s' % (brain.review_state, brain.portal_type.lower())
                }
                related_items.append(item_infos)
        return related_items

    def searchRelatedLicences(self):
        """
          Do the search and return licence brains
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        parcel = getattr(context, self.parcel_id)
        parcel_infos = parcel.getIndexValue()

        related_brains = catalog(object_provides=IGenericLicence.__identifier__, parcelInfosIndex=parcel_infos, sort_on='sortable_title')

        return related_brains


class ParcelHistoricRecordsView(ParcelRecordsView):
    """
     Search for licences related to the parcel historic of the current licence
    """
    def searchRelatedLicences(self):
        """
          Returns the licences related to a parcel
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_urban = getToolByName(context, 'portal_urban')
        parcel = getattr(context, self.parcel_id)
        parcel_infos = set()

        parcel_infos.add(parcel.getIndexValue())
        parcels_historic = portal_urban.queryParcels(
            parcel.getDivision(), parcel.getSection(), parcel.getRadical(), parcel.getBis(), parcel.getExposant(), parcel.getPuissance(),
            historic=True, fuzzy=False, browseold=True
        )
        for parcel in parcels_historic:
            for ref in parcel.getAllSearchRefs():
                parcel_infos.add(ref)

        related_brains = catalog(object_provides=IGenericLicence.__identifier__, parcelInfosIndex=list(parcel_infos), sort_on='sortable_title')

        return related_brains
