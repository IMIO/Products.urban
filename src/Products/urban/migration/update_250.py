# -*- coding: utf-8 -*-

from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate
from collective.documentgenerator.content.vocabulary import (
    AllPODTemplateWithFileVocabularyFactory,
)
from collective.documentgenerator.search_replace.pod_template import (
    SearchAndReplacePODTemplates,
)

from Products.urban.profiles.extra.config_default_values import default_values
from Products.urban.setuphandlers import createVocabularyFolder
from Products.urban.setuphandlers import createFolderDefaultValues

from plone import api
from plone.app.textfield import RichTextValue
from plone.app.uuid.utils import uuidToObject

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from Products.urban.config import URBAN_TYPES
from Products.urban.profiles.extra.schedule_config import (
    schedule_config as schedule_config_dict,
)

from Products.urban.interfaces import IGenericLicence, IBaseBuildLicence
import logging
import re

logger = logging.getLogger("urban: migrations")


def add_new_default_personTitle(context):
    logger = logging.getLogger("urban: add new default personTitle")
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-extraPostInstall"
    )
    logger.info("upgrade done!")


def delete_migrated_miscdemands(context):
    """ """
    logger = logging.getLogger("urban: delete migrated miscdemands")
    logger.info("starting upgrade steps")
    urban = api.portal.get().urban
    to_delete = [
        misc
        for misc in urban.miscdemands.objectValues()
        if misc.id in urban.inspections.objectIds()
    ]
    api.content.delete(objects=to_delete)
    logger.info("upgrade done!")


def fix_POD_templates_odt_file(context):
    """
    Sometimes the template is stored in a tuple which is incorrect.
    """
    logger = logging.getLogger("urban: fix PODTemplates od_file")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    all_templates = [
        b.getObject() for b in catalog(object_provides=IPODTemplate.__identifier__)
    ]
    for template in all_templates:
        if type(template.odt_file) in [list, tuple]:
            template.odt_file = template.odt_file[0]
            logger.info("fixed template {}".format(template))
    logger.info("upgrade done!")


def replace_mailing_loop_owners(context):
    """
    For the mailing loop, owners are those in a zone of inquiry, and not the owners of the parcels like for inspections
    """
    logger = logging.getLogger("urban: replace mailing loop owners")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    template_brains = catalog(object_provides=IConfigurablePODTemplate.__identifier__)
    # get brains instead of all templates because brains are small
    for brain in template_brains:
        template = brain.getObject()
        # get the template we need
        if template.context_variables:
            # false if template.context_variables is None or empty
            new_value = []
            for line in template.context_variables:
                if line["value"] == "proprietaires":
                    logger.info("migrated template : {} ".format(template))
                    line["value"] = "proprietaires_voisinage_enquete"
                new_value.append(line)
            template.context_variables = new_value
    logger.info("upgrade done!")


def fix_type_eventtype_in_config(context):
    """
    Sometimes the type of the eventtype in the config is a string instead of what is expected.
    """
    logger = logging.getLogger("urban: fix type of eventtype in config")
    logger.info("starting upgrade steps")
    config = api.portal.get_tool("portal_urban")
    all_eventconfigs = []
    for licenceconf in config.get_all_licence_configs():
        all_eventconfigs.extend(licenceconf.getEventConfigs())
    for eventc in all_eventconfigs:
        eventtype = eventc.getEventType()
        if isinstance(eventtype, basestring):
            eventc.eventType = [eventtype]
            logger.info("modification on : {} ").format(eventc)
    logger.info("upgrade done!")


