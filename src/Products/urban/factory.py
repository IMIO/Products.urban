# -*- coding: utf-8 -*-

from five import grok

from imio.schedule.utils import tuple_to_interface

from plone import api

from Products.urban.interfaces import ICollegeEvent

from zope.component import IFactory


class UrbanEventFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEvent')

    def __call__(self, licence, event_type, id='', **kwargs):
        portal_urban = api.portal.get_tool('portal_urban')
        catalog = api.portal.get_tool('portal_catalog')

        #is event_type and UID?
        if type(event_type) is str:
            brains = catalog(UID=event_type)
            event_type = brains and brains[0].getObject() or event_type

        #is event_type and id?
        if type(event_type) is str:
            eventtypes = licence.getUrbanConfig().urbaneventtypes
            event_type = getattr(eventtypes, event_type, event_type)

        event_type.checkCreationInLicence(licence)
        eventtype_type = event_type.getEventTypeType()
        portal_type = portal_urban.portal_types_per_event_type_type.get(eventtype_type, "UrbanEvent")
        if eventtype_type:
            type_interface = tuple_to_interface(('.'.join(eventtype_type.split('.')[:-1]), eventtype_type.split('.')[-1]))
            if issubclass(type_interface, ICollegeEvent):
                portal_type = 'UrbanEventCollege'

        urban_event_id = licence.invokeFactory(
            portal_type,
            id=id or portal_urban.generateUniqueId(portal_type),
            title=event_type.Title(),
            urbaneventtypes=(event_type,),
            **kwargs
        )
        urban_event = getattr(licence, urban_event_id)
        urban_event._at_rename_after_creation = False
        urban_event.processForm()

        return urban_event


class UrbanEventInquiryFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEventInquiry')

    def __call__(self, eventType, licence, **kwargs):
        urbanTool = api.portal.get_tool('portal_urban')
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        eventtypetype.checkCreationInLicence(licence)
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


class BuildLicenceFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('BuildLicence')

    def __call__(self, context, licenceId=None, **kwargs):
        portal = api.portal.getSite()
        urban = portal.urban
        buildLicences = urban.buildlicences
        if licenceId is None:
            urbanTool = api.portal.get_tool('portal_urban')
            licenceId = urbanTool.generateUniqueId('BuildLicence')
        licenceId = buildLicences.invokeFactory("BuildLicence",
                                                id=licenceId,
                                                **kwargs)
        licence = getattr(buildLicences, licenceId)
        licence._at_rename_after_creation = False
        licence.processForm()
        return licence
