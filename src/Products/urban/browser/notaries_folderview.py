# -*- coding: utf-8 -*-

from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView
from Products.urban.browser.urbantable import NotariesTable


class NotariesFolderView(UrbanConfigFolderView):
    """
      This manage the notaries folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(NotariesTable)

    def getCSSClass(self):
        return 'contenttype-notary button-notary'
