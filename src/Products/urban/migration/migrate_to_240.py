# encoding: utf-8

from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues

from plone import api

import logging

logger = logging.getLogger("urban: migrations")


def migrate_codt_buildlicences_schedule(context):
    """
    Disbale recurrency for task 'deposit'
    """
    logger = logging.getLogger("urban: migrate codt buildlicences schedule")
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool("portal_urban")
    schedule = portal_urban.codt_buildlicence.schedule
    schedule.reception.deposit.ending_states = ()
    schedule.incomplet2.notify_refused.ending_states = ()
    schedule.reception.deposit.recurrence_states = ()
    schedule.reception.deposit.activate_recurrency = False
    if "deposit" not in (schedule.incomplet.attente_complements.ending_states or ()):
        old_states = schedule.incomplet.attente_complements.ending_states or ()
        new_states = tuple(old_states) + ("deposit",)
        schedule.incomplet.attente_complements.ending_states = new_states
    if "complete" not in (schedule.reception.ending_states or ()):
        old_states = schedule.reception.ending_states or ()
        new_states = tuple(old_states) + ("deposit",)
        schedule.reception.ending_states = new_states
    if "incomplete" not in (schedule.reception.ending_states or ()):
        old_states = schedule.reception.ending_states or ()
        new_states = tuple(old_states) + ("incomplete",)
        schedule.reception.ending_states = new_states

    logger.info("migration step done!")


def migrate_create_voc_classification_order_scope(context):
    """ """
    logger = logging.getLogger("urban: migrate create_voc_classification_order_scope")
    logger.info("starting migration step")
    container = api.portal.get_tool("portal_urban")
    classification_order_scope_vocabularies_config = default_values["global"][
        "classification_order_scope"
    ]
    allowedtypes = classification_order_scope_vocabularies_config[0]
    classification_order_scope_vocabularies_config = createVocabularyFolder(
        container, "classification_order_scope", context, allowedtypes
    )
    createFolderDefaultValues(
        classification_order_scope_vocabularies_config,
        default_values["global"]["classification_order_scope"][1:],
        default_values["global"]["classification_order_scope"][0],
    )

    logger.info("migration step done!")


def migrate_create_voc_general_disposition(context):
    """ """
    logger = logging.getLogger("urban: migrate create_voc_general_disposition")
    logger.info("starting migration step")
    container = api.portal.get_tool("portal_urban")
    general_disposition_vocabularies_config = default_values["global"][
        "general_disposition"
    ]
    allowedtypes = general_disposition_vocabularies_config[0]
    general_disposition_vocabularies_config = createVocabularyFolder(
        container, "general_disposition", context, allowedtypes
    )
    createFolderDefaultValues(
        general_disposition_vocabularies_config,
        default_values["global"]["general_disposition"][1:],
        default_values["global"]["general_disposition"][0],
    )

    logger.info("migration step done!")


def migrate_create_voc_tax(context):
    """ """
    logger = logging.getLogger("urban: migrate create_voc_tax")
    logger.info("starting migration step")
    container = api.portal.get_tool("portal_urban")
    tax_vocabularies_config = default_values["shared_vocabularies"]["tax"]
    allowedtypes = tax_vocabularies_config[0]
    tax_vocabularies_config = createVocabularyFolder(
        container, "tax", context, allowedtypes
    )

    createFolderDefaultValues(
        tax_vocabularies_config,
        default_values["shared_vocabularies"]["tax"][1:],
        default_values["shared_vocabularies"]["tax"][0],
    )

    logger.info("migration step done!")


def migrate_enable_optional_tax_field_by_default(context):
    """ """
    logger = logging.getLogger(
        "urban: migrate migrate_enable_optional_tax_field_by_default"
    )
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool("portal_urban")
    portal_urban.manage_field_activation(fields_to_enable=["tax"])
    logger.info("migration step done!")


def migrate_update_empty_sols_pcas_title(context):
    """ """
    logger = logging.getLogger("urban: migrate migrate_update_empty_sols_pcas_title")
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool("portal_urban")

    pca_folder = urban_tool.pcas
    for pca in pca_folder.objectValues():
        if (not pca.Title()) and pca.getLabel():
            pca.setTitle(pca.getLabel())
    sol_folder = urban_tool.sols
    for sol in sol_folder.objectValues():
        if (not sol.Title()) and sol.getLabel():
            sol.setTitle(sol.getLabel())

    logger.info("migration step done!")


def migrate_update_foldermanagers_layout(context):
    """ """
    logger = logging.getLogger("urban: migrate migrate_update_foldermanagers_layout")
    logger.info("starting migration step")

    urban_tool = api.portal.get_tool("portal_urban")
    folder = getattr(urban_tool, "foldermanagers")
    folder.setLayout("sorted_title_folderview")

    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger("urban: migrate to 2.4")
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:default", "plone.app.registry"
    )
    setup_tool.runAllImportStepsFromProfile("profile-Products.urban:preinstall")
    setup_tool.runAllImportStepsFromProfile("profile-urban.vocabulary:default")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-extraPostInstall"
    )
    setup_tool.runAllImportStepsFromProfile("profile-collective.externaleditor:default")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "urban-postInstall"
    )
    migrate_create_voc_classification_order_scope(context)
    migrate_create_voc_general_disposition(context)
    migrate_update_empty_sols_pcas_title(context)
    migrate_codt_buildlicences_schedule(context)
    migrate_enable_optional_tax_field_by_default(context)
    migrate_update_foldermanagers_layout(context)
    catalog = api.portal.get_tool("portal_catalog")
    catalog.clearFindAndRebuild()
    logger.info("migration done!")
