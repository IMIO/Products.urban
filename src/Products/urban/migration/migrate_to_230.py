# encoding: utf-8

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def copy_sol_values_from_pca(context):
    """
    Duplicate pca values vocabulary to sol vocabulary
    """
    logger = logging.getLogger('urban: duplicate pcas vocabulary to sol')
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool('portal_urban')

    pca_folder = urban_tool.pcas
    sol_folder = urban_tool.sols
    if not sol_folder.objectIds():
        for pca_term in pca_folder.objectValues():
            api.content.move(pca_term, sol_folder)

    pcazone_folder = urban_tool.pcazones
    solzone_folder = urban_tool.solzones
    if not sol_folder.objectIds():
        for pca_zone in pcazone_folder.objectValues():
            api.content.move(pca_zone, solzone_folder)

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.3')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-imio.schedule:default', 'urban-postInstall')
    copy_sol_values_from_pca(context)
    logger.info("migration done!")
