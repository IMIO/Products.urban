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
        return ['public_settings', 'vocabulary_folders', 'events', 'schedule']

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        eventconfigs_folder = self.getEventConfigs()
        folders = [fld for fld in context.objectValues('ATFolder') if fld not in eventconfigs_folder]
        return folders

    def getMiscConfigFolders(self):
        return []

    def getEventConfigs(self):
        context = aq_inner(self.context)
        eventconfigs_folder = getattr(context, 'eventconfigs')
        return [eventconfigs_folder]

    def getScheduleConfigs(self):
        context = aq_inner(self.context)
        schedule_folder = getattr(context, 'schedule')
        return [schedule_folder]
