# -*- coding: utf-8 -*-

from Products.urban.browser.licence.buildlicenceview import BuildLicenceView
from Products.urban.browser.licence.licenceview import EnvironmentLicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from plone import api


class UniqueLicenceView(BuildLicenceView, EnvironmentLicenceView):
    """
      This manage the view of BuildLicence
    """
    def __init__(self, context, request):
        super(BuildLicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")

    def getMacroViewName(self):
        return 'uniquelicence-macros'

    def getImpactStudyInfos(self):
        impact_study_event = self.context.getLastImpactStudyEvent()
        if impact_study_event:
            urban_tool = api.portal.get_tool('portal_urban')
            date = impact_study_event.getEventDate()
            infos = {
                'url': impact_study_event.absolute_url(),
                'date': date and urban_tool.formatDate(date, translatemonth=False) or None,
            }
            return infos
        return {}
