# -*- coding: utf-8 -*-

from Products.urban.browser.exportimport.interfaces import IConfigExportMarker
from Products.urban.docgen.UrbanTemplate import IUrbanTemplate
from collective.exportimport.serializer import ChoiceFieldSerializer
from collective.exportimport.serializer import CollectionFieldSerializer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IVocabularyTokenized

def handle_uid_field(value):
    if not value:
        return value
    try:
        template_obj = api.content.get(UID=value)
    except ValueError:
        return value
    path = "/".join(template_obj.getPhysicalPath())
    return {"uid": value, "path": path, "id": template_obj.id}


@implementer(IFieldSerializer)
@adapter(ICollection, IDexterityContent, IConfigExportMarker)
class UrbanConfigCollectionFieldSerializer(CollectionFieldSerializer):
    def __call__(self):
        values = super(UrbanConfigCollectionFieldSerializer, self).__call__()
        value_type = self.field.value_type
        if (
            values is not None
            and IChoice.providedBy(value_type)
            and IVocabularyTokenized.providedBy(value_type.vocabulary)
        ):
            values = [value for value in values if self._check_value(value, value_type)]
        if (
            IUrbanTemplate.providedBy(self.context)
            and self.field.getName() == "merge_templates"
        ):
            values = self.handle_merge_templates(values)
        return values

    def _check_value(self, value, value_type):
        try:
            value_type.vocabulary.getTerm(value)
            return True
        except LookupError:
            return False

    def handle_merge_templates(self, values):
        output = []
        for value in values:
            template = value.get("template", None)
            if template is None:
                output.append(value)
                continue
            value["template"] = handle_uid_field(template)
            output.append(value)
        return output


@implementer(IFieldSerializer)
@adapter(IChoice, IDexterityContent, IConfigExportMarker)
class UrbanConfigChoiceFieldSerializer(ChoiceFieldSerializer):
    def __call__(self):
        value = super(UrbanConfigChoiceFieldSerializer, self).__call__()
        if self.field.getName() == "scheduled_contenttype" and isinstance(value, list):
            value = (value[0], tuple(tuple(inner_list) for inner_list in value[1]))
        if value is not None and IVocabularyTokenized.providedBy(self.field.vocabulary):
            try:
                self.field.vocabulary.getTerm(value)
            except LookupError:
                return json_compatible(None)
        if (
            IUrbanTemplate.providedBy(self.context)
            and self.field.getName() == "mailing_loop_template"
        ):
            value = handle_uid_field(value)
        return json_compatible(value)
