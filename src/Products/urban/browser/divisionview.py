from Acquisition import aq_inner
from Products.urban.browser.licenceview import LicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class DivisionView(LicenceView):
    """
      This manage the view of Division
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getProprietaries():
            plone_utils.addPortalMessage(_('warning_add_a_proprietary'), type="warning")
        if self.hasOutdatedParcels():
            plone_utils.addPortalMessage(_('warning_outdated_parcel'), type="warning")

    def getCollegeReportDecisionDate(self):
        """
          Returns the last college report decision date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        collegeReport = context.getLastCollegeReport()
        if not collegeReport or not collegeReport.getEventDate():
            return None
        dict = {
                'url': collegeReport.absolute_url(),
                'date': "%s - %s" % (tool.formatDate(collegeReport.getEventDate(), translatemonth=False), \
                context.displayValue(collegeReport.Vocabulary('decision')[0], collegeReport.getDecision()))
               }
        return dict

class DivisionMacros(LicenceView):
    """
      This manage the macros of Division
    """
