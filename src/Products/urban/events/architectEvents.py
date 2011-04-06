from OFS.ObjectManager import BeforeDeleteException

def beforeDelete(ob, event):
    """
      Before deleting, check that no licence is linked to the architect
    """
    title = ob.Title()
    ob.getBRefs()
    if ob.getBRefs():
        raise BeforeDeleteException, "This architect is linked to a licence.  You can not delete it!!!"
