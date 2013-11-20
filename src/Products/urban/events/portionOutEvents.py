from Products.CMFCore.utils import getToolByName


def onDelete(parcel, event):
    """
      Reindex licence of this parcel after deletion.
    """
    parcel.aq_inner.aq_parent.reindexObject(idxs=["parcelInfosIndex"])


def setValidParcel(parcel, event):
    """
     Check if the manually added parcel exists in he cadastral DB
     and set its "isvalidparcel" attribute accordingly.
    """
    urban_tool = getToolByName(parcel, 'portal_urban')
    references = {
        'division': parcel.getDivisionCode(),
        'section': parcel.getSection(),
        'radical': parcel.getRadical(),
        'bis': parcel.getBis(),
        'exposant': parcel.getExposant(),
        'puissance': parcel.getPuissance(),
    }
    exists_in_DB = urban_tool.queryParcels(
        browseold=True,
        fuzzy=False,
        **references
    ) and True or False
    parcel.setIsOfficialParcel(exists_in_DB)
    if exists_in_DB:
        if not urban_tool.queryParcels(fuzzy=False, **references):
            parcel.setOutdated(True)
        else:
            parcel.setOutdated(False)
    else:
        parcel.setIsOfficialParcel(False)
    parcel.reindexObject()


def setDivisionCode(parcel, event):
    """
     Set the division code value of the parcel
    """
    parcel.setDivisionCode(parcel.getDivision())
    parcel.reindexObject()
