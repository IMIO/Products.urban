# encoding: utf-8

from collective.noindexing import patches

from imio.urban.core.contents.eventconfig import IEventConfig

from plone import api

from Products.urban.migration.to_DX.migration_utils import migrate_date
from Products.urban.migration.to_DX.migration_utils import migrate_to_richtext
from Products.urban.migration.to_DX.migration_utils import migrate_to_tuple
from Products.urban.migration.to_DX.migration_utils import migrateCustomAT
from Products.urban.migration.to_DX.migration_utils import uid_catalog_reindex_objects
from Products.urban.migration.utils import disable_schedule


def migrate_PortionOut_to_DX(context):
    fields_mapping = (
        {
            "AT_field_name": "division",
            "DX_field_name": "division",
        },
        {
            "AT_field_name": "section",
            "DX_field_name": "section",
        },
        {
            "AT_field_name": "radical",
            "DX_field_name": "radical",
        },
        {
            "AT_field_name": "bis",
            "DX_field_name": "bis",
        },
        {
            "AT_field_name": "exposant",
            "DX_field_name": "exposant",
        },
        {
            "AT_field_name": "puissance",
            "DX_field_name": "puissance",
        },
        {
            "AT_field_name": "partie",
            "DX_field_name": "partie",
        },
        {
            "AT_field_name": "isOfficialParcel",
            "DX_field_name": "isOfficialParcel",
        },
        {
            "AT_field_name": "outdated",
            "DX_field_name": "outdated",
        },
    )
    # disable linkintegrity, catalog and schedule
    patches.apply()
    disable_schedule()
    portal = api.portal.get()
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    result = migrateCustomAT(
        fields_mapping,
        src_type="PortionOut",
        dst_type="Parcel",
        transaction_size=100000,
    )
    # restore catalog and linkintegrity
    patches.unapply()
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    return result


def migrate_ParcellingTerm_to_DX(context):

    fields_mapping = (
        {
            "AT_field_name": "label",
            "DX_field_name": "label",
        },
        {
            "AT_field_name": "subdividerName",
            "DX_field_name": "subdividerName",
        },
        {
            "AT_field_name": "authorizationDate",
            "DX_field_name": "authorizationDate",
            "field_migrator": migrate_date,
        },
        {
            "AT_field_name": "approvalDate",
            "DX_field_name": "approvalDate",
            "field_migrator": migrate_date,
        },
        {
            "AT_field_name": "communalReference",
            "DX_field_name": "communalReference",
        },
        {
            "AT_field_name": "DGO4Reference",
            "DX_field_name": "DGO4Reference",
        },
        {
            "AT_field_name": "numberOfParcels",
            "DX_field_name": "numberOfParcels",
        },
        {
            "AT_field_name": "changesDescription",
            "DX_field_name": "changesDescription",
        },
    )
    portal = api.portal.get()
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    result = migrateCustomAT(
        fields_mapping,
        src_type="ParcellingTerm",
        dst_type="Parcelling",
        transaction_size=100000,
    )
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    # should at least recatalog them in the archetypes UID catalog
    portal = api.portal.get()
    parcellings = portal.urban.parcellings.objectValues()
    uid_catalog_reindex_objects(parcellings)
    return result


def migrate_UrbanEventType_to_DX(context):
    fields_mapping = [
        {
            "AT_field_name": "title",
            "DX_field_name": "title",
        },
        {
            "AT_field_name": "description",
            "DX_field_name": "description",
            "field_migrator": migrate_to_richtext,
        },
        {
            "AT_field_name": "TALCondition",
            "DX_field_name": "TALCondition",
        },
        {
            "AT_field_name": "eventDateLabel",
            "DX_field_name": "eventDateLabel",
        },
        {
            "AT_field_name": "activatedFields",
            "DX_field_name": "activatedFields",
            "field_migrator": migrate_to_tuple,
        },
        {
            "AT_field_name": "textDefaultValues",
            "DX_field_name": "textDefaultValues",
        },
        {
            "AT_field_name": "showTitle",
            "DX_field_name": "showTitle",
        },
        {
            "AT_field_name": "eventTypeType",
            "DX_field_name": "eventType",
            "field_migrator": migrate_to_tuple,
        },
        {
            "AT_field_name": "eventPortalType",
            "DX_field_name": "eventPortalType",
        },
        {
            "AT_field_name": "isKeyEvent",
            "DX_field_name": "isKeyEvent",
        },
        {
            "AT_field_name": "keyDates",
            "DX_field_name": "keyDates",
            "field_migrator": migrate_to_tuple,
        },
    ]
    portal = api.portal.get()
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    result = migrateCustomAT(
        fields_mapping,
        src_type="UrbanEventType",
        dst_type="EventConfig",
        transaction_size=100000,
    )

    fields_mapping.append(
        {
            "AT_field_name": "linkedReport",
            "DX_field_name": "linkedreport",
        },
    )

    result = migrateCustomAT(
        fields_mapping,
        src_type="FollowUpEventType",
        dst_type="FollowUpEventConfig",
        transaction_size=100000,
    )

    fields_mapping.pop()
    fields_mapping.extend(
        [
            {
                "AT_field_name": "extraValue",
                "DX_field_name": "abbreviation",
            },
            {
                "AT_field_name": "recipientSName",
                "DX_field_name": "recipientName",
            },
            {
                "AT_field_name": "function_department",
                "DX_field_name": "function_department",
            },
            {
                "AT_field_name": "organization",
                "DX_field_name": "organization",
            },
            {
                "AT_field_name": "dispatchInformation",
                "DX_field_name": "dispatchInformation",
            },
            {
                "AT_field_name": "typeAndStreetName_number_box",
                "DX_field_name": "typeAndStreetName_number_box",
            },
            {
                "AT_field_name": "postcode_locality",
                "DX_field_name": "postcode_locality",
            },
            {
                "AT_field_name": "country",
                "DX_field_name": "country",
            },
            {
                "AT_field_name": "is_internal_service",
                "DX_field_name": "is_internal_service",
            },
            {
                "AT_field_name": "internal_service",
                "DX_field_name": "internal_service",
            },
            {
                "AT_field_name": "concernedOutsideDirections",
                "DX_field_name": "externalDirections",
                "field_migrator": migrate_to_tuple,
            },
        ]
    )
    result = migrateCustomAT(
        fields_mapping,
        src_type="OpinionRequestEventType",
        dst_type="OpinionEventConfig",
        transaction_size=100000,
    )

    # restore linkintegrity
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    # should at least recatalog them in the archetypes UID catalog
    catalog = api.portal.get_tool("portal_catalog")
    event_configs = [
        b.getObject() for b in catalog(object_provides=IEventConfig.__identifier__)
    ]
    uid_catalog_reindex_objects(event_configs)
    # should at least reindex the Title
    for event_config in event_configs:
        event_config.reindexObject(idxs=["Title", "sortable_title"])
    # update voc cache for opinion request vocabulary.
    portal_urban = api.portal.get_tool("portal_urban")
    cache_view = portal_urban.unrestrictedTraverse("urban_vocabulary_cache")
    cache_view.update_all_cache()
    # as its he last DX migration step -> recatalog evrything
    catalog = api.portal.get_tool("portal_catalog")
    catalog.clearFindAndRebuild()
    return result
