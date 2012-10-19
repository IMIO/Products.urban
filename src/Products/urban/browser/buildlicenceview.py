from Acquisition import aq_inner
from Products.urban.browser.licenceview import LicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class BuildLicenceView(LicenceView):
    """
      This manage the view of BuildLicence
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

    def getAcknowledgmentDate(self):
        """
          Returns the acknowledgmentDate
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        lastAcknowledgment = context.getLastAcknowledgment()
        if not lastAcknowledgment or not lastAcknowledgment.getEventDate():
            return None
        dict = {
                'url': lastAcknowledgment.absolute_url(),
                'date': tool.formatDate(lastAcknowledgment.getEventDate(), translatemonth=False)
               }
        return dict

    def getMissingPartDate(self):
        """
          Returns the last missing parts UrbanEvent date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        lastMissingPart = context.getLastMissingPart()
        if not lastMissingPart or not lastMissingPart.getEventDate():
            return None
        dict = {
                'url': lastMissingPart.absolute_url(),
                'date': tool.formatDate(lastMissingPart.getEventDate(), translatemonth=False)
               }
        return dict

    def getWalloonRegionPrimoDate(self):
        """
          Returns the last Walloon Region primo UrbanEvent date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        walloonRegionPrimo = context.getLastWalloonRegionPrimo()
        if not walloonRegionPrimo or not walloonRegionPrimo.getEventDate():
            return None
        dict = {
                'url': walloonRegionPrimo.absolute_url(),
                'date': tool.formatDate(walloonRegionPrimo.getEventDate(), translatemonth=False)
               }        
        return dict

    def getOpinionRequestsDate(self):
        """
          Returns the last opinion request date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        opinionRequest = context.getLastOpinionRequest()
        if not opinionRequest or not opinionRequest.getEventDate():
            return None
        dict = {
                'url': opinionRequest.absolute_url(),
                'date': tool.formatDate(opinionRequest.getEventDate(), translatemonth=False)
               }
        return dict

    def getOpinionRequestsTransmitDate(self):
        """
          Returns the last opinion request date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        opinionRequest = context.getLastOpinionRequest()
        if not opinionRequest or not opinionRequest.getTransmitDate():
            return None
        dict = {
                'url': opinionRequest.absolute_url(),
                'date': tool.formatDate(opinionRequest.getTransmitDate(), translatemonth=False)
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

class BuildLicenceMacros(LicenceView):
    """
      This manage the macros of BuildLicence
    """
