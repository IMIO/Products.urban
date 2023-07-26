# -*- coding: utf-8 -*-

from collective.archetypes.select2.select2widget import Select2Widget as CollectiveSelect2Widget
from collective.archetypes.select2.select2widget import MultiSelect2Widget as CollectiveMultiSelect2Widget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import logging
import six

logger = logging.getLogger("urban debug")


def resolve_vocabulary(context, field, values):
    if type(field.vocabulary) == UrbanVocabulary:
        result = [
            field.vocabulary.getAllVocTerms(context)[value].title
            for value in values
            if value
        ]
    elif type(field.vocabulary) == str:
        display_list = getattr(context, field.vocabulary)()
        result = [display_list.getValue(value) for value in values if value]
    elif type(field.vocabulary) == tuple and getattr(
        field, "vocabulary_factory", False
    ):
        vocabulary_factory = field.vocabulary_factory
        factory = getUtility(IVocabularyFactory, vocabulary_factory)
        vocabulary = factory(context)
        result = [vocabulary.by_token[value].title for value in values if value]
    if len(result) != len(filter(None, result)):
        logger.info(
            "{0}: Unknown value for field '{1}' in '{2}'".format(
                context.absolute_url(), field.__name__, values
            )
        )
    return ", ".join(filter(None, result))


class Select2Widget(CollectiveSelect2Widget):
    def view(self, context, field, request):
        values = super(Select2Widget, self).view(context, field, request)
        return resolve_vocabulary(context, field, values)


class MultiSelect2Widget(CollectiveMultiSelect2Widget):
    def view(self, context, field, request):
        values = super(MultiSelect2Widget, self).view(context, field, request)
        if values != getattr(context, field.__name__):
            # inexpected stored value
            logger.info(
                "{0}: Inexpected value for field '{1}'".format(
                    context.absolute_url(),
                    field.__name__,
                )
            )
            value = getattr(context, field.__name__)
            if isinstance(value, six.string_types):
                values = (value,)
        return resolve_vocabulary(context, field, values)
