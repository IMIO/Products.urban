# -*- coding: utf-8 -*-

from zope.pagetemplate.engine import TrustedAppPT
from zope.pagetemplate.pagetemplate import PageTemplate

from plone import api


class DefaultTextRenderer(TrustedAppPT, PageTemplate):
    """
    """

    def __init__(self, urban_event):
        self.event_helper = urban_event.unrestrictedTraverse('document_generation_helper_view')
        self.real_event = urban_event
        self.event = self.event_helper.context
        self.licence_helper = urban_event.aq_parent.unrestrictedTraverse('document_generation_helper_view')
        self.real_licence = urban_event.aq_parent
        self.licence = self.licence_helper.context

    def __call__(self, text, *args, **keywords):
        self.pt_edit(text, 'text/html')
        namespace = self.pt_getContext()
        rendered = self.pt_render(namespace)
        return rendered

    def pt_getContext(self, args=(), options={}, **ignored):
        rval = {
            'template': self,
            'options': options,
            'args': args,
            'nothing': None,
            'self': self.licence,
            'helper': self.licence_helper,
            'context': self.real_licence,
            'event': self.event,
            'event_helper': self.event_helper,
            'real_event': self.real_event,
            'tool': api.portal.get_tool('portal_urban'),
        }
        rval.update(self.pt_getEngine().getBaseNames())
        return rval
