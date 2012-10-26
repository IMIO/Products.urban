## -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

class UrbanConfigFolderView(BrowserView):
    """
      This manage methods common in all config folders view out of the portal_urban
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def listObjects(self, portal_type, context=None, batchlen=50):
        context = context and contenxt or aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        queryString = {'portal_type': portal_type,
                       'path':'/'.join(context.getPhysicalPath()),
                       'sort_on':'getObjPositionInParent'}
        res = portal_catalog(queryString)
        b_start = context.REQUEST.get('b_start', 0)
        return Batch(res, batchlen, int(b_start), orphan=0)

