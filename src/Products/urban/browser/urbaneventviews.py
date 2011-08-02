from Acquisition import aq_inner
from zope.i18n import translate
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

class UrbanEventInquiryView(UrbanEventView):
    """
      This manage the view of UrbanEventInquiry
      It is based on the default UrbanEventView
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.linkedInquiry = self.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !'), type="error")

    def getInquiryData(self):
        """
          This will return data to display about the UrbanEventInquiry
          See UrbanEventView.getData doc string
        """
        context = aq_inner(self.context)
        linkedInquiry = self.getLinkedInquiry()
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
    
    def getLinkedInquiry(self):
        """
          Return the right object to find data about the inquiry
          This object can be a licence if this is the first inquiry or an
          "Inquiry" for the next inquiries
        """
        context = aq_inner(self.context)
        #find the position of the current UrbanEventInquiry
        #and get the corresponding data
        urbanEventInquiries = context.aq_inner.aq_parent.getUrbanEventInquiries()
        contextUID = context.UID()
        i = 0
        for urbanEventInquiry in urbanEventInquiries:
            if urbanEventInquiry.UID() == contextUID:
                break
            i = i + 1
        inquiries = context.aq_inner.aq_parent.getInquiries()
        if i >= len(inquiries):
            #here we have a problem with a UrbanEventInquiry that is not linked to any
            #existing Inquiry.  This should not happen...
            return None
        else:
            return inquiries[i]

    def getLinkedInquiryTitle(self):
        """
          Returns the title of the linked Inquiry object
          We want to show in the title the number of the Inquiry
        """
        context = aq_inner(self.context)
        #find the position of the current UrbanEventInquiry
        #and get the corresponding data
        urbanEventInquiries = context.aq_inner.aq_parent.getUrbanEventInquiries()
        contextUID = context.UID()
        i = 1
        for urbanEventInquiry in urbanEventInquiries:
            if urbanEventInquiry.UID() == contextUID:
                break
            i = i + 1
        #here, i is the number of the UrbanEventInquiry that is corresponding to the 'ith'
        #Inquiry object
        return translate('inquiry_title_and_number', 'urban', mapping={'number': i}, context=context.REQUEST)