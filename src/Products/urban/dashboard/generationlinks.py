# -*- coding: utf-8 -*-


from eea.facetednavigation.interfaces import IFacetedNavigable

from imio.dashboard.browser.overrides import IDDocumentGeneratorLinksViewlet

from plone import api


class DashboardLinksViewlet(IDDocumentGeneratorLinksViewlet):

    def available(self):
        """
        Enable the generation links only on dashboard contexts.
        """
        return IFacetedNavigable.providedBy(self.context)

    def get_all_pod_templates(self):
        """
        All dashboard PODTemplates are in dashboardtemplates
        folder.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        templates_folder = portal_urban.dashboardtemplates
        templates = templates_folder.objectValues()

        return templates
