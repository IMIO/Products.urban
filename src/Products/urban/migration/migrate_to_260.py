# -*- coding: utf-8 -*-


from plone import api
from Products.urban.interfaces import IBaseBuildLicence

import logging

logger = logging.getLogger('urban: migrations')


def migrate_move_basebuildlicence_architects_and_geometricians_to_representative_contacts(context):
    """
    """
    logger = logging.getLogger('urban: migrate migrate_move_basebuildlicence_architects_and_geometricians_to_representative_contacts')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IBaseBuildLicence.__identifier__)
    licences = [li.getObject() for li in licence_brains]
    for licence in licences:
        architects = licence.getField('architects')
        if architects:
            for architect in architects.get(licence):
                rc_list = licence.getRepresentativeContacts()
                rc_list.append(architect)
                licence.setRepresentativeContacts(rc_list)
                licence.setArchitects([])
        geometricians = licence.getField('geometricians')
        if geometricians:
            for geometrician in geometricians.get(licence):
                rc_list = licence.getRepresentativeContacts()
                rc_list.append(geometrician)
                licence.setRepresentativeContacts(rc_list)
                licence.setGeometricians([])

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.6')
    logger.info("starting migration steps")
    migrate_move_basebuildlicence_architects_and_geometricians_to_representative_contacts(context)
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    logger.info("catalog rebuilt!")
    logger.info("refreshing reference catalog...")
    REQUEST = context.REQUEST
    ref_catalog = api.portal.get_tool('reference_catalog')
    ref_catalog.manage_catalogReindex(REQUEST, REQUEST.RESPONSE, REQUEST.URL)
    logger.info("migration done!")
