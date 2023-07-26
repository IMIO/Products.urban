# -*- coding: utf-8 -*-

# from Acquisition import aq_inner

from Products.Five import BrowserView

import urllib


class GigCoringView(BrowserView):
    """
    view to send parcels id and connect to gig interface
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def open_gig_and_load_parcels(self):
        licence = self.context
        capakeys = [urllib.quote(parcel.capakey, safe='') for parcel in licence.getParcels()]
        gig_url = "https://carto.luxembourg.be/matcad?matrices={}&post_carottage={}/gig_coring_response".format(
            ','.join(capakeys),
            urllib.quote(licence.absolute_url(), safe=''),
        )
        return self.request.RESPONSE.redirect(gig_url)


class GigCoringResponse(BrowserView):
    """
    Store coring result on coringResult field of the licence.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, **kwargs):
        self.request.RESPONSE.setHeader(
            "Access-Control-Allow-Origin", self.request.get("HTTP_ORIGIN")
        )
        self.request.RESPONSE.setHeader(
            "Access-Control-Allow-Headers", "content-type,x-requested-with"
        )
        self.request.RESPONSE.setHeader("Access-Control-Allow-Methods", "POST, PATCH")
        if self.request.get("REQUEST_METHOD") == "OPTIONS":
            self.request.RESPONSE.setStatus(204, reason="No Content", lock=True)
        else:
            self.context.setCoringResult(self.request["BODY"])
            return self.request.RESPONSE.redirect(self.context.absolute_url())
