# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement
from Products.urban import services


class NoticeParcel(NoticeElement):
    _excluded_keys = (
        "parcel",
        "capakey",
    )

    def __init__(self, service, json):
        self.service = service
        self.json = json
        self.outdated = False

    def _find_parcel(self):
        """Try to find a parcel that match informations"""
        cadastre = services.cadastre.new_session()
        result = cadastre.query_parcel_by_capakey(self.capakey)
        if not result:
            result = cadastre.query_old_parcel_by_capakey(self.capakey)
            if result:
                self.outdated = True
        return result

    @property
    def parcel(self):
        """Return parcel from database"""
        if not hasattr(self, "_parcel"):
            self._parcel = self._find_parcel()
        return self._parcel

    @property
    def type(self):
        return "Parcel"

    @property
    def capakey(self):
        return self._get_data("capakey")

    @property
    def id(self):
        return self.capakey.replace("/", "_")

    @property
    def division(self):
        return self._get_data("codeDivision")

    @property
    def section(self):
        return self._get_data("section")

    @property
    def radical(self):
        return self._get_data("radical")

    @property
    def bis(self):
        return self._get_data("bisTier")

    @property
    def exposant(self):
        return self._get_data("exponent")

    @property
    def puissance(self):
        return self._get_data("power")

    @property
    def partie(self):
        return self._get_data("part")