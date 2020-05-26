# -*- coding: utf-8 -*-

from collective.documentgenerator.adapters import GenerablePODTemplatesAdapter
from collective.documentgenerator.content.pod_template import IPODtemplate

from plone import api


class GenerableDashboardPODTemplatesAdapter(GenerablePODTemplatesAdapter):
    """ """
    def __init__(self, context):
        self.context = context

    def get_all_pod_templates(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.unrestrictedSearchResults(object_provides=IPODtemplate.__identifier__, sort_on='getObjPositionInParent')
        pod_templates = [self.context.unrestrictedTraverse(brain.getPath()) for brain in brains]

        return pod_templates
