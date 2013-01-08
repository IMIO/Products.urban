# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')

def migrateToUrban116(context):
    """
     Launch every migration steps for the version 1.1.6
    """
    logger = logging.getLogger('urban: migrate to 1.1.6')
    logger.info("starting migration steps")
    # the environment declaration config has changed
    # the portal_type used has changed as well
    migrateEnvironmentDeclaration(context)
    # specificFeatures text is now editable
    migrateSpecificFeatures(context)
    # add extravalue 'Madame, Monsieur' to 'no value' title vocterm (or create it)
    migrateSocietyTitle(context)

    # finish with reinstalling urban and adding the templates
    logger.info("starting to reinstall urban...")
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:tests', 'urban-addTestObjects')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")

def migrateEnvironmentDeclaration(context):
    """
     rename the licence folder and config 'environmentaldeclaration' into 'envclassthree'
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')
    logger = logging.getLogger('urban: migrate to environmental declarations ->')
    logger.info("starting migration step")

    if hasattr(site.urban, 'environmentaldeclarations'):
        site.urban.manage_delObjects('environmentaldeclarations')
        logger.info("deleted old environmental declarations folder")
    if hasattr(urban_tool, 'environmentaldeclaration'):
        urban_tool.manage_renameObject(id='environmentaldeclaration',  new_id='envclassthree')
        logger.info("deleted old environmental declarations config folder")
    logger.info("migration step done!")

def migrateSpecificFeatures(context):
    """
     merge the content of the old 'detail' text zone with the specificFeature description text
     and put the result in the 'text' zone
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')
    logger = logging.getLogger('urban: migrate specific features ->')
    logger.info("starting migration step")

    catalog = getToolByName(site, 'portal_catalog')
    # gather all CU1, CU2 and notary letters
    portal_types = ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter']
    for portal_type in portal_types:
        licences_to_migrate = catalog(portal_type=portal_type)
        for brain in licences_to_migrate:
            licence = brain.getObject()
            for subtype in ['', 'location', 'road', 'township']:
                features_accessor = getattr(licence, 'get%sSpecificFeatures' % subtype.capitalize())
                specificfeatures = features_accessor()
                new_specificfeatures = []
                for spf in specificfeatures:
                    path = '%s/portal_urban/%s/%sspecificfeatures' % (site.absolute_url_path(), portal_type.lower(), subtype)
                    vocterm_brain = catalog(id=spf['id'], path=path)
                    vocterm = len(vocterm_brain) == 1 and vocterm_brain[0].getObject() or None
                    newtext = ''
                    if spf.has_key('detail'):
                        newtext = spf.pop('detail')
                        spf['value'] = spf['text']
                        logger.info("migrating %sSpecificFeature of licence %s" % (location, licence.Title()))
                    if vocterm:
                        newtext = '%s %s</p>' % (vocterm.Description()[:-4], newtext)
                    spf['text'] = newtext
                    new_specificfeatures.append(spf)
                features_mutator = getattr(licence, 'set%sSpecificFeatures' % subtype.capitalize())
                features_mutator(tuple(new_specificfeatures))
    logger.info("migration step done!")

def migrateSocietyTitle(context):
    """
     Migrate the vocterm value 'notitle' to add it the extraValue "Madame, Monsieur"
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')
    logger = logging.getLogger('urban: migrate society title ->')
    logger.info("starting migration step")

    titles_folder = urban_tool.persons_titles
    notitle_id = 'notitle'
    notitle_term = getattr(titles_folder, notitle_id, None)
    if notitle_term and not notitle_term.Title():
        notitle_term.setExtraValue('Madame, Monsieur')
        notitle_term.reindexObject()
        logger.info("migrated PersonTitleTerm 'notitle'")
    else:
        if notitle_term:
            notitle_id = 'society'
        notitle_id = titles_folder.invokeFactory('PersonTitleTerm', id=notitle_id, title=u'', extraValue='Madame, Monsieur', gender='male', multiplicity='single')
        notitle_term = getattr(urban_tool.persons_titles, notitle_id)
        notitle_term.processForm()
        titles_folder.moveObjectsToTop(notitle_id)
        notitle_term.reindexObject()
        logger.info("created a new PersonTitleTerm 'notitle'")
    logger.info("migration step done!")

