def onDelete(ob, event):
    """
      reindex licence after deletion
    """
    parent = ob.aq_inner.aq_parent
    #as the name of the applicant appears in the licence's title, update it!
    parent.updateTitle()
