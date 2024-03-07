# -*- coding: utf-8 -*-

from eea.facetednavigation.widgets.select import widget
from eea.facetednavigation.widgets.select.interfaces import ISelectSchema as ISchema
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import logging

from Products.urban import UrbanMessage as _


logger = logging.getLogger("eea.facetednavigation.widgets.portlet")


class ISelectSchema(ISchema):
    pass


class Widget(widget.Widget):
    """Widget"""

    widget_type = "select_to_list"
    widget_label = _("Select to list")

    def query(self, form):
        """Get value from form and return a catalog dict query"""
        query = {}
        index = self.data.get("index", "")
        index = index.encode("utf-8", "replace")
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), "")

        if not value:
            return query
        voc_factory = getUtility(IVocabularyFactory, name=self.data.vocabulary)
        voc = voc_factory(self.context)

        term = voc.by_value.get(value, None)
        items = getattr(term, "token", "").split(",")
        query[index] = {"query": items, "operator": "or"}
        return query

    def css_class(self):
        return "faceted-select-widget {0}".format(super(Widget, self).css_class)
