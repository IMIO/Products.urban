# -*- coding: utf-8 -*-

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from Products.urban.config import GLOBAL_TEMPLATES
from Products.urban.interfaces import IPortionOut
from Products.urban.interfaces import IUrbanDoc
from Products.urban.profiles.extra.config_default_values import default_values

from plone import api
from plone.namedfile.file import NamedBlobFile

from zope.event import notify
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectCreatedEvent

import logging

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban1110(context):
    """
     Launch every migration steps for the version 1.11.0
    """
    logger = logging.getLogger('urban: migrate to 1.11.0')
    logger.info("starting migration steps")
    #  migrate UrbanDoc to File type with an IUrbanDoc marker interface on it.
    migrateGeneratedUrbanDocToATFile(context)
    migrateUrbanDocToSubTemplate(context)
    migrateUrbanDocToStyleTemplate(context)
    migrateUrbanDocToUrbantemplate(context)
    migratePersonTitleTerm(context)
    migratePortionOut(context)

    logger.info("starting to reinstall urban...")  # finish with reinstalling urban and adding the templates
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


class UrbanDocToATFileMigrator(InplaceATFolderMigrator):
    """
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanDoc"
    src_portal_type = "UrbanDoc"
    dst_meta_type = "ATBlob"
    dst_portal_type = "File"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)

    def custom(self):
        """ set IUrbanDoc interface on migrated File"""
        alsoProvides(self.new, IUrbanDoc)


def migrateGeneratedUrbanDocToATFile(context):
    """
    UrbanDoc type is now File.
    """
    logger = logging.getLogger('urban: migrate Generated UrbanDoc to ATFile type ->')
    logger.info("starting migration step")

    migrator = UrbanDocToATFileMigrator
    portal = api.portal.get()
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    folder_path = '/'.join(portal.urban.getPhysicalPath())
    walker = migrator.walker(
        portal,
        migrator,
        query={'path': folder_path},
        callBefore=contentmigrationLogger,
        logger=logger,
        purl=portal.portal_url
    )
    walker.go()

    # we need to reset the class variable to avoid using current query in
    # next use of CustomQueryWalker
    walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


def migrateUrbanDocToSubTemplate(context):
    """
    UrbanDoc global templates are now SubTemplate.
    """
    logger = logging.getLogger('urban: migrate UrbanDoc global templates to SubTemplate type ->')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    globaltemplates = portal_urban.globaltemplates

    for folder in globaltemplates.objectValues('ATFolder'):
        folder.setConstrainTypesMode(1)
        folder.setLocallyAllowedTypes(['SubTemplate', 'StyleTemplate'])
        folder.setImmediatelyAddableTypes(['SubTemplate', 'StyleTemplate'])

        for urbandoc in folder.objectValues('UrbanDoc'):
            template_blob = urbandoc.getFile()
            template_id = urbandoc.id
            template_title = [t.get('title') for t in GLOBAL_TEMPLATES[folder.id] if t.get('id') == template_id]
            template_title = template_title and template_title[0] or urbandoc.Title()
            urban_template_args = {
                'type': 'SubTemplate',
                'id': template_id,
                'odt_file': NamedBlobFile(
                    data=template_blob.data,
                    contentType=template_blob.getContentType(),
                    filename=template_blob.getFilename().decode('utf-8'),
                ),
                'title': template_title,
                'container': folder,
            }
            api.content.delete(urbandoc)
            api.content.create(**urban_template_args)
            logger.info(
                '{config} {template}'.format(
                    config=folder.Title(),
                    template=template_id
                )
            )

    logger.info("migration step done!")


def migrateUrbanDocToStyleTemplate(context):
    """
    UrbanDoc style templates are now StyleTemplate.
    """
    logger = logging.getLogger('urban: migrate UrbanDoc style template to SubTemplate type ->')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    globaltemplates = portal_urban.globaltemplates

    styles_id = 'styles.odt'
    if styles_id in globaltemplates.objectIds():
        old_styles = globaltemplates.get(styles_id)
        style_blob = old_styles.getFile()

        for folder in globaltemplates.objectValues('ATFolder'):
            folder.setConstrainTypesMode(1)
            folder.setLocallyAllowedTypes(['SubTemplate', 'StyleTemplate'])
            folder.setImmediatelyAddableTypes(['SubTemplate', 'StyleTemplate'])

            style_title = GLOBAL_TEMPLATES[folder.id][4]['title']
            urban_style_args = {
                'type': 'StyleTemplate',
                'id': styles_id,
                'odt_file': NamedBlobFile(
                    data=style_blob.data,
                    contentType=style_blob.getContentType(),
                    filename=style_blob.getFilename().decode('utf-8'),
                ),
                'title': style_title,
                'container': folder,
            }
            api.content.create(**urban_style_args)
            logger.info(
                '{config} {template}'.format(
                    config=folder.Title(),
                    template=style_title
                )
            )

        api.content.delete(old_styles)

    logger.info("migration step done!")


def migrateUrbanDocToUrbantemplate(context):
    """
    UrbanDoc templates are now UrbanTemplate.
    """
    logger = logging.getLogger('urban: migrate UrbanDoc templates to UrbanTemplate type ->')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    catalog = api.portal.get_tool('portal_catalog')
    licence_configs = [brain.getObject() for brain in catalog(portal_type='LicenceConfig')]

    for config in licence_configs:
        events_folder = config.urbaneventtypes
        environment_config = ['envclassone', 'envclasstwo', 'envclassthree']
        globaltemplates_id = config.id in environment_config and 'environmenttemplates' or 'urbantemplates'
        globaltemplates = getattr(portal_urban.globaltemplates, globaltemplates_id)

        style_template = getattr(globaltemplates, 'styles.odt').UID()
        subtemplates = []
        for subtemplate in globaltemplates.listFolderContents({'portal_type': 'SubTemplate'}):
            subtemplate_name = subtemplate.id.split('.')[0]
            line = {'pod_context_name': subtemplate_name, 'template': subtemplate.UID()}
            subtemplates.append(line)

        for eventtype in events_folder.objectValues():
            for urbandoc in eventtype.objectValues('UrbanDoc'):
                template_blob = urbandoc.getFile()
                template_id = urbandoc.id
                urban_template_args = {
                    'type': 'UrbanTemplate',
                    'id':  template_id,
                    'odt_file': NamedBlobFile(
                        data=template_blob.data,
                        contentType=template_blob.getContentType(),
                        filename=template_blob.getFilename().decode('utf-8'),
                    ),
                    'title': urbandoc.Title(),
                    'pod_portal_type': 'UrbanEvent',
                    'style_template': style_template,
                    'merge_templates': subtemplates,
                    'container': eventtype,
                }
                api.content.delete(urbandoc)
                api.content.create(**urban_template_args)
                logger.info(
                    '{config} {template}'.format(
                        config=config.Title(),
                        template=template_id
                    )
                )

    logger.info("migration step done!")


def migratePersonTitleTerm(context):
    """
    toggle value from extraValue to reverseTitle
    """
    logger = logging.getLogger('urban: migrate personTitleTerm')
    logger.info("starting migration step")

    portal_urban = api.portal.get_tool('portal_urban')
    personsTitleTerms = portal_urban.persons_titles.objectValues()

    for personsTitleTerm in personsTitleTerms:
        personsTitleTerm.reverseTitle = getReverseTitleValue(context, personsTitleTerm.id)

    logger.info("migration step done!")


def getReverseTitleValue(context, id):
    """
    Get reverseTitle from config
    """
    vocabularies = default_values['global']
    persons_titles = vocabularies['persons_titles']
    for persons_title in persons_titles[1:]:
        if persons_title['id'] == id:
            return persons_title['reverseTitle']
    return ''


def migratePortionOut(context):
    """
    Mark portion
    """
    logger = logging.getLogger('urban: migrate PortionOut')
    logger.info("starting migration step")

    catalog = api.portal.get_tool('portal_catalog')
    portionout_brains = catalog(object_provides=IPortionOut.__identifier__)
    for brain in portionout_brains:
        portion_out = brain.getObject()
        notify(ObjectCreatedEvent(portion_out))
        logger.info(
            '{licence} {portion_out}'.format(
                licence=portion_out.aq_parent.Title(),
                portion_out=portion_out.Title()
            )
        )

    logger.info("migration step done!")
