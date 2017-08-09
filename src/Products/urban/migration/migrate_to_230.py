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


def move_noteworthytrees_vocabulary(context):
    """
    """
    logger = logging.getLogger('urban: move noteworthytrees vocabulary')
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool('portal_urban')
    noteworthytrees = urban_tool.noteworthytrees

    for licence_config in urban_tool.objectValues('LicenceConfig'):
        if hasattr(licence_config, 'noteworthytrees'):
            for voc_id in licence_config.noteworthytrees.objectIds():
                if voc_id not in noteworthytrees.objectIds():
                    api.content.move(getattr(licence_config.noteworthytrees, voc_id), noteworthytrees)
            try:
                api.content.delete(licence_config.noteworthytrees)
            except:
                continue

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.3')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:default', 'urban-postInstall')
    copy_sol_values_from_pca(context)
    move_noteworthytrees_vocabulary(context)
    logger.info("migration done!")
