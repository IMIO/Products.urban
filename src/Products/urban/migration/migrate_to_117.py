# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
import re

logger = logging.getLogger('urban: migrations')


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
    logger = logging.getLogger('urban: migrate to environmental declarations ->')
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
    logger = logging.getLogger('urban: migrate to environmental declarations ->')
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
