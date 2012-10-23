from Acquisition import aq_inner
from Products.urban.browser.licenceview import LicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class MiscDemandView(LicenceView):
    """
      This manage the view of
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")
        if self.hasOutdatedParcels():
            plone_utils.addPortalMessage(_('warning_outdated_parcel'), type="warning")

class MiscDemandMacros(LicenceView):
    """
      This manage the macros of Declaration
    """
