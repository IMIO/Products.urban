# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.urban.browser.exportimport.interfaces import IConfigImportMarker
from collective.z3cform.datagridfield.interfaces import IRow
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.deserializer.dxfields import ChoiceFieldDeserializer
from plone.restapi.deserializer.dxfields import CollectionFieldDeserializer
from plone.restapi.deserializer.dxfields import DatetimeFieldDeserializer
from plone.restapi.deserializer.dxfields import DefaultFieldDeserializer
from plone.restapi.interfaces import IFieldDeserializer
from pytz import timezone
from pytz import utc
from zope import schema
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema import getFields
from zope.schema import ValidationError
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import IField
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import dateutil
import logging
import six


logger = logging.getLogger("Import Urban Config")


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
        except ValidationError as error:
            logger.warn(
                "Error '{}' for value '{}', as been removed because of a ValidationError for {}".format(
                    error.doc(), error.message, "/".join(self.context.getPhysicalPath())
                )
            )
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

            value = (value[0], tuple(tuple(inner_list) for inner_list in value[1]))
        if IVocabularyTokenized.providedBy(self.field.vocabulary):
            try:
                value = self.field.vocabulary.getTerm(value).value
            except LookupError:
                return None

        self.field.validate(value)
        return value


@implementer(IFieldDeserializer)
@adapter(IRow, IDexterityContent, IConfigImportMarker)
class DatagridRowDeserializer(DefaultFieldDeserializer):
    def __call__(self, value):
        row_data = {}

        for name, field in getFields(self.field.schema).items():
            if field.readonly:
                continue

            if IDatetime.providedBy(field):
                # use the overriden deserializer to get the right
                # datamanager context
                context = self.field
            else:
                context = self.context

            deserializer = queryMultiAdapter(
                (field, context, self.request), IFieldDeserializer
            )
            if deserializer is None:
                # simply add value
                if name in value:
                    row_data[name] = value[name]
                continue
            if not isinstance(value[name], six.text_type):
                value[name] = safe_unicode(value[name])

            if isinstance(field, schema.Choice):
                self._set_vocabulary(field)

            row_data[name] = deserializer(value[name])

        return row_data

    def _set_vocabulary(self, field):
        """Ensure that vocabularies have the right values
        to avoid errors during validation"""
        vocabulary_factory = getUtility(
            IVocabularyFactory,
            name=field.vocabularyName,
        )
        field.vocabulary = vocabulary_factory(self.context)


# We override DatetimeDeserializer because of the IDatamanager context
# in a DatagridField the context is the field not the dexterity type
@implementer(IFieldDeserializer)
@adapter(IDatetime, IRow, IConfigImportMarker)
class DatagridDatetimeDeserializer(DatetimeFieldDeserializer):
    def __call__(self, value):
        # TODO: figure out how to get tsinfo from current context
        tzinfo = None

        # see plone.restapi.deserializer.dxfields
        # This happens when a 'null' is posted for a non-required field.
        if value is None:
            self.field.validate(value)
            return

        # Parse ISO 8601 string with dateutil
        try:
            dt = dateutil.parser.parse(value)
        except ValueError:
            raise ValueError("Invalid date: {}".format(value))

        # Convert to TZ aware in UTC
        if dt.tzinfo is not None:
            dt = dt.astimezone(utc)
        else:
            dt = utc.localize(dt)

        # Convert to local TZ aware or naive UTC
        if tzinfo is not None:
            tz = timezone(tzinfo.zone)
            value = tz.normalize(dt.astimezone(tz))
        else:
            value = utc.normalize(dt.astimezone(utc)).replace(tzinfo=None)

        self.field.validate(value)
        return value
