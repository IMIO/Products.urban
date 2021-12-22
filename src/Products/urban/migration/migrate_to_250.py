# -*- coding: utf-8 -*-

from Acquisition import aq_base

from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate
from collective.iconifieddocumentactions.upgrades import move_to_collective_iconifieddocumentactions
from collective.noindexing import patches

from imio.schedule.content.object_factories import MacroCreationConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject
from imio.schedule.content.object_factories import MacroRecurrenceConditionObject

from plone.browserlayer.interfaces import ILocalBrowserLayerType

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from Products.urban import services
from Products.urban.config import URBAN_TYPES
from Products.urban.config import LICENCE_FINAL_STATES
from Products.urban.interfaces import ICODT_BaseBuildLicence
from Products.urban.interfaces import ICODT_UrbanCertificateBase
from Products.urban.interfaces import IGenericLicence
from Products.urban.migration.to_DX.migration_utils import clean_obsolete_portal_type
from Products.urban.migration.utils import disable_licence_default_values
from Products.urban.migration.utils import disable_schedule
from Products.urban.migration.utils import restore_licence_default_values
from Products.urban.setuphandlers import setFolderAllowedTypes
from Products.urban.utils import getLicenceFolderId

from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from plone import api

import logging

logger = logging.getLogger('urban: migrations')


def clear_communesplone_iconifiedactions_layer(context):
    logger = logging.getLogger('urban: clear communesplone.iconifieddocumentactions layer')
    logger.info("starting migration step")
    if queryUtility(ILocalBrowserLayerType, name='communesplone.iconified_document_actions.layer'):
        move_to_collective_iconifieddocumentactions(context)
        logger.info("cleared communesplone.iconifieddocumentactions layer")
        logger.info("rebuilding catalog...")
    logger.info("starting step done")


def migrate_codt_buildlicences_schedule(context):
    """
    Disbale recurrency for task 'deposit'
    """
    logger = logging.getLogger('urban: migrate codt buildlicences schedule')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    schedule = portal_urban.codt_buildlicence.schedule
    if hasattr(schedule.incomplet2, 'notify_refused'):
        schedule.incomplet2.notify_refused.ending_states = ()
    if hasattr(schedule.reception, 'deposit'):
        schedule.reception.deposit.ending_states = ()
        schedule.reception.deposit.recurrence_states = ()
        schedule.reception.deposit.activate_recurrency = False
    if 'deposit' not in (schedule.incomplet.attente_complements.ending_states or ()):
        old_states = schedule.incomplet.attente_complements.ending_states or ()
        new_states = tuple(old_states) + ('deposit',)
        schedule.incomplet.attente_complements.ending_states = new_states
    if 'complete' not in (schedule.reception.ending_states or ()):
        old_states = schedule.reception.ending_states or ()
        new_states = tuple(old_states) + ('deposit',)
        schedule.reception.ending_states = new_states
    if 'incomplete' not in (schedule.reception.ending_states or ()):
        old_states = schedule.reception.ending_states or ()
        new_states = tuple(old_states) + ('incomplete',)
        schedule.reception.ending_states = new_states

    logger.info("migration step done!")


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


