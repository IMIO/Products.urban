from plone import api
import logging


def update_delais_vocabularies_and_activate_prorogation_field(context):
    """ """
    logger = logging.getLogger(
        "urban: update delais vocabularies and activate prorogation field"
    )
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-update-vocabularies"
    )
    portal_urban = api.portal.get_tool("portal_urban")
    for config in portal_urban.objectValues("LicenceConfig"):
        if (
            "prorogation" in config.listUsedAttributes()
            and "prorogation" not in config.getUsedAttributes()
        ):
            to_set = ("prorogation",)
            config.setUsedAttributes(config.getUsedAttributes() + to_set)
    logger.info("upgrade step done!")
