from Acquisition import aq_inner
from Products.Five import BrowserView

class BuildLicenceView(BrowserView):
    """
      This manage the view of BuildLicence
    """
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
