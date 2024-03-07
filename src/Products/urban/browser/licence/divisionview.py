from Products.urban.browser.licence.licenceview import CODTLicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


class DivisionView(CODTLicenceView):
    """
    This manage the view of Division
    """

    def __init__(self, context, request):
        super(CODTLicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)
        plone_utils = getToolByName(context, "plone_utils")
        if not self.context.getProprietaries():
            plone_utils.addPortalMessage(_("warning_add_a_proprietary"), type="warning")

    def getMacroViewName(self):
        return "division-macros"
