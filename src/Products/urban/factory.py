# -*- coding: utf-8 -*-

from five import grok

from plone import api

from zope.component import IFactory


class UrbanEventFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('UrbanEvent')

    def __call__(self, licence, event_config, id='', **kwargs):
        portal_urban = api.portal.get_tool('portal_urban')
        catalog = api.portal.get_tool('portal_catalog')

        # is event_config and UID?
        if type(event_config) is str:
            brains = catalog(UID=event_config)
            event_config = brains and brains[0].getObject() or event_config

        # is event_config and id?
        if type(event_config) is str:
            eventconfigs = licence.getLicenceConfig().eventconfigs
            event_config = getattr(eventconfigs, event_config, event_config)

        event_config.checkCreationInLicence(licence)
        portal_type = event_config.getEventPortalType() or 'UrbanEvent'

        urban_event_id = licence.invokeFactory(
            portal_type,
            id=id or portal_urban.generateUniqueId(portal_type),
            **kwargs
        )
        urban_event = getattr(licence, urban_event_id)
        # 'urbaneventconfigs' is sometimes not initialized correctly with
        # invokeFactory, so explicitly set it after
        urban_event.setUrbaneventtypes(event_config.UID())
        urban_event.setTitle(event_config.Title())
        urban_event._at_rename_after_creation = False
        urban_event.processForm()

        return urban_event


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
