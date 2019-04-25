# encoding: utf-8

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as _

from Products.urban.interfaces import IGenericLicence

from plone import api


class ParcelRecordsView(BrowserView):
    """
      This manage the view of the popup showing the licences related to some parcels
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.parcel_id = self.request.get('id', None)
        if not self.parcel_id:
            plone_utils = api.portal.get_tool('plone_utils')
            plone_utils.addPortalMessage(_('Nothing to show !!!'), type="error")

    def get_related_licences_of_parcel(self):
        """
          Returns the licences related to a parcel
        """
        licence_brains = self.search_licences()
        to_display = self.get_display(licence_brains)
        return to_display

    def get_display(self, licence_brains):
        context = aq_inner(self.context)
        related_items = []
        for brain in licence_brains:
            if brain.id != context.id:
                item_infos = {
                    'title': len(brain.Title) < 40 and brain.Title or '{}...'.format(brain.Title[:40]),
                    'url': brain.getURL(),
                    'class': 'state-{} contenttype-{}'.format(brain.review_state, brain.portal_type.lower())
                }
                related_items.append(item_infos)
        return related_items

    def search_licences(self):
        """
          Do the search and return licence brains
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool('portal_catalog')
        parcel = getattr(context, self.parcel_id)
        capakey = parcel.get_capakey()

        related_brains = catalog(
            object_provides=IGenericLicence.__identifier__,
            parcelInfosIndex=capakey,
            sort_on='sortable_title'
        )

        return related_brains
