from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class DeclarationView(BrowserView):
    """
      This manage the view of Declaration
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")

    def getReceiptDate(self):
        """
          Returns the receiptDate
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        lastDeposit = context.getLastDeposit()
        if not lastDeposit or not lastDeposit.getEventDate():
            return None
        dict = {
                'url': lastDeposit.absolute_url(),
                'date': tool.formatDate(lastDeposit.getEventDate(), translatemonth=False)
               }
        return dict

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
                'date': tool.formatDate(collegeReport.getEventDate(), translatemonth=False)
               }
        return dict

    def getTheLicenceDate(self):
        """
          Returns the last licence notification date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        theLicence = context.getLastTheLicence()
        if not theLicence or not theLicence.getEventDate():
            return None
        dict = {
                'url': theLicence.absolute_url(),
                'date': tool.formatDate(theLicence.getEventDate(), translatemonth=False)
               }
        return dict

class DeclarationMacros(BrowserView):
    """
      This manage the macros of Declaration
    """
