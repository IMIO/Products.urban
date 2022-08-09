# encoding: utf-8

from imio.dashboard.utils import _updateDefaultCollectionFor
from plone import api
from Products.urban.config import URBAN_TYPES
import logging

logger = logging.getLogger('urban: migrations')


def fix_licences_breadcrumb(context):
    logger = logging.getLogger('urban: fix licence breadcrumb')
    logger.info("starting upgrade steps")

    portal = api.portal.get()
    urban_folder = portal.urban
    for urban_type in URBAN_TYPES:
        folder = getattr(urban_folder, urban_type.lower() + 's')
        collection_id = 'collection_%s' % urban_type.lower()
        collection = getattr(folder, collection_id)
        _updateDefaultCollectionFor(folder, collection.UID())
    logger.info("upgrade done!")


def fix_external_edition_settings(context):
    logger = logging.getLogger('urban: fix external edition settings')
    logger.info("starting upgrade steps")

    values = api.portal.get_registry_record('externaleditor.externaleditor_enabled_types')
    if 'UrbanDoc' not in values:
        values.append('UrbanDoc')
    if 'UrbanTemplate' not in values:
        values.append('UrbanTemplate')
    if 'ConfigurablePODTemplate' not in values:
        values.append('ConfigurablePODTemplate')
    if 'SubTemplate' not in values:
        values.append('SubTemplate')
    if 'StyleTemplate' not in values:
        values.append('StyleTemplate')
    if 'DashboardPODTemplate' not in values:
        values.append('DashboardPODTemplate')
    if 'MailingLoopTemplate' not in values:
        values.append('MailingLoopTemplate')
    api.portal.set_registry_record('externaleditor.externaleditor_enabled_types', values)
    logger.info("upgrade done!")


def add_applicant_couple_type(context):
        """
        """
        logger = logging.getLogger('urban: add second default LO port')
        logger.info("starting upgrade steps")
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'factorytool')
        setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
        setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'workflow')
        setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'update-workflow-rolemap')
        setup_tool.runImportStepFromProfile('profile-liege.urban:default', 'typeinfo')
        setup_tool.runImportStepFromProfile('profile-liege.urban:default', 'workflow')
        setup_tool.runImportStepFromProfile('profile-liege.urban:default', 'update-workflow-rolemap')
        wf_tool = api.portal.get_tool('portal_workflow')
        wf_tool.updateRoleMappings()
        logger.info("upgrade step done!")
