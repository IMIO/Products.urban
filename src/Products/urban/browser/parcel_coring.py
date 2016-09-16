# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from Products.urban.services import cadastre
from Products.urban.services import parcel_coring

from plone import api

import json

MATCH_CORING = {'folderprotectedbuildings': {'coringids': [17, 20, 19, 16, 18],
                                             'fieldname': 'protectedBuilding',
                                             'valuetype': 'list',
                                             },
                'folerzones': {'coringids': [12, 2],
                               'fieldname': 'folderZone',
                               'valuetype': 'list',
                               },
                'PCA': {'coringids': [7],
                        'fieldname': 'isInPCA',
                        'valuetype': 'bool',
                        },
                'LOTISSEMENT': {'coringids': [8],
                                'fieldname': 'isInSubdivision',
                                'valuetype': 'bool',
                                },
                }


class Coring(object):

    def __init__(self, layer):
        for l in layer:
            setattr(self, l, layer[l])
        self.catalog = api.portal.get_tool('portal_catalog')
        self.portal_urban = api.portal.get_tool('portal_urban')
        self.folderzone_folder = self.portal_urban.folderzones

    @property
    def type(self):
        for key in MATCH_CORING:
            if self.layer_id in MATCH_CORING[key]['coringids']:
                return key

    @property
    def valuetype(self):
        if self.type:
            return MATCH_CORING[self.type]['valuetype']

    @property
    def fieldname(self):
        if self.type:
            return MATCH_CORING[self.type]['fieldname']

    def getValues(self):
        if self.valuetype == 'bool':
            return self.fieldname, [True], 'Vrai'
        voc_folder = self.portal_urban.get(self.type)
        if not voc_folder:
            return '', [], ''
        folder_path = '/'.join(voc_folder.getPhysicalPath())
        values = []
        display_values = []
        for layer_value in self.attributes:
            layer_name = layer_value['attributes'].get('layerName')
            if self.layer_id not in voc_folder.objectIds():
                voc_brains = self.catalog(portal_type='UrbanVocabularyTerm', path={'query': folder_path, 'depth': 1})
                voc_brains = [i for i in voc_brains if i.getObject()['coring_id'] == self.layer_id]
                if len(voc_brains) == 1:
                    values.append(voc_brains[0].id)
                    display_values.append(voc_brains[0].Title)
                    continue
                else:
                    with api.env.adopt_roles(['Manager']):
                        voc_folder.invokeFactory('UrbanVocabularyTerm', id=self.layer_id, coring_id=self.layer_id, title=layer_name)
            values.append(self.layer_id)
            display_values.append(layer_name)
        return self.fieldname, values, ', '.join(display_values)


class ParcelCoringView(BrowserView):
    """
    """

    def __init__(self, context, request):
        """
        """
        super(ParcelCoringView, self).__init__(context, request)
        self.catalog = api.portal.get_tool('portal_catalog')
        self.portal_urban = api.portal.get_tool('portal_urban')
        self.helper = self.context.unrestrictedTraverse('@@document_generation_helper_view')

    def coring_result(self):
        """
        """
        status, data = self.core()
        if status != 200:
            return status, data
        fields_to_update = self.get_fields_to_update(coring_json=data)
        return status, fields_to_update

    def get_fields_to_update(self, coring_json):
        """
        """
        fields_to_update = []
        fields = {}
        for layer in coring_json:
            if not layer.get('attributes'):
                continue
            layer = Coring(layer)
            field_name, proposed_value, display_value = layer.getValues()
            if not field_name:
                continue
            if field_name not in fields:
                fields[field_name] = []
            fields[field_name].append({'field_name': field_name,
                                       'proposed_value': proposed_value,
                                       'proposed_display_value': display_value})
        for key in fields:
            field = fields[key]
            proposed_value = []
            proposed_display_value = []
            [proposed_value.extend(value['proposed_value']) for value in field]
            [proposed_display_value.append(value['proposed_display_value']) for value in field]
            urban_field = self.context.getField(key)
            line = {
                'field_name': key,
                'field_name_label': urban_field.widget.label_msgid,
                'proposed_display_value': ', '.join(proposed_display_value),
                'proposed_value': json.dumps(proposed_value),
                'current_value': urban_field.get(self.context) or 'N.C.',
            }
            if tuple(proposed_value) != urban_field.get(self.context):
                fields_to_update.append(line)
        return fields_to_update

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
