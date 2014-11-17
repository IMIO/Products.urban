# -*- coding: utf-8 -*-

from Products.urban.appy_pod import generateUrbanDocFile
from Products.urban.config import GENERATED_DOCUMENT_FORMATS
from Products.urban.utils import generateAvailableId

from five import grok

from plone import api

from zope.component import IFactory
# from zope.interface import Interface

import os


class UrbanEventFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEvent')

    def __call__(self, licence, event_type, **kwargs):
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

        urban_event_id = licence.invokeFactory(
            portal_type,
            id=kwargs.pop('id', None) or portal_urban.generateUniqueId(portal_type),
            title=kwargs.pop('Title', None) or event_type.Title(),
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


class UrbanDocFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('GeneratedUrbanDoc')

    def __call__(self, container, odt_template, appy_context=None):
        portal_urban = api.portal.get_tool('portal_urban')

        file_type = portal_urban.getEditionOutputFormat()
        template_id = os.path.splitext(odt_template.getId())[0]
        proposed_id = generateAvailableId(container, template_id, file_type)

        doc = generateUrbanDocFile(container, odt_template, appy_context=appy_context)

        urban_doc_id = container.invokeFactory(
            "UrbanDoc",
            id=proposed_id,
            title=odt_template.Title(),
            content_type=GENERATED_DOCUMENT_FORMATS[file_type],
            file=doc
        )
        urban_doc = getattr(container, urban_doc_id)
        urban_doc.setFilename(proposed_id)
        urban_doc.setFormat(GENERATED_DOCUMENT_FORMATS[file_type])
        urban_doc._at_rename_after_creation = False
        urban_doc.processForm()

        return urban_doc
