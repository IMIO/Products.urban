# -*- coding: utf-8 -*-

from collective.archetypes.select2.select2widget import Select2Widget as CollectiveSelect2Widget
from collective.archetypes.select2.select2widget import MultiSelect2Widget as CollectiveMultiSelect2Widget



class Select2Widget(CollectiveSelect2Widget):
    def view(self, context, field, request):
        values = super(Select2Widget, self).view(context, field, request)
        return ", ".join(
            [field.vocabulary.getAllVocTerms(context)[value].title for value in values]
        )


class MultiSelect2Widget(CollectiveMultiSelect2Widget):
    def view(self, context, field, request):
        values = super(MultiSelect2Widget, self).view(context, field, request)
        return ", ".join(
            [field.vocabulary.getAllVocTerms(context)[value].title for value in values]
        )
