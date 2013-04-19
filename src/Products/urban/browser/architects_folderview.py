# -*- coding: utf-8 -*-

from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView
from Products.urban.browser.urbantable import ArchitectsTable


class ArchitectsFolderView(UrbanConfigFolderView):
    """
      This manage the architects folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(ArchitectsTable)

    def getCSSClass(self):
        return 'contenttype-architect button-architect'
