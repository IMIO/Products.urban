from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class ParcelHistoricView(BrowserView):
    """
      This manage the view of long text
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.parcel_id = self.request.get('id', None)
        if not self.parcel_id:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('Nothing to show !!!'), type="error")

    def getParcelHistoric(self):
        """
          Returns the entire text
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        parcel = getattr(context, self.parcel_id)
        res = []
        res.append(parcel.getDivisionCode())
        res.append(parcel.getSection())
        res.append(parcel.getRadical())
        res.append(parcel.getBis())
        res.append(parcel.getExposant())
        res.append(parcel.getPuissance())
        if parcel.getPartie():
            res.append('1')
        else:
            res.append('0')
        parcel_infos = ",".join(res)
        base_url = '/'.join(getToolByName(context, 'portal_url')().split('/')[:-1])
        return [{'title':brain.Title, 
                 'url':'%s%s' % (base_url, brain.getPath()), 
                 'class':'state-%s contenttype-%s' % (brain.review_state, brain.portal_type.lower())}
                for brain in catalog(parcelInfosIndex=parcel_infos, sort_on='sortable_title') if brain.id != context.id]
