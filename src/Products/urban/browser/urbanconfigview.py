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
        return ['public_settings', 'licences_config', 'vocabulary_folders', 'admin_settings']

    def getAdminFolders(self):
        context = aq_inner(self.context)
        names = ['additional_layers']
        folders = [folder for folder in context.objectValues('ATFolder') if folder.id in names]
        return folders

    def getMiscConfigFolders(self):
        context = aq_inner(self.context)
        names = ['globaltemplates', 'foldermanagers', 'streets', 'topics']
        folders = [folder for folder in context.objectValues('ATFolder') if folder.id in names]
        return folders

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        other_folders = self.getAdminFolders() + self.getMiscConfigFolders()
        folders = [folder for folder in context.objectValues('ATFolder') if folder not in other_folders]
        return folders


class UrbanConfigMacros(BrowserView):
    """
      This manage the macros of UrbanConfig
    """
