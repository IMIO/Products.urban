from Products.urban.browser.licence.licenceview import LicenceView
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
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")

    def getMacroViewName(self):
        return 'miscdemand-macros'
