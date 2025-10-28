# encoding: utf-8
from Products.CMFCore.utils import getToolByName
from Products.urban import URBAN_TYPES
from Products.urban import UrbanMessage as _
from Products.urban.utils import moveElementAfter
from plone import api
from plone.app.textfield import RichTextValue
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.event import notify

import logging


logger = logging.getLogger("urban: migrations")


def initialize_notice_settings(context):
    from Products.urban.browser.notice_settings import INoticeSettings

    logger = logging.getLogger("urban: Initialize Notice Settings")
    registry = getUtility(IRegistry)
    base = "Products.urban.browser.notice_settings.INoticeSettings"
    if "{0}.url".format(base) not in registry.records:
        registry_field = field.TextLine(title=INoticeSettings["url"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.url".format(base)] = registry_record
    if "{0}.municipality_id".format(base) not in registry.records:
        registry_field = field.TextLine(title=INoticeSettings["municipality_id"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.municipality_id".format(base)] = registry_record
    if "{0}.sent_on_behalf_of_municipality_id".format(base) not in registry.records:
        registry_field = field.TextLine(
            title=INoticeSettings["sent_on_behalf_of_municipality_id"].title
        )
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records[
            "{0}.sent_on_behalf_of_municipality_id".format(base)
        ] = registry_record
    if "{0}.last_import_date".format(base) not in registry.records:
        registry_field = field.Datetime(title=INoticeSettings["last_import_date"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.last_import_date".format(base)] = registry_record
    logger.info("Upgrade done!")


def add_event_config_types_notice(context):
    from Products.urban.profiles.extra.data import EventConfigs

    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "workflow"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "typeinfo"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "factorytool"
    )
    portal_setup.runImportStepFromProfile("profile-Products.urban:default", "actions")

    # migrate event configs
    tool = getToolByName(context, "portal_urban")
    for urban_config_id in EventConfigs:
        try:
            uet_folder = getattr(
                tool.getLicenceConfig(None, urbanConfigId=urban_config_id),
                "eventconfigs",
            )
        except AttributeError:
            continue  # TODO: log ?
        last_urbaneventype_id = None

        for uet in EventConfigs[urban_config_id]:
            portal_type = uet.get("portal_type", "EventConfig")
            if portal_type == "OpinionEventConfig":
                continue
            id = uet["id"]
            folder_event = getattr(uet_folder, id, None)

            if not folder_event:
                # create new eventConfig
                new_uet_id = uet_folder.invokeFactory(portal_type, **uet)
                new_uet = getattr(uet_folder, new_uet_id)
                if new_uet.description == "":
                    new_uet.description = RichTextValue("")
                if last_urbaneventype_id:
                    moveElementAfter(new_uet, uet_folder, "id", last_urbaneventype_id)
                else:
                    uet_folder.moveObjectToPosition(new_uet.getId(), 0)
                # updateTemplates(context, new_uet, uet['podTemplates'], new_install=False)  # TODO: AttributeError: _profile_path
                api.content.transition(
                    new_uet, "disable"
                )  # TODO: why ? line still useful ?

            else:  # patch existing eventConfig

                # set eventPortalType
                required_event_portal_type = uet.get("eventPortalType", "UrbanEvent")
                if folder_event.getEventPortalType() != required_event_portal_type:
                    setattr(folder_event, "eventPortalType", required_event_portal_type)

                # activate new fields
                old_fields = folder_event.getActivatedFields()
                missing_fields = set(uet.get("activatedFields", [])) - set(old_fields)
                if missing_fields:
                    new_fields = list(old_fields) + list(missing_fields)
                    setattr(folder_event, "activatedFields", new_fields)

                # add new eventType elements
                old_interfaces = folder_event.getEventType()
                missing_interfaces = set(uet.get("eventType", [])) - set(old_interfaces)
                if missing_interfaces:
                    new_interfaces = list(old_fields) + list(missing_interfaces)
                    setattr(folder_event, "eventType", new_interfaces)

            last_urbaneventype_id = id


def add_folder_manager_notice(context):
    from Products.urban.setuphandlers import _activate_dashboard_navigation
    from collective.eeafaceted.collectionwidget.utils import _updateDefaultCollectionFor
    from eea.facetednavigation.criteria.interfaces import ICriteria
    from eea.facetednavigation.events import FacetedGlobalSettingsChangedEvent

    logger = logging.getLogger("urban: Add folder manager for notice import")

    # create folder manager
    urban_tool = api.portal.get_tool("portal_urban")
    foldermanagers = getattr(urban_tool, "foldermanagers")
    if "notice" not in foldermanagers.objectIds():
        foldermanagers.invokeFactory(
            "FolderManager",
            "notice",
            name1="Import NOTICE",
            grade="agent-technique",
            ploneUserId="",
            manageableLicences=URBAN_TYPES,
        )
    notice_folder_manager = foldermanagers.notice
    notice_folder_manager.reindexObject()

    # create dashboard for incoming notice notifications
    urban_folder = api.portal.get().urban

    if "import-notice" not in urban_folder.objectIds():
        import_notice_folder = api.content.create(
            container=urban_folder,
            type="Folder",
            id="import-notice",
            title="Import NOTICE",
        )

        _activate_dashboard_navigation(
            import_notice_folder, "/dashboard/config/import_notice.xml"
        )

        # no need to create another collection, this one does the job
        all_licences_collection = getattr(urban_folder, "collection_all_licences")
        _updateDefaultCollectionFor(import_notice_folder, all_licences_collection.UID())

        # set notice folder manager's UID as default in faceted filter widget
        criteria = ICriteria(import_notice_folder).criteria
        for criterion in criteria:
            if criterion.index == "folder_manager":
                ICriteria(import_notice_folder).edit(
                    criterion.__name__,
                    default=notice_folder_manager.UID(),
                )
        notify(FacetedGlobalSettingsChangedEvent(import_notice_folder))

    logger.info("Upgrade done!")
