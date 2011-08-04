from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.Inquiry import Inquiry

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

    def getLinkToTheLicence(self):
        """
          This will return a link to the inquiries on the linked licence
        """
        context = aq_inner(self.context)
        return context.aq_inner.aq_parent.absolute_url() + '/#fieldsetlegend-urban_investigation_and_advices'

class UrbanEventInquiryView(UrbanEventView):
    """
      This manage the view of UrbanEventInquiry
      It is based on the default UrbanEventView
    """
    def __init__(self, context, request):
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
            inquiryData[1].append(inquiryAttributeName)
        return inquiryData
