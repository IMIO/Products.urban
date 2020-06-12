# encoding: utf-8

from plone.app.contenttypes.migration.migration import migrateCustomAT


def migrate_PortionOut_to_DX(context):
    fields_mapping = (
        {
            'AT_field_name': 'divisionCode',
            'DX_field_name': 'divisionCode',
        },
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
    import ipdb; ipdb.set_trace()
    return result
