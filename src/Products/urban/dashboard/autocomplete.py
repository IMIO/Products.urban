# encoding: utf-8

from Products.Five import BrowserView
from Products.urban.services import cadastre
from Products.ZCTextIndex.ParseTree import ParseError

from eea.faceted.vocabularies.autocomplete import IAutocompleteSuggest

from plone import api

from zope.interface import implements

import json


class SuggestView(BrowserView):
    """Autocomplete suggestions base class."""

    implements(IAutocompleteSuggest)

    def __call__(self):

        suggestions = [{"label": "", "value": ""}]
        try:
            suggestions.extend(self.compute_suggestions())
            return json.dumps(suggestions)
        except ParseError:
            pass


class RepresentativeSuggestView(SuggestView):
    """
    Base class for autocomplete suggestions of licence representatives
    (architects, geometricians, notaries, ... ).
    """

    contact_type = ""  # to override

    def compute_suggestions(self):
        term = self.request.get("term")
        if not term:
            return

        portal = api.portal.get()
        terms = term.strip().split()

        kwargs = {
            "Title": " AND ".join(["%s*" % t for t in terms]),
            "sort_on": "sortable_title",
            "path": "/".join(portal.urban.getPhysicalPath()),
            "portal_type": self.contact_type,
        }

        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog(**kwargs)

        suggestions = [{"label": b.Title, "value": [b.UID]} for b in brains]
        return suggestions


class ArchitectSuggest(RepresentativeSuggestView):
    """
    Autocomplete suggestions of licence architects.
    """

    label = "Architecte"
    contact_type = "Architect"


class GeometricianSuggest(RepresentativeSuggestView):
    """
    Autocomplete suggestions of licence geometrician.
    """

    label = "Géomètre"
    contact_type = "Geometrician"


class NotarySuggest(RepresentativeSuggestView):
    """
    Autocomplete suggestions of licence notary.
    """

    label = "Notaire"
    contact_type = "Notary"


class UrbanStreetsSuggest(SuggestView):
    """Autocomplete suggestions on urban streets."""

    label = "Rues urban"

    def compute_suggestions(self):
        term = self.request.get("term")
        if not term:
            return

        terms = term.strip().split()
        urban_config = api.portal.get_tool("portal_urban")
        path = "/".join(urban_config.streets.getPhysicalPath())

        kwargs = {
            "Title": " AND ".join(["%s*" % x for x in terms]),
            "sort_on": "sortable_title",
            "sort_order": "reverse",
            "path": path,
            "object_provides": [
                "Products.urban.interfaces.IStreet",
                "Products.urban.interfaces.ILocality",
            ],
            "review_state": "enabled",
        }

        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog(**kwargs)

        suggestions = [{"label": b.Title, "value": b.UID} for b in brains]
        return suggestions


class LicenceReferenceSuggest(SuggestView):
    """Autocomplete suggestions of licence references."""

    label = "Référence des dossiers"

    def compute_suggestions(self):
        term = self.request.get("term")
        if not term:
            return

        terms = term.strip().split()

        kwargs = {
            "Title": " AND ".join(["%s*" % t for t in terms]),
            "sort_on": "sortable_title",
            "sort_order": "reverse",
            "path": "/".join(self.context.getPhysicalPath()),
            "object_provides": "Products.urban.interfaces.IGenericLicence",
        }

        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog(**kwargs)

        suggestions = [
            {"label": b.getReference, "value": b.getReference} for b in brains
        ]
        return suggestions


class CadastralReferenceSuggest(SuggestView):
    """Autocomplete suggestions on cadastral references."""

    label = "Parcelles urban"

    def _all_parcels_values(self):
        cat = api.portal.get_tool("portal_catalog")
        values = [v for v in cat.Indexes["parcelInfosIndex"].uniqueValues()]
        session = cadastre.new_session()
        all_divisions = dict(session.get_all_divisions())
        session.close()
        all_divisions = dict([(str(int(k)), v) for k, v in all_divisions.iteritems()])
        all_values = [
            (
                "{} {} {} {} {} {}".format(
                    all_divisions.get(v[0:5]),
                    v[5].lstrip("0"),
                    v[6:10].lstrip("0"),
                    v[11:13].lstrip("0"),
                    v[13].lstrip("0"),
                    v[14:].lstrip("0"),
                ),
                v,
            )
            for v in values
            if len(v) > 14
        ]
        return all_values

    def compute_suggestions(self):
        term = self.request.get("term")
        if len(term) < 4:
            return

        terms = term.strip().split()
        all_parcels = self._all_parcels_values()
        raw_suggestions = [
            (prc, index)
            for prc, index in all_parcels
            if all([t.lower() in prc.lower() for t in terms])
        ]
        suggestions = [{"label": x[0], "value": x[1]} for x in raw_suggestions]
        return suggestions
