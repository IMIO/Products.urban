# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
import re

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

logger = logging.getLogger('urban: migrations')


def contentmigrationLogger(oldObject, **kwargs):
    """ Generic logger method to be used with CustomQueryWalker """
    kwargs['logger'].info('/'.join(kwargs['purl'].getRelativeContentPath(oldObject)))
    return True


def migrateToUrban117(context):
    """
     Launch every migration steps for the version 1.1.7
    """
    logger = logging.getLogger('urban: migrate to 1.1.7')
    logger.info("starting migration steps")
    #the method getCurrentFolderManager has changed
    # we have to migrate the tal expressions used for numerotation
    migrateNumerotationExpressions(context)
    # the default text of inquiry 'claimsText' field is now defined on the urbaneventtype
    migrateInquiryDefaultText(context)
    # specific feature vocabulary terms have their own type (SpecificFeatureTerm)
    migrateSpecificFeatureTerms(context)
    # licence_portal_type is now an AT field on the LicenceConfig schema
    migrateLicenceConfigPortalType(context)

    # finish with reinstalling urban and adding the templates
    logger.info("starting to reinstall urban...")
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    setup_tool.runImportStepFromProfile('profile-Products.urban:extra', 'urban-extraPostInstall')
    logger.info("reinstalling urban done!")
    logger.info("migration done!")


def migrateNumerotationExpressions(context):
    """
     adapt the way to call getCurrentFolderManager method in numerotation expressions
    """
    urban_tool = getToolByName(context, 'portal_urban')
    logger = logging.getLogger('urban: migrate numerotation expressions->')
    logger.info("starting migration step")

    configs = urban_tool.objectValues('LicenceConfig')
    regex = 'getCurrentFolderManager\\(.*?(obj\s*,?\s*).*?\\)'

    def adaptCall(matchobj):
        return matchobj.group(0).replace(matchobj.group(1), '')

    for config in configs:
        numerotation_expression = config.getReferenceTALExpression()
        new_expression = re.sub(regex, adaptCall, numerotation_expression)
        if new_expression != numerotation_expression:
            logger.info("Migrated tal expression of '%s' " % config.Title())
            config.setReferenceTALExpression(new_expression)

    logger.info("migration step done!")


def migrateInquiryDefaultText(context):
    """
     set a default value to the field 'claimsText' of urban event 'enquête-publique'
    """
    urban_tool = getToolByName(context, 'portal_urban')
    logger = logging.getLogger('urban: migrate default text of inquiry events ->')
    logger.info("starting migration step")

    default_text = [
        "<p>Considérant que xxx réclamations écrites ont été introduites au cours de l'enquête émanant des riverains (xxx lettres identiques et xxx lettres individuelles);</p>",
        "<p>Considérant que xxx réclamations orales ont été consignées dans le registre;</p>",
        "<p>Considérant que ces réclamations portent principalement sur :</p>",
        "<p>* ...</p>",
        "<p>* ...</p>",
        "<p>* ...</p>",
        "<p>Attendu qu'une réunion de clôture d'enquête à été organisée le xxx dans les bureaux du service de l'urbanisme de la Commune de Mons, conformément aux dispositions de l'article 340 du Code modifié;</p>",
        "<p>Considérant qu'aucune personnes ne s'est présentée lors de cette réunion pour faire opposition;</p>",
        "<p>Considérant que xxx personnes se sont présentées à cette réunion et ont émis les réclamations suivantes :</p>",
        "<p>* ...</p>",
        "<p>* ...</p>",
        "<p>* ...</p>",
    ]

    confignames = ['buildlicence', 'parceloutlicence', 'urbancertificatetwo']
    for configname in confignames:
        config = getattr(urban_tool, configname)
        eventtypes = config.urbaneventtypes
        inquiry_event = getattr(eventtypes, 'enquete-publique', None)
        if inquiry_event:
            logger.info("Migrated default text of %s inquiry" % configname)
            inquiry_event.setTextDefaultValues([{'text': '\n'.join(default_text), 'fieldname': 'claimsText'}])

    logger.info("migration step done!")


class UrbanVocabularyTermToSpecificFeatureTermMigrator(object, InplaceATFolderMigrator):
    """
     Migrate the UrbanEvent having an id of 'enquete-publique'
     to UrbanEventInquiries
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanVocabularyTerm"
    src_portal_type = "UrbanVocabularyTerm"
    dst_meta_type = "SpecificFeatureTerm"
    dst_portal_type = "SpecificFeatureTerm"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


def migrateSpecificFeatureTerms(context):
    """
     The voc used for the specific features has now its own type : SpecificFeatureTerm
     We have to migrate the UrbanVocabularyTerm used for the specific features to this new Type
    """
    urban_tool = getToolByName(context, 'portal_urban')
    logger = logging.getLogger('urban: migrate SpecificFeatureTerm ->')
    logger.info("starting migration step")

    migrator = UrbanVocabularyTermToSpecificFeatureTermMigrator
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    foldernames = ['specificfeatures', 'roadspecificfeatures', 'locationspecificfeatures', 'townshipspecificfeatures']
    licences = ['urbancertificateone', 'urbancertificatetwo', 'notaryletter']
    for licence_name in licences:
        licence_config = getattr(urban_tool, licence_name)
        for foldername in foldernames:
            folder = getattr(licence_config, foldername)
            # we have to change the allowed content types on this folder
            folder.setLocallyAllowedTypes('SpecificFeatureTerm')
            folder.setImmediatelyAddableTypes('SpecificFeatureTerm')
            folder_path = '/'.join(folder.getPhysicalPath())
            walker = migrator.walker(portal, migrator, query={'path': folder_path}, callBefore=contentmigrationLogger, logger=logger, purl=portal.portal_url)
            walker.go()
        # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
        walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("migration step done!")


def migrateLicenceConfigPortalType(context):
    """
     The field 'licence_portal_type' is now a real schema field rather than a normal class attribute
    """
    logger = logging.getLogger('urban: migrate SpecificFeatureTerm ->')
    logger.info("starting migration step")

    catalog = getToolByName(context, 'portal_catalog')
    licenceconfigs = catalog(portal_type='LicenceConfig')

    for brain in licenceconfigs:
        licenceconfig = brain.getObject()
        if hasattr(licenceconfig, 'licence_portal_type'):
            portal_type = licenceconfig.licence_portal_type
            licenceconfig.licencePortalType = portal_type
            delattr(licenceconfig, 'licence_portal_type')
            logger.info("Migrated licence_portal_type attr from licence config %s" % licenceconfig)

    logger.info("migration step done!")
