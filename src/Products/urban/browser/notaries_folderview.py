# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView

class NotariesFolderView(UrbanConfigFolderView):
    """
      This manage the notaries folder config view
    """
    def __init__(self, context, request):
        super(UrbanConfigFolderView, self).__init__(context, request)
        self.context = context
        self.request = request


    def listObjects(self, batchlen):
        return super(NotariesFolderView, self).listObjects('Notary', batchlen=batchlen)

    def getCSSClass(self):
        return 'contenttype-notary button-notary'

    def getColumnLabel(self):
        return 'notary_data'
