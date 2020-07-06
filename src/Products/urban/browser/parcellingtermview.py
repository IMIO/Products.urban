# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.urban.browser.table.urbantable import ParcelsTable


class ParcellingTermView(BrowserView):
    """
    This manage methods of ParcellingTerm view
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ""
        parceltable = ParcelsTable(self.context, self.request, values=parcels)
        parceltable.update()
        render = parceltable.render()
        return render
