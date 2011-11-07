from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.urban.UrbanTool import DB_QUERY_ERROR

class SearchParcelsView(BrowserView):
    """
      This manage the search parcels view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        portal_urban = getToolByName(context, 'portal_urban')        
        #this way, if portal_urban.findDivisions display a portal message
        #it will be displayed on the page
        self.divisions = portal_urban.findDivisions()

    def getDivisions(self):
        """
          Returns the existing divisions
          If we had a problem getting the divisions, we return nothing so the
          search form is not displayed
        """
        #check that we correctly received divisions
        if DB_QUERY_ERROR in str(self.divisions):
            return None
        return self.divisions