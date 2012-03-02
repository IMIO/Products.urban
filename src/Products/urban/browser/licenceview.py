from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

class LicenceView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

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

    def getEmptyTabs(self):
        tabnames = ['urban_location', 'urban_road']
        return [tabname for tabname in tabnames if self.isEmptyTab(tabname)]

    def isEmptyTab(self, tab_name):
        context = aq_inner(self.context)
        urban_tool = getToolByName(context, 'portal_urban') 
        used_fields_names = set(getattr(urban_tool, context.getPortalTypeName().lower()).getUsedAttributes())
        if used_fields_names :
            for field in context.schema.getSchemataFields(tab_name):
                if field.getName() in used_fields_names:
                    return False
        return True

class LicenceMacros(BrowserView):
    """
      This manage the macros of BuildLicence
    """
