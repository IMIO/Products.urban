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
    # migrate api change of method 'getCurrentFolderManager'
    migrateTALExpressionForReferenceGeneration(context)
    # migrate global templates to distinguish those used by Urban licence and EnvironmentLicence
    migrateUrbanGlobalTemplates(context)

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

    logger.info("migration step done!")


def migrateUrbanGlobalTemplates(context):
    """
     Move 'header.odt', 'footer.odt', 'reference.odt' and 'signatures.odt' from globaltemplates
     folder to globaltemplates.urbantemplates folder and duplicate them into
     globaltemplates.environmenttemplatesfolder templates.
    """
    logger = logging.getLogger('urban: migrate global templates and duplicate them for environment licences->')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    globaltemplates = portal_urban.globaltemplates
    urbantemplates_folder = getattr(globaltemplates, 'urbantemplates', None)
    environmenttemplates_folder = getattr(globaltemplates, 'environmenttemplates', None)

    if not urbantemplates_folder and not environmenttemplates_folder:
        globaltemplates.setConstrainTypesMode(1)
        globaltemplates.setLocallyAllowedTypes(['UrbanDoc', 'Folder'])
        globaltemplates.setImmediatelyAddableTypes(['UrbanDoc', 'Folder'])

        portal_setup = api.portal.get_tool('portal_setup')
        portal_setup.runImportStepFromProfile('profile-Products.urban:default', 'urban-postInstall')

        urbantemplates_folder = getattr(globaltemplates, 'urbantemplates')
        environmenttemplates_folder = getattr(globaltemplates, 'environmenttemplates')

        template_ids = ['header.odt', 'footer.odt', 'reference.odt', 'signatures.odt']

        for each in template_ids:
            logger.info("migrate template '{}' ...".format(each))
            template = getattr(globaltemplates, each)
            api.content.move(template, urbantemplates_folder)

        portal_setup.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')

    logger.info("migration step done!")
