# -*- coding: utf-8 -*-

from Products.urban.services.base import WebService


class GigService(WebService):
    """
    Service specific to gig service
    """
    def __init__(self, url="", user="", password=""):
        super(GigService, self).__init__(url, user=user, password=password)
