## -*- coding: utf-8 -*-

from Products.Five import BrowserView


class UrbanConfigFolderView(BrowserView):
    """
      This manage methods common in all config folders view out of the portal_urban
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderObjectListing(self, table):
        if not self.context.objectValues():
            return ''
        listing = table(self.context, self.request)
        listing.update()
        listing_render = listing.render()
        batch_render = listing.renderBatch()
        return '%s%s' % (listing_render, batch_render)

    def getCSSClass(self):
        return ''
