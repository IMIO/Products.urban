# encoding: utf-8

from textwrap import dedent

from Products.CMFCore.utils import getToolByName
from Products.cron4plone.browser.configlets.cron_configuration import ICronConfiguration
from Products.urban import URBAN_TYPES
from Products.urban import UrbanMessage as _
from Products.urban.contentrules.notice import INoticeImportFailedEvent
from Products.urban.contentrules.notice import INoticeImportSucceededEvent
from Products.urban.contentrules.utils import ContentRulesUtils
from Products.urban.migration.utils import cook_javascript_resources
from Products.urban.setuphandlers import add_new_urban_licence_type
from Products.urban.utils import moveElementAfter
from Products.urban.setuphandlers import set_licence_folder_security
from dm.historical import getHistory
from imio.helpers.catalog import reindexIndexes
from plone import api
from plone.app.textfield import RichTextValue
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import queryUtility
from zope.event import notify

import logging


logger = logging.getLogger("urban: migrations")


def initialize_notice_settings(context):
    from Products.urban.browser.notice_settings import INoticeSettings

    logger = logging.getLogger("urban: Initialize Notice Settings")
    registry = getUtility(IRegistry)
    base = "Products.urban.browser.notice_settings.INoticeSettings"
    if "{0}.url".format(base) not in registry.records:
        registry_field = field.TextLine(title=INoticeSettings["url"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.url".format(base)] = registry_record
    if "{0}.municipality_id".format(base) not in registry.records:
        registry_field = field.TextLine(title=INoticeSettings["municipality_id"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.municipality_id".format(base)] = registry_record
    if "{0}.sent_on_behalf_of_municipality_id".format(base) not in registry.records:
        registry_field = field.TextLine(
            title=INoticeSettings["sent_on_behalf_of_municipality_id"].title
        )
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records[
            "{0}.sent_on_behalf_of_municipality_id".format(base)
        ] = registry_record
    if "{0}.last_import_date".format(base) not in registry.records:
        registry_field = field.Datetime(title=INoticeSettings["last_import_date"].title)
        registry_record = Record(registry_field)
        registry_record.value = None
        registry.records["{0}.last_import_date".format(base)] = registry_record
    if "{0}.failed_notifications".format(base) not in registry.records:
        registry_field = field.List(title=INoticeSettings["failed_notifications"].title)
        registry_record = Record(registry_field)
        registry_record.value = []
        registry.records["{0}.failed_notifications".format(base)] = registry_record
    logger.info("Upgrade done!")


def add_event_config_types_notice(context):
    from Products.urban.profiles.extra.data import EventConfigs

    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "workflow"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "typeinfo"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "factorytool"
    )
    portal_setup.runImportStepFromProfile("profile-Products.urban:default", "actions")

    # migrate event configs
    tool = getToolByName(context, "portal_urban")
    for urban_config_id in EventConfigs:
        try:
            uet_folder = getattr(
                tool.getLicenceConfig(None, urbanConfigId=urban_config_id),
                "eventconfigs",
            )
        except AttributeError:
            continue  # TODO: log ?
        last_urbaneventype_id = None

        for uet in EventConfigs[urban_config_id]:
            portal_type = uet.get("portal_type", "EventConfig")
            if portal_type == "OpinionEventConfig":
                continue
            id = uet["id"]
            folder_event = getattr(uet_folder, id, None)

            if not folder_event:
                # create new eventConfig
                new_uet_id = uet_folder.invokeFactory(portal_type, **uet)
                new_uet = getattr(uet_folder, new_uet_id)
                if new_uet.description == "":
                    new_uet.description = RichTextValue("")
                if last_urbaneventype_id:
                    moveElementAfter(new_uet, uet_folder, "id", last_urbaneventype_id)
                else:
                    uet_folder.moveObjectToPosition(new_uet.getId(), 0)
                # updateTemplates(context, new_uet, uet['podTemplates'], new_install=False)  # TODO: AttributeError: _profile_path
                api.content.transition(
                    new_uet, "disable"
                )  # TODO: why ? line still useful ?

            else:  # patch existing eventConfig

                # set eventPortalType
                required_event_portal_type = uet.get("eventPortalType", "UrbanEvent")
                if folder_event.getEventPortalType() != required_event_portal_type:
                    setattr(folder_event, "eventPortalType", required_event_portal_type)

                # activate new fields
                old_fields = folder_event.getActivatedFields()
                missing_fields = set(uet.get("activatedFields", [])) - set(old_fields)
                if missing_fields:
                    new_fields = list(old_fields) + list(missing_fields)
                    setattr(folder_event, "activatedFields", new_fields)

                # add new eventType elements
                old_interfaces = folder_event.getEventType()
                missing_interfaces = set(uet.get("eventType", [])) - set(old_interfaces)
                if missing_interfaces:
                    new_interfaces = tuple(
                        list(old_interfaces) + list(missing_interfaces)
                    )
                    setattr(folder_event, "eventType", new_interfaces)

            last_urbaneventype_id = id


def add_folder_manager_notice(context):
    from Products.urban.setuphandlers import _activate_dashboard_navigation
    from collective.eeafaceted.collectionwidget.utils import _updateDefaultCollectionFor
    from eea.facetednavigation.criteria.interfaces import ICriteria
    from eea.facetednavigation.events import FacetedGlobalSettingsChangedEvent

    logger = logging.getLogger("urban: Add folder manager for notice import")

    # create folder manager
    urban_tool = api.portal.get_tool("portal_urban")
    foldermanagers = getattr(urban_tool, "foldermanagers")
    if "notice" not in foldermanagers.objectIds():
        foldermanagers.invokeFactory(
            "FolderManager",
            "notice",
            name1="Import NOTICE",
            grade="agent-technique",
            ploneUserId="",
            manageableLicences=URBAN_TYPES,
        )
    notice_folder_manager = foldermanagers.notice
    notice_folder_manager.reindexObject()

    # create dashboard for incoming notice notifications
    urban_folder = api.portal.get().urban

    if "import-notice" not in urban_folder.objectIds():
        import_notice_folder = api.content.create(
            container=urban_folder,
            type="Folder",
            id="import-notice",
            title="Import NOTICE",
        )

        _activate_dashboard_navigation(
            import_notice_folder, "/dashboard/config/import_notice.xml"
        )

        # no need to create another collection, this one does the job
        all_licences_collection = getattr(urban_folder, "collection_all_licences")
        _updateDefaultCollectionFor(import_notice_folder, all_licences_collection.UID())

        # set notice folder manager's UID as default in faceted filter widget
        criteria = ICriteria(import_notice_folder).criteria
        for criterion in criteria:
            if criterion.index == "folder_manager":
                ICriteria(import_notice_folder).edit(
                    criterion.__name__,
                    default=notice_folder_manager.UID(),
                )
        notify(FacetedGlobalSettingsChangedEvent(import_notice_folder))

    logger.info("Upgrade done!")


def refresh_javascript(context):
    logger = logging.getLogger("urban: Cook javascript resources")
    cook_javascript_resources()
    logger.info("Upgrade done!")


def recover_event_config_interfaces(context):
    from Products.urban.profiles.extra.data import EventConfigs

    logger = logging.getLogger("urban: Recover event config interfaces")

    def get_previous_event_type_interfaces(event):
        history = getHistory(event)
        for version in history:
            old_obj = version["obj"]
            event_type_interfaces = old_obj.getEventType()
            broken_data_present = any(
                [
                    ".interfaces." not in event_type
                    for event_type in event_type_interfaces
                ]
            )
            if not broken_data_present:
                return event_type_interfaces

    # migrate event configs
    tool = getToolByName(context, "portal_urban")
    for urban_config_id in EventConfigs:
        try:
            uet_folder = getattr(
                tool.getLicenceConfig(None, urbanConfigId=urban_config_id),
                "eventconfigs",
            )
        except AttributeError:
            continue  # TODO: log ?

        for uet in EventConfigs[urban_config_id]:
            portal_type = uet.get("portal_type", "EventConfig")
            if portal_type == "OpinionEventConfig":
                continue
            id = uet["id"]
            folder_event = getattr(uet_folder, id, None)

            if folder_event:  # patch existing eventConfig
                # look for broken data in eventType field
                event_type_interfaces = folder_event.getEventType()
                broken_data_present = any(
                    [
                        ".interfaces." not in event_type
                        for event_type in event_type_interfaces
                    ]
                )
                if broken_data_present:
                    old_interfaces = get_previous_event_type_interfaces(folder_event)
                    if old_interfaces:
                        # restore old interfaces
                        setattr(folder_event, "eventType", old_interfaces)
                        # continue treatment from add_event_config_types_notice
                        missing_interfaces = set(uet.get("eventType", [])) - set(
                            old_interfaces
                        )
                        if missing_interfaces:
                            new_interfaces = tuple(
                                list(old_interfaces) + list(missing_interfaces)
                            )
                            setattr(folder_event, "eventType", new_interfaces)

    logger.info("Upgrade done!")


def update_documentation_url(context):
    """
    Update documentation url
    """
    logger = logging.getLogger("urban: Update documentation url")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "actions")
    logger.info("upgrade step done!")


def add_architect_folder_view(context):
    """
    Add architect folder view
    """
    logger = logging.getLogger("urban: Add architect folder view")
    logger.info("starting upgrade steps")
    portal = api.portal.get()
    architects_folder = portal["urban"]["architects"]
    architects_folder.setLayout("architects_folderview")
    logger.info("upgrade step done!")


def recover_event_config_portal_types(context):
    from Products.urban.profiles.extra.data import EventConfigs

    logger = logging.getLogger(
        "urban: Recover `UrbanEventCollege` portal type in relevant EventConfig"
    )

    tool = getToolByName(context, "portal_urban")
    for urban_config_id in EventConfigs:
        try:
            uet_folder = getattr(
                tool.getLicenceConfig(None, urbanConfigId=urban_config_id),
                "eventconfigs",
            )
        except AttributeError:
            continue

        for uet in EventConfigs[urban_config_id]:
            portal_type = uet.get("portal_type", "EventConfig")
            if portal_type == "OpinionEventConfig":
                continue
            id = uet["id"]
            folder_event = getattr(uet_folder, id, None)

            if folder_event:  # patch existing eventConfig
                should_be_college = "pmTitle" in folder_event.getActivatedFields()
                if (
                    should_be_college
                    and folder_event.getEventPortalType() != "UrbanEventCollege"
                ):
                    setattr(folder_event, "eventPortalType", "UrbanEventCollege")

    logger.info("upgrade step done!")


def setup_index_referenceFT(context):
    logger = logging.getLogger("urban: Set up `referenceFT` index")

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:urbantypes", "catalog")

    reindexIndexes(None, ["referenceFT"])

    logger.info("upgrade step done!")


def fix_housing_roaddecree(context):
    logger = logging.getLogger("urban: Fix housing and roaddecree security")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "factorytool"
    )
    portal_types = ["Housing", "RoadDecree"]
    for portal_type in portal_types:
        set_licence_folder_security(portal_type)
    logger.info("upgrade step done!")


def update_folder_manager_notice(context):

    UPDATED_URBAN_TYPES = [
        "CODT_Article127",
        "CODT_UniqueLicence",
        "EnvClassOne",
        "EnvClassTwo",
        "EnvClassBordering",
    ]

    logger = logging.getLogger("urban: Update manageableLicences for notice")

    urban_tool = api.portal.get_tool("portal_urban")
    foldermanagers = getattr(urban_tool, "foldermanagers", None)

    if not foldermanagers or "notice" not in foldermanagers.objectIds():
        logger.warning("Notice FolderManager not found, skipping")
        return

    notice_folder_manager = foldermanagers.notice
    notice_folder_manager.manageableLicences = UPDATED_URBAN_TYPES
    notice_folder_manager.reindexObject()

    logger.info("manageableLicences updated for notice FolderManager")


def setup_index_referenceDGATLP(context):
    logger = logging.getLogger("urban: Set up `referenceDGATLP` index")

    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:urbantypes", "catalog")

    reindexIndexes(None, ["referenceDGATLP"])

    logger.info("upgrade step done!")


def add_codt_uniquebordering_licences(context):
    """
    Note: the events must be added by upgrade step in `urban.events`
    """

    logger = logging.getLogger("urban: Add CODT unique bordering licences")

    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "workflow"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:preinstall", "update-workflow-rolemap"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "typeinfo"
    )
    portal_setup.runImportStepFromProfile(
        "profile-Products.urban:urbantypes", "factorytool"
    )

    add_new_urban_licence_type("CODT_UniqueBorderingLicence")

    logger.info("Upgrade done!")


