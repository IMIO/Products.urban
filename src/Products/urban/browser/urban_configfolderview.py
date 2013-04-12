## -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.urban.browser.urbantable import ContactTable


class UrbanConfigFolderView(BrowserView):
    """
      This manage methods common in all config folders view out of the portal_urban
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderContactListing(self):
        if not self.context.objectValues():
            return ''
        contactlisting = ContactTable(self.context, self.request)
        contactlisting.update()
        return contactlisting.render()

    def listObjects(self, portal_type, context=None, batchlen=50):
        context = context and context or aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        query_string = {
            'portal_type': portal_type,
            'path': '/'.join(context.getPhysicalPath()),
            'sort_on': 'getObjPositionInParent',
        }
        res = portal_catalog(query_string)
        b_start = context.REQUEST.get('b_start', 0)
        return Batch(res, batchlen, int(b_start), orphan=0)
