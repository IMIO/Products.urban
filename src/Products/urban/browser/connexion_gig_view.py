# -*- coding: utf-8 -*-

# from Acquisition import aq_inner

from Products.Five import BrowserView


class ConnexionGigView(BrowserView):
    """
    view to send parcels id and connect to gig interface
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def connexionGig(self):
#        parcels_keys = [p.capakey for p in self.context.getParcels()]
#        engine = create_engine("mysql+pymysql://GIG_TRANS:GIG_TRANS@193.190.113.125/sigped")
        import ipdb; ipdb.set_trace()
