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

    def __call__(self, eventType, licence, **kwargs):
        urbanTool = api.portal.get_tool('portal_urban')
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        eventtypetype.checkCreationInLicence(licence)
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


class UrbanEventOpinionRequestFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEventOpinionRequest')

    def __call__(self, eventType, licence, **kwargs):
        urbanTool = api.portal.get_tool('portal_urban')
        urbanConfig = urbanTool.buildlicence
        eventTypes = urbanConfig.urbaneventtypes
        eventtypetype = getattr(eventTypes, eventType)
        eventtypetype.checkCreationInLicence(licence)
        urbanEventId = urbanTool.generateUniqueId('UrbanEvent')
        licence.invokeFactory("UrbanEventOpinionRequest",
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
