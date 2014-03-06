# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban160(context):
    """
     Launch every migration steps for the version 1.6.0
    """
    logger = logging.getLogger('urban: migrate to 1.6.0')
    logger.info("starting migration steps")
    # migrate default view of urban root folder
    migrateTALExpressionForReferenceGeneration(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


def migrateTALExpressionForReferenceGeneration(context):
    """
    """
    logger = logging.getLogger('urban: migrate TAL expression used to generate licence references->')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')

    for config in portal_urban.objectValues('LicenceConfig'):
        TAL_expr = config.getReferenceTALExpression()
        new_TAL_expr = TAL_expr.replace(
            'tool.getCurrentFolderManager(initials=True)',
            'tool.getCurrentFolderManagerInitials()',
        )
        config.setReferenceTALExpression(new_TAL_expr)
