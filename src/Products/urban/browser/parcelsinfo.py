## -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.interfaces import IGenericLicence
from Products.urban.services import cadastre
from Products.urban.services.cadastral import ParcelHistoric

from plone import api


class ParcelsInfo(BrowserView):
    """
    This manage parcelinfos methods.
    """

    def licences_of_parcel(self, parcel):
        """
        Find licences with parcel paramaters
        """
        catalog = api.portal.get_tool('portal_catalog')
        parcel_historic = ParcelHistoric(**parcel.reference_as_dict())
        licence_brains = catalog(
            object_provides=IGenericLicence.__identifier__,
            parcelInfosIndex=parcel_historic.get_all_reference_indexes()
        )
        return licence_brains

    def get_parcel(self, capakey):
        parcel = cadastre.query_parcel_by_capakey(capakey)
        return parcel
