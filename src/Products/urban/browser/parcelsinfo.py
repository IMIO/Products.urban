# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.browser.parcelrecordsview import ParcelRecordsView
from Products.urban.interfaces import IGenericLicence
from Products.urban import services

from plone import api


class ParcelsInfo(ParcelRecordsView):
    """
    This manage parcelinfos methods.
    """

    def licences_of_parcel(self, parcel):
        """
        Find licences with parcel paramaters
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence_brains = catalog(
            object_provides=IGenericLicence.__identifier__,
            parcelInfosIndex=parcel.capakey
        )
        return licence_brains

    def get_parcel(self, capakey):
        cadastre = services.cadastre.new_session()
        parcel = cadastre.query_parcel_by_capakey(capakey)
        cadastre.close()
        return parcel