def migrate_eventconfigs_description_field(context):
    """
    Description field should store RichTextValue objects.
    """
    logger = logging.getLogger("urban: migrate eventconfigs description field")
    logger.info("starting upgrade steps")
    config = api.portal.get_tool("portal_urban")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-imio.urban.core:default", "typeinfo")
    all_eventconfigs = []
    for licenceconf in config.get_all_licence_configs():
        all_eventconfigs.extend(licenceconf.getEventConfigs())
    for eventc in all_eventconfigs:
        description = (
            type(eventc.description) is RichTextValue
            and eventc.description.raw
            or eventc.description
        )
        if type(description) is str:
            description = description.decode("utf-8")
        if isinstance(description, basestring):
            eventc.description = RichTextValue(description)
            eventc.reindexObject()
            logger.info("migrated : {} ".format(eventc))
    logger.info("upgrade done!")


def reinstall_ticket_workflow(context):
    """ """
    logger = logging.getLogger("urban: reinstall ticket workflow")
    logger.info("starting upgrade steps")
    wf_tool = api.portal.get_tool("portal_workflow")
    wf_tool.manage_delObjects(ids=["ticket_workflow"])
    portal = api.portal.get()
    for ticket in portal.urban.tickets.objectValues()[1:]:
        ticket.manage_permission("imio.urban: Add Parcel", roles=[], acquire=1)

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    logger.info("upgrade done!")


def update_POD_expressions(context):
    """
    Execute automatic search and replace for POD template code.
    """
    logger = logging.getLogger("urban: search and replace POD expressions")
    logger.info("starting upgrade steps")
    voc = AllPODTemplateWithFileVocabularyFactory()
    uids = [brain.UID for brain in voc._get_all_pod_templates_with_file()]
    templates = [uuidToObject(template_uuid) for template_uuid in uids]

    replacements = [
        {
            "search": "for\s+(\w+)\s+in\s+self.getValuesForTemplate\('(\w+)'\)$",
            "replace": "for \\1 in self.voc_terms('\\2')",
            "is_regex": True,
        },
        {
            "search": "self.getValuesForTemplate\('(\w+)'\)",
            "replace": "self.\\1",
            "is_regex": True,
        },
        {
            "search": "self.getValueForTemplate\('(\w+)'\)",
            "replace": "self.\\1",
            "is_regex": True,
        },
        {
            "search": "self.getValueForTemplate\('(\w+)',\s*obj=(\S+)\s*\)",
            "replace": "\\2.\\1",
            "is_regex": True,
        },
        {
            "search": "self.getValueForTemplate\('(\w+)',\s*([^= ]+)\)",
            "replace": "\\2.\\1",
            "is_regex": True,
        },
        {
            "search": "self.getValueForTemplate\('(\w+)',\s*subfield='(\w+)'\)",
            "replace": "self.voc_term('\\1').\\2",
            "is_regex": True,
        },
        {
            "search": "from xhtml\(.*decorateHTML\('(\w+)',\s*(.*)\s*\)\)",
            "replace": r"from self.xhtml(\2, style='\1')",
            "is_regex": True,
        },
        {
            "search": "self.getValuesForTemplate\('(\w*)',\s*subfield='description'\)",
            "replace": "self.voc_terms('\\1')",
            "is_regex": True,
        },
        {
            "search": "self.getValueForTemplate\('(\w*)',\s*subfield='description'\)",
            "replace": "self.voc_terms('\\1')",
            "is_regex": True,
        },
        {
            "search": "from\s+xhtml\((\w*)\)",
            "replace": "from self.xhtml(\\1.Description())",
            "is_regex": True,
        },
        {"search": "parcel['title']", "replace": "parcel.Title", "is_regex": False},
        {
            "search": "getFormattedDescription()",
            "replace": "Description()",
            "is_regex": False,
        },
        {
            "search": "do\s*section(-?)\s*for\s*(\w*)\s*in\s*self.getInvestigationArticles\(\)",
            "replace": "do section\\1 for \\2 in self.voc_terms('investigationArticles')",
            "is_regex": True,
        },
        {
            "search": "self.getValuesForTemplate\('(\w*)Articles'.*",
            "replace": "self.voc_terms('\\1Articles')",
            "is_regex": True,
        },
        {"search": "^\s*subfield='description'\)", "replace": "", "is_regex": True},
        {
            "search": "for\s+(\w+)\s+in\s+self.(\w+)$",
            "replace": "for \\1 in self.voc_terms('\\2')",
            "is_regex": True,
        },
    ]

    with SearchAndReplacePODTemplates(templates) as replace:
        for row in replacements:
            row["replace"] = row["replace"] or ""
            search_expr = row["search"]
            replace_expr = row["replace"]
            logger.info(
                "Replacing POD expression {} by {}".format(search_expr, replace_expr)
            )
            replace.replace(search_expr, replace_expr, is_regex=row["is_regex"])
    logger.info("upgrade done!")


