# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')

def migrateToUrban115(context):
    """
     Launch every migration steps for the version 1.1.5
    """
    # now use the extravalue of the person Titles to distinguish the title use to adress a contact
    # from the one used in the contact signaletic
    migratePersonTitles(context)
    # The key dates displayed on the each licence summary are now configurable rather than hard-coded.
    # This step turns some urbanEventTypes as keyEvent and select their key dates to keep the same dates
    # displayed as before the change
    migrateKeyDates(context)
    # The parcellings folder has been moved from './portal_urban' to './urban'
    # the notaries , geometricians and architects folders views are now a browserview
    migrateParcellingsFolder(context)
    #PEB categories are now configurable, this step creates the folder configs with some vocabulary
    migratePEBCategories(context)
    #numerotation and reference TAL expression is now specific to each licence type
    migrateReferenceNumerotation(context)
    # the fields specificFeature and specificFeaturesDetail of CU1, CU2, NotaryLetter are now merged
    migrateSpecificFeatures(context)
    # the css file needed for the street autocomplete cannot be merged an cached else the autocomplete is broken
     migrateAutocompleteCSS(context)

def migratePersonTitles(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')
    for persontitle in urban_tool.persons_titles.objectValues():
        if not persontitle.extraValue:
            persontitle.extraValue = persontitle.Title()
            logger.info("Migrated personTitleTerm '%s'" % persontitle.Title())

def migrateKeyDates(context):
    """
    set some eventType as keyEvent and set their eventDate as keyDate
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_urban = getToolByName(site, 'portal_urban')
    # browse trough all the configs of all the licences, turn some UrbanEventType into key Events
    # and select some key dates
    to_migrate = {
            'buildlicence':[
                'depot-de-la-demande',
                'dossier-incomplet',
                'accuse-de-reception',
                'transmis-1er-dossier-rw',
                'rapport-du-college',
                'delivrance-du-permis-octroi-ou-refus',
                ],
            'declaration':[
                'depot-de-la-demande',
                'deliberation-college',
                'transmis-decision',
                ],
            'urbancertificateone':[
                'depot-de-la-demande',
                'octroi-cu1',
                ],
            'urbancertificatetwo':[
                'depot-de-la-demande',
                'octroi-cu2',
                ],
            'division':[
                'depot-de-la-demande',
                'decision-octroi-refus',
                ],
            'notaryletter':[
                'depot-de-la-demande',
                'octroi-lettre-notaire',
                ],
            'miscdemand':[
                'depot-de-la-demande',
                'deliberation-college',
                'transmis-decision',
                ],
            'parceloutlicence':[
                'depot-de-la-demande',
                'dossier-incomplet',
                'accuse-de-reception',
                'transmis-1er-dossier-rw',
                'rapport-du-college',
                'delivrance-du-permis-octroi-ou-refus',
                ],
           }
    for configname, eventtypes in to_migrate.iteritems():
        config = getattr(getattr(portal_urban, configname), 'urbaneventtypes')
        for event_id in eventtypes:
            if hasattr(config, event_id):
                eventtype = getattr(config, event_id)
                eventtype.setIsKeyEvent(True)
                eventtype.setKeyDates(('eventDate',))
                logger.info("Migrated key date on  urbanEventType '%s'" % eventtype.Title())
            else:
                logger.info("Could not find urbanEventType '%s'" % eventtype.Title())

def migrateParcellingsFolder(context):
    """
    cut and paste the folder parcellings from './portal_urban' to './urban'
    change the layout name of the notaries, geometricians, architects and parcellings folders
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_urban = getToolByName(site, 'portal_urban')

    if not hasattr(portal_urban, 'parcellings'): return
    if hasattr(site.urban, 'parcellings'):
        site.urban.manage_delObjects(['parcellings'])
    cut_data = portal_urban.manage_cutObjects(['parcellings',])
    site.urban.manage_pasteObjects(cut_data)

    for foldername in ['notaries', 'architects', 'geometricians', 'parcellings']:
        folder = getattr(site.urban, foldername)
        folder.setLayout('%s_folderview' % foldername)
    logger.info("Migrated parcellings")

def migratePEBCategories(context):
    """
    Create pebcategories folders and their default values in buildlicence and parceloutlicence configs
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_urban = getToolByName(site, 'portal_urban')
    from Products.urban.setuphandlers import addPEBCategories
    for config_name in ['buildlicence',]:
        config = getattr(portal_urban, config_name)
        addPEBCategories(context, config)
    logger.info("Migrated PEB categories")

def migrateReferenceNumerotation(context):
    """
    Copy each numerotation value found on portal_urban to the 'numerotation' field on each licence folder.
    Copy the numerotationTALExpression value of portal_urban to the referenceTALExpression field
    of each licence config.
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_urban = getToolByName(site, 'portal_urban')
    for licence_type in [pt for pt in  URBAN_TYPES if pt != 'EnvClassThree']:
        config = getattr(portal_urban, licence_type.lower())
        if hasattr(portal_urban, 'numerotationTALExpression'):
            config.setReferenceTALExpression(portal_urban.numerotationTALExpression)
        if hasattr(portal_urban, '%sNumerotation' % licence_type):
            config.setNumerotation(getattr(portal_urban, '%sNumerotation' % licence_type))
            delattr(portal_urban, '%sNumerotation' % licence_type)
    if hasattr(portal_urban, 'numerotationTALExpression'):
        delattr(portal_urban, 'numerotationTALExpression')
    logger.info("Migrated numerotation")

def migrateSpecificFeatures(context):
    """
    Migrate old fields xxxSpecificFeatures and xxxSpecificFeaturesDetails from CU1, CU2 and notary letters into one field
    """
    for portal_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter']:
        # gather all the folders to migrate
        catalog = getToolByName(context, 'portal_catalog')
        licence_brains = catalog(portal_type=portal_type)
        for brain in licence_brains:
            licence = brain.getObject()
            logger.info("Migrate specificFeatures of licence: '%s'" % licence.Title())
            for subtype in ['', 'township', 'location', 'road']:
                # generate the default values from the config (getFixedRows...)
                defaultrows_method =  'get%sFeaturesRows' % (subtype and subtype.capitalize() or 'Specific')
                default_rows = [row.initialData for row in getattr(licence, defaultrows_method)()]
                # get the old values from the old field and the detail field
                old_specificFeatures = getattr(licence, '%s%specificFeatures' % (subtype, subtype and 'S' or 's'))
                detail = None
                if hasattr(licence, '%s%specificFeaturesDetail' % (subtype, subtype and 'S' or 's')):
                    detail = getattr(licence, '%s%specificFeaturesDetail' % (subtype, subtype and 'S' or 's'))
                # modify these rows accordingly to the old values found
                #import ipdb; ipdb.set_trace()
                for index, row in enumerate(default_rows):
                    if row['id'] in old_specificFeatures:
                        row['check'] = '1'
                    try:
                        row['detail'] = detail[index]['detail']
                    except:
                        pass
                getattr(licence, 'set%sSpecificFeatures' % subtype.capitalize())(default_rows)
                # delete detail field
                if hasattr(licence, '%s%specificFeaturesDetail' % (subtype, subtype and 'S' or 's')):
                    delattr(licence, '%s%specificFeaturesDetail' % (subtype, subtype and 'S' or 's'))
    logger.info("Migrated specificFeatures")

def migrateAutocompleteCSS(context):
     """
     For now theres a bug in the autocomplete product: it broke when its css file is cached and merged
     This step make sure that this css ressource is kept non-cached and non-merged
     """
     site = context.getSite()
     portal_css = getToolByName(site, 'portal_css')
     style_sheet = portal_css.getResource('++resource++jquery-ui-autocomplete.theme/jquery.ui.all.css')
     style_sheet.setCookable(False)
     style_sheet.setCacheable(False)
     logger.info("Migrated worklocation autocomplete stylesheet")

