# encoding: utf-8

from plone import api
from plone.portlets.constants import CONTEXT_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IInquiry
from Products.urban.interfaces import IUrbanCertificateBase
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor

import logging

logger = logging.getLogger('urban: migrations')


def migrate_inquiry_tabs():
    logger = logging.getLogger('urban: disable old investigation_and_advices tab from licence configs')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        old_tabs = licence_config.getTabsConfig()
        tab_ids = [t['value'] for t in old_tabs]
        if 'investigation_and_advices' in tab_ids:
            new_tabs = tuple([t for t in old_tabs if t['value'] != 'investigation_and_advices'])
            licence_config.setTabsConfig(new_tabs)

    logger.info("migration step done!")


def migrate_inquiry_eventtype():
    logger = logging.getLogger('urban: migrate inquiry event type')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues():
            if 'enquete-publique' in event_type.id:
                event_type.setEventPortalType('UrbanEventInquiry')
                old_fields = event_type.getActivatedFields()
                new_fields = list(old_fields)
                if 'investigationStart' not in old_fields:
                    new_fields = ['investigationStart', 'investigationEnd'] + list(old_fields)
                if 'explanationsDate' in old_fields:
                    index = new_fields.index('explanationsDate')
                    new_fields[index] = 'explanationStartSDate'
                event_type.setActivatedFields(new_fields)

    logger.info("migration step done!")


def migrate_inquiry_explanationsdate_field():
    logger = logging.getLogger('urban: migrate inquiry explanationsDate to explanationStartSDate')
    logger.info("starting migration step")
    cat = api.portal.get_tool('portal_catalog')
    licence_brains = cat(object_provides=IInquiry.__identifier__)
    licences = [l.getObject() for l in licence_brains if IGenericLicence.providedBy(l.getObject())]
    for licence in licences:
        event_inquiries = [o for o in licence.objectValues() if o.portal_type == 'UrbanEventInquiry']
        for inquiry in event_inquiries:
            if hasattr(inquiry, 'explanationsDate'):
                inquiry.explanationStartSDate = inquiry.explanationsDate
                delattr(inquiry, 'explanationsDate')
    logger.info("migration step done!")


def migrate_opinionrequest_eventtype():
    logger = logging.getLogger('urban: migrate opinion request event type')
    logger.info("starting migration step")
    portal_urban = api.portal.get_tool('portal_urban')
    licence_configs = portal_urban.objectValues('LicenceConfig')
    for licence_config in licence_configs:
        eventtype_folder = licence_config.urbaneventtypes
        for event_type in eventtype_folder.objectValues('OpinionRequestEventType'):
            event_type.setEventPortalType('UrbanEventOpinionRequest')

    logger.info("migration step done!")


def block_urban_parent_portlets():
    logger = logging.getLogger('urban: block urban folder portlets')
    logger.info("starting migration step")
    portal = api.portal.get()
    urban_folder = portal.urban
    for manager_name, src_manager in getUtilitiesFor(IPortletManager, context=urban_folder):
        assignment_manager = getMultiAdapter(
            (urban_folder, src_manager),
            ILocalPortletAssignmentManager
        )
        assignment_manager.setBlacklistStatus(CONTEXT_CATEGORY, True)
        for category in (GROUP_CATEGORY, CONTENT_TYPE_CATEGORY):
            assignment_manager.setBlacklistStatus(
                category,
                assignment_manager.getBlacklistStatus(category)
            )
    logger.info("migration step done!")


def migrate_python_expression_of_specificfeatures():
    logger = logging.getLogger('urban: sepficic features python expressions')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')

    voc_term_brains = catalog(portal_type='SpecificFeatureTerm')
    for brain in voc_term_brains:
        voc_term = brain.getObject()
        if '[[python: ' in voc_term.description():
            new_description = voc_term.description().replace('[[python: ', '[[')
            voc_term.setDescription(new_description)
            voc_term.reindexObject()

    field_ids = [
        'specificFeatures',
        'roadSpecificFeatures',
        'locationSpecificFeatures',
        'townshipSpecificFeatures'
    ]
    licence_brains = catalog(object_provides=IUrbanCertificateBase.__identifier__)
    for brain in licence_brains:
        licence = brain.getObject()
        for field_id in field_ids:
            specificfeature_field = licence.getField(field_id)
            field_value = specificfeature_field.get(licence)
            new_field_value = []
            for row in field_value:
                new_text = row['text'].replace('[[python: ', '[[')
                row['text'] = new_text
                new_field_value.append(row)
            specificfeature_field.set(licence, new_field_value)
        logger.info("migrated licence {} {}".format(licence.id, licence.Title()))

    logger.info("migration step done!")


def migrate_map_layers():
    logger = logging.getLogger('urban: sepficic features python expressions')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')

    layer_brains = catalog(portal_type='Layer')
    for brain in layer_brains:
        layer = brain.getObject()
        layer.setWMSUrl('http://geoserver1.communesplone.be/geoserver/gwc/service/wms')

    logger.info("migration step done!")


def migrate_collection_all_licences_add_codt_licence():
    logger = logging.getLogger('urban: specific features python expressions')
    logger.info("starting migration step")
    containerCollection = api.content.get(path='/urban/collection_all_licences')
    if 'CODT_BuildLicence' not in containerCollection.query[0]['v']:
        containerCollection.query[0]['v'].append('CODT_BuildLicence')
    logger.info("migration step done!")


def activate_faceted_navigation_on_licence():
    """
    """
    logger = logging.getLogger('urban: activate faceted navigation on licence')
    logger.info("starting migration step")
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)

    for licence_brain in licence_brains:
        licence = licence_brain.getObject()

        if IFacetedNavigable.providedBy(licence):
            return
        elif IPossibleFacetedNavigable.providedBy(licence):
            subtyper = licence.unrestrictedTraverse('@@faceted_subtyper')
            subtyper.enable()
            IFacetedLayout(licence).update_layout('list_tasks')
            licence.manage_delProperties(['layout'])
    logger.info("migration step done!")


def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.2')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-imio.schedule:default')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    block_urban_parent_portlets()
    migrate_inquiry_tabs()
    migrate_inquiry_eventtype()
    migrate_inquiry_explanationsdate_field()
    migrate_opinionrequest_eventtype()
    migrate_python_expression_of_specificfeatures()
    migrate_map_layers()
    migrate_collection_all_licences_add_codt_licence()
    activate_faceted_navigation_on_licence()
    logger.info("migration done!")
