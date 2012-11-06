# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')

def migrateToUrban114(context):
    """
     Launch every migration steps for the version 1.1.4
    """
    if isNoturbanMigrationsProfile(context): return

    #add the role 'contributor' to the urban_editors group
    migrateUrbanEditorRoles(context)
    #change voc terms used for the CU1 CU2 and notary letter specific features
    migrateVocabularyTermsOfCUSpecificFeatures(context)
    #workType field is now multivalued, string values should be put into a tuple
    migrateWorkTypes(context)

def migrateUrbanEditorRoles(context):
    """
     the group urban_editor should have the role 'Contributor' to be able to generate singleton documents
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    app_folder = getattr(site, "urban")
    for foldername in ['buildlicences', 'parceloutlicences', 'declarations', 'divisions', 'urbancertificateones', 'urbancertificatetwos', 'notaryletters', 'environmentaldeclarations', 'miscdemands', 'architects', 'geometricians', 'notaries']:
        if hasattr(app_folder, foldername):
            folder = getattr(app_folder, foldername)
            roles = dict(folder.get_local_roles())
            if roles.has_key('urban_editors') and not 'Contributor' in roles['urban_editors']:
                ex_roles = list(roles['urban_editors'])
                ex_roles.append("Contributor")
                folder.manage_setLocalRoles('urban_editors', ex_roles)
                folder.reindexObject()
                logger.info("Added locally contributor role to urban_editors group on folder '%s'"%foldername)

def migrateVocabularyTermsOfCUSpecificFeatures(context):
    """
     Changes in getValueForTemplate method
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urbancfg = site.portal_urban
    vocterms_ids = {
            'plan-communal-ammenagement':"<p>est situé en [[python: object.getValueForTemplate('folderZone')]] dans le périmètre du plan communal d'aménagement [[python: object.getValueForTemplate('pca', subfield='label')]] approuvé par [[python: object.getValueForTemplate('pca', subfield='decreeType')]] du [[python: '/'.join(object.getValueForTemplate('pca', subfield='decreeDate').split()[0].split('/')[::-1]) ]] et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
            'plan-communal-ammenagement-revision':"<p>est situé en [[python: object.getValueForTemplate('folderZone')]] dans le périmètre du projet - de révision du - de - plan communal d'aménagement [[python: object.getValueForTemplate('pca', subfield='label')]] approuvé par [[python: object.getValueForTemplate('pca', subfield='decreeType')]] du [[python: '/'.join(object.getValueForTemplate('pca', subfield='decreeDate').split()[0].split('/')[::-1]) ]];</p>",
            'perimetre-lotissement':"<p>est situé sur le(s) lot(s) n° [[python: object.getValueForTemplate('subdivisionDetails')]] dans le périmètre du lotissement [[python: object.getValueForTemplate('parcellings', subfield='label')]]non périmé autorisé du [[python: '/'.join(object.getValueForTemplate('parcellings', subfield='authorizationDate').split()[0].split('/')[::-1]) ]];</p>",
            'ssc':"<p> est situé en [[python: object.getValueForTemplate('SSC')]] au schéma de structure communal adopté par [[python: object.getValueForTemplate('SSC', subfield='extraValue') ]];</p>",
            'ssc-revision':"<p> est situé en [[python: object.getValueForTemplate('SSC')]] au projet de - révision du - de - schéma de structure communal adopté par [[python: object.getValueForTemplate('SSC', subfield='extraValue') ]];</p>",
            'rcu':"<p>est situé sur le territoire ou la partie du territoire communal où le règlement régional d'urbanisme [[python: object.getValueForTemplate('folderZone') ]] est applicable;</p>",
            'rcu-approuve':"<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé par [[python: object.getValueForTemplate('RCU', subfield='extraValue')]] est applicable;</p>",
            'rcu-revision':"<p>est situé sur le territoire ou la partie du territoire communal visé(e) par le projet - de révision du - de - règlement communal d'urbanisme approuvé par [[python: object.getValueForTemplate('RCU', subfield='extraValue')]] est applicable;</p>",
            'rcu-approuve-provisoirement':"<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé provisoirement par [[python: ', '.join(object.getValuesForTemplate('RCU', subfield='extraValue')) ]] est applicable;</p>",
            }

    for licence_type in ['urbancertificateone', 'urbancertificatetwo', 'notaryletter']:
        configfolder = getattr(urbancfg, licence_type)
        for vocfolder in ['specificfeatures', 'locationspecificfeatures']:
            if hasattr(configfolder, vocfolder):
                folder = getattr(configfolder, vocfolder)
                for id_key, replacement_text in vocterms_ids.iteritems():
                    if hasattr(folder, id_key):
                        getattr(folder, id_key).setDescription(replacement_text)
                        logger.info("Set new description in folder '%s: %s', on term '%s'"%(licence_type, vocfolder, id_key))


def migrateWorkTypes(context):
    """
    Make sure the value(s) of the field workType are in a list
    """
    if isNoturbanMigrationsProfile(context): return

    site = getToolByName(context, 'portal_url').getPortalObject()
    catalog = site.portal_catalog
    brains = catalog(portal_type=URBAN_TYPES)
    for brain in brains:
        licence = brain.getObject()
        if licence.getField('workType'):
            old_val = licence.getWorkType()
            if old_val and len(old_val) == len([val for val in old_val if len(val) == 1]):
                logger.info("Corrected workType for %s"%licence.absolute_url())
                licence.setWorkType(''.join(licence.getWorkType()))