def setup_notice_mailing_content_rules(context):
    logger = logging.getLogger("urban: Set up NOTICE mailing content rules")

    portal = api.portal.get()

    success_template = dedent(
        u"""
        Bonjour,

        Une notification du SPW a été réceptionnée pour:

        - Dossier : ${parent_url}
        - Type de notification : ${notice_type}
        - Mail de l'agent traitant : ${folder_manager_email}

        Belle journée.
        """
    ).strip()

    failure_template = dedent(
        u"""
        Créer un ticket JIRA à l'attention d'un développeur
        (composant : Dématérialisation, sprint : En cours, état : Bloquant)

        "Bonjour,

        Une erreur d'implémentation de notification du webservice Notice a été enregistrée.
        Merci de prendre connaissance des raisons dans Kibana et de la débloquer.

        - commune / dossier : ${parent_url}
        - identifiant NOTICE : ${notice_id}

        ```
        ${notice_error}
        ```

        Belle journée.

        Aurore"
        """
    ).strip()

    rule_id = "notification_tlpe_imported_successfully"
    if not ContentRulesUtils.rule_exists(rule_id):
        ContentRulesUtils.create_content_rule(
            title=u"Notification TLPE importée",
            event_interface=INoticeImportSucceededEvent,
            rule_id=rule_id,
        )
        ContentRulesUtils.add_condition(
            rule_id=rule_id,
            condition_name="urban.conditions.licence_type",
            data={"licence_type": ["CODT_Article127"]},
        )
        ContentRulesUtils.add_action(
            rule_id=rule_id,
            action_name="plone.actions.Mail",
            data={
                "exclude_actor": False,
                "subject": u"Notification importée",
                "recipients": u"support-urban@imio.be",
                "message": success_template,
            },
        )
        ContentRulesUtils.assign_rule(portal, rule_id)
        ContentRulesUtils.enable_rule(portal, rule_id, bubbles=True)

    rule_id = "notification_arne_imported_successfully"
    if not ContentRulesUtils.rule_exists(rule_id):
        ContentRulesUtils.create_content_rule(
            title=u"Notification ARNE importée",
            event_interface=INoticeImportSucceededEvent,
            rule_id=rule_id,
        )
        ContentRulesUtils.add_condition(
            rule_id=rule_id,
            condition_name="urban.conditions.licence_type",
            data={
                "licence_type": [
                    "CODT_UniqueLicence",
                    "CODT_UniqueBorderingLicence",
                    "EnvClassOne",
                    "EnvClassTwo",
                    "EnvClassThree",
                    "EnvClassBordering",
                ]
            },
        )
        ContentRulesUtils.add_action(
            rule_id=rule_id,
            action_name="plone.actions.Mail",
            data={
                "exclude_actor": False,
                "subject": u"Notification importée",
                "recipients": u"support-urban@imio.be",
                "message": success_template,
            },
        )
        ContentRulesUtils.assign_rule(portal, rule_id)
        ContentRulesUtils.enable_rule(portal, rule_id, bubbles=True)

    rule_id = "notification_import_failed"
    if not ContentRulesUtils.rule_exists(rule_id):
        ContentRulesUtils.create_content_rule(
            title=u"Notification NOTICE en erreur",
            event_interface=INoticeImportFailedEvent,
            rule_id=rule_id,
        )
        ContentRulesUtils.add_action(
            rule_id=rule_id,
            action_name="plone.actions.Mail",
            data={
                "exclude_actor": False,
                "subject": u"Notification Notice en erreur",
                "recipients": u"support-urban@imio.be",
                "message": failure_template,
            },
        )
        ContentRulesUtils.assign_rule(portal, rule_id)
        ContentRulesUtils.enable_rule(portal, rule_id, bubbles=True)

    logger.info("Upgrade done!")


