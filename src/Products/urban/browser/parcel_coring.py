# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import collections
import json

from Products.urban.services import cadastre
from Products.urban.services import parcel_coring


class CoringUtility(object):
    fieldname = ''
    vocabulary_name = ''
    valuetype = 'list'
    coring_attribute = u''

    def __init__(self, values, context):
        self.values = values
        self.context = context
        voc = getUtility(IVocabularyFactory, name=self.vocabulary_name)
        self.vocabulary = voc(context)

    @property
    def _coring_values(self):
        values = []
        normalizer = getUtility(IIDNormalizer)
        for attributes in self.values['attributes']:
            values.append(attributes['attributes'][self.coring_attribute])
        return map(normalizer.normalize, values)

    def _get_terms(self, values):
        return map(
            self.vocabulary.getTermByToken,
            [v for v in values if v in self.vocabulary.by_token],
        )

    @staticmethod
    def _to_str(values):
        return [u', '.join(values)]

    def _to_boolean(self, values):
        terms = self._get_terms(values)
        return [True in [t.title for t in terms]]

    def _convert_to_value(self, values):
        method = getattr(self, '_to_{0}'.format(self.valuetype), None)
        if method:
            return method(values)
        return values

    def _display_values(self, values, raw_values):
        if self.valuetype == 'str':
            return values
        terms = self._get_terms(raw_values)
        return [t.title for t in terms]

    def get_values(self):
        raw_values = self._coring_values
        values = self._convert_to_value(raw_values)
        display_values = self._display_values(values, raw_values)
        return self.fieldname, {
            'values': values,
            'display_values': display_values,
            'type': self.valuetype,
        }


class CoringPCA(CoringUtility):
    fieldname = 'pca'
    vocabulary_name = 'urban.vocabulary.PCAZones'
    valuetype = 'list'
    coring_attribute = u'CODECARTO'


class CoringPCABoolean(CoringPCA):
    fieldname = 'isInPCA'
    vocabulary_name = 'urban.vocabulary.PCAZonesBoolean'
    valuetype = 'boolean'


class CoringProtectedBuilding(CoringUtility):
    fieldname = 'protectedBuilding'
    vocabulary_name = 'urban.vocabulary.ProtectedBuilding'
    valuetype = 'list'
    coring_attribute = u'Code carto'


class CoringNatura2000(CoringUtility):
    fieldname = 'natura_2000'
    vocabulary_name = 'urban.vocabulary.Natura2000'
    valuetype = 'list'
    coring_attribute = u'Code du site'


class CoringParcellings(CoringUtility):
    fieldname = 'subdivisionDetails'
    vocabulary_name = 'urban.vocabulary.Parcellings'
    valuetype = 'str'
    coring_attribute = u'CODEUNIQUE'

    def _to_str(self, values):
        terms = self._get_terms(values)
        values = [u'{0} ({1})'.format(t.title, t.token) for t in terms]
        return [u', '.join(values)]


class CoringParcellingsBoolean(CoringParcellings):
    fieldname = 'isInSubdivision'
    vocabulary_name = 'urban.vocabulary.ParcellingsBoolean'
    valuetype = 'boolean'


class CoringNoteworthyTrees(CoringUtility):
    fieldname = 'noteworthyTrees'
    vocabulary_name = 'urban.vocabulary.NoteworthyTrees'
    valuetype = 'list'
    coring_attribute = u'N\xb0 du site'


MATCH_CORING = {
    2: CoringNatura2000,
    7: (CoringPCA, CoringPCABoolean),
    8: (CoringParcellings, CoringParcellingsBoolean),
    12: CoringProtectedBuilding,
    16: CoringProtectedBuilding,
    18: CoringProtectedBuilding,
    14: CoringNoteworthyTrees,
    15: CoringNoteworthyTrees,
}


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
            if layer.get('layer_id') not in MATCH_CORING:
                continue
            classes = MATCH_CORING[layer['layer_id']]
            if not isinstance(classes, collections.Iterable):
                classes = [classes]
            for cls in classes:
                coring = cls(layer, self.context)
                fieldname, values = coring.get_values()
                if fieldname not in fields:
                    fields[fieldname] = []
                fields[fieldname].append(values)
        for key, field_values in fields.items():
            context_field = self.context.getField(key)
            if not context_field:
                continue
            current_value = context_field.get(self.context)
            values, display_values = self._format_values(field_values)
            if values != current_value:
                fields_to_update.append({
                    'field': key,
                    'label': context_field.widget.label_msgid,
                    'new_value_display': ', '.join(display_values),
                    'new_value': json.dumps(values),
                })
        return fields_to_update

    def _format_values(self, field_values):
        values = []
        map(values.extend, [e['values'] for e in field_values])
        if field_values[0]['type'] == 'boolean':
            values = True in values
            return values, [{True: u'Oui', False: u'Non'}.get(values)]
        display_values = []
        map(display_values.extend, [e['display_values'] for e in field_values])
        if field_values[0]['type'] == 'str':
            values = ', '.join(values)
        return tuple(values), display_values

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
            msg = u'<h1>{status}</h1><p>{error}</p><p>polygon:</p><p>{polygon}</p>'.format(
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
