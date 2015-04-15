# -*- coding: utf-8 -*-

from Products.urban.interfaces import IEnvironmentBase

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def migrateToUrban1100(context):
    """
     Launch every migration steps for the version 1.10.0
    """
    logger = logging.getLogger('urban: migrate to 1.10.0')
    logger.info("starting migration steps")
    # migrate environment licences rubrics
    migrateReferencedEnvironmentRubrics(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


def migrateReferencedEnvironmentRubrics(context):
    """
    Applicant meta_type is now Applicant (instead of Contact).
    """
    logger = logging.getLogger('urban: migrate referenced rubrics ->')
    logger.info("starting migration step")

    site = api.portal.get()

    envclassthree_cfg = site.portal_urban.envclassthree

    if hasattr(envclassthree_cfg, 'rubrics'):
        catalog = api.portal.get_tool('portal_catalog')
        env_licences = catalog(object_provides=IEnvironmentBase.__identifier__)
        rubrics_cfg = site.portal_urban.rubrics

        for brain in env_licences:
            licence = brain.getObject()
            logger.info("migrating licence {}".format(licence.Title()))

            new_rubrics = []
            for rubric in licence.getRubrics():
                new_rubric = catalog(
                    path={'query': '/'.join(rubrics_cfg.getPhysicalPath())},
                    id=rubric.id
                )
                new_rubrics.append(new_rubric[0].getObject())

            licence.setRubrics(new_rubrics)

    logger.info("migration step done!")
