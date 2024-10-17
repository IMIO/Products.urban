# -*- coding: utf-8 -*-

from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IFieldDeserializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IField
from zope.schema.interfaces import IVocabularyTokenized
from plone.restapi.deserializer.dxfields import CollectionFieldDeserializer
from plone.restapi.deserializer.dxfields import ChoiceFieldDeserializer
from .interfaces import IConfigImportMarker
from zope.schema.interfaces import ConstraintNotSatisfied
from zope.schema.interfaces import RequiredMissing
from zope.schema import ValidationError
from plone.restapi.interfaces import IDeserializeFromJson
from Products.Archetypes.interfaces import IBaseObject
from plone.restapi.deserializer.atcontent import DeserializeFromJson
from zope.schema.interfaces import IObject
from imio.schedule.deserializer import ObjectDeserializer


@implementer(IFieldDeserializer)
@adapter(ICollection, IDexterityContent, IConfigImportMarker)
class UrbanConfigCollectionFieldDeserializer(CollectionFieldDeserializer):
    def __call__(self, values):
        if not isinstance(values, list):
            values = [values]
        if IField.providedBy(self.field.value_type):
            deserializer = getMultiAdapter(
                (self.field.value_type, self.context, self.request), IFieldDeserializer
            )

            values = [
                self._deserialize(value, deserializer)
                for value in values
                if self._check_value(value, deserializer)
            ]

        values = self.field._type(values)
        self.field.validate(values)

        return values

    def _check_value(self, value, deserializer):
        try:
            output = self._deserialize(value, deserializer)
            if output is None:
                return False
        except ConstraintNotSatisfied:
            return False
        except RequiredMissing:
            return False
        except ValidationError:
            return False
        return True

    def _deserialize(self, value, deserializer):
        if isinstance(value, dict) and "token" in value:
            value = value["token"]
        return deserializer(value)


@implementer(IFieldDeserializer)
@adapter(IChoice, IDexterityContent, IConfigImportMarker)
class UrbanConfigChoiceFieldDeserializer(ChoiceFieldDeserializer):
    def __call__(self, value):
        if isinstance(value, dict) and "token" in value:
            value = value["token"]
        if self.field.getName() == "scheduled_contenttype" and isinstance(value, list):

            value = (
                value[0],
                tuple(tuple(inner_list) for inner_list in value[1])
            )
        if IVocabularyTokenized.providedBy(self.field.vocabulary):
            try:
                value = self.field.vocabulary.getTerm(value).value
            except LookupError:
                return None

        self.field.validate(value)
        return value
