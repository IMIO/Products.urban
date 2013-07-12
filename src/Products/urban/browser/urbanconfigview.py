# -*- coding: utf-8 -*-

from plone.memoize import view
from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName


class UrbanConfigView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(UrbanConfigView, self).__init__(context, request)
        self.context = context
        self.request = request

    @view.memoize
    def getCatalog(self):
        context = aq_inner(self.context)
        return getToolByName(context, 'portal_catalog')

    @view.memoize
    def getMember(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@plone_portal_state/member')()

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = '%s_macro' % tab
        macro = context.unrestrictedTraverse('@@urbanconfigmacros/%s' % macro_name)
        return macro

    def getTabs(self):
        return ['licences_config', 'public_settings', 'admin_settings']


class UrbanConfigMacros(BrowserView):
    """
      This manage the macros of UrbanConfig
    """
