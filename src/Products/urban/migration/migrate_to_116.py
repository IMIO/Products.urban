# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from Products.urban.config import URBAN_TYPES

logger = logging.getLogger('urban: migrations')

def migrateToUrban116(context):
    """
     Launch every migration steps for the version 1.1.6
    """
    # the environment declaration config has changed
    # the portal_type used has changed as well
    migrateEnvironmentDeclaration(context)
    # specificFeatures text is now editable
    migrateSpecificFeatures(context)

    # finish with reinstalling urban and adding the templates
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:tests', 'urban-addTestObjects')

def migrateEnvironmentDeclaration(context):
    """
     rename the licence folder and config 'environmentaldeclaration' into 'envclassthree'
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')

    site.urban.manage_delObjects('environmentaldeclarations')
    urban_tool.manage_renameObject(id='environmentaldeclaration',  new_id='envclassthree')

def migrateSpecificFeatures(context):
    """
     merge the content of the old 'detail' text zone with the specificFeature description text
     and put the result in the 'text' zone
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_tool = getToolByName(site, 'portal_urban')

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
                for spf in specificfeatures:
                    path = '%s/portal_urban/%s' % (site.absolute_url_path(), portal_type.lower())
                    vocterm_brain = catalog(id=spf['id'], path=path)
                    vocterm = len(vocterm_brain) == 1 and vocterm_brain[0].getObject() or None
                    newtext = ''
                    if spf.has_key('detail'):
                        newtext = spf.pop('detail')
                        spf['value'] = spf['text']
                    if vocterm:
                        newtext = '%s %s</p>' % (vocterm.Description()[:-4], newtext)
                    spf['text'] = newtext


