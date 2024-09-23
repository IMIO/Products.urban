# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask

from eea.facetednavigation.search.catalog import FacetedCatalog

# XXX Should be migrated
try:
    from plone.app.collection.interfaces import ICollection
except ImportError:

    class ICollection(Interface):
        """plone.app.collection not installed"""


from Products.urban.interfaces import IFacetedCollection

from zope.component import queryAdapter
from zope.interface import implements


class UrbanFacetedCatalog(FacetedCatalog):
    def __call__(self, context, **query):
        """ """
        faceted_context = queryAdapter(context, IFacetedCollection) or context
        return super(UrbanFacetedCatalog, self).__call__(faceted_context, **query)


class LicenceToFacetedCollection(object):
    implements(
        ICollection,
        IFacetedCollection,
    )

    def __init__(self, licence):
        self.licence = licence

    def getRawQuery(self):
        """ """
        query = [
            {
                "i": "object_provides",
                "o": "plone.app.querystring.operation.selection.is",
                "v": ITask.__identifier__,
            },
            {
                "i": "path",
                "o": "plone.app.querystring.operation.string.relativePath",
                "v": ".",
            },
        ]
        return query

    def __getattr__(self, attrname):
        return getattr(self.licence, attrname)
