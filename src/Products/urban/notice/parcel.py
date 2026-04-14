# -*- coding: utf-8 -*-

from Products.urban import services
from Products.urban.notice.base import NoticeElement
from plone import api

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
        return self._get_data("radical").lstrip("0")

    @property
    def bis(self):
        return self._get_data("bisTer").lstrip("0")

    @property
    def exposant(self):
        return self._get_data("exponent")

    @property
    def puissance(self):
        return self._get_data("power").lstrip("0")

    @property
    def partie(self):
        return self._get_data("part")

    @property
    def division_text(self):
        return self._get_data("division")

    @property
    def resolved_division(self):
        code = self._get_data("codeDivision")
        if code:
            return code
        #do mapping 
        division_name = self._get_data("division")
        if not division_name:
            return None
        division_name = division_name.strip().upper()
        if not division_name:
            return None
        urban_tool = api.portal.get_tool("portal_urban")
        divisions = urban_tool.getDivisionsRenaming()

        mapping = {
            div.get("alternative_name", "").strip().upper(): str(div.get("division"))
            for div in divisions
            if div.get("alternative_name") and div.get("division")
        }
        return mapping.get(division_name)
