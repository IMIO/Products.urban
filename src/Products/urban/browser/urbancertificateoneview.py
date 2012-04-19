from Acquisition import aq_inner
from Products.urban.browser.licenceview import LicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class UrbanCertificateOneView(LicenceView):
    """
      This manage the view of UrbanCertificateOne
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getProprietaries():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")

class UrbanCertificateOneMacros(LicenceView):
    """
      This manage the macros of UrbanCertificateOne
    """
