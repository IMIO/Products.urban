def onDelete(ob, event):
    """
      reindex licence after deletion
    """
    ob.aq_inner.aq_parent.reindexObject(idxs=('applicantInfosIndex',))
