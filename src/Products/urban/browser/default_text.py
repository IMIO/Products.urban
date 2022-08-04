# -*- coding: utf-8 -*-

from zope.pagetemplate.engine import TrustedAppPT
from zope.pagetemplate.pagetemplate import PageTemplate

from plone.memoize.request import cache

from plone import api


class DefaultTextRenderer(TrustedAppPT, PageTemplate):
    """
    """

    def __init__(self, urban_event):
        self.docgen_view = urban_event.unrestrictedTraverse('urban-document-generation')
        self.licence = urban_event.aq_parent

    def __call__(self, text, *args, **keywords):
        self.pt_edit(text, 'text/html')
        namespace = self.pt_getContext()
        rendered = self.pt_render(namespace)
        return rendered

    @cache(get_key=lambda f, self: self.licence.id, get_request='self.licence.REQUEST')
    def pt_getContext(self, args=(), options={}, **ignored):
        with api.env.adopt_roles(['Manager']):
            base_context = self.docgen_view.get_base_generation_context(None, None)
        rval = {
            'template': self,
            'options': options,
            'args': args,
            'nothing': None,
            'helper': base_context['licence_view'],
            'context': base_context['licence'],
        }
        rval.update(base_context)
        rval.update(self.pt_getEngine().getBaseNames())
        return rval
