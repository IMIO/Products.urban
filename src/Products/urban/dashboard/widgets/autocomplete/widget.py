# encoding: utf-8

from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.ZCTextIndex.ParseTree import ParseError

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.autocomplete.widget import Widget as AutocompleteWidget

from plone import api

import json


class AutocompleteSelectionWidget(AutocompleteWidget):
    """
    eea.facetednavigation selection autocomplete widget.
    """

    # Widget properties
    widget_label = _('Selection field with suggestions')
    view_js = '++resource++eea.facetednavigation.widgets.autocompleteselection.view.js'
    edit_js = '++resource++eea.facetednavigation.widgets.autocompleteselection.edit.js'
    view_css = '++resource++eea.facetednavigation.widgets.autocompleteselection.view.css'

    index = ViewPageTemplateFile('widget.pt')


class AutocompleteVocabularySuggest(BrowserView):
    """ Autocomplete view to be called by the jQuery autocomplete. """

    def __call__(self):
        term = self.request.get('term')
        terms = term.strip().split()
        urban_config = api.portal.get_tool('portal_urban')
        path = '/'.join(urban_config.streets.getPhysicalPath())

        kwargs = {
            'Title': ' AND '.join(["%s*" % x for x in terms]),
            'sort_on': 'sortable_title',
            'sort_order': 'reverse',
            'path': path,
            'object_provides': 'Products.urban.interfaces.IStreet',
            'review_state': 'enabled',
        }

        catalog = api.portal.get_tool('portal_catalog')
        try:
            results = catalog(**kwargs)
            return json.dumps(
                [{'label': x.Title, 'value': x.UID} for x in results]
            )
        except ParseError:
            pass
