
# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner


class LicenceConfigView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(LicenceConfigView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = '%s_macro' % tab
        macro = context.unrestrictedTraverse('@@licenceconfigmacros/%s' % macro_name)
        return macro

    def getTabs(self):
        return ['public_settings', 'vocabulary_folders', 'events']

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        eventtypes_folder = self.getEventTypes()
        folders = [fld for fld in context.objectValues('ATFolder') if fld not in eventtypes_folder]
        return folders

    def getMiscConfigFolders(self):
        return []

    def getEventTypes(self):
        context = aq_inner(self.context)
        eventtypes_folder = getattr(context, 'urbaneventtypes')
        return [eventtypes_folder]


class LicenceConfigMacros(BrowserView):
    """
      This manage the macros of LicenceConfig
    """
