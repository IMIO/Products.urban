from plone import api
import logging


def add_couple_to_preliminary_notice(context):
    """
    """
    logger = logging.getLogger('urban: add Couple to Preliminary Notice')
    logger = logging.getLogger('urban: add Couple to Project Meeting')
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'workflow')
    logger.info("upgrade step done!")
