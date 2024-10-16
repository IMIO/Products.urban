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


def allow_corporate_tenant_in_inspections(context):
    """ """
    logger = logging.getLogger("urban: Allow corporate tenant in inspections")
    logger.info("starting upgrade steps")

    portal_types_tool = api.portal.get_tool("portal_types")
    isp_tool = portal_types_tool.get("Inspection")
    if "CorporationTenant" not in isp_tool.allowed_content_types:
        new_allowed_types = list(isp_tool.allowed_content_types) + ["CorporationTenant"]
        isp_tool.allowed_content_types = tuple(new_allowed_types)

    logger.info("upgrade step done!")
