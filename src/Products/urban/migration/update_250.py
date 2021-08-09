# encoding: utf-8

from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate

from plone import api
import logging

logger = logging.getLogger('urban: migrations')


def add_new_default_personTitle(context):
    logger = logging.getLogger('urban: add new default personTitle')
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')
    logger.info("upgrade done!")


def delete_migrated_miscdemands(context):
    """
    """
    logger = logging.getLogger('urban: delete migrated miscdemands')
    logger.info("starting upgrade steps")
    urban = api.portal.get().urban
    to_delete = [misc for misc in urban.miscdemands.objectValues() if misc.id in urban.inspections.objectIds()]
    api.content.delete(objects=to_delete)
    logger.info("upgrade done!")


def fix_POD_templates_odt_file(context):
    """
    Sometimes the template is stored in a tuple which is incorrect.
    """
    logger = logging.getLogger('urban: fix PODTemplates od_file')
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool('portal_catalog')
    all_templates = [b.getObject() for b in catalog(object_provides=IPODTemplate.__identifier__)]
    for template in all_templates:
        if type(template.odt_file) in [list, tuple]:
            template.odt_file = template.odt_file[0]
            logger.info("fixed template {}".format(template))
    logger.info("upgrade done!")


def replace_mailing_loop_owners(context):
    """
    For the mailing loop, owners are those in a zone of inquiry, and not the owners of the parcels like for inspections
    """
    logger = logging.getLogger('urban: replace mailing loop owners')
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool('portal_catalog')
    template_brains = catalog(object_provides=IConfigurablePODTemplate.__identifier__)
    brains_context_var = [ elt for elt in template_brains if elt.getObject().context_variables != None]
    doc_proprietaires = [elm for elm in brains_context_var if len(elm.getObject().context_variables) > 0 and elm.getObject().context_variables[0]['value'] == 'proprietaires']
    for j in range(0, len(doc_proprietaires)) : doc_proprietaires[j].getObject().context_variables[0]['value'] = 'proprietaires_voisinage_enquete'
    logger.info("upgrade done!")



