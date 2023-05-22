# -*- coding: utf-8 -*-

from collective.exportimport.export_content import ExportContent


class UrbanExportContent(ExportContent):
    def update_data_for_migration(self, item, obj):
        item.pop("@components", None)
        item.pop("next_item", None)
        item.pop("batching", None)
        item.pop("items", None)
        item.pop("previous_item", None)
        item.pop("immediatelyAddableTypes", None)
        item.pop("locallyAllowedTypes", None)
        return item
