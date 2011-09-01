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
        if not lastDeposit:
            return None
        return tool.formatDate(lastDeposit.getEventDate(), translatemonth=False)

    def getAcknowledgmentDate(self):
        """
          Returns the acknowledgmentDate
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        lastAcknowledgment = context.getLastAcknowledgment()
        if not lastAcknowledgment:
            return None
        return tool.formatDate(lastAcknowledgment.getEventDate(), translatemonth=False)

    def getMissingPartDate(self):
        """
          Returns the last missing parts UrbanEvent date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        lastMissingPart = context.getLastMissingPart()
        if not lastMissingPart:
            return None
        return tool.formatDate(lastMissingPart.getEventDate(), translatemonth=False)

    def getWalloonRegionPrimoDate(self):
        """
          Returns the last Walloon Region primo UrbanEvent date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        walloonRegionPrimo = context.getLastWalloonRegionPrimo()
        if not walloonRegionPrimo:
            return None
        return tool.formatDate(walloonRegionPrimo.getEventDate(), translatemonth=False)

    def getOpinionRequestsDate(self):
        """
          Returns the last opinion request date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        opinionRequest = context.getLastOpinionRequest()
        if not opinionRequest :
            return None
        return tool.formatDate(opinionRequest.getEventDate(), translatemonth=False)

    def getOpinionRequestsTransmitDate(self):
        """
          Returns the last opinion request date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        opinionRequest = context.getLastOpinionRequest()
        if not opinionRequest :
            return None
        return tool.formatDate(opinionRequest.getTransmitDate(), translatemonth=False)

    def getCollegeReportDecisionDate(self):
        """
          Returns the last college report decision date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        collegeReport = context.getLastCollegeReport()
        if not collegeReport :
            return None
        return tool.formatDate(collegeReport.getDecisionDate(), translatemonth=False)

    def getTheLicenceDate(self):
        """
          Returns the last licence notification date
        """
        context = aq_inner(self.context)
        tool = context.portal_urban
        theLicence = context.getLastTheLicence()
        if not theLicence :
            return None
        return tool.formatDate(theLicence.getEventDate(), translatemonth=False)
