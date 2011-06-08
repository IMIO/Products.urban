# -*- coding: utf-8 -*-
from five import grok
from zope.component import IFactory
from Products.CMFCore.utils import getToolByName


class UrbanEventFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEvent')

    def __call__(self, eventType, licence, **kwargs):
        portal = getToolByName(licence, 'portal_url').getPortalObject()
        urbanTool = getToolByName(portal, 'portal_urban')
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        urbanEventId = urbanTool.generateUniqueId('UrbanEvent')
        licence.invokeFactory("UrbanEvent",
                              id=urbanEventId,
                              title=eventtypetype.Title(),
                              urbaneventtypes=(eventtypetype,),
                              **kwargs)
        urbanEvent = getattr(licence, urbanEventId)
        urbanEvent._at_rename_after_creation = False
        urbanEvent.processForm()

        return urbanEvent
