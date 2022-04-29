# -*- coding: utf-8 -*-

from Products.urban.browser.licence.licenceview import EnvironmentLicenceView
from Products.CMFPlone import PloneMessageFactory as _

from plone import api


class ExplosivesPossessionView(EnvironmentLicenceView):

    def __init__(self, context, request):
        super(ExplosivesPossessionView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)
        plone_utils = api.portal.get_tool('plone_utils')
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_a_proprietary'), type="warning")

    def getMacroViewName(self):
        return 'explosivespossession-macros'

    def getExpirationDate(self):
        return None
