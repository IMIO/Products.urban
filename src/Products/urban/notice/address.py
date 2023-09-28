# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement
from Products.urban import utils


class NoticeAddress(NoticeElement):
    _notice_keys = ("notice_street",)
    _excluded_keys = (
        "address",
        "search_term",
        "municipality",
        "locality",
        "postCode",
    )

    def __init__(self, service, json):
        self.service = service
        self.json = json

    def _find_address(self):
        """Try to find an address"""
        result = utils.find_address(self.search_term, exact_match=True)
        if not result:
            result = utils.find_address(self.search_term, exact_match=False)
        return result

    @property
    def address(self):
        if not hasattr(self, "_address"):
            self._address = self._find_address()
        return self._address

    @property
    def search_term(self):
        """Return a search term based on parameters"""
        if not self.notice_street:
            return
        term = self.notice_street
        if self.postCode:
            term = "{0} {1}".format(term, self.postCode)
        if self.locality:
            term = "{0} {1}".format(term, self.locality)

    @property
    def street(self):
        """UID of the street in Urban"""
        if not self.address:
            return
        if len(self.address) == 1:
            return self.address[0]["id"]

    @property
    def municipality(self):
        return self._get_data("municipality")

    @property
    def locality(self):
        return self._get_data("locality")

    @property
    def postCode(self):
        return self._get_data("postCode")

    @property
    def notice_street(self):
        return self._get_data("notice_street")

    @property
    def number(self):
        box_nbr = self._get_data("boxNumber")
        house_nbr = self._get_data("houseNumber")
        if not house_nbr:
            return ""
        if box_nbr:
            return "{0} {1}".format(house_nbr, box_nbr)
        return house_nbr