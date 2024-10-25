# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.urban.browser.exportimport.interfaces import IConfigExportMarker
from Products.urban.interfaces import ILicenceConfig
from Products.urban.interfaces import IUrbanTool
from collective.exportimport.export_content import ExportContent
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class UrbanExportConfig(ExportContent):
    template = ViewPageTemplateFile("templates/export_urban_config.pt")

    migration = False

    def __call__(
        self,
        portal_type=None,
        path=None,
        depth=-1,
        include_blobs=1,
        download_to_server=False,
        migration=False,
        include_revisions=False,
    ):
        alsoProvides(self.request, IConfigExportMarker)
        output = super(UrbanExportConfig, self).__call__(
            portal_type,
            path,
            depth,
            include_blobs,
            download_to_server,
            migration,
            include_revisions,
        )
        noLongerProvides(self.request, IConfigExportMarker)
        return output

    def add_licence_context(self, item, obj):
        check, context_licence = self.check_in_licence_config(obj)
        if not check:
            return item
        item["licence_url"] = context_licence.absolute_url()
        obj_parent = aq_parent(obj)
        check, context_licence = self.check_in_licence_config(obj_parent)
        if check:
            item["parent"]["licence_url"] = context_licence.absolute_url()
        return item

    def check_in_licence_config(self, context):
        if ILicenceConfig.providedBy(context):
            return True, context
        current = context
        while not IUrbanTool.providedBy(current):
            if ILicenceConfig.providedBy(current):
                return True, current
            current = aq_parent(current)
        return False, None

    def update_export_data(self, item, obj):
        item.pop("@components", None)
        item.pop("next_item", None)
        item.pop("batching", None)
        item.pop("items", None)
        item.pop("previous_item", None)
        item.pop("immediatelyAddableTypes", None)
        item.pop("locallyAllowedTypes", None)
        item = self.add_licence_context(item, obj)
        return super(UrbanExportConfig, self).update_export_data(item, obj)