def add_all_applicants_in_title(context):
    """
    Adding all applicants or proprietaries or notaries in title
    """
    logger = logging.getLogger("urban: add all applicants in title")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
    licences = [
        l.getObject()
        for l in licence_brains
        if IGenericLicence.providedBy(l.getObject())
    ]
    for licence in licences:
        licence.updateTitle()
    logger.info("upgrade done!")


def add_trails_and_watercourses_to_global_vocabularies(context):
    """ """
    logger = logging.getLogger(
        "urban: add trails and watercourses to global vocabularies"
    )
    logger.info("starting upgrade steps")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-update-vocabularies"
    )
    logger.info("upgrade done!")


def fix_PODTemplates_empty_filename(context):
    """ """
    logger = logging.getLogger("urban: fix PODTemplates empty filename")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    all_templates = [
        b.getObject() for b in catalog(object_provides=IPODTemplate.__identifier__)
    ]
    for template in all_templates:
        # odt_file can be stored in tuples
        if template.odt_file and hasattr(template.odt_file, "__iter__"):
            template.odt_file = template.odt_file[0]
        if not template.odt_file:
            continue
        if not template.odt_file.filename:
            template_id = template.id
            if type(template_id) is str:
                template_id = template_id.decode("utf-8")
            template.odt_file.filename = template_id
            logger.info("fixed template {}".format(template))
        if template.odt_file.contentType == "applications/odt":
            template.odt_file.contentType = "application/vnd.oasis.opendocument.text"
    logger.info("upgrade done!")


def migrate_notaryletter_specificfeatures_texts(context):
    """ """
    logger = logging.getLogger("urban: migrate specificfeatures text codes")
    logger.info("starting upgrade steps")
    portal_urban = api.portal.get_tool("portal_urban")
    config = portal_urban.codt_notaryletter
    voc_folder_ids = [
        "specificfeatures",
        "locationspecificfeatures",
        "roadspecificfeatures",
    ]
    for voc_folder_id in voc_folder_ids:
        voc_folder = getattr(config, voc_folder_id)
        for value in voc_folder.objectValues():
            if "[[" in value.Description():
                new_text = re.sub(
                    "\[\[object.getValueForTemplate\('parcellings'\s*,\s*subfield='(\w*)'\),?\s*\]\]",
                    r"[[object.getParcellings().\1]]",
                    value.Description(),
                )
                new_text = re.sub(
                    "\[\['/'.join\(object.getValueForTemplate\('parcellings'\s*,\s*subfield='authorizationDate'\).split\(\)\[0\].split\('/'\)\[::-1\]\),?\s*\]\]",
                    r"[[format_date(object.getParcellings().getAuthorizationDate())]]",
                    new_text,
                )
                new_text = re.sub(
                    "\[\[object.getValueForTemplate\('(\w*)'\),?\s*\]\]",
                    r"[[object.\1]]",
                    new_text,
                )
                new_text = re.sub(
                    "\[\[object.getValueForTemplate\('(\w*)'},?\s*\]\]",
                    r"[[object.\1]]",
                    new_text,
                )
                new_text = re.sub(
                    "\[\[object.getValueForTemplate\('(\w*)'\s*,\s*subfield='(\w*)'\),?\s*\]\]",
                    r"[[voc_term('\1').\2]]",
                    new_text,
                )
                new_text = re.sub(
                    "\[\['/'.join\(object.getValueForTemplate\('(\w*)'\s*,\s*subfield='decreeDate'\).split\(\)\[0\].split\('/'\)\[::-1\]\),?\s*\]\]",
                    r"[[format_date(voc_term('\1').getDecreeDate())]]",
                    new_text,
                )
                new_text = re.sub(
                    "\[\[', '.join\(object.getValuesForTemplate\('(\w*)'\s*,\s*subfield='(\w*)'\)\),?\s*\]\]",
                    r"[[', '.join([t.\2 for t in voc_terms('\1')])]]",
                    new_text,
                )
                new_text = re.sub(
                    "\[\[', '.join\(object.getValuesForTemplate\('(\w*)'\s*,\s*subfield='(\w*)'},?\),?\s*\]\]",
                    r"[[', '.join([t.\2 for t in voc_terms('\1')])]]",
                    new_text,
                )
                value.setDescription(new_text)
                value.reindexObject()
    logger.info("upgrade done!")


