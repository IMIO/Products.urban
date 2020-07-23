# encoding: utf-8

from plone import api
from plone.app.contenttypes.migration.migration import migrateCustomAT

from Products.urban.migration.to_DX.migration_utils import migrate_date


def migrate_PortionOut_to_DX(context):
    fields_mapping = (
        {
            'AT_field_name': 'division',
            'DX_field_name': 'division',
        },
        {
            'AT_field_name': 'section',
            'DX_field_name': 'section',
        },
        {
            'AT_field_name': 'radical',
            'DX_field_name': 'radical',
        },
        {
            'AT_field_name': 'bis',
            'DX_field_name': 'bis',
        },
        {
            'AT_field_name': 'exposant',
            'DX_field_name': 'exposant',
        },
        {
            'AT_field_name': 'puissance',
            'DX_field_name': 'puissance',
        },
        {
            'AT_field_name': 'partie',
            'DX_field_name': 'partie',
        },
        {
            'AT_field_name': 'isOfficialParcel',
            'DX_field_name': 'isOfficialParcel',
        },
        {
            'AT_field_name': 'outdated',
            'DX_field_name': 'outdated',
        },
    )
    result = migrateCustomAT(
        fields_mapping,
        src_type='PortionOut',
        dst_type='Parcel'
    )
    return result


def migrate_ParcellingTerm_to_DX(context):
    # delete parcels in parcellings first
    portal = api.portal.get()
    parcellings_folder = portal.urban.parcellings
    for parcelling in parcellings_folder.objectValues():
        api.content.delete(objects=parcelling.objectValues())

    fields_mapping = (
        {
            'AT_field_name': 'label',
            'DX_field_name': 'label',
        },
        {
            'AT_field_name': 'subdividerName',
            'DX_field_name': 'subdividerName',
        },
        {
            'AT_field_name': 'authorizationDate',
            'DX_field_name': 'authorizationDate',
            'field_migrator': migrate_date,
        },
        {
            'AT_field_name': 'approvalDate',
            'DX_field_name': 'approvalDate',
            'field_migrator': migrate_date,
        },
        {
            'AT_field_name': 'communalReference',
            'DX_field_name': 'communalReference',
        },
        {
            'AT_field_name': 'DGO4Reference',
            'DX_field_name': 'DGO4Reference',
        },
        {
            'AT_field_name': 'numberOfParcels',
            'DX_field_name': 'numberOfParcels',
        },
        {
            'AT_field_name': 'changesDescription',
            'DX_field_name': 'changesDescription',
        },
    )
    result = migrateCustomAT(
        fields_mapping,
        src_type='ParcellingTerm',
        dst_type='Parcelling'
    )

    # should at least recatalog them in the archetypes UID catalog
    uid_catalog = api.portal.get_tool('uid_catalog')
    portal = api.portal.get()
    parcellings = portal.urban.parcellings.objectValues()
    for parcelling in parcellings:
        uid_catalog.catalog_object(parcelling, '/'.join(parcelling.getPhysicalPath()))

    return result
