# encoding: utf-8

import logging

from plone import api
from Products.urban.setuphandlers import createFolderDefaultValues


def rename_patrimony_certificate(context):
    """ """
    logger = logging.getLogger("urban: rename Patrimony certificate")
    logger.info("starting upgrade steps")
    portal = api.portal.get()

    patrimony_folder = portal.urban.patrimonycertificates
    patrimony_folder.setTitle(u"Patrimoines")
    patrimony_folder.reindexObject(["Title"])

    patrimony_collection = portal.urban.patrimonycertificates.collection_patrimonycertificate
    patrimony_collection.setTitle(u"Patrimoines")
    patrimony_collection.reindexObject(["Title"])

    patrimony_config_folder = portal.portal_urban.patrimonycertificate
    patrimony_config_folder.setTitle(u"Paramètres des patrimoines")
    patrimony_config_folder.reindexObject(["Title"])

    logger.info("upgrade step done!")


def rename_content_rule(context):
    """ """
    logger = logging.getLogger("urban: Rename a content rules")
    logger.info("starting upgrade steps")

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "contentrules")

    logger.info("upgrade step done!")


def add_new_voc_terms_for_form_composition(context):
    logger = logging.getLogger("urban: Add new vocabularies to portal_urban/form_composition")
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get()["portal_urban"]
    form_composition_folder = portal_urban.form_composition

    # Those are the new vocabulary terms that will be added
    # Refer to profiles/extra/config_default_values.py
    # for the existing vocabulary terms
    # that will be initiated in each new instance
    form_composition_new_vocabulary_terms_to_add = [
        {
            "id": "10",
            "title": u"1/1 Formulaire général permis environnement et unique"
        },
        {
            "id": "11",
            "title": u"1/2 Élevage et détention d'animaux"
        },
        {
            "id": "12",
            "title": u"Annexe V/1 - Implantation d'un commerce",
        },
        {
            "id": "13",
            "title": u"Annexe IX - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
        },
        {
            "id": "14",
            "title": u"Annexe X - Demande de permis d'urbanisation ou de modification de permis d'urbanisation"
        },
        {
            "id": "15",
            "title": u"Annexe XI - Demande de permis d'urbanisation ou de modification de permis d'urbanisation avec contenu simplifié"
        },
        {
            "id": "16",
            "title": u"Annexe XV - Demande de certificat d'urbanisme n°2"
        },

    ]

    createFolderDefaultValues(
        form_composition_folder,
        form_composition_new_vocabulary_terms_to_add,
        portal_type="UrbanVocabularyTerm",
    )

    logger.info("upgrade done!")
