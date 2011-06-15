from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.urban.config import URBAN_TYPES

class ContactView(BrowserView):
    """
      This manage the view of every Contacts :
      Applicant, Architect, Geometrician, Notary
    """
    def getLinkToLinkedLicence(self):
        """
          Return a link to the licence if available
          (protected by showLinkToLinkedLicence here above)
        """
        context = aq_inner(self.context)
        #either the parent is in URBAN_TYPES
        parent = context.aq_inner.aq_parent
        if parent.portal_type in URBAN_TYPES:
            return parent.absolute_url()
        #or we have a "came_from_licence_uid" in the REQUEST
        else:
            came_from_licence_uid = context.REQUEST.get('came_from_licence_uid', None)
            uid_catalog = getToolByName(context, 'uid_catalog')
            linkedLicenceBrains = uid_catalog(UID=came_from_licence_uid)
            linkedLicence = linkedLicenceBrains[0].getObject()
            return linkedLicence.absolute_url()
   
    def showLinkToLinkedLicence(self):
        """
          Check if we have what necessary to show a link to the linked licence :
          either the parent is a licence, or we have a "came_from_licence_uid" in
          the REQUEST
        """
        context = aq_inner(self.context)
        res = False
        if context.aq_inner.aq_parent.portal_type in URBAN_TYPES:
            res = True
        elif context.REQUEST.has_key('came_from_licence_uid'):
            came_from_licence_uid = context.REQUEST.get('came_from_licence_uid', None)
            #check if we really have a 'came_from_licence_uid'
            if came_from_licence_uid:
                uid_catalog = getToolByName(context, 'uid_catalog')
                linkedLicenceBrains = uid_catalog(UID=came_from_licence_uid)
                if linkedLicenceBrains:
                    res = True
        return res
    
    def getContactLegendValue(self):
        """
          Generates a label that will be used in the legend of a fieldset
          This value will be translated in the template using i18n:translate=""
        """
        context = aq_inner(self.context)
        return "%s data" % context.portal_type
