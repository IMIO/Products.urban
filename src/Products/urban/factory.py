# -*- coding: utf-8 -*-

from five import grok

from plone import api

from zope.lifecycleevent import ObjectCreatedEvent
from zope.component import IFactory
from zope import event


class UrbanEventFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name("UrbanEvent")

    def __call__(self, licence, event_type, id="", **kwargs):
        portal_urban = api.portal.get_tool("portal_urban")
        catalog = api.portal.get_tool("portal_catalog")

        # is event_type and UID?
        if type(event_type) is str:
            brains = catalog(UID=event_type)
            event_type = brains and brains[0].getObject() or event_type

        # is event_type and id?
        if type(event_type) is str:
            eventtypes = licence.getUrbanConfig().urbaneventtypes
            event_type = getattr(eventtypes, event_type, event_type)

        event_type.checkCreationInLicence(licence)
        portal_type = event_type.getEventPortalType() or "UrbanEvent"

        urban_event_id = licence.invokeFactory(
            portal_type, id=id or portal_urban.generateUniqueId(portal_type), **kwargs
        )
        urban_event = getattr(licence, urban_event_id)
        # 'urbaneventtypes' is sometimes not initialized correctly with
        # invokeFactory, so explicitly set it after
        urban_event.setUrbaneventtypes(event_type.UID())
        urban_event.setTitle(event_type.Title())
        urban_event._at_rename_after_creation = False
        urban_event.processForm()
        event.notify(ObjectCreatedEvent(urban_event))

        return urban_event


class UrbanEventInquiryFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name("UrbanEventInquiry")

    def __call__(self, eventType, licence, **kwargs):
        urbanTool = api.portal.get_tool("portal_urban")
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        eventtypetype.checkCreationInLicence(licence)
        urbanEventId = urbanTool.generateUniqueId("UrbanEventInquiry")
        licence.invokeFactory("UrbanEventInquiry", id=urbanEventId, **kwargs)
        urbanEvent = getattr(licence, urbanEventId)
        urbanEvent.setUrbaneventtypes(eventtypetype.UID())
        urbanEvent.setTitle(eventtypetype.Title())
        urbanEvent._at_rename_after_creation = False
        urbanEvent.processForm()

        return urbanEvent


class BuildLicenceFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name("BuildLicence")

    def __call__(self, context, licenceId=None, **kwargs):
        portal = api.portal.getSite()
        urban = portal.urban
        buildLicences = urban.buildlicences
        if licenceId is None:
            urbanTool = api.portal.get_tool("portal_urban")
            licenceId = urbanTool.generateUniqueId("BuildLicence")
        licenceId = buildLicences.invokeFactory("BuildLicence", id=licenceId, **kwargs)
        licence = getattr(buildLicences, licenceId)
        licence._at_rename_after_creation = False
        licence.processForm()
        return licence
