# encoding: utf-8

from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError

from eea.faceted.vocabularies.autocomplete import IAutocompleteSuggest

from plone import api

from zope.interface import implements

import json


class UrbanStreetsSuggest(BrowserView):
    """ Autocomplete suggestions on urban streets."""

    implements(IAutocompleteSuggest)

    label = 'Rues urban'

    def __call__(self):
        term = self.request.get('term')
        if not term:
            return

        terms = term.strip().split()
        urban_config = api.portal.get_tool('portal_urban')
        path = '/'.join(urban_config.streets.getPhysicalPath())

        kwargs = {
            'Title': ' AND '.join(["%s*" % x for x in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': path,
            'object_provides': 'Products.urban.interfaces.IStreet',
            'review_state': 'enabled',
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)
        try:
            return json.dumps(
                [{'label': b.Title, 'value': b.UID} for b in brains]
            )
        except ParseError:
            pass


class LicenceReferenceSuggest(BrowserView):
    """ Autocomplete suggestions of licence references."""

    implements(IAutocompleteSuggest)

    label = 'Référence des dossiers'

    def __call__(self):
        term = self.request.get('term')
        if not term:
            return

        terms = term.strip().split()
        portal = api.portal.get()
        path = '/'.join(portal.urban.getPhysicalPath())

        kwargs = {
            'Title': ' AND '.join(["%s*" % t for t in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': path,
            'object_provides': 'Products.urban.interfaces.IGenericLicence',
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)

        try:
            return json.dumps(
                [{'label': b.getReference, 'value': b.getReference} for b in brains]
            )
        except ParseError:
            pass


class CadastralReferenceSuggest(BrowserView):
    """ Autocomplete suggestions on cadastral references."""

    implements(IAutocompleteSuggest)

    label = 'Parcelles urban'

    def __call__(self):
        term = self.request.get('term')
        if not term:
            return

        terms = term.strip().split()
        portal = api.portal.get()
        path = '/'.join(portal.urban.getPhysicalPath())

        kwargs = {
            'Title': ' AND '.join(["%s*" % x for x in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': path,
            'object_provides': 'Products.urban.interfaces.IPortionOut',
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)
        unique_brains = []
        unique_info = set()
        for brain in brains:
            parcel_reference = brain.parcelInfosIndex[0]
            if parcel_reference in unique_info:
                continue
            unique_info.add(parcel_reference)
            unique_brains.append(brain)

        try:
            return json.dumps(
                [{'label': x.Title, 'value': x.parcelInfosIndex[0]} for x in unique_brains]
            )
        except ParseError:
            pass
