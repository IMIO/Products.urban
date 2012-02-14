from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class UrbanCertificateTwoView(BrowserView):
    """
      This manage the view of UrbanCertificateTwo
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

    def getInquiriesForDisplay(self):
        """
          Returns the inquiries to display on the buildlicence_view
          This will move to the buildlicenceview when it will exist...
        """
        context = aq_inner(self.context)
        inquiries = context.getInquiries()
        if not inquiries:
            #we want to display at least the informations about the inquiry
            #defined on the licence even if no data have been entered
            inquiries.append(context)
        return inquiries

class UrbanCertificateTwoMacros(BrowserView):
    """
      This manage the macros of UrbanCertificateTwo
    """
