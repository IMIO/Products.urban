from plone import api
import logging
from Products.urban.interfaces import IInspection


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


def fix_inspection_title(context):
    logger = logging.getLogger('urban: Fix inspection title')
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IInspection.__identifier__)
    for licence_brain in licence_brains:
        if IInspection.providedBy(licence_brain.getObject()):
            licence = licence_brain.getObject()
            licence.updateTitle()
    logger.info("upgrade done!")
