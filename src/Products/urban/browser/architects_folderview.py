# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView

class ArchitectsFolderView(UrbanConfigFolderView):
    """
      This manage the architects folder config view
    """
    def __init__(self, context, request):
        super(UrbanConfigFolderView, self).__init__(context, request)
        self.context = context
        self.request = request


    def listObjects(self, batchlen):
        return super(ArchitectsFolderView, self).listObjects('Architect', batchlen=batchlen)

    def getCSSClass(self):
        return 'contenttype-architect button-architect'

    def getColumnLabel(self):
        return 'architect_data'
