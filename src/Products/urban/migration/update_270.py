# encoding: utf-8

from plone import api
import logging


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


def remove_permission_to_create_integrated_licences(context):
    logger = logging.getLogger("urban: remove permission to create integrated licences")
    logger.info("starting upgrade step")

    portal = api.portal.get()
    codt_integratedlicences_folder = getattr(portal.urban, "codt_integratedlicences")
    if not codt_integratedlicences_folder:
        logger.error("couldn't find codt_integratedlicences folder, aborting!")
        return

    for principal_id, roles in codt_integratedlicences_folder.get_local_roles():
        if "Contributor" in roles:
            remaining_roles = tuple(set(roles).difference(["Contributor"]))
            codt_integratedlicences_folder.manage_delLocalRoles([principal_id])
            if remaining_roles:
                codt_integratedlicences_folder.manage_addLocalRoles(principal_id, remaining_roles)

    codt_integratedlicences_folder.reindexObjectSecurity()
    logger.info("upgrade step done!")
