# encoding: utf-8

from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError

from eea.faceted.vocabularies.autocomplete import IAutocompleteSuggest

from plone import api

from zope.interface import implements

import json


class SuggestView(BrowserView):
    """ Autocomplete suggestions base class."""

    implements(IAutocompleteSuggest)

    def __call__(self):
        try:
            return json.dumps(self.compute_suggestions())
        except ParseError:
            pass


class ApplicantSuggest(SuggestView):
    """ Autocomplete suggestions of licence applicants."""

    label = 'Demandeur(s)/propriétaire(s)'

    def compute_suggestions(self):
        term = self.request.get('term')
        if not term:
            return

        terms = term.strip().split()

        kwargs = {
            'applicantInfosIndex': ' AND '.join(["%s*" % t for t in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': '/'.join(self.context.getPhysicalPath()),
            'object_provides': 'Products.urban.interfaces.IApplicant',
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)

        suggestions = [{'label': b.Title, 'value': ' '.join(b.applicantInfosIndex)} for b in brains]
        return suggestions


class UrbanStreetsSuggest(SuggestView):
    """ Autocomplete suggestions on urban streets."""

    label = 'Rues urban'

    def compute_suggestions(self):
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

        suggestions = [{'label': b.Title, 'value': b.UID} for b in brains]
        return suggestions


class LicenceReferenceSuggest(SuggestView):
    """ Autocomplete suggestions of licence references."""

    label = 'Référence des dossiers'

    def compute_suggestions(self):
        term = self.request.get('term')
        if not term:
            return

        terms = term.strip().split()

        kwargs = {
            'Title': ' AND '.join(["%s*" % t for t in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': '/'.join(self.context.getPhysicalPath()),
            'object_provides': 'Products.urban.interfaces.IGenericLicence',
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)

        suggestions = [{'label': b.getReference, 'value': b.getReference} for b in brains]
        return suggestions


class CadastralReferenceSuggest(SuggestView):
    """ Autocomplete suggestions on cadastral references."""

    label = 'Parcelles urban'

    def compute_suggestions(self):
        term = self.request.get('term')
        if not term:
            return

        terms = term.strip().split()

        kwargs = {
            'Title': ' AND '.join(["%s*" % x for x in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': '/'.join(self.context.getPhysicalPath()),
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

        suggestions = [{'label': x.Title, 'value': x.parcelInfosIndex[0]} for x in unique_brains]
        return suggestions
