# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.services import cadastre
from Products.urban.services import parcel_coring

from plone import api

import json


class ParcelCoringView(BrowserView):
    """
    """

    def __init__(self, context, request):
        """
        """
        super(ParcelCoringView, self).__init__(context, request)
        self.catalog = api.portal.get_tool('portal_catalog')
        self.portal_urban = api.portal.get_tool('portal_urban')

    def coring_result(self):
        """
        """
#        status, data = self.core()
#        if status != 200:
#            return status, data

#        fields_to_update = self.get_fields_to_update(coring_json=data)
        status, fields_to_update = (
            200,
            [{
                'field_name': 'folderZone',
                'field_name_label': 'urban_label_folderZone',
                'proposed_display_value': 'Zone d\'activité économique industrielle',
                'proposed_value': json.dumps(['zaei']),
                'current_value': self.context.getFolderZone() or 'N.C.',
            }]
        )

        return status, fields_to_update

    def get_fields_to_update(self, coring_json):
        """
        """
        fields_to_update = []
        for layer in coring_json:
            field_name, proposed_value, display_value = self.get_value_from_maplayer(layer)
            if field_name:
                urban_field = self.context.getField(field_name)
                line = {
                    'field_name': field_name,
                    'field_name_label': urban_field.widget.label_msgid,
                    'proposed_display_value': display_value,
                    'proposed_value': json.dumps(proposed_value),
                    'current_value': urban_field.get(self.context) or 'N.C.',
                }
                fields_to_update.append(line)

        return fields_to_update

    def get_value_from_maplayer(self, layer):
        """
        """
        layer_name = layer['description']
        if layer_name == u'SPW PDS Affectation':
            folderzone_folder = self.portal_urban.folderzones
            values, display_values = self.get_vocabulary_value(layer, voc_folder=folderzone_folder, id_key='AFFECT', title_key='value')
            return 'folderZone', values, display_values

        return None, None, None

    def get_vocabulary_value(self, layer, voc_folder, id_key, title_key):
        """
        """
        folder_path = '/'.join(voc_folder.getPhysicalPath())
        values = []
        display_values = []
        for layer_value in layer['attributes']:
            layer_value = layer_value['attributes']

            term_id = layer_value.get(id_key)
            term_title = layer_value.get(title_key)

            if term_id not in voc_folder.objectIds():
                voc_brains = self.catalog(portal_type='UrbanVocabularyTerm', Title=term_title, path={'query': folder_path, 'depth': 1})
                if len(voc_brains) == 1:
                    values.append(voc_brains[0].id)
                    display_values.append(voc_brains[0].Title)
                    continue
                else:
                    with api.env.adopt_roles(['Manager']):
                        voc_folder.invokeFactory('UrbanVocabularyTerm', id=term_id, title=term_title)
            values.append(term_id)
            display_values.append(voc_brains[0].Title)

        return values, ', '.join(display_values)

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


class UpdateLicenceForm(BrowserView):
    """
    """

    def __call__(self):
        """
        """
        for field_name, value in self.request.form.iteritems():
            field = self.context.getField(field_name)
            value = json.loads(value)
            field.getMutator(self.context)(value)

        self.request.RESPONSE.redirect(self.context.absolute_url() + '/view')