def migrate_add_tax_other_option(context):
    """
    Add 'other' tax vocabulary value for all licence type config
    Used for show taxDetails field in all licence edition form.
    """
    logger = logging.getLogger("urban: migrate_add_tax_other_option")
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool("portal_urban")
    licence_configs = portal_urban.objectValues("LicenceConfig")
    for licence_config in licence_configs:
        if "other" not in licence_config.tax:
            licence_config.tax.invokeFactory(
                "UrbanVocabularyTerm", id="other", title="Autre"
            )

    logger.info("migration step done!")


def migrate_move_basebuildlicence_architects_and_geometricians_to_representative_contacts(
    context,
):
    """ """
    logger = logging.getLogger(
        "urban: migrate migrate_move_basebuildlicence_architects_and_geometricians_to_representative_contacts"
    )
    logger.info("starting migration step")
    catalog = api.portal.get_tool("portal_catalog")
    licence_brains = catalog(object_provides=IBaseBuildLicence.__identifier__)
    licences = [li.getObject() for li in licence_brains]
    for licence in licences:
        architects = licence.getField("architects")
        if architects:
            for architect in architects.get(licence):
                print(
                    "{} : move architect {} in representativeContacts".format(
                        licence.getReference(), architect.name1.encode("utf-8")
                    )
                )
                rc_list = licence.getRepresentativeContacts()
                rc_list.append(architect)
                licence.setRepresentativeContacts(rc_list)
                licence.setArchitects([])
        geometricians = licence.getField("geometricians")
        if geometricians:
            for geometrician in geometricians.get(licence):
                print(
                    "{} : move geometrician {} in representativeContacts".format(
                        licence.getReference(), geometrician.name1.encode("utf-8")
                    )
                )
                rc_list = licence.getRepresentativeContacts()
                rc_list.append(geometrician)
                licence.setRepresentativeContacts(rc_list)
                licence.setGeometricians([])

    logger.info("migration step done!")


def reinstall_registry_and_vocabularies(context):
    """
    Add collegeopinions vocabulary for all licence type config
    Reinstall plone registry with GIG coring settings.
    """
    logger = logging.getLogger("urban: reinstall_registry_and_vocabularies")
    logger.info("starting migration step")
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-update-vocabularies"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:default", "plone.app.registry"
    )
    logger.info("migration step done!")


def activate_divergence_field(context):
    """
    Enable divergence and divergenceDetails as they are now optionnals.
    """
    logger = logging.getLogger("urban: activate divergence")
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool("portal_urban")
    for config in portal_urban.objectValues("LicenceConfig"):
        if (
            "divergence" in config.listUsedAttributes()
            and "divergence" not in config.getUsedAttributes()
        ):
            to_set = ("divergence", "divergenceDetails")
            config.setUsedAttributes(config.getUsedAttributes() + to_set)
    logger.info("migration step done!")


