# encoding: utf-8

from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues
from Products.urban.config import URBAN_TYPES

from plone import api

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


import logging

logger = logging.getLogger("urban: migrations")


def update_urban_dashboard_collection(context):
    """ """
    logger = logging.getLogger(
        'urban: update filtered licence types of urban "all" collection'
    )
    logger.info("starting migration step")
    site = api.portal.get()
    urban_folder = getattr(site, "urban")
    all_licences_collection = getattr(urban_folder, "collection_all_licences")
    filter_type = [type for type in URBAN_TYPES]
    query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.is",
            "v": filter_type,
        }
    ]
    all_licences_collection.setQuery(query)
    logger.info("migration step done!")


def copy_sol_values_from_pca(context):
    """
    Duplicate pca values vocabulary to sol vocabulary
    """
    logger = logging.getLogger("urban: duplicate pcas vocabulary to sol")
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool("portal_urban")

    pca_folder = urban_tool.pcas
    sol_folder = urban_tool.sols
    if not sol_folder.objectIds():
        for pca_term in pca_folder.objectValues():
            api.content.copy(pca_term, sol_folder)

    pcazone_folder = urban_tool.pcazones
    solzone_folder = urban_tool.solzones
    if not solzone_folder.objectIds():
        for pca_zone in pcazone_folder.objectValues():
            api.content.copy(pca_zone, solzone_folder)

    logger.info("migration step done!")


def move_noteworthytrees_vocabulary(context):
    """ """
    logger = logging.getLogger("urban: move noteworthytrees vocabulary")
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool("portal_urban")
    noteworthytrees = urban_tool.noteworthytrees

    for licence_config in urban_tool.objectValues("LicenceConfig"):
        if hasattr(licence_config, "noteworthytrees"):
            for voc_id in licence_config.noteworthytrees.objectIds():
                if voc_id not in noteworthytrees.objectIds():
                    api.content.move(
                        getattr(licence_config.noteworthytrees, voc_id), noteworthytrees
                    )
            try:
                api.content.delete(licence_config.noteworthytrees)
            except Exception:
                continue

    logger.info("migration step done!")


def migrate_eventtypes_values():
    logger = logging.getLogger("urban: migrate urbaneventtype event type")
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool("portal_urban")
    licence_configs = portal_urban.objectValues("LicenceConfig")
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues():
            old_event_type = event_type.eventTypeType
            if type(old_event_type) == str or type(old_event_type) == unicode:
                event_type.setEventTypeType([event_type.eventTypeType])

    logger.info("migration step done!")


def migrate_sct(context):
    """ """
    logger = logging.getLogger("urban: migrate karst constraints")
    logger.info("starting migration step")

    container = api.portal.get_tool("portal_urban")
    sct_vocabularies_config = default_values["global"]["sct"]
    allowedtypes = sct_vocabularies_config[0]
    sct_folder_config = createVocabularyFolder(container, "sct", context, allowedtypes)
    createFolderDefaultValues(
        sct_folder_config,
        default_values["global"]["sct"][1:],
        default_values["global"]["sct"][0],
    )

    logger.info("migration step done!")


def migrate_opinionrequest_event_portaltype(context):
    """ """
    logger = logging.getLogger("urban: migrate opinion request portal type")
    logger.info("starting migration step")

    catalog = api.portal.get_tool("portal_catalog")
    opinion_request_cfgs = [
        b.getObject() for b in catalog(portal_type="OpinionRequestEventType")
    ]
    for cfg in opinion_request_cfgs:
        if cfg.getEventPortalType() != "UrbanEventOpinionRequest":
            cfg.setEventPortalType("UrbanEventOpinionRequest")
            print "migrated {}".format(cfg)

    logger.info("migration step done!")


def migrate_users_in_environment_groups(context):
    """ """
    logger = logging.getLogger("urban: migrate users in environment groups")
    logger.info("starting migration step")

    for user in api.user.get_users(groupname="urban_editors"):
        api.group.add_user(user=user, groupname="environment_editors")
    for user in api.user.get_users(groupname="urban_readers"):
        api.group.add_user(user=user, groupname="environment_readers")

    logger.info("migration step done!")


def migrate_users_in_urbanmanagers_group(context):
    """ """
    logger = logging.getLogger("urban: migrate users in urban managers group")
    logger.info("starting migration step")

    for user in api.user.get_users(groupname="urban_managers"):
        api.group.add_user(user=user, groupname="urban_editors")
        api.group.add_user(user=user, groupname="environment_editors")

    logger.info("migration step done!")


def migrate_college_urban_event_types(context):
    """ """
    logger = logging.getLogger("urban: migrate colleg urban event types")
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool("portal_urban")
    licence_configs = portal_urban.objectValues("LicenceConfig")
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues():
            if event_type.getEventPortalType().endswith("College"):
                notify(ObjectModifiedEvent(event_type))

    logger.info("migration step done!")


def migrate_create_voc_mainsignatures(context):
    """ """
    logger = logging.getLogger("urban: migrate mainsignatures")
    logger.info("starting migration step")
    container = api.portal.get_tool("portal_urban")
    mainsignatures_vocabularies_config = default_values["global"]["mainsignatures"]
    allowedtypes = mainsignatures_vocabularies_config[0]
    mainsignatures_vocabularies_config = createVocabularyFolder(
        container, "mainsignatures", context, allowedtypes
    )
    createFolderDefaultValues(
        mainsignatures_vocabularies_config,
        default_values["global"]["mainsignatures"][1:],
        default_values["global"]["mainsignatures"][0],
    )

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger("urban: migrate to 2.3")
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:default", "plone.app.registry"
    )
    setup_tool.runAllImportStepsFromProfile("profile-Products.urban:preinstall")
    setup_tool.runAllImportStepsFromProfile("profile-urban.vocabulary:default")
    migrate_eventtypes_values()
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-extraPostInstall"
    )
    update_urban_dashboard_collection(context)
    copy_sol_values_from_pca(context)
    move_noteworthytrees_vocabulary(context)
    migrate_sct(context)
    migrate_opinionrequest_event_portaltype(context)
    migrate_users_in_environment_groups(context)
    migrate_users_in_urbanmanagers_group(context)
    migrate_college_urban_event_types(context)
    migrate_create_voc_mainsignatures(context)
    logger.info("migration done!")
