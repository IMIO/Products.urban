# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Acquisition import aq_inner


class UrbanConfigView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(UrbanConfigView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = '%s_macro' % tab
        macro = context.unrestrictedTraverse('@@urbanconfigmacros/%s' % macro_name)
        return macro

    def getTabs(self):
        return ['public_settings', 'licences_config', 'vocabulary_folders', 'schedule', 'admin_settings']

    def getAdminFolders(self):
        context = aq_inner(self.context)
        names = ['additional_layers']
        folders = [folder for folder in context.objectValues('ATFolder') if folder.id in names]
        return folders

    def getMiscConfigFolders(self):
        context = aq_inner(self.context)
        names = ['globaltemplates', 'dashboardtemplates', 'foldermanagers', 'streets']
        folders = [folder for folder in context.objectValues('ATFolder') if folder.id in names]
        return folders

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        other_folders = self.getAdminFolders() + self.getMiscConfigFolders()
        folders = [folder for folder in context.objectValues('ATFolder') if folder not in other_folders]
        return folders

    def getScheduleConfigs(self):
        context = aq_inner(self.context)
        return []
        survey_schedule = getattr(context, 'survey_schedule')
        opinions_schedule = getattr(context, 'opinions_schedule')
        return [survey_schedule, opinions_schedule]