def remove_icons_from_transitions(context):
    """
    launch import step to remove transitions icons and show them in letters
    """
    logger = logging.getLogger("urban: remove icons from transitions")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    logger.info("upgrade done!")


def add_and_active_corporation_tenant(context):
    """
    add corporation tenant content type and activate it
    """
    logger = logging.getLogger("urban: add and activate corporation tenant")
    logger.info("starting upgrade step")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    logger.info("upgrade step done!")


def addDocumentationLinkToUserPortalActionAndHideViewlet(context):
    """
    add documentation link to useractions and hide contact viewlet in footer
    """
    logger = logging.getLogger(
        "urban: add documentation link to user portal_actions and hide contact viewlet in footer"
    )
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "actions")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "viewlets")
    logger.info("upgrade step done!")


def add_deposit_date_column_to_dashboards(context):
    """
    Activate deposit date column on all licence dashboards.
    """
    logger = logging.getLogger("urban: add deposit date to dashboards")
    logger.info("starting upgrade steps")
    site = api.portal.get()

    old_fields = (
        "sortable_title",
        "CreationDate",
        "folder_manager",
        "actions",
        "select_row",
    )
    new_fields = (
        "sortable_title",
        "CreationDate",
        "getDepositDate",
        "folder_manager",
        "actions",
        "select_row",
    )

    collection = site.urban.collection_all_licences
    if collection.customViewFields == old_fields:
        collection.setCustomViewFields(new_fields)

    for folder in site.urban.objectValues("ATFolder"):
        collection = folder.objectIds() and folder.objectValues()[0]
        if not collection or folder.id in ["patrimonycertificates", "inspections"]:
            continue
        if collection.portal_type == "DashboardCollection":
            if collection.customViewFields == old_fields:
                collection.setCustomViewFields(new_fields)
    logger.info("upgrade step done!")


def replace_mailing_loop_proprietaries(context):
    """
    Mailing typo: replace proprietaire by proprietaires (with 's')
    """
    logger = logging.getLogger("urban: replace mailing loop proprietaries")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    template_brains = catalog(object_provides=IConfigurablePODTemplate.__identifier__)
    # get brains instead of all templates because brains are small
    for brain in template_brains:
        template = brain.getObject()
        # get the template we need
        if template.context_variables:
            # false if template.context_variables is None or empty
            new_value = []
            for line in template.context_variables:
                if line["value"] == "proprietaire":
                    logger.info("migrated template : {} ".format(template))
                    line["value"] = "proprietaires"
                new_value.append(line)
            template.context_variables = new_value
    logger.info("upgrade done!")


def set_default_warnings(context):
    """
    Set parcels warning on portal_urban warnings field.
    """
    logger = logging.getLogger("urban: replace mailing loop proprietaries")
    logger.info("starting upgrade steps")
    portal_urban = api.portal.get_tool("portal_urban")
    portal_urban.setWarnings(
        (
            {
                "condition": "urban.warnings.define_parcels",
                "level": "warning",
                "message": "Veuillez renseigner la ou les parcelle(s) concern\xc3\xa9e(s).",
            },
        )
    )
    logger.info("upgrade done!")


def update_tickets_title(context):
    """
    Recompute ticket title.
    """
    logger = logging.getLogger("urban: replace mailing loop proprietaries")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    brains = catalog(portal_type="Ticket")
    for brain in brains:
        ticket = brain.getObject()
        ticket.updateTitle()
    logger.info("upgrade done!")


