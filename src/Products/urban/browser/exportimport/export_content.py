# -*- coding: utf-8 -*-

from collective.exportimport.export_content import ExportContent
from plone.restapi.interfaces import ISerializeToJson
from Products.urban.config import URBAN_TYPES
from zope.component import getMultiAdapter


class UrbanExportContent(ExportContent):
    def _serializer(self, obj, with_files=False):
        serializer = getMultiAdapter((obj, self.request), ISerializeToJson)
        item = serializer()
        if with_files:
            sub_files = obj.listFolderContents(
                contentFilter={"portal_type": "File"}
            )
            for file in sub_files:
                file_serializer = getMultiAdapter((file, self.request), ISerializeToJson)
                if "documents" not in item:
                    item["documents"] = []
                item["documents"].append(self.update_data_for_migration(file_serializer(), obj))
        item["@id"] = obj.absolute_url()
        return self.update_data_for_migration(item, obj)

    def global_dict_hook(self, item, obj):
        item = super(UrbanExportContent, self).global_dict_hook(item, obj)
        if item["@type"] in URBAN_TYPES:
            item["events"] = [
                self._serializer(event, with_files=True)
                for event in obj.listFolderContents(
                    contentFilter={"portal_type": [
                        "UrbanEvent",
                        "UrbanEventAnnouncement",
                        "UrbanEventCollege",
                        "UrbanEventNotificationCollege",
                        "UrbanEventOpinionRequest",
                        "UrbanEventInquiry",
                        "UrbanEventMayor",
                        "CODT_Inquiry",
                        "Inquiry",
                        "CODT_UniqueLicenceInquiry",
                        "UrbanEventInspectionReport",
                        "UrbanEventFollowUp",
                    ]}
                )
            ]
            item["parcels"] = [
                self._serializer(event)
                for event in obj.listFolderContents(
                    contentFilter={"portal_type": "Parcel"}
                )
            ]
            item["notary_worklocation"] = [
                self._serializer(event)
                for event in obj.listFolderContents(
                    contentFilter={"portal_type": "WorkLocation"}
                )
            ]
            item["applicants"] = [
                self._serializer(event)
                for event in obj.listFolderContents(
                    contentFilter={"portal_type": [
                        "Applicant",
                        "Couple",
                        "Corporation",
                        "Proprietary",
                        "CorporationProprietary",
                        "ProprietaryCouple",
                        "Tenant",
                        "Plaintiff",
                        "CorporationPlaintiff",
                    ]}
                )
            ]
        return item

    def update_data_for_migration(self, item, obj):
        item.pop("@components", None)
        item.pop("next_item", None)
        item.pop("batching", None)
        item.pop("items", None)
        item.pop("previous_item", None)
        item.pop("immediatelyAddableTypes", None)
        item.pop("locallyAllowedTypes", None)
        return item
