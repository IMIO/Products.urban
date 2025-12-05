# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from plone import api


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
        macro_name = "%s_macro" % tab
        macro = context.unrestrictedTraverse("@@licenceconfigmacros/%s" % macro_name)
        return macro

    def getTabs(self):
        return ["public_settings", "vocabulary_folders", "events", "schedule"]

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        eventconfigs_folder = self.getEventConfigs()
        folders = [
            fld
            for fld in context.objectValues("ATFolder")
            if fld not in eventconfigs_folder
        ]
        return folders

    def getMiscConfigFolders(self):
        return []

    def getEventConfigs(self):
        context = aq_inner(self.context)
        eventconfigs_folder = getattr(context, "eventconfigs")
        return [eventconfigs_folder]

    def getScheduleConfigs(self):
        context = aq_inner(self.context)
        schedule_folder = getattr(context, "schedule")
        return [schedule_folder]

    def getTestConfigs(self):
        context = aq_inner(self.context)
        test_folder = getattr(context, "test")
        return [test_folder]

    def get_events(self):
        licence = aq_inner(self.context)
        tool = api.portal.get_tool("portal_types")
        portal_type = tool[licence.licencePortalType]
        config_id = portal_type.id.lower()
        portal_urban = api.portal.get_tool("portal_urban")
        eventtypes = portal_urban.listEventTypes(licence, urbanConfigId=config_id)
        events_objects = [event.getObject() for event in eventtypes]
        return events_objects
