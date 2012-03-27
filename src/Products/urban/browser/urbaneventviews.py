from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.Inquiry import Inquiry
from Products.urban.browser.mapview import MapView

class UrbanEventView(BrowserView):
    """
      This manage the view of UrbanEvent
    """
    def getData(self):
        """
          This will return data to display about the UrbanEvent
          This returns a tuple where the element [0]
          is an object and the element [1] is a list of attributes
          Example : (context, [field1, field2, field3,])
        """
        context = aq_inner(self.context)
        linkedUrbanEventType = context.getUrbaneventtypes()
        data = (context, [],)
        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                #in some case, there could be an empty value in activatedFields...
                continue
            data[1].append(activatedField)
        return data
    
    def mayAddUrbanEvent(self):
        """
          Return True if the current user may add an UrbanEvent
        """
        context = aq_inner(self.context)
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        if member.has_permission('ATContentTypes: Add File', context):
            return True
        return False

    def mayAddAnnex(self):
        """
          Return True if the current user may add an Annex (File)
        """
        context = aq_inner(self.context)
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        if member.has_permission('ATContentTypes: Add File', context):
            return True
        return False

    def getListOfTemplatesToGenerate(self):
        """
        Return a list of dicts. Each dict contains all the infos needed in the html <href> tag to create the 
        corresponding link for document generation
        """
        context = aq_inner(self.context)
        template_list = [{'name':template.id.split('.')[0], 
                          'title':template.Title(),
                          'class':'',
                          'href':self._generateDocumentHref(context, template),
                         } for template in context.getTemplates()]
        for generated_doc in context.objectValues():
            for template in template_list:
                if generated_doc.id.startswith(template['name']):
                    template['class'] = 'urban-document-already-created'
        return template_list

    def _generateDocumentHref(self, context, template):
        """
        """
        return "%s/createUrbanDoc?urban_template_uid=%s&urban_event_uid=%s" %(context.absolute_url(), template.UID(), context.UID())

class UrbanEventMacros(BrowserView):
    """
      This manage the macros of BuildLicence
    """

class UrbanEventInquiryView(UrbanEventView, MapView):
    """
      This manage the view of UrbanEventInquiry
      It is based on the default UrbanEventView
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.linkedInquiry = self.context.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !'), type="error")

    def getInquiryData(self):
        """
          This will return data to display about the UrbanEventInquiry
          See UrbanEventView.getData doc string
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        if not linkedInquiry:
            #this should not happen...
            return None
        inquiryData = (linkedInquiry, [])
        #we want to display the fields corresponding to the Inquiry
        #the linkedInquiry can be the licence itself or an Inquiry object
        inquiryAttributes = Inquiry.schema.filterFields(isMetadata=False)
        #do not take the 2 first fields into account, it is 'id' and 'title'
        inquiryAttributes = inquiryAttributes[2:]
        for inquiryAttribute in inquiryAttributes:
            inquiryAttributeName = inquiryAttribute.getName()
            if inquiryAttributeName == "claimsText":
                #as this text can be very long, we do not want to show it with the other
                #fields, we will display it in the "Claimants" part of the template
                continue
            inquiryData[1].append(inquiryAttributeName)
        return inquiryData

    def getLinkToTheInquiries(self):
        """
          This will return a link to the inquiries on the linked licence
        """
        context = aq_inner(self.context)
        return context.aq_inner.aq_parent.absolute_url() + '/#fieldsetlegend-urban_investigation_and_advices'

    def getLinkedInquiryTitle(self):
        """
          This will return the title of the linked Inquiry
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        if linkedInquiry:
            if not linkedInquiry.portal_type == 'Inquiry':
                #we do not use Title as this inquiry is the licence
                return linkedInquiry.generateInquiryTitle()
            else:
                return linkedInquiry.Title()