class CODT_NotaryLetterMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanCertificateBase"
    src_portal_type = "CODT_NotaryLetter"
    dst_meta_type = "CODT_UrbanCertificateBase"
    dst_portal_type = "CODT_NotaryLetter"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrate_CODT_NotaryLetter_to_CODT_UrbanCertificateBase(context):
    """
    Base class of CODT_NotaryLetter is now CODT_UrbanCertificateBase
    """
    logger = logging.getLogger('urban: migrate CODT_NotaryLetter meta type to CODT_UrbanCertificateBase ->')
    logger.info("starting migration step")

    migrator = CODT_NotaryLetterMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    # disable catalog and default values
    disable_licence_default_values()
    patches.apply()

    # Run the migrations
    folder_path = '/'.join(portal.urban.codt_notaryletters.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={'path': folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url,
        transaction_size=100000,
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    # restore catalog and default values
    restore_licence_default_values()
    patches.unapply()

    logger.info("migration step done!")


class CODT_UrbanCertificateOneMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanCertificateBase"
    src_portal_type = "CODT_UrbanCertificateOne"
    dst_meta_type = "CODT_UrbanCertificateBase"
    dst_portal_type = "CODT_UrbanCertificateOne"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrate_CODT_UrbanCertificateOne_to_CODT_UrbanCertificateBase(context):
    """
    Base class of CODT_NotaryLetter is now CODT_UrbanCertificateBase
    """
    logger = logging.getLogger('urban: migrate CODT_UrbanCertificateOne meta type to CODT_UrbanCertificateBase ->')
    logger.info("starting migration step")

    migrator = CODT_UrbanCertificateOneMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    # disable catalog and default values
    disable_licence_default_values()
    patches.apply()

    # Run the migrations
    folder_path = '/'.join(portal.urban.codt_urbancertificateones.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={'path': folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url,
        transaction_size=100000,
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    # restore catalog and default values
    restore_licence_default_values()
    patches.unapply()

    logger.info("migration step done!")


class CODT_UniqueLicenceInquiryMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "Inquiry"
    src_portal_type = "Inquiry"
    dst_meta_type = "CODT_UniqueLicenceInquiry"
    dst_portal_type = "CODT_UniqueLicenceInquiry"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrate_Env_Inquiry_to_CODT_UniquelicenceInquiry(context):
    """
    Migrate env licences Inquiry to CODT_UniquelicenceInquiry.
    """
    logger = logging.getLogger('urban: migrate Inquiry meta type to CODT_UniquelicenceInquiry ->')
    logger.info("starting migration step")

    migrator = CODT_UniqueLicenceInquiryMigrator
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    # disable catalog and default values
    disable_licence_default_values()
    patches.apply()

    # Run the migrations
    folder_path = '/'.join(portal.urban.envclassones.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={'path': folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url,
        transaction_size=100000,
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}

    folder_path = '/'.join(portal.urban.envclasstwos.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={'path': folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url,
        transaction_size=100000,
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    # restore catalog and default values
    restore_licence_default_values()
    patches.unapply()

    logger.info("migration step done!")


def migrate_CODT_UrbanCertificateBase_add_permissions(context):
    """
    """
    logger = logging.getLogger('urban: migrate CODT_UrbanCertificateBase add permission')
    logger.info("starting migration step")

    portal = api.portal.get()
    for urban_type in URBAN_TYPES:
        licence_folder_id = getLicenceFolderId(urban_type)
        licence_folder = getattr(portal.urban, licence_folder_id)
        if urban_type in ['CODT_UrbanCertificateOne', 'CODT_NotaryLetter', ]:
            licence_folder.manage_permission(
                'urban: Add CODT_UrbanCertificateBase',
                ['Manager', 'Contributor', ],
                acquire=0
            )

    logger.info("migration step done!")


def migrate_opinion_request_TAL_expression(context):
    """
    """
    logger = logging.getLogger('urban: migrate opinion request TAL expression')
    logger.info("starting migration step")

    catalog = api.portal.get_tool('portal_catalog')
    opinion_request_eventtypes = [b.getObject() for b in catalog(portal_type='OpinionRequestEventType')]
    for opinion_request_eventtype in opinion_request_eventtypes:
        if opinion_request_eventtype.getTALCondition().strip():
            opinion_request_eventtype.setTALCondition("python: event.mayAddOpinionRequestEvent(here)")
            logger.info("migrated TAL condition of {}".format(opinion_request_eventtype))

    logger.info("migration step done!")


def migrate_report_and_remove_urbandelay_portal_type(context):
    """
    """
    logger = logging.getLogger('urban: report_and_remove_urbandelay_portal_type')
    logger.info("starting migration step")
    clean_obsolete_portal_type(portal_type_to_remove='UrbanDelay')
    logger.info("migration step done!")


def migrate_default_states_to_close_tasks(context):
    logger = logging.getLogger('urban: migrate default states to close all tasks')
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool('portal_urban')
    for licence_config in urban_tool.get_all_licence_configs():
        states_voc = getUtility(IVocabularyFactory, 'urban.licence_state')(licence_config)
        default_end_states = [st for st in states_voc.by_value.keys() if st in LICENCE_FINAL_STATES]
        licence_config.setStates_to_end_all_tasks(default_end_states)
        schedule_cfg = getattr(licence_config, 'schedule', None)
        for task_cfg in schedule_cfg.get_all_task_configs():
            # remove 'licence_ended' from  the end conditions
            end_conditions = task_cfg.end_conditions or []
            end_condition_ids = end_conditions and [c.condition for c in end_conditions]
            condition_id = 'urban.schedule.licence_ended'
            if end_condition_ids and condition_id in end_condition_ids:
                old_end_conditions = task_cfg.end_conditions
                new_end_conditions = [c for c in old_end_conditions if c.condition != condition_id]
                task_cfg.end_conditions = tuple(new_end_conditions)
    logger.info("migration step done!")


def migrate_parcellings_folder_allowed_type(context):
    logger = logging.getLogger('migrate parcellings folder allowed type')
    logger.info("starting migration step")
    portal = api.portal.get()
    parcellings = portal.urban.parcellings
    setFolderAllowedTypes(parcellings, 'Parcelling')


def migrate_urbaneventtypes_folder(context):
    logger = logging.getLogger('migrate urbaneventtypes folder')
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool('portal_urban')
    for config_folder in urban_tool.get_all_licence_configs():
        if hasattr(aq_base(config_folder), 'urbaneventtypes'):
            eventconfigs = getattr(config_folder, 'urbaneventtypes')
            api.content.rename(obj=eventconfigs, new_id='eventconfigs', safe_id=False)
    logger.info("migration step done!")


def migrate_inquiry_parcels(context):
    logger = logging.getLogger('migrate inquiry parcels')
    logger.info("starting migration step")
    portal = api.portal.get()
    # to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    # disable catalog
    patches.apply()
    catalog = api.portal.get_tool('portal_catalog')
    cadastre = services.cadastre.new_session()
    for rec_brain in catalog(portal_type='RecipientCadastre'):
        recipient = rec_brain.getObject()
        parcels = recipient.objectValues()
        if parcels:
            parcel_ob = parcels[0]
            parcel = cadastre.query_parcel_by_capakey(parcel_ob.capakey)
            if parcel:
                recipient.setCapakey(parcel_ob.capakey)
                recipient.setParcel_street(parcel.locations and parcel.locations.values()[0]['street_name'] or '')
                recipient.setParcel_police_number(parcel.locations and parcel.locations.values()[0]['number'] or '')
                recipient.setParcel_nature(', '.join(parcel.natures))
            api.content.delete(objects=parcels)
            logger.info("migrated recipient {}".format(recipient))
    # restore catalog
    patches.unapply()
    # enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    logger.info("migration step done!")


def migrate_remove_prov_in_folderroadtypes(context):
    logger = logging.getLogger('migrate remove prov in folderroadtypes voc')
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool('portal_urban')
    for folderroadtype in urban_tool.folderroadtypes.objectValues():
        if folderroadtype.id == "prov":
            api.content.transition(obj=folderroadtype, to_state='disabled')
    logger.info("migration step done!")


def migrate_disable_natura2000_folderzone(context):
    logger = logging.getLogger('migrate disable natura2000 folderzone')
    logger.info("starting migration step")
    urban_tool = api.portal.get_tool('portal_urban')
    for folderzone in urban_tool.folderzones.objectValues():
        if folderzone.id == "znatura2000":
            api.content.transition(obj=folderzone, to_state='disabled')
    logger.info("migration step done!")


def migrate_inquiry_investigationStart_date(context):
    """
    investigationStart and investigationEnd are no longer optional fields
    """
    logger = logging.getLogger('migrate inquiry start/end date')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')
    eventtypes = [b.getObject() for b in
                  catalog(portal_type=['UrbanEventType', 'EventConfig'])]
    for eventtype in eventtypes:
        active_fields = eventtype.getActivatedFields()
        if 'investigationEnd' in active_fields or 'investigationStart' in active_fields:
            new_value = [f for f in active_fields if f not in ['investigationStart', 'investigationEnd']]
            eventtype.activatedFields = new_value
            logger.info("migrated inquiry config {}".format(eventtype))
    logger.info("migration step done!")


def migrate_flooding_level(context):
    """
    Migrate old text single value to tuple for multiselection for floodingLevel and locationFloodingLevel
    """
    logger = logging.getLogger('migrate flooding level to tuple type')
    logger.info("starting migration step")
    cat = api.portal.get_tool('portal_catalog')
    licence_brains = cat(object_provides=IGenericLicence.__identifier__)
    licences = [lic.getObject() for lic in licence_brains]
    for licence in licences:
        if licence.floodingLevel and isinstance(licence.floodingLevel, basestring):
            licence.setFloodingLevel((licence.floodingLevel,))
        if licence.locationFloodingLevel and isinstance(licence.locationFloodingLevel, basestring):
            licence.setLocationFloodingLevel((licence.locationFloodingLevel,))

    logger.info("migration step done!")


def migrate_announcement_schedule_config(context):
    """
    """
    logger = logging.getLogger('migrate announcement schedule config')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    for licence_config in portal_urban.objectValues('LicenceConfig'):
        schedule_cfg = getattr(licence_config, 'schedule', None)
        if schedule_cfg and hasattr(schedule_cfg, 'announcement-preparation'):
            announcement_prep_task = getattr(schedule_cfg, 'announcement-preparation')
            announcement_prep_task.creation_conditions = (
                MacroCreationConditionObject('urban.schedule.condition.will_have_announcement', 'AND'),
            )
            announcement_prep_task.end_conditions = (
                MacroEndConditionObject('urban.schedule.condition.announcement_dates_defined', 'AND'),
            )
            announcement_prep_task.activate_recurrency = True
            announcement_prep_task.recurrence_conditions = (
                MacroRecurrenceConditionObject('urban.schedule.condition.will_have_announcement', 'AND'),
            )
            announcement_done_task = getattr(schedule_cfg, 'announcement')
            announcement_done_task.creation_conditions = (
                MacroCreationConditionObject('urban.schedule.condition.announcement_dates_defined', 'AND'),
            )
            announcement_done_task.end_conditions = (
                MacroEndConditionObject('urban.schedule.condition.announcement_done', 'AND'),
            )
            announcement_done_task.activate_recurrency = True
            announcement_done_task.recurrence_conditions = (
                MacroRecurrenceConditionObject('urban.schedule.condition.announcement_dates_defined', 'AND'),
            )
    logger.info("migration step done!")


def migrate_styles_pod_templates(context):
    """
    """
    logger = logging.getLogger('migrate pod templates styles')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')
    podt_template_brains = catalog(object_provides=IConfigurablePODTemplate.__identifier__)
    # set style template to None on all POD templates
    for brain in podt_template_brains:
        pod_template = brain.getObject()
        pod_template.style_template = None
    # then delete all style templates
    style_templates = [b.getObject() for b in catalog(portal_type='StyleTemplate')]
    api.content.delete(objects=style_templates)
    logger.info("migration step done!")


def migrate_rich_texts(context):
    logger = logging.getLogger('migrate rich text fields')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')
    to_migrate_brains = catalog(
        object_provides=[ICODT_BaseBuildLicence.__identifier__, ICODT_UrbanCertificateBase.__identifier__]
    )
    for brain in to_migrate_brains:
        licence = brain.getObject()
        field = licence.getField('sdcDetails')
        raw_value = field.getRaw(licence)
        if not raw_value.startswith('<p>'):
            licence.setSdcDetails('<p>{}</p>'.format(raw_value))
            logger.info("migrated rich text of licence: {}".format(licence))

    logger.info("migration step done!")


def fix_missing_streets(context):
    logger = logging.getLogger('urban: migrate to 2.5')
    logger.info("starting migration steps")
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
    portal_urban = api.portal.get_tool('portal_urban')
    streets = portal_urban.streets
    missing_street = api.content.create(type='Street', id='manquant', container=streets.objectValues()[0])
    api.content.transition(missing_street, 'disable')
    for brain in licence_brains:
        licence = brain.getObject()
        address = licence.getWorkLocations()
        do_fix = False
        new_address = []
        for wl in address:
            street_brains = catalog(UID=wl['street'])
            if not street_brains:
                do_fix = True
                wl['street'] = missing_street.UID()
                new_address.append(wl)
            if do_fix:
                licence.setWorkLocations(new_address)
                licence.reindexObject(idxs=['StreetsUID'])
                logger.info('fixed street licence {}'.format(licence))


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.5')
    logger.info("starting migration steps")
    # disable task creation/update
    disable_schedule()
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'workflow')
    fix_missing_streets(context)
    migrate_urbaneventtypes_folder(context)
    # reinstall pm.wsclient registry to add new registry record.
    setup_tool.runImportStepFromProfile('profile-imio.pm.wsclient:default', 'content_type_registry')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runAllImportStepsFromProfile('profile-plonetheme.imioapps:urbanskin')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-update-rubrics')
    migrate_codt_buildlicences_schedule(context)
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-update-schedule')
    migrate_flooding_level(context)
    migrate_Env_Inquiry_to_CODT_UniquelicenceInquiry(context)
    migrate_CODT_NotaryLetter_to_CODT_UrbanCertificateBase(context)
    migrate_CODT_UrbanCertificateOne_to_CODT_UrbanCertificateBase(context)
    migrate_CODT_UrbanCertificateBase_add_permissions(context)
    migrate_opinion_request_TAL_expression(context)
    migrate_report_and_remove_urbandelay_portal_type(context)
    migrate_inquiry_investigationStart_date(context)
    migrate_parcellings_folder_allowed_type(context)
    migrate_default_states_to_close_tasks(context)
    migrate_inquiry_parcels(context)
    migrate_remove_prov_in_folderroadtypes(context)
    migrate_disable_natura2000_folderzone(context)
    migrate_announcement_schedule_config(context)
    migrate_styles_pod_templates(context)
    migrate_rich_texts(context)
    # Clearing iconified actions MUST be juste before the catalog reindex!!!
    clear_communesplone_iconifiedactions_layer(context)
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    logger.info("catalog rebuilt!")
    logger.info("refreshing reference catalog...")
    REQUEST = context.REQUEST
    ref_catalog = api.portal.get_tool('reference_catalog')
    ref_catalog.manage_catalogReindex(REQUEST, REQUEST.RESPONSE, REQUEST.URL)
    logger.info("migration done!")
