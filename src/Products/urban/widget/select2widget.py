# -*- coding: utf-8 -*-

from collective.archetypes.select2.select2widget import Select2Widget as CollectiveSelect2Widget
from collective.archetypes.select2.select2widget import MultiSelect2Widget as CollectiveMultiSelect2Widget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


def resolve_vocabulary(context, field, values):
    if type(field.vocabulary) == UrbanVocabulary:
        return ", ".join(
            [
                field.vocabulary.getAllVocTerms(context)[value].title
                for value in values
            ]
        )
    elif type(field.vocabulary) == str:
        display_list = getattr(context, field.vocabulary)()
        return ", ".join(
            [display_list.getValue(value) for value in values]
        )
    elif (
        type(field.vocabulary) == tuple
        and getattr(field, "vocabulary_factory", False)
    ):
        vocabulary_factory = field.vocabulary_factory
        factory = getUtility(IVocabularyFactory, vocabulary_factory)
        vocabulary = factory(context)
        return ", ".join(
            [vocabulary.by_token[value].title for value in values]
        )


class Select2Widget(CollectiveSelect2Widget):
    def view(self, context, field, request):
        values = super(Select2Widget, self).view(context, field, request)
        return resolve_vocabulary(context, field, values)


class MultiSelect2Widget(CollectiveMultiSelect2Widget):
    def view(self, context, field, request):
        values = super(MultiSelect2Widget, self).view(context, field, request)
        return resolve_vocabulary(context, field, values)
