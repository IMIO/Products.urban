# -*- coding: utf-8 -*-

from collective.exportimport.import_content import ImportContent
from plone import api
from plone.restapi.interfaces import IDeserializeFromJson
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter, getUtility
from zope.schema.interfaces import IVocabularyFactory

import logging

logger = logging.getLogger("Import Urban Config")

DEFERRED_KEY = "exportimport.deferred"
DEFERRED_FIELD_MAPPING = {
    "EventConfig": ["keyDates"],
}
SIMPLE_SETTER_FIELDS = {"EventConfig": ["eventPortalType"]}


class ConfigImportContent(ImportContent):

    title = "Import Urban Config data"
    DROP_FIELDS = {
        "OpinionEventConfig": ["internal_service"],
        "UrbanTemplate": [
            "mailing_loop_template",
        ],
    }
    default_value_none = {"EventConfig": {"activatedFields": []}}

    def global_dict_hook(self, item):
        item = self.handle_default_value_none(item)
        item = self.handle_template_urbantemplate(item)

        item[DEFERRED_KEY] = {}
        for fieldname in DEFERRED_FIELD_MAPPING.get(item["@type"], []):
            if item.get(fieldname):
                item[DEFERRED_KEY][fieldname] = item.pop(fieldname)

        simple = {}
        for fieldname in SIMPLE_SETTER_FIELDS.get("ALL", []):
            if fieldname in item:
                value = item.pop(fieldname)
                if value:
                    simple[fieldname] = value
        for fieldname in SIMPLE_SETTER_FIELDS.get(item["@type"], []):
            if fieldname in item:
                value = item.pop(fieldname)
                if value:
                    simple[fieldname] = value
        if simple:
            item["exportimport.simplesetter"] = simple

        return item

    def finish(self):
        self.results = []
        for brain in api.content.find(portal_type=DEFERRED_FIELD_MAPPING.keys()):
            obj = brain.getObject()
            self.import_deferred(obj)
        api.portal.show_message(
            "Imported deferred data for {} items!".format(len(self.results)),
            self.request,
        )

    def import_deferred(self, obj):
        annotations = IAnnotations(obj, {})
        deferred = annotations.get(DEFERRED_KEY, None)
        if not deferred:
            return
        deserializer = getMultiAdapter((obj, self.request), IDeserializeFromJson)
        try:
            obj = deserializer(validate_all=False, data=deferred)
        except Exception as e:
            logger.info(
                "Error while importing deferred data for %s",
                obj.absolute_url(),
                exc_info=True,
            )
            logger.info("Data: %s", deferred)
        else:
            self.results.append(obj.absolute_url())
        # cleanup
        del annotations[DEFERRED_KEY]

    def handle_default_value_none(self, item):
        for key in self.default_value_none.get(item["@type"], {}):
            if item[key] is None:
                item[key] = self.default_value_none[item["@type"]][key]
        return item

    def handle_template_urbantemplate(self, item):
        if item["@type"] != "UrbanTemplate":
            return item
        context = api.portal.get_tool("portal_urban")
        factory = getUtility(
            IVocabularyFactory, "collective.documentgenerator.MergeTemplates"
        )
        vocabulary = factory(context)

        new_merge_templates = []
        for merge_template in item.get("merge_templates", []):
            merge_template["template"] = "--NOVALUE--"
            new_merge_templates.append(merge_template)
        item["merge_templates"] = new_merge_templates
        return item

    def global_obj_hook_before_deserializing(self, obj, item):
        """Hook to modify the created obj before deserializing the data."""
        # import simplesetter data before the rest
        for fieldname, value in item.get("exportimport.simplesetter", {}).items():
            setattr(obj, fieldname, value)
        return obj, item

    def global_obj_hook(self, obj, item):
        # Store deferred data in an annotation.
        deferred = item.get(DEFERRED_KEY, {})
        if deferred:
            annotations = IAnnotations(obj)
            annotations[DEFERRED_KEY] = {}
            for key, value in deferred.items():
                annotations[DEFERRED_KEY][key] = value

    def _handle_drop_in_dict(self, key, dict_value):
        dict_value.pop(key[0], None)
        return dict_value

    def _handle_drop_path(self, path, item):
        key = path[0]
        if type(item[key]) is list:
            new_list = []
            for value in item[key]:
                new_list.append(self._handle_drop_in_dict(path[1:], value))
            item[key] = new_list
        return item

    def handle_dropped(self, item):
        for key in self.DROP_FIELDS.get(item["@type"], []):
            split_key = key.split("/")
            if len(split_key) == 1:
                item.pop(key, None)
            if len(split_key) > 1:
                item = self._handle_drop_path(split_key, item)
        return item
