# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import collections
import json

from Products.urban import services


class CoringUtility(object):
    fieldname = ''
    vocabulary_name = ''
    valuetype = 'list'
    coring_attribute = u''

    def __init__(self, values, context):
        self.values = values
        self.context = context
        voc = getUtility(IVocabularyFactory, name=self.vocabulary_name)
        self.vocabulary = voc(context, all=True)

    @property
    def _coring_values(self):
        values = []
        normalizer = getUtility(IIDNormalizer)
        if self.values.get('attributes', []):
            for attributes in self.values.get('attributes', []):
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

    def _to_reference(self, values):
        terms = self._get_terms(values)
        return [t.title for t in terms]

    def _convert_to_value(self, values):
        method = getattr(self, '_to_{0}'.format(self.valuetype), None)
        if method:
            return method(values)
        return values

    def _display_values(self, values, terms):
        if self.valuetype == 'str':
            return values
        if self.valuetype == 'reference':
            catalog = api.portal.get_tool('portal_catalog')
            return [b.Title for b in catalog(UID=values)]
        return [t.title for t in terms]

    def get_values(self):
        raw_values = self._coring_values
        terms = self._get_terms(raw_values)
        values = [t.token for t in terms]
        values = self._convert_to_value(values)
        display_values = self._display_values(values, terms)
        return self.fieldname, {
            'values': values,
            'display_values': display_values,
            'type': self.valuetype,
        }


class CoringReferenceUtility(CoringUtility):
    """ """

    def get_values(self):
        raw_values = self._coring_values
        terms = self._get_terms(raw_values)
        values = [t.token for t in terms]
        values = self._convert_to_value(values)
        display_values = self._display_values(values, terms)
        return self.fieldname, {
            'values': values,
            'display_values': display_values,
            'type': self.valuetype,
        }


class CoringSOLZone(CoringUtility):
    fieldname = 'pcaZone'
    vocabulary_name = 'urban.vocabulary.SOLZones'
    valuetype = 'list'
    coring_attribute = u'CODECARTO'


class CoringSOLBoolean(CoringSOLZone):
    fieldname = 'isInPCA'
    vocabulary_name = 'urban.vocabulary.SOLZonesBoolean'
    valuetype = 'boolean'


class CoringProtectedBuilding(CoringUtility):
    fieldname = 'protectedBuilding'
    vocabulary_name = 'urban.vocabulary.ProtectedBuilding'
    valuetype = 'list'
    coring_attribute = u'CODECARTO'


class CoringNatura2000(CoringUtility):
    fieldname = 'natura_2000'
    vocabulary_name = 'urban.vocabulary.Natura2000'
    valuetype = 'list'
    coring_attribute = u'CODE_SITE'


class CoringParcellings(CoringReferenceUtility):
    fieldname = 'parcellings'
    vocabulary_name = 'urban.vocabulary.Parcellings'
    valuetype = 'reference'
    coring_attribute = u'CODEUNIQUE'


class CoringParcellingsBoolean(CoringParcellings):
    fieldname = 'isInSubdivision'
    vocabulary_name = 'urban.vocabulary.Parcellings'
    valuetype = 'boolean'

    def _to_boolean(self, values):
        return [bool(values)]


class CoringReparcellings(CoringUtility):
    fieldname = 'reparcellingDetails'
    vocabulary_name = 'urban.vocabulary.Reparcelling'
    valuetype = 'str'
    coring_attribute = u'CODECARTO'

    def _to_str(self, values):
        terms = self._get_terms(values)
        return [u', '.join([t.title for t in terms])]


class CoringNoteworthyTrees(CoringUtility):
    fieldname = 'noteworthyTrees'
    vocabulary_name = 'urban.vocabulary.NoteworthyTrees'
    valuetype = 'list'
    coring_attribute = u'SITEAR'


class CoringFolderZone(CoringUtility):
    fieldname = 'folderZone'
    vocabulary_name = 'urban.vocabulary.AreaPlan'
    valuetype = 'list'
    coring_attribute = u'AFFECT'


class CoringFolderZonePIP(CoringUtility):
    fieldname = 'folderZone'
    vocabulary_name = 'urban.vocabulary.AreaPlan'
    valuetype = 'list'
    coring_attribute = u'STYPE'


class CoringCatchmentArea(CoringUtility):
    fieldname = 'catchmentArea'
    vocabulary_name = 'urban.vocabulary.CatchmentArea'
    valuetype = 'list'
    coring_attribute = u'TYPE_CODE'


MATCH_CORING = {
    2: CoringNatura2000,
    8: (CoringParcellings, CoringParcellingsBoolean),
    12: CoringProtectedBuilding,
    16: CoringProtectedBuilding,
    18: CoringProtectedBuilding,
    14: CoringNoteworthyTrees,
    15: CoringNoteworthyTrees,
    29: CoringFolderZone,
    30: CoringReparcellings,
    37: CoringFolderZonePIP,
    38: CoringFolderZone,
    39: CoringFolderZone,
    40: CoringFolderZone,
    41: CoringFolderZone,
    42: CoringCatchmentArea,
    43: CoringCatchmentArea,
    44: CoringCatchmentArea,
    46: (CoringSOLZone, CoringSOLBoolean),
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
            print layer['layer_id']
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
            new_value, display_values = self._format_values(field_values)
            fields_to_update.append({
                'field': key,
                'label': getattr(context_field.widget, 'label_msgid',
                                    context_field.widget.label),
                'new_value_display': ', '.join(display_values),
                'new_value': new_value and json.dumps(new_value) or '',
            })
        return fields_to_update

    @staticmethod
    def _compare_values(new_value, current_value):
        new_value = ParcelCoringView._cleanup_for_comparison(new_value)
        current_value = ParcelCoringView._cleanup_for_comparison(current_value)
        return current_value != new_value

    @staticmethod
    def _cleanup_for_comparison(value):
        """cleanup value for comparison"""
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = [e for e in value if e]
        else:
            value = [value]
        tags = ('<p>', '</p>', '<b>', '</b>', '<strong>', '</strong>')
        result = []
        for v in value:
            for tag in tags:
                if isinstance(v, basestring):
                    v = v.replace(tag, '')
            result.append(v)
        return result

    def _format_values(self, field_values):
        values = []
        map(values.extend, [e['values'] for e in field_values])
        if field_values[0]['type'] == 'boolean':
            values = True in values
            return values, [{True: u'Oui', False: u'Non'}.get(values)]
        display_values = []
        map(display_values.extend, [e['display_values'] for e in field_values])
        if field_values[0]['type'] == 'str':
            return ', '.join(values), display_values
        return tuple(values), display_values

    def core(self, coring_type=None):
        """
        """
        parcels = self.context.getOfficialParcels()
        cadastre = services.cadastre.new_session()
        parcels_wkt = cadastre.query_parcels_wkt(parcels)
        cadastre.close()

        parcel_coring = services.parcel_coring
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
