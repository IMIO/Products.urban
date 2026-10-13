# -*- coding: utf-8 -*-

from Products.urban import UrbanMessage as _
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.widgets.select import widget
from eea.facetednavigation.widgets.select.interfaces import ISelectSchema as ISchema
from eea.facetednavigation.widgets.interfaces import FacetedSchemata
from z3c.form import field
from zope import schema
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import logging


logger = logging.getLogger("eea.facetednavigation.widgets.portlet")


class ISelectSchema(ISchema):
    remember = schema.Bool(
        title=_(u"Remember choice"),
        description=_(
            u"Store the selected value in the browser (localStorage) "
            u"and restore it when coming back to the page"
        ),
        required=False,
        default=False,
    )


class RememberSchemata(FacetedSchemata):
    """Schemata remember"""

    label = u"remember"
    fields = field.Fields(ISelectSchema).select(u"remember")


class Widget(widget.Widget):
    """Widget"""

    widget_type = "select_to_list"
    widget_label = _("Select to list")
    groups = widget.Widget.groups + (RememberSchemata,)

    @property
    def remember(self):
        value = self.data.get("remember", False)
        return value in (True, "True", "true", "on", "1", 1)

    def _items_for(self, criterion, form):
        """Return the set of items selected for a criterion, or None"""
        if criterion.get("hidden"):
            value = criterion.get("default")
        else:
            value = form.get(criterion.getId(), "")
        if not value:
            return None

        vocabulary = criterion.get("vocabulary", "")
        if not vocabulary:
            return None
        voc_factory = getUtility(IVocabularyFactory, name=vocabulary)
        term = voc_factory(self.context).by_value.get(value, None)
        if term is None:
            return None
        return set(term.token.split(","))

    def query(self, form):
        """Get value from form and return a catalog dict query

        All select_to_list criteria on the same index are intersected,
        otherwise the last one would overwrite the others in the query.
        """
        query = {}
        index = self.data.get("index", "")
        if not index:
            return query

        items = None
        for criterion in ICriteria(self.context).values():
            if criterion.get("widget") != self.widget_type:
                continue
            if criterion.get("index") != index:
                continue
            crit_items = self._items_for(criterion, form)
            if crit_items is None:
                continue
            items = crit_items if items is None else items & crit_items

        if items is None:
            return query
        if not items:
            # Empty intersection: an empty list would be ignored by the
            # catalog and return everything
            items = {"__no_match__"}

        query[index.encode("utf-8", "replace")] = {
            "query": sorted(items),
            "operator": "or",
        }
        return query

    def css_class(self):
        css = "faceted-select-widget {0}".format(super(Widget, self).css_class)
        if self.remember:
            css += " faceted-remember"
        return css