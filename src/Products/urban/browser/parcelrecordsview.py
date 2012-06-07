from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

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
        catalog = getToolByName(context, 'portal_catalog')
        parcel = getattr(context, self.parcel_id)
        parcel_infos = parcel.getIndexValue()
        base_url = getToolByName(context, 'portal_url').getPortalObject().absolute_url()
        return [{'title':brain.Title,
            'url':'%s/%s' % (base_url, '/'.join(brain.getPath().split('/')[2:])),
                 'class':'state-%s contenttype-%s' % (brain.review_state, brain.portal_type.lower())}
                for brain in catalog(parcelInfosIndex=parcel_infos, sort_on='sortable_title') if brain.id != context.id]
