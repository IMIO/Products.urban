# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.urban.browser.urban_configfolderview import UrbanConfigFolderView

class ParcellingsFolderView(UrbanConfigFolderView):
    """
      This manage the parcellings folder config view
    """
    def __init__(self, context, request):
        super(UrbanConfigFolderView, self).__init__(context, request)
        self.context = context
        self.request = request


    def listObjects(self, batchlen):
        return super(ParcellingsFolderView, self).listObjects('ParcellingTerm', batchlen=batchlen)

    def getCSSClass(self):
        return ''

    def getColumnLabel(self):
        return 'parcellingterm_data'
