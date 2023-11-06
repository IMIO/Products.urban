# -*- coding: utf-8 -*-

from plone import api
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.atfields import DefaultFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces.field import IField
from Products.urban.interfaces import IProductUrbanLayer
from zope.component import adapter
from zope.interface import Interface, implementer


@adapter(IField, IBaseObject, IProductUrbanLayer)
@implementer(IFieldSerializer)
class UrbanDefaultFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        self.results = super(UrbanDefaultFieldSerializer, self).__call__()

        if self.field.getName() in [
            "workLocations",
            "businessOldLocation",
            "publicRoadModifications",
        ]:
            self._resolve_street_uid()
        return self.results

    def _resolve_street_uid(self):
        urban_config = api.portal.get_tool("portal_urban")
        path = "/".join(urban_config.streets.getPhysicalPath())
        result_process = []
        for result in self.results:
            kwargs = {
                "UID": result[u"street"],
                "sort_on": "sortable_title",
                "sort_order": "reverse",
                "path": path,
                "object_provides": [
                    "Products.urban.interfaces.IStreet",
                    "Products.urban.interfaces.ILocality",
                ],
            }

            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog(**kwargs)
            if len(brains) > 0:
                result[u"street"] = brains[0].Title
            result_process.append(result)

        self.result = result_process
