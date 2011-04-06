from OFS.ObjectManager import BeforeDeleteException

def onDelete(ob, event):
    """
      reindex licence after deletion
    """
    #ob.aq_inner.aq_parent.reindexObject()
    
