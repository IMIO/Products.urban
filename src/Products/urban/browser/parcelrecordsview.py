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
        licence_brains = self.searchRelatedLicences()
        to_display = self.getDisplayForRelatedLicences(licence_brains)
        return to_display

    def getDisplayForRelatedLicences(self, licence_brains):
        context = aq_inner(self.context)
        related_items = []
        for brain in licence_brains:
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

    def getParcelHistoric(self):
        return []


class ParcelHistoricRecordsView(ParcelRecordsView):
    """
     Search for licences related to the parcel historic of the current licence
    """

    def getRelatedLicencesOfParcel(self):
        """
          Returns the licences related to a parcel
        """
        licence_brains, parcel_historic = self.searchRelatedLicences()
        to_display = self.getDisplay(parcel_historic, licence_brains)
        return to_display

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
        parcels_historic = parcels_historic[0]
        for ref in parcels_historic.getAllIndexableRefs():
            parcel_infos.add(ref)

        related_brains = catalog(object_provides=IGenericLicence.__identifier__, parcelInfosIndex=list(parcel_infos), sort_on='sortable_title')

        return related_brains, parcels_historic

    def getDisplay(self, parcels_historic, related_brains):
        historic = parcels_historic.listHistoric()
        to_return = []
        sorted_keys = sorted(historic.keys())
        delta = abs(min(sorted_keys))

        for level in sorted_keys:
            lines = []
            for parcel in historic[level]:
                line = {'parcel': parcel, 'level': level + delta, 'highlight': False}
                if level == 0:
                    line['highlight'] = True
                licences = [brain for brain in related_brains if parcel.getIndexableRef() in brain.parcelInfosIndex]
                line['licences'] = self.getDisplayForRelatedLicences(licences)
                lines.append(line)
            to_return.append(lines)

        return to_return
