# -*- coding: utf-8 -*-

from Products.urban.services.base import WebService

import requests


class ParcelCoringService(WebService):
    """
    """

    def __init__(self, url=None, coring_type=None, user='', password=''):
        super(ParcelCoringService, self).__init__(url, user, password)
        self.coring_type = coring_type

    def get_coring(self, parcels_wkt, coring_type=None):
        """
        """
        params = {
            'st': coring_type or self.coring_type,
            'geom': parcels_wkt,
        }
        coring_response = requests.post(self.url, data=params, verify='/etc/ssl/certs/ca-certificates.crt')

        return coring_response
