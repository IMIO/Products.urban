# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.services import cadastre
from Products.urban.services import parcel_coring


class ParcelCoringView(BrowserView):
    """
    """

    def coring_result(self):
        """
        """
        status, data = self.core()
        if status != 200:
            return status, data

#        fields_to_update = self.get_fields_to_update(coring_json=data)

        return status, data

#    def fields_to_update(self, coring_json):
#        """
#        """
#        fields_to_update = []
#        for layer in coring_json:
#            field_name = self.get_fieldname(layer),
#            line = {
#                'field_name': field_name,
#                'proposed_value': self.get_value(layer),
#                'current_value': self.get_field_value(field_name),
#            }
#            fields_to_update.append(line)

#        return fields_to_update

    def core(self, coring_type=None):
        """
        """
        parcels = self.context.getOfficialParcels()
        parcels_wkt = cadastre.query_parcels_wkt(parcels)
        coring_response = parcel_coring.get_coring(
            parcels_wkt,
            self.request.get('st', coring_type)
        )

        status = coring_response.status_code
        if status != 200:
            msg = '<h1>{status}</h1><p>{error}</p><p>polygon:</p><p>{polygon}</p>'.format(
                status=status,
                error=coring_response.text,
                polygon=parcels_wkt
            )
            return status, msg

        return status, coring_response.json()
