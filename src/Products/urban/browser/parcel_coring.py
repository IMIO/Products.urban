# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.services import cadastre
from Products.urban.services import parcel_coring


class ParcelCoringView(BrowserView):
    """
    """

    def __call__(self, coring_type=None):
        """
        """
        parcels = self.context.getOfficialParcels()
        parcels_wkt = cadastre.query_parcels_wkt(parcels)

        coring_response = parcel_coring.get_coring(
            parcels_wkt,
            self.request.get('st', coring_type)
        )
        if coring_response.status_code != 200:
            msg = '<p>message:</p><p>{error}</p><p>polygon:</p><p>{polygon}</p>'.format(
                error=coring_response.text,
                polygon=parcels_wkt
            )
            return msg

        return coring_response.text
