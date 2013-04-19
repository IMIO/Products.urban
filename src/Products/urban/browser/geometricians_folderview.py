# -*- coding: utf-8 -*-

from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView
from Products.urban.browser.urbantable import GeometriciansTable


class GeometriciansFolderView(UrbanConfigFolderView):
    """
      This manage the geometricans folder config view
    """
    def renderListing(self):
        return self.renderObjectListing(GeometriciansTable)

    def getCSSClass(self):
        return 'contenttype-geometrician button-geometrician'
