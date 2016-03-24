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
        suggestions = [{'label': '', 'value': ''}]
        try:
            suggestions.extend(self.compute_suggestions())
            return json.dumps(suggestions)
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
	    'sort_limit': 30,
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)

        suggestions = [{'label': b.Title, 'value': ' '.join(b.applicantInfosIndex)} for b in brains]
        return suggestions


class RepresentativeSuggestView(SuggestView):
    """
    Base class for autocomplete suggestions of licence representatives
    (architects, geometricians, notaries, ... ).
    """

    contact_type = ''  # to override

    def compute_suggestions(self):
        term = self.request.get('term')
        if not term:
            return

        portal = api.portal.get()
        terms = term.strip().split()

        kwargs = {
            'Title': ' AND '.join(["%s*" % t for t in terms]),
            'sort_on': 'sortable_title',
            'path': '/'.join(portal.urban.getPhysicalPath()),
            'portal_type': self.contact_type,
        }

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(**kwargs)

        suggestions = [{'label': b.Title, 'value': [b.UID]} for b in brains]
        return suggestions


class ArchitectSuggest(RepresentativeSuggestView):
    """
    Autocomplete suggestions of licence architects.
    """

    label = 'Architecte'
    contact_type = 'Architect'


class GeometricianSuggest(RepresentativeSuggestView):
    """
    Autocomplete suggestions of licence geometrician.
    """

    label = 'Géomètre'
    contact_type = 'Geometrician'


class NotarySuggest(RepresentativeSuggestView):
    """
    Autocomplete suggestions of licence notary.
    """

    label = 'Notaire'
    contact_type = 'Notary'


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
            'object_provides': [
                'Products.urban.interfaces.IStreet',
                'Products.urban.interfaces.ILocality'
            ],
            'review_state': 'enabled',
            'sort_limit': 30,
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
            'sort_limit': 30,
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
            'object_provides': 'Products.urban.interfaces.ILicencePortionOut',
            'sort_limit': 30,
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