def reindex_getDecisionDate(context):
    logger = logging.getLogger("urban: Reindex getDecisionDate")

    reindexIndexes(None, ["getDecisionDate"])


def add_digital_term_to_deposit_type(context):
    """
    Add 'digital' term to the global deposittype vocabulary
    and activate depositType on the depot-de-la-demande event config for
    licence types.
    """
    logger = logging.getLogger("urban: Add MonEspace deposit type")
    tool = getToolByName(context, "portal_urban")

    if hasattr(tool, "deposittype"):
        deposittype_folder = tool.deposittype
        if "digital" not in deposittype_folder.objectIds():
            deposittype_folder.invokeFactory(
                "UrbanVocabularyTerm", id="digital", title=u"Dématérialisé"
            )
            logger.info("Added 'digital' vocabulary term to global deposittype")

    target_configs = {
        "codt_uniquelicence": "depot-de-la-demande",
        "envclassone": "depot-de-la-demande",
        "envclasstwo": "depot-de-la-demande",
        "envclassthree": "depot-de-la-demande",
    }
    for urban_config_id, event_config_id in target_configs.items():
        try:
            licence_config = tool.getLicenceConfig(None, urbanConfigId=urban_config_id)
            event_config = getattr(licence_config.eventconfigs, event_config_id, None)
        except AttributeError:
            logger.warning("Could not find config for %s, skipping", urban_config_id)
            continue

        if event_config is None:
            logger.warning(
                "Event config '%s' not found for %s, skipping",
                event_config_id,
                urban_config_id,
            )
            continue

        activated = list(event_config.getActivatedFields())
        if "depositType" not in activated:
            activated.insert(0, "depositType")
            setattr(event_config, "activatedFields", activated)
            logger.info(
                "Activated depositType on '%s' for %s", event_config_id, urban_config_id
            )

    logger.info("upgrade step done!")


