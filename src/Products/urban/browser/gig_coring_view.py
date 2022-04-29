# -*- coding: utf-8 -*-

# from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.urban import services


class GigCoringView(BrowserView):
    """
    view to send parcels id and connect to gig interface
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def open_gig_and_load_parcels(self):
        licence = self.context
        capakeys = [parcel.capakey for parcel in licence.getParcels()]
        gig_session = services.gig.new_session()
        gig_session.insert_parcels(capakeys)
        gig_session.close()
        return self.request.RESPONSE.redirect('https://www.gigwal.org/')
