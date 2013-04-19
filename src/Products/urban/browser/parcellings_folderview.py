# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView
from Products.urban.browser.urbantable import ParcellingsTable


class ParcellingsFolderView(UrbanConfigFolderView):
    """
      This manage the parcellings folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(ParcellingsTable)