def update_env_licences_schedule(context):
    """
    Install default schedule config for env licences and adapts default events.
    """
    logger = logging.getLogger("urban: Add schedule for env licences 1 & 2")
    logger.info("starting upgrade steps")
    portal_urban = api.portal.get_tool("portal_urban")

    # reinstall env licences workflows
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "workflow"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )

    # install schedule configs
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-update-schedule"
    )
    # reinstall event configs
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-updateAllUrbanTemplates"
    )
    catalog = api.portal.get_tool("portal_catalog")

    # tag complement deposit event config with IMissingPartTransmitToSPWEvent
    # marker interface
    for licence_type in ["envclasstwo", "envclassone"]:
        config = getattr(portal_urban, licence_type).eventconfigs
        event_cfg = getattr(config, "recepisse-complement")
        new_marker = "Products.urban.interfaces.IMissingPartTransmitToSPWEvent"
        if new_marker not in event_cfg.getEventType():
            event_cfg.eventType = tuple(list(event_cfg.getEventType()) + [new_marker])

    # reindex everything
    catalog.clearFindAndRebuild()

    logger.info("upgrade done!")


def hide_folder_contents_action(context):
    """ """
    logger = logging.getLogger("urban: hide folder_contents action")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "actions")
    logger.info("upgrade step done!")


def add_default_LO_server_port(context):
    """ """
    logger = logging.getLogger("urban: add second default LO port")
    logger.info("starting upgrade steps")
    old_port = api.portal.get_registry_record(
        "collective.documentgenerator.browser.controlpanel.IDocumentGeneratorControlPanelSchema.oo_port"
    )
    new_port = api.portal.get_registry_record(
        "collective.documentgenerator.browser.controlpanel.IDocumentGeneratorControlPanelSchema.oo_port_list"
    )
    if "2002" not in new_port or unicode(old_port) not in new_port:
        new_port = u"{};2002".format(old_port)
        api.portal.set_registry_record(
            "collective.documentgenerator.browser.controlpanel.IDocumentGeneratorControlPanelSchema.oo_port_list",
            new_port,
        )
    logger.info("upgrade step done!")


def add_applicant_couple_type(context):
    """ """
    logger = logging.getLogger("urban: add second default LO port")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "factorytool"
    )
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "typeinfo")
    setup_tool.runImportStepFromProfile("profile-Products.urban:preinstall", "workflow")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    logger.info("upgrade step done!")


def install_environment_article65(context):
    """ """
    logger = logging.getLogger("urban: configure environment configs for article 65")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-update-vocabularies"
    )
    portal_urban = api.portal.get_tool("portal_urban")
    for config_id in ["codt_uniquelicence", "envclassone", "envclasstwo"]:
        config = getattr(portal_urban, config_id)
        for event_config in config.eventconfigs.objectValues():
            if not event_config.getTALCondition():
                event_config.TALCondition = (
                    "python: licence.getProcedureChoice() != 'article65'"
                )
                logger.info("migrated eventconfig: {}".format(event_config))
    logger.info("upgrade step done!")


def install_environment_cession(context):
    """ """
    logger = logging.getLogger("urban: configure environment configs for cession")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:extra", "urban-updateAllUrbanTemplates"
    )
    portal_urban = api.portal.get_tool("portal_urban")
    for config_id in ["envclassone", "envclasstwo", "envclassthree"]:
        config = getattr(portal_urban, config_id)
        cession_event = getattr(config.eventconfigs, "cession-permis", None)
        if api.content.get_state(cession_event) == "disabled":
            api.content.transition(obj=cession_event, to_state="enabled")
    logger.info("upgrade step done!")


def install_auto_page_style_for_mailing_templates(context):
    """ """
    logger = logging.getLogger("urban: enable auto page style for mailing templates")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-collective.documentgenerator:default", "plone.app.registry"
    )
    enable_auto_page_style = api.portal.set_registry_record(
        "collective.documentgenerator.browser.controlpanel.IDocumentGeneratorControlPanelSchema.force_default_page_style_for_mailing",
        True,
    )
    logger.info("upgrade step done!")


