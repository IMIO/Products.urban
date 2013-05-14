# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
import logging

from Acquisition import aq_parent

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban118(context):
    """
     Launch every migration steps for the version 1.1.8
    """
    logger = logging.getLogger('urban: migrate to 1.1.8')
    logger.info("starting migration steps")
    # geometricians are now a portal_type of class Contact
    migrateGeometriciansMetaType(context)
    # we merge organisationRequest vocabulary terms into their linked UrbanEventType
    migrateOrganisationTerms(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


class GeometricianMetaTypeMigrator(object, InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "Geometrician"
    src_portal_type = "Geometrician"
    dst_meta_type = "Contact"
    dst_portal_type = "Geometrician"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrateGeometriciansMetaType(context):
    """
     Now, Geometrician class inherits from Contact class.
     We have to migrate geometrician objects meta_type.
    """
    logger = logging.getLogger('urban: migrate Geometricians meta_type ->')
    logger.info("starting migration step")

    migrator = GeometricianMetaTypeMigrator
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    geometricians_folder = portal.urban.geometricians
    folder_path = '/'.join(geometricians_folder.getPhysicalPath())
    walker = migrator.walker(portal, migrator, query={'path': folder_path}, callBefore=contentmigrationLogger, logger=logger, purl=portal.portal_url)
    walker.go()

    # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


class OrganisationTermMigrator(object, InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanEventType"
    src_portal_type = "UrbanEventType"
    dst_meta_type = "OpinionRequestEventType"
    dst_portal_type = "OpinionRequestEventType"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrateOrganisationTerms(context):
    """
    """
    logger = logging.getLogger('urban: migrate organisationTerm into OpinionRequestEventType ->')
    logger.info("starting migration step")

    migrator = OrganisationTermMigrator
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    catalog = getToolByName(portal, 'portal_catalog')
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    # gather the uids of the UrbanEventType to migrate, for this we just follow
    # the referenced UrbanEventType of each OrganisationTerm
    organisationterm_brains = catalog(portal_type='OrganisationTerm')
    organisationterms = [brain.getObject() for brain in organisationterm_brains]
    temp = []
    for term in organisationterms:
        linked_eventtype = term.getLinkedOpinionRequestEvent()
        if linked_eventtype:
            temp.append((term, linked_eventtype.UID()))
    uids_to_migrate = dict(temp).values()

    # Run the walker to migrate portal_type
    walker = migrator.walker(portal, migrator, query={'UID': uids_to_migrate}, callBefore=contentmigrationLogger, logger=logger, purl=portal.portal_url)
    walker.go()

    # update the new OpinionRequestEventType with the values of their old corresponding organistion term
    for term in organisationterms:
        event = term.getLinkedOpinionRequestEvent()
        if event:
            event.setDescription(term.Description())
            event.setExtraValue(term.Title())
            event.reindexObject()
            event_id = event.getId()
            if event_id.endswith('-opinion-request'):
                new_event_id = event_id.replace('-opinion-request', '')
                parent = aq_parent(event)
                try:
                    parent.manage_renameObject(event_id, new_event_id)
                except:
                    event.setTALCondition("python: here.mayAddOpinionRequestEvent('%s')" % event_id)
            logger.info("migrated UrbanEventType %s" % event.id)

    # set OpinionRequestEventType in the allowed_types of urbaneventtypes folders
    portal_urban = portal.portal_urban
    folder_path = '/'.join(portal_urban.getPhysicalPath())
    eventtypesfolder_brains = catalog(portal_type='Folder', id='urbaneventtypes', path={'query': folder_path, 'depth': 2})
    eventtypesfolders = [brain.getObject() for brain in eventtypesfolder_brains]
    for eventtypesfolder in eventtypesfolders:
        portal_types = ['UrbanEventType', 'OpinionRequestEventType']
        eventtypesfolder.setLocallyAllowedTypes(portal_types)
        eventtypesfolder.setImmediatelyAddableTypes(portal_types)
        logger.info("migrated urbaneventtypes config folder")

    # Eventually remove the foldermakers folder from urban config
    foldermaker_brains = catalog(portal_type='Folder', id='foldermakers', path={'query': folder_path, 'depth': 2})
    foldermakers = dict([(aq_parent(brain.getObject()), brain.id) for brain in foldermaker_brains])
    for parent_folder, foldermakers_id in foldermakers.iteritems():
        parent_folder.manage_delObjects(foldermakers_id)
        logger.info("removed %s foldermakers config folder" % parent_folder)

    # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")
