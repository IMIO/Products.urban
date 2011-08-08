# -*- coding: utf-8 -*-
from five import grok
from zope.component import IFactory
from Products.CMFCore.utils import getToolByName
from AccessControl import Unauthorized
from Products.CMFPlone import PloneMessageFactory as _


class UrbanEventFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEvent')

    def __call__(self, eventType, licence, **kwargs):
        portal = getToolByName(licence, 'portal_url').getPortalObject()
        urbanTool = getToolByName(portal, 'portal_urban')
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        if not eventtypetype.isApplicable(licence):
            raise Unauthorized, _("You can not create this UrbanEvent !")
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

class UrbanEventInquiryFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEventInquiry')

    def __call__(self, eventType, licence, **kwargs):
        portal = getToolByName(licence, 'portal_url').getPortalObject()
        urbanTool = getToolByName(portal, 'portal_urban')
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        if not eventtypetype.isApplicable(licence):
            raise Unauthorized, _("You can not create this UrbanEventInquiry !")
        urbanEventId = urbanTool.generateUniqueId('UrbanEventInquiry')
        licence.invokeFactory("UrbanEventInquiry",
                              id=urbanEventId,
                              title=eventtypetype.Title(),
                              urbaneventtypes=(eventtypetype,),
                              **kwargs)
        urbanEvent = getattr(licence, urbanEventId)
        urbanEvent._at_rename_after_creation = False
        urbanEvent.processForm()

        return urbanEvent