def normalize_externaldecisions_vocabulary(context):

    VOCABULARY_TERMS = [
        "FAVORABLE",
        "DEFAVORABLE",
        "FAVORABLE_PARTIEL",
        "FAVORABLE_CONDITIONS",
    ]

    EXTERNALDECISIONS_MAPPING = {
        "favorable": "FAVORABLE",
        "defavorable": "DEFAVORABLE",
        "favorable-conditionnel": "FAVORABLE_CONDITIONS",
    }
    DESCRIPTION = u"obligatoire pour la dématérialisation => NE PAS SUPPRIMER"
    portal_urban = api.portal.get_tool("portal_urban")
    voc_folder = portal_urban.externaldecisions
    term_objects = portal_urban.listVocabularyObjects(
        "externaldecisions",
        context,
        inUrbanConfig=False,
        allowedStates=["enabled", "disabled"],
    )

    found_terms = set()

    for term_id, term_obj in term_objects.items():
        # 1st case: term already has vocabulary_term id
        if term_id in VOCABULARY_TERMS:
            term_obj.setDescription(DESCRIPTION)
            found_terms.add(term_id)
            continue

        # 2nd case: term exists but needs mapping
        existing_vocabulary_term = EXTERNALDECISIONS_MAPPING.get(term_id)
        if existing_vocabulary_term in VOCABULARY_TERMS:
            term_obj.setDescription(DESCRIPTION)
            found_terms.add(existing_vocabulary_term)

    # 3rd case: vocabulary_term term doesn't exist yet, must be added
    for vocabulary_term in VOCABULARY_TERMS:
        if vocabulary_term not in found_terms:
            voc_folder.invokeFactory(
                "UrbanVocabularyTerm",
                id=vocabulary_term,
                title=vocabulary_term.replace("_", " ").capitalize(),
            )
            new_term = getattr(voc_folder, vocabulary_term)
            new_term.setDescription(DESCRIPTION)
            logger.info("Created missing vocabulary term: %s", vocabulary_term)


def setup_cron4plone_notice_import(context):
    logger = logging.getLogger("urban: Setup cron4plone notice import")

    cron_cfg = queryUtility(
        ICronConfiguration, name="cron4plone_config", context=api.portal.get()
    )

    line_to_add = u"0 * * * portal/@@import-from-notice"
    if line_to_add not in cron_cfg.cronjobs:
        new_list = list(cron_cfg.cronjobs) + [line_to_add]
        cron_cfg.cronjobs = new_list

    logger.info("upgrade step done!")