def activate_env_divergence_and_referenceFT_fields(context):
    """
    Enable divergence and divergenceDetails as they are now optionnals.
    """
    logger = logging.getLogger("urban: activate divergence")
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool("portal_urban")
    for config in portal_urban.objectValues("LicenceConfig"):
        if (
            "divergences" in config.listUsedAttributes()
            and "divergences" not in config.getUsedAttributes()
        ):
            to_set = ("divergences",)
            config.setUsedAttributes(config.getUsedAttributes() + to_set)
        if (
            "referenceFT" in config.listUsedAttributes()
            and "referenceFT" not in config.getUsedAttributes()
        ):
            to_set = ("referenceFT",)
            config.setUsedAttributes(config.getUsedAttributes() + to_set)
    logger.info("migration step done!")


def set_page_style_for_mailing_templates(context):
    """ """
    logger = logging.getLogger("urban: set page style for mailing templates")
    logger.info("starting upgrade steps")
    catalog = api.portal.get_tool("portal_catalog")
    templates = [
        b.getObject()
        for b in catalog(object_provides=IConfigurablePODTemplate.__identifier__)
    ]
    for template in templates:
        if template.mailing_loop_template:
            notify(ObjectModifiedEvent(template))
            logger.info("Set defaut page style for {}".format(template))
    logger.info("upgrade step done!")


def install_browserlayer(context):
    """ """
    logger = logging.getLogger("urban: Install browserlayer")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:default", "browserlayer"
    )
    logger.info("upgrade step done!")


def add_new_vocabulary_for_zoning_field(context):
    """ """
    logger = logging.getLogger("urban: Add new vocabulary for Zoning field")
    logger.info("starting upgrade steps")

    container = api.portal.get_tool("portal_urban")
    vocabulary_name = "zoning"
    zoning_vocabularies_config = default_values["global"][vocabulary_name]
    allowedtypes = zoning_vocabularies_config[0]
    zoning_folder_config = createVocabularyFolder(
        container, vocabulary_name, context, allowedtypes
    )
    createFolderDefaultValues(
        zoning_folder_config,
        default_values["global"][vocabulary_name][1:],
        default_values["global"][vocabulary_name][0],
    )

    logger.info("migration step done!")


def _update_collection(context):
    dashboard_collection = getattr(context, "dashboard_collection", None)
    if "assigned_user_column" in dashboard_collection.customViewFields:
        customViewFields = list(dashboard_collection.customViewFields)
        customViewFields = [
            "assigned_user" if field == "assigned_user_column" else field
            for field in customViewFields
        ]
        dashboard_collection.customViewFields = tuple(customViewFields)


def update_collection_column(context):
    logger = logging.getLogger("urban: Update Collection Column")
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get_tool("portal_urban")
    for urban_type in URBAN_TYPES:
        config_folder = getattr(portal_urban, urban_type.lower())
        schedule_config = getattr(config_folder, "schedule")
        _update_collection(schedule_config)

        for task in schedule_config_dict.get(urban_type.lower(), []):
            task_collection = getattr(schedule_config, task["id"])
            _update_collection(task_collection)

            for subtask in task.get("subtasks", []):
                subtask_collection = getattr(task_collection, subtask["id"])
                _update_collection(subtask_collection)

    logger.info("upgrade step done!")


def update_faceted_collection_widget(context):
    from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
    from eea.facetednavigation.interfaces import ICriteria

    logger = logging.getLogger("Urban: Update collection widget")
    logger.info("starting upgrade steps")

    brains = api.content.find(object_provides=IFacetedNavigable.__identifier__)
    for brain in brains:
        faceted = brain.getObject()
        criterion = ICriteria(faceted)
        for criteria in criterion.values():
            if criteria.widget == "collection-link":
                setattr(criteria, "hide_category", True)
                setattr(criteria, "hidealloption", True)
                criteria._p_changed = 1
                criterion.criteria._p_changed = 1

    logger.info("migration step done!")
