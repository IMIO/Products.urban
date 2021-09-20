# -*- coding: utf-8 -*-
from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate
from collective.documentgenerator.content.vocabulary import AllPODTemplateWithFileVocabularyFactory
from collective.documentgenerator.search_replace.pod_template import SearchAndReplacePODTemplates

from plone import api
from plone.app.uuid.utils import uuidToObject
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
    # get brains instead of all templates because brains are small
    for brain in template_brains:
        template = brain.getObject()
        # get the template we need
        if template.context_variables:
            # false if template.context_variables is None or empty
            new_value = []
            for line in template.context_variables:
                if line['value'] == 'proprietaires':
                    logger.info("migrated template : {} ".format(template))
                    line['value'] = 'proprietaires_voisinage_enquete'
                new_value.append(line)
            template.context_variables = new_value
    logger.info("upgrade done!")


def fix_type_eventtype_in_config(context):
    """
    Sometimes the type of the eventtype in the config is a string instead of what is expected.
    """
    logger = logging.getLogger('urban: fix type of eventtype in config')
    logger.info("starting upgrade steps")
    config = api.portal.get_tool('portal_urban')
    all_eventconfigs = []
    for licenceconf in config.get_all_licence_configs():
        all_eventconfigs.extend(licenceconf.getEventConfigs())
    for eventc in all_eventconfigs:
        eventtype = eventc.getEventType()
        if isinstance(eventtype, basestring):
            eventc.eventType = [eventtype]
            logger.info("modification on : {} ").format(eventc)
    logger.info("upgrade done!")


def update_POD_expressions(context):
    """
    Execute automatic search and replace for POD template code.
    """
    logger = logging.getLogger('urban: search and replace POD expressions')
    logger.info("starting upgrade steps")
    voc = AllPODTemplateWithFileVocabularyFactory()
    uids = [brain.UID for brain in voc._get_all_pod_templates_with_file()]
    templates = [uuidToObject(template_uuid) for template_uuid in uids]

    replacements = {
        {
            "search": "self.getValuesForTemplate\('(\w*)'\)",
            "replace": "self.\1",
            "is_regex": True,
        },
        {
            "search": "self.getValueForTemplate\('(\w*)'\)",
            "replace": "self.\1",
            "is_regex": True
        },
        {
            "search": "from xhtml\(tool.decorateHTML\('UrbanAddress',(.*)\)\)",
            "replace": "from self.xhtml(\1, style='UrbanAddress')",
            "is_regex": True
        },
        {
            "search": "self.getValuesForTemplate\('(\w*)',\s*subfield='description'\)",
            "replace": "self.voc_terms('\1')",
            "is_regex": True
        },
        {
            "search": "self.getValueForTemplate\('(\w*)',\s*subfield='description'\)",
            "replace": "self.voc_terms('\1')",
            "is_regex": True
        },
        {
            "search": "from\s*xhtml\((\w*)\)",
            "replace": "from xhtml(\1.Description())",
            "is_regex": True
        },
    }

    with SearchAndReplacePODTemplates(templates) as replace:
        for row in replacements:
            row["replace"] = row["replace"] or ""
            search_expr = row["search"]
            replace_expr = row["replace"]
            logger.info("Replacing POD expression {} by {}".format(search_expr, replace_expr))
            replace.replace(search_expr, replace_expr, is_regex=row["is_regex"])
    logger.info("upgrade done!")
