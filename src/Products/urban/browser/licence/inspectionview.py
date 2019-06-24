# -*- coding: utf-8 -*-

from Products.urban.browser.licence.licenceview import LicenceView
from Products.CMFPlone import PloneMessageFactory as _

from plone import api


class InspectionView(LicenceView):

    def __init__(self, context, request):
        super(InspectionView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)
        plone_utils = api.portal.get_tool('plone_utils')
        if not self.context.getParcels() and not self.context.getBound_licence():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if self.hasOutdatedParcels():
            plone_utils.addPortalMessage(_('warning_outdated_parcel'), type="warning")

    def getMacroViewName(self):
        return 'inspection-macros'

    def getExpirationDate(self):
        return None

    def getInquiriesForDisplay(self):
        """
          Returns the inquiries to display on the buildlicence_view
        """
        return [self.context]