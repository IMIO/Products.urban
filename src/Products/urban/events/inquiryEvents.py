def beforeDelete(ob, event):
    """
      Check that we can delete this inquiry...
      We can not delete an Inquiry if an UrbanEventInquiry is linked
    """
    #XXX too late???
    #XXX the code here above is useless as every references have already
    #XXX been removed here...  We use manage_beforeDelete...
    #if ob.getLinkedUrbanEventInquiry():
    #    raise BeforeDeleteException, "You can not..."

def afterDelete(ob, event):
    """
      After having deleted an Inquiry, we need to generate
      the title of the others so we have something coherent as
      the number of the inquiry is in the title
    """
    for inquiry in ob.getInquiries():
        inquiry.setTitle(inquiry.generateInquiryTitle())
        inquiry.reindexObject(idxs=('title',))

def setGeneratedTitle(ob, event):
    """
      Set my title
    """
    ob.setTitle(ob.generateInquiryTitle())
    ob.reindexObject(idxs=('title',))
