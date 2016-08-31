def setLinkedInquiry(ob, event):
    """
      After creation, link me to my Inquiry
    """
    #find the right inquiry and link me to it
    inquiries = ob.aq_inner.aq_parent.getAllInquiries()
    existingUrbanEventInquiries = ob.aq_inner.aq_parent.getUrbanEventInquiries()
    myinquiry = inquiries[len(existingUrbanEventInquiries)-1]
    ob.setLinkedInquiry(myinquiry)
