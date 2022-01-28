# -*- coding: utf-8 -*-

# from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.urban import services
import requests


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
        #
        # To Do: open gig application in another tab of the browser
        #
        gig_coring = requests.get('https://carto.luxembourg.be/', verify='/etc/ssl/certs/ca-certificates.crt')
        return gig_coring
