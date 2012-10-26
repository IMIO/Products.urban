# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView

class GeometriciansFolderView(UrbanConfigFolderView):
    """
      This manage the geometricans folder config view
    """
    def __init__(self, context, request):
        super(UrbanConfigFolderView, self).__init__(context, request)
        self.context = context
        self.request = request


    def listObjects(self, batchlen):
        return super(GeometriciansFolderView, self).listObjects('Geometrician', batchlen=batchlen)

    def getCSSClass(self):
        return 'contenttype-geometrician button-geometrician'

    def getColumnLabel(self):
        return 'geometrician_data'
