# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2013 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('urban: setuphandlers')
from Products.urban.config import DEPENDENCIES
from Products.CMFCore.utils import getToolByName
##code-section HEAD
from Acquisition import aq_base
from Products.CMFPlone.utils import base_hasattr
from Products.urban.config import TOPIC_TYPE
from Products.urban.config import DefaultTexts
from zExceptions import BadRequest
from Products.urban.config import URBAN_TYPES
from Products.urban.interfaces import ILicenceContainer
from zope.interface import alsoProvides
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope import event
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import EditBegunEvent
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from exportimport import updateAllUrbanTemplates
from Products.urban.utils import generatePassword
from datetime import date
##/code-section HEAD


def isNoturbanProfile(context):
    return context.readDataFile("urban_marker.txt") is None


def setupHideToolsFromNavigation(context):
    """
     hide tools
    """
    if isNoturbanProfile(context):
        return

    # uncatalog tools
    site = context.getSite()
    toolnames = ['portal_urban']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                site[toolname].unindexObject()
            except:
                pass
            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code

    if isNoturbanProfile(context):
        return

    corePostInstall(context, refresh=False)
    extraPostInstall(context, refresh=False)
    site = context.getSite()
    #refresh catalog after all these objects have been added...
    logger.info("Refresh portal_catalog : starting...")
    site.portal_catalog.refreshCatalog(clear=True)
    logger.info("Refresh portal_catalog : Done!")


def corePostInstall(context, refresh=True):
    # all installation custom code required for tests
    if isNoturbanProfile(context):
        return

    site = context.getSite()
    #we need external edition so make sure it is activated
    site.portal_properties.site_properties.manage_changeProperties(ext_editor=True)
    site.portal_memberdata.manage_changeProperties(ext_editor=True)
    site.portal_properties.site_properties.manage_changeProperties(typesUseViewActionInListings=('Image', 'File', 'UrbanDoc'))
    #for collective.externaleditor
    try:
        from collective.externaleditor.browser.controlpanel import IExternalEditorSchema
        control_panel_adapter_obj = IExternalEditorSchema(site)
        control_panel_adapter_obj.ext_editor = True
        if not 'UrbanDoc' in control_panel_adapter_obj.externaleditor_enabled_types:
            control_panel_adapter_obj.externaleditor_enabled_types.append('UrbanDoc')
    except:
        pass

    #install dependencies manually...
    quick_installer = site.portal_quickinstaller
    for dependency in DEPENDENCIES:
        if not dependency in quick_installer.listInstalledProducts():
            quick_installer.installProduct(dependency)

    #add our own portal_types to portal_factory
    factory_tool = getToolByName(site, "portal_factory")
    alreadyRegTypes = factory_tool.getFactoryTypes()
    typesToRegister = {
        'Architect': 1,
        'UrbanCertificateOne': 1,
        'UrbanCertificateTwo': 1,
        'EnvClassThree': 1,
        'NotaryLetter': 1,
        'Notary': 1,
        'Proprietary': 1,
        'Applicant': 1,
        'Claimant': 1,
    }
    alreadyRegTypes.update(typesToRegister)
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=alreadyRegTypes)

    #to be removed after deletion of class Architect
    architect_type = site.portal_types.Architect
    architect_type.content_meta_type = "Contact"
    architect_type.factory = "addContact"

    logger.info("setUrbanConfigWFPolicy : starting...")
    setUrbanConfigWFPolicy(context)
    logger.info("setUrbanConfigWFPolicy : Done")
    logger.info("addApplicationFolders : starting...")
    addApplicationFolders(context)
    logger.info("addApplicationFolders : Done")
    logger.info("setDefaultApplicationSecurity : starting...")
    setDefaultApplicationSecurity(context)
    logger.info("setDefaultApplicationSecurity : Done")
    logger.info("addUrbanGroups : starting...")
    addUrbanGroups(context)
    logger.info("addUrbanGroups : Done")
    logger.info("adaptDefaultPortal : starting...")
    adaptDefaultPortal(context)
    logger.info("adaptDefaultPortal : Done")
    #install the urbanskin if available
    logger.info("installUrbanskin : starting...")
    installUrbanskin(context)
    logger.info("installUrbanskin : Done")
    if refresh:
        #refresh catalog after all these objects have been added...
        logger.info("Refresh portal_catalog : starting...")
        site.portal_catalog.refreshCatalog(clear=True)
        logger.info("Refresh portal_catalog : Done!")


def extraPostInstall(context, refresh=True):
    # all installation custom code not required for tests
    if context.readDataFile('urban_extra_marker.txt') is None:
        return

    site = context.getSite()
    logger.info("addGlobalFolders : starting...")
    addGlobalFolders(context)
    logger.info("addGlobalFolders : Done")
    logger.info("addUrbanConfigs : starting...")
    addUrbanConfigs(context)
    logger.info("addUrbanConfigs : Done")
    logger.info("addDefaultObjects : starting...")
    addDefaultObjects(context)
    logger.info("addDefaultObjects : Done")
    logger.info("addEventTypesAndTemplates : starting...")
    addDefaultEventTypesAndTemplates(context)
    logger.info("addEventTypesAndTemplates : Done")
    logger.info("addUrbanConfigsTopics : starting...")
    addUrbanConfigsTopics(context)
    logger.info("addUrbanConfigsTopics : Done")
    logger.info("addLicencesection : starting...")
    addLicencesCollection(context)
    logger.info("addLicencesCollection : Done")
    if refresh:
        #refresh catalog after all these objects have been added...
        logger.info("Refresh portal_catalog : starting...")
        site.portal_catalog.refreshCatalog(clear=True)
        logger.info("Refresh portal_catalog : Done!")


##code-section FOOT
def _(msgid, domain, context):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default='')


def setUrbanConfigWFPolicy(context):
    """
      Define a local wf policy to allow to enable/disable urban templates documents in the config
    """
    site = context.getSite()
    wf_tool = getToolByName(site, 'portal_workflow')
    #create the local policy for the urban config
    placefulwf_tool = getToolByName(site, 'portal_placeful_workflow')
    if not hasattr(placefulwf_tool, 'urban_cfg_policy'):
        placefulwf_tool.manage_addWorkflowPolicy('urban_cfg_policy',
                                                 workflow_policy_type='default_workflow_policy (Simple Policy)',
                                                 duplicate_id='empty')
    policy = getattr(placefulwf_tool, 'urban_cfg_policy')
    policy.setTitle('Urban config workflow policy')
    policy.setChain('UrbanDoc', ('activation_workflow', ))
    wf_tool.updateRoleMappings()

    #set this local policy to the urban config folder
    tool = getToolByName(site, 'portal_urban')
    if not hasattr(tool, WorkflowPolicyConfig_id):
        tool.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        wf_policy_cfg = getattr(tool, WorkflowPolicyConfig_id)
        wf_policy_cfg.setPolicyBelow('urban_cfg_policy')
    wf_tool.updateRoleMappings()


def setFolderAllowedTypes(folder, portal_types):
    """
    """
    if type(portal_types) != list:
        portal_types = [portal_types]
    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(portal_types)
    folder.setImmediatelyAddableTypes(portal_types)


def createFolderVocabulary(folder, vocabulary_list, portal_type):
    """
    """
    for voc in vocabulary_list[1:]:
        folder.invokeFactory(portal_type, **voc)


def addUrbanConfigs(context):
    """
      Add the different urban configs
    """
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')

    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.config_default_values' % profile_name
    attribute = 'default_values'
    module = __import__(module_name, fromlist=[attribute])
    default_values = getattr(module, attribute)

    for urban_type in URBAN_TYPES:
        licenceConfigId = urban_type.lower()
        if not hasattr(aq_base(tool), licenceConfigId):
            configFolderid = tool.invokeFactory("LicenceConfig", id=licenceConfigId, title=_("%s_urbanconfig_title" % urban_type.lower(), 'urban', context=site.REQUEST))
            configFolder = getattr(tool, configFolderid)
            configFolder.licence_portal_type = urban_type
            configFolder.setUsedAttributes(configFolder.listUsedAttributes().keys())
            configFolder.reindexObject()
        else:
            configFolder = getattr(tool, licenceConfigId)

        #we just created the urbanConfig, proceed with other parameters...
        #parameters for every LicenceConfigs
        #add UrbanEventTypes folder
        if not hasattr(aq_base(configFolder), 'urbaneventtypes'):
            newFolderid = configFolder.invokeFactory("Folder", id="urbaneventtypes", title=_("urbaneventtypes_folder_title", 'urban', context=site.REQUEST))
            newFolder = getattr(configFolder, newFolderid)
            setFolderAllowedTypes(newFolder, 'UrbanEventType')

        #add TownshipFolderCategories folder
        if not hasattr(aq_base(configFolder), 'townshipfoldercategories'):
            newFolderid = configFolder.invokeFactory("Folder", id="townshipfoldercategories", title=_("townshipfoldercategories_folder_title", 'urban', context=site.REQUEST))
            newFolder = getattr(configFolder, newFolderid)
            vocabulary_list = default_values['townshipfoldercategories']
            portal_type = vocabulary_list[0]
            setFolderAllowedTypes(newFolder, portal_type)
            createFolderVocabulary(newFolder, vocabulary_list, portal_type)

        #add FolderCategories folder
        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'Declaration', 'Division', 'MiscDemand']:
            if not hasattr(aq_base(configFolder), 'foldercategories'):
                newFolderid = configFolder.invokeFactory("Folder", id="foldercategories", title=_("foldercategories_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                if urban_type in ['BuildLicence']:
                    #categories for BuildLicences
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="uap", title=u"UAP (permis d'urbanisme avec avis préalable du FD)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="udc", title=u"UDC (permis dans PCA, RCU, LOTISSEMENT, parfois avec demande de dérogation)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="upp", title=u"UPP (petit permis délivré directement par le Collège)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="pu", title=u"PU (demande de PERMIS UNIQUE)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="art127", title=u"UCP (article 127)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="inconnu", title=u"Inconnue")
                elif urban_type in ['ParcelOutLicence']:
                    #categories for ParcelOutLicences
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="lap", title=u"LAP (permis de lotir avec avis préalable du FD)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="lapm", title=u"LAP/M (modification du permis de lotir avec avis du FD)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="ldc", title=u"LDC (permis de lotir dans un PCA, lotissement ou en décentralisation)")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="ldcm", title=u"LDC/M (modification du permis de lotir dans un PCA, RCU, LOTISSEMENT)")
                    #categories for UrbanCertificateOnes
                elif urban_type in ['UrbanCertificateOne']:
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="cu1", title=u"CU1 (certificat d'urbanisme 1)")
                    #categories for UrbanCertificateTwos
                elif urban_type in ['UrbanCertificateTwo']:
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="cu2", title=u"CU2 (certificat d'urbanisme 2)")
                    #categories for Declarations
                elif urban_type in ['Declaration']:
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="dup", title=u"DUP (Déclaration Urbanistique Préalable)")
                    #categories for Divisions
                elif urban_type in ['Division']:
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="dup", title=u"DIV (Division notariale)")
                    #categories for MiscDemands
                elif urban_type in ['MiscDemand']:
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="apct", title=u"Avis préalable construction ou transformation")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="appu", title=u"Avis préalable permis d'urbanisation")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="apd", title=u"Avis préalable de division")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="dre", title=u"Demande de raccordement à l'égout")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="div", title=u"Divers")

        if urban_type in ['Declaration', ]:
            #add "Articles" folder
            if not hasattr(aq_base(configFolder), 'articles'):
                newFolderid = configFolder.invokeFactory("Folder", id="articles", title=_("articles_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['articles']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

        if urban_type == 'ParcelOutLicence':
            if not hasattr(aq_base(configFolder), 'lotusages'):
                newFolderid = configFolder.invokeFactory("Folder", id="lotusages", title=_("lotusages_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['lotusages']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)
            if not hasattr(aq_base(configFolder), 'equipmenttypes'):
                newFolderid = configFolder.invokeFactory("Folder", id="equipmenttypes", title=_("folderequipmenttypes_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['equipmenttypes']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

        if urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter']:
            #we add the specific features folder
            if not hasattr(aq_base(configFolder), 'specificfeatures'):
                newFolderid = configFolder.invokeFactory("Folder", id="specificfeatures", title=_("urban_label_specificFeatures", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['specificfeatures']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)
                setHTMLContentType(newFolder, 'description')

            if not hasattr(aq_base(configFolder), 'roadspecificfeatures'):
                newFolderid = configFolder.invokeFactory("Folder", id="roadspecificfeatures", title=_("urban_label_roadSpecificFeatures", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['roadspecificfeatures']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

            if not hasattr(aq_base(configFolder), 'locationspecificfeatures'):
                newFolderid = configFolder.invokeFactory("Folder", id="locationspecificfeatures", title=_("urban_label_locationSpecificFeatures", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['locationspecificfeatures']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

            #we add the custom township specific features folder
            if not hasattr(aq_base(configFolder), 'townshipspecificfeatures'):
                newFolderid = configFolder.invokeFactory("Folder", id="townshipspecificfeatures", title=_("urban_label_townshipSpecificFeatures", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['townshipspecificfeatures']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

            if not hasattr(aq_base(configFolder), 'opinionstoaskifworks'):
                #add "Ask opinions to in case of works" folder
                newFolderid = configFolder.invokeFactory("Folder", id="opinionstoaskifworks", title=_("opinionstoaskifworks_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['opinionstoaskifworks']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)
                #now, we need to specify that the description's mimetype is 'text/html'
                setHTMLContentType(newFolder, 'description')

        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', 'EnvClassThree']:
            if not hasattr(aq_base(configFolder), 'missingparts'):
                #add "missingparts" folder
                newFolderid = configFolder.invokeFactory("Folder", id="missingparts", title=_("missingparts_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                if urban_type in ['BuildLicence', ]:
                    #necessary documents for BuildLicences
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="form_demande", title=u"Formulaire de demande (annexe 20) en 2 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="plan_travaux", title=u"Plan des travaux en 4 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="attestation_archi", title=u"Attestation de l'architecte (annexe 21) en 2 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="attestation_ordre_archi", title=u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="photos", title=u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="notice_environnement", title=u"Notice d'évaluation préalable incidences environnement (annexe 1C) en 2 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="plan_secteur", title=u"Une copie du plan de secteur")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="isolation", title=u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="peb", title=u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires")
                if urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', ]:
                    #necessary documents for UrbanCertificates
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="form_demande", title=u"Formulaire de demande (formulaire 1A) en 3 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="extrait_cadastral", title=u"Extrait cadastral en 3 exemplaires")
                if urban_type in ['EnvClassThree', ]:
                    #necessary documents for environment licences
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="form_demande", title=u"Formulaire de demande en 4 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm", id="plan", title=u"Plans")

        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateTwo', 'EnvClassThree']:
            if not hasattr(aq_base(configFolder), 'foldermakers'):
                #add Makers folder
                newFolderid = configFolder.invokeFactory("Folder", id="foldermakers", title=_("foldermakers_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['foldermakers']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)
                #now, we need to specify that the description's mimetype is 'text/html'
                setHTMLContentType(newFolder, 'description')

        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateTwo']:
            #add investigation articles folder
            #this is done by a method because the migrateBuildLicencesInvestigationArticles
            #migration step will use it too
            addInvestigationArticles(context, configFolder)
            if not hasattr(aq_base(configFolder), 'folderdelays'):
                #add Delays folder
                newFolderid = configFolder.invokeFactory("Folder", id="folderdelays", title=_("folderdelays_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['folderdelays']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

            if not hasattr(aq_base(configFolder), 'derogations'):
                #add the derogations folder
                newFolderid = configFolder.invokeFactory("Folder", id="derogations", title=_("derogations_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['derogations']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

            if not hasattr(aq_base(configFolder), 'folderbuildworktypes'):
                #add BuildWorkTypes folder
                newFolderid = configFolder.invokeFactory("Folder", id="folderbuildworktypes", title=_("folderbuildworktype_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['folderbuildworktypes']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

        if urban_type in ['BuildLicence', ]:
            #add PEB categories folder
            #this is done by a method because the migrateToUrban115
            #migration step will use it too
            addPEBCategories(context, configFolder)

        if urban_type in ['EnvClassThree', ]:
            if not hasattr(aq_base(configFolder), 'rubrics'):
                newFolderid = configFolder.invokeFactory("Folder", id="rubrics", title=_("rubrics_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['Folder'])
                newFolder.setImmediatelyAddableTypes(['Folder'])
                addRubricValues(context, 3, newFolder)

            if not hasattr(aq_base(configFolder), 'inadmissibilityreasons'):
                newFolderid = configFolder.invokeFactory("Folder", id="inadmissibilityreasons", title=_("inadmissibilityreasons_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['inadmissibilityreasons']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)

            if not hasattr(aq_base(configFolder), 'applicationreasons'):
                newFolderid = configFolder.invokeFactory("Folder", id="applicationreasons", title=_("applicationreasons_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                vocabulary_list = default_values['applicationreasons']
                portal_type = vocabulary_list[0]
                setFolderAllowedTypes(newFolder, portal_type)
                createFolderVocabulary(newFolder, vocabulary_list, portal_type)


def addRubricValues(context, class_type, config_folder):
    categories = [
        "01   AGRICULTURE, DETENTION D'ANIMAUX, SERVICES ANNEXES",
        "02   SYLVICULTURE, EXPLOITATION FORESTIÈRE, SERVICES ANNEXES",
        "05   PÊCHE, AQUACULTURE",
        "10   EXTRACTION DE HOUILLE, DE LIGNITE ET DE TOURBE",
        "11   EXTRACTION D'HYDROCARBURES, SERVICES ANNEXES",
        "13   EXTRACTION DE MINERAIS MÉTALLIQUES ",
        "14   AUTRES INDUSTRIES EXTRACTIVES",
        "15   INDUSTRIES AGRO-ALIMENTAIRES",
        "16   INDUSTRIE DU TABAC",
        "17   INDUSTRIE TEXTILE",
    ]

    for category in categories:
        newFolderid = config_folder.invokeFactory("Folder", id=category.split()[0], title=category)
        newFolder = getattr(config_folder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['EnvironmentRubricTerm'])
        newFolder.setImmediatelyAddableTypes(['EnvironmentRubricTerm'])
    return


def addPEBCategories(context, configFolder):
    """
      This method add default PEB categories
    """
    site = hasattr(context, 'getSite') and context.getSite() or getToolByName(context, 'portal_url').getPortalObject()
    if not hasattr(aq_base(configFolder), 'pebcategories'):
        newFolderid = configFolder.invokeFactory("Folder", id="pebcategories", title=_("pebcategories_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(configFolder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm", id="not_applicable", title=_('peb_not_applicable', 'urban', context=site.REQUEST))
        newFolder.invokeFactory("UrbanVocabularyTerm", id="complete_process", title=_('peb_complete_process', 'urban', context=site.REQUEST))
        newFolder.invokeFactory("UrbanVocabularyTerm", id="form1_process", title=_('peb_form1_process', 'urban', context=site.REQUEST))
        newFolder.invokeFactory("UrbanVocabularyTerm", id="form2_process", title=_('peb_form2_process', 'urban', context=site.REQUEST))


def addInvestigationArticles(context, configFolder):
    """
      This method add default investigation articles
    """
    site = context.getSite()

    if not hasattr(aq_base(configFolder), 'investigationarticles'):
        newFolderid = configFolder.invokeFactory("Folder", id="investigationarticles", title=_("investigationarticles_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(configFolder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-1", title=u"330 1° - « [...] bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et [...] »", description="<p>« la construction ou la reconstruction de bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu'à cinquante mètres de part et d'autre de la construction projetée ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 1°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-2", title=u"330 2° - « [...] bâtiment dont la profondeur, mesurée [...] est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments [...] »", description="<p>« la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës (AGW du 23 décembre 1998, art 1er), la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 2°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-3", title=u"330 3° - « [...] un magasin [...] dont la surface nette de vente est supérieure à 400 m² [...] »", description="<p>« la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface nette de vente est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 3°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-4", title=u"330 4° - « [...] de bureaux [...] dont la superficie des planchers est supérieure à 650 m² [...] »", description="<p>« la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à 650 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 4°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-5", title=u"330 5° - « [...] bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² [...] »", description="<p>« la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 5°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-6", title=u"330 6° - « l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »", description="<p>« l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »</p>", extraValue="330 6°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-7", title=u"330 7° - « [...] permis de lotir ou de permis d'urbanisme [...] constructions groupées visées à l'article 126 qui portent sur une superficie de 2 hectares et plus »", description="<p>« les demandes de permis de lotir ou de permis d'urbanisme relatives à des constructions groupées visées à l'article 126 qui portent sur une superficie de 2 hectares et plus »</p>", extraValue="330 7°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-8", title=u"330 8° - « [...] permis de lotir ou de permis d'urbanisme [...] constructions groupées visées à l'article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°, 3°, 4° et 5° »", description="<p>« les demandes de permis de lotir ou de permis d'urbanisme relatives à des constructions groupées visées à l'article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°, 3°, 4° et 5° »</p>", extraValue="330 8°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-9", title=u"330 9° - « les demandes de permis de lotir ou de permis d'urbanisme visées à l'article 128 »", description="<p>« les demandes de permis de lotir ou de permis d'urbanisme visées à l'article 128 »</p>", extraValue="330 9°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-10", title=u"330 10° - « les demandes de permis de lotir visées à l'article 97 »", description="<p>« les demandes de permis de lotir visées à l'article 97 »</p>", extraValue="330 10°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-11", title=u"330 11° - « les demandes de permis de lotir ou de permis d'urbanisme impliquant l'application des articles 110 à 113 »", description="<p>« les demandes de permis de lotir ou de permis d'urbanisme impliquant l'application des articles 110 à 113 »</p>", extraValue="330 11°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-12", title=u"330 12° - « [...] permis de lotir et les demandes de permis d'urbanisme [...] d'un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde [...] »", description="<p>« les demandes de permis de lotir et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protection visée à l'article 205 (lire article 209) ou localisés dans un site mentionné à l'atlas visé à l'article 215 (lire article 233) »</p>", extraValue="330 12°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="330-13", title=u"330 13° - « les voiries publiques de la Région classées en réseau interurbain (RESI) par l'arrêté ministériel du 11 août 1994 »", description="<p>« les voiries publiques de la Région classées en réseau interurbain (RESI) par l'arrêté ministériel du 11 août 1994 »</p>", extraValue="330 13°")
        newFolder.invokeFactory("UrbanVocabularyTerm", id="334-2", title=u"334 2° - « Dès le lendemain du jour où il est en possession de l'accusé de réception et jusqu'au jour de la clôture de l'enquête publique [...]»", description="<p>« Dès le lendemain du jour où il est en possession de l'accusé de réception et jusqu'au jour de la clôture de l'enquête publique, le demandeur est tenu d'afficher sur le terrain faisant l'objet de la demande : 2° dans les cas visés à l'article 330, 1° à 5°, et 12°, ou lorsque la dérogation porte sur le gabarit d'un bâtiment, une vue axonométrique du projet et des bâtiments contigus »</p>", extraValue="334 2°")
        #now, we need to specify that the description's mimetype is 'text/html'
        setHTMLContentType(newFolder, 'description')


def addUrbanGroups(context):
    """
       Add a group of 'urban' application users...
    """
    site = context.getSite()
    #add 3 groups
    #one with urban Managers
    site.portal_groups.addGroup("urban_managers", title="Urban Managers")
    site.portal_groups.setRolesForGroup('urban_managers', ('UrbanMapReader', ))
    #one with urban Readers
    site.portal_groups.addGroup("urban_readers", title="Urban Readers")
    site.portal_groups.setRolesForGroup('urban_readers', ('UrbanMapReader', ))
    #one with urban Editors
    site.portal_groups.addGroup("urban_editors", title="Urban Editors")
    site.portal_groups.setRolesForGroup('urban_editors', ('UrbanMapReader', ))
    #one with map Readers
    site.portal_groups.addGroup("urban_map_readers", title="Urban Map Readers")
    site.portal_groups.setRolesForGroup('urban_map_readers', ('UrbanMapReader', ))


def addLicencesCollection(context):
    """
        Add a collection in urban folder, regrouping all licences
    """
    coll_id = 'licences-collection'
    site = context.getSite()
    if not base_hasattr(site.urban, coll_id):
        site.urban.invokeFactory("Topic", id=coll_id)
        topic = getattr(site.urban, coll_id)
        type_crit = topic.addCriterion('Type', 'ATPortalTypeCriterion')
        type_crit.setValue(URBAN_TYPES)


def setDefaultApplicationSecurity(context):
    """
       Set sharing on differents folders to access the application
    """
    #we have to :
    #give the Reader role to the urban_readers and urban_editors groups on
    #portal_urban and application folders
    #give the Editor role on urban application folders
    site = context.getSite()
    #make the undo action visible for the site manager
    site.portal_actions.user.undo.visible = True
    site.manage_permission('List undoable changes', ['Site Administrator', 'Manager'], acquire=1, REQUEST=None)
    #portal_urban local roles
    site.portal_urban.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
    site.portal_urban.manage_addLocalRoles("urban_readers", ("Reader", ))
    site.portal_urban.manage_addLocalRoles("urban_editors", ("Reader", ))
    site.portal_urban.manage_addLocalRoles("urban_map_readers", ("Reader", ))

    #application folders local roles
    #global application folder : "urban_readers" and "urban_editors" can read...
    if hasattr(site, "urban"):
        app_folder = getattr(site, "urban")
        app_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        app_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        app_folder.manage_addLocalRoles("urban_editors", ("Reader", ))
        #set some hardcoded permissions
        #sharing is only managed by the 'Managers'
        app_folder.manage_permission('Sharing page: Delegate roles', ['Manager', ], acquire=0)
        #hide the 'Properties' tab to other roles than 'Manager'
        app_folder.manage_permission('Manage properties', ['Manager', ], acquire=0)

    #buildlicences folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "buildlicences"):
        b_folder = getattr(app_folder, "buildlicences")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            b_folder.manage_addProperty('urbanConfigId', 'buildlicence', 'string')
        except BadRequest:
            pass
        b_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        b_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        b_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #parceloutlicences application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "parceloutlicences"):
        p_folder = getattr(app_folder, "parceloutlicences")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'parceloutlicence', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #declarations application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "declarations"):
        p_folder = getattr(app_folder, "declarations")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'declaration', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #division application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "divisions"):
        p_folder = getattr(app_folder, "divisions")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'division', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #urbancertificatesones application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "urbancertificateones"):
        p_folder = getattr(app_folder, "urbancertificateones")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'urbancertificateone', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #urbancertificatetwos application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "urbancertificatetwos"):
        p_folder = getattr(app_folder, "urbancertificatetwos")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'urbancertificatetwo', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #notaryletters application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "notaryletters"):
        p_folder = getattr(app_folder, "notaryletters")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'notaryletter', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #envclassthrees folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "envclassthrees"):
        p_folder = getattr(app_folder, "envclassthrees")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'envclassthree', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #architects application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "architects"):
        p_folder = getattr(app_folder, "architects")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #geometricians application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "geometricians"):
        p_folder = getattr(app_folder, "geometricians")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #notaries application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "notaries"):
        p_folder = getattr(app_folder, "notaries")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #parcellings application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "parcellings"):
        p_folder = getattr(app_folder, "parcellings")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))
    #misc demands application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "miscdemands"):
        p_folder = getattr(app_folder, "miscdemands")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'miscdemand', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader", ))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))


def addGlobalFolders(context):
    """
    Add folders with properties used by several licence types
    """
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    site = context.getSite()
    tool = site.portal_urban

    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.config_default_values' % profile_name
    attribute = 'default_values'
    module = __import__(module_name, fromlist=[attribute])
    default_values = getattr(module, attribute)

    #add global topics
    #a criterion can have 4 values if necessary
    topicsInfo = (
        # Lots
        (
            'searchlots',
            (
                ('Type', 'ATPortalTypeCriterion', ['Lot', ], ''),
                ('path', 'ATPathCriterion', '', False),
            ),
            None, ['Title', 'Creator']
        ),
        # Equipments
        (
            'searchequipments',
            (
                ('Type', 'ATPortalTypeCriterion', ['Equipment', ], ''),
                ('path', 'ATPathCriterion', '', False),
            ),
            None, ['Title', 'Creator']
        ),
    )

    #add globaltemplates folder
    if not hasattr(tool, "globaltemplates"):
        globaltemplatesFolderid = tool.invokeFactory("Folder", id="globaltemplates",
                                                     title=_("globaltemplates_folder_title", 'urban', context=site.REQUEST))
        globaltemplatesFolder = getattr(tool, globaltemplatesFolderid)
        setFolderAllowedTypes(globaltemplatesFolder, 'UrbanDoc')

    #add foldermanagers folder
    if not hasattr(tool, "foldermanagers"):
        foldermanagersFolderid = tool.invokeFactory("Folder", id="foldermanagers",
                                                    title=_("foldermanagers_folder_title", 'urban', context=site.REQUEST))
        foldermanagersFolder = getattr(tool, foldermanagersFolderid)
        setFolderAllowedTypes(foldermanagersFolder, 'FolderManager')

    if not hasattr(tool, "topics"):
        topicsFolderId = tool.invokeFactory("Folder", id="topics", title=_("topics", 'urban', context=site.REQUEST))
        topicsFolder = getattr(tool, topicsFolderId)
        #restrict the addable types to "ATTopic"
        #Add these searches for portal_urban
        setFolderAllowedTypes(topicsFolder, 'Topic')
    else:
        topicsFolder = getattr(tool, "topics")
    for topicId, topicCriteria, stateValues, topicViewFields in topicsInfo:
        if hasattr(topicsFolder, topicId):
            continue
        topicsFolder.invokeFactory('Topic', topicId)
        topic = getattr(topicsFolder, topicId)
        topic.setExcludeFromNav(True)
        topic.setTitle(topicId)
        for criterionName, criterionType, criterionValue, criterionExtraValue in topicCriteria:
            criterion = topic.addCriterion(field=criterionName, criterion_type=criterionType)
            criterion.setValue(criterionValue)
            #define if the ATPathCriterion must search into subfolders
            if criterionType == 'ATPathCriterion':
                criterion.setRecurse(criterionExtraValue)
            #add a property defining if the topic is relative to a BuildLicence or a ParcelOutLicence or a PortionOut
            if criterionType == 'ATPortalTypeCriterion':
                topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
        #add a review_state criterion if needed...
        if stateValues:
            stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
            stateCriterion.setValue(stateValues)
        topic.setTitle(_(topicId, 'urban', context=site.REQUEST))
        topic.setLimitNumber(True)
        topic.setItemCount(20)
        #set the sort criterion as reversed
        if topicId in ['searcharchitects', 'searchgeometricians', 'searchnotaries', ]:
            #these topics are used for showing things
            topic.setSortCriterion('sortable_title', False)
        else:
            topic.setSortCriterion('created', True)
        topic.setCustomView(True)
        topic.setCustomViewFields(topicViewFields)
        topic.reindexObject()

    #add the pcas folder
    if not hasattr(tool, "pcas"):
        newFolderid = tool.invokeFactory("Folder", id="pcas", title=_("pcas_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['pcas']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the streets folder
    if not hasattr(tool, "streets"):
        newFolderid = tool.invokeFactory("Folder", id="streets", title=_("streets_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        setFolderAllowedTypes(newFolder, 'City')

    if not hasattr(tool, "pashs"):
        #add pashs folder
        newFolderid = tool.invokeFactory("Folder", id="pashs", title=_("pashs_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['pashs']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add global folderroadtypes folder
    if not hasattr(tool, "folderroadtypes"):
        newFolderid = tool.invokeFactory("Folder", id="folderroadtypes", title=_("folderroadtypes_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['pcas']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    if not hasattr(tool, 'folderprotectedbuildings'):
        #add ProtectedBuildings folder
        newFolderid = tool.invokeFactory("Folder", id="folderprotectedbuildings", title=_("folderprotectedbuildings_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['folderprotectedbuildings']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    if not hasattr(tool, 'folderroadequipments'):
        #add RoadEquipments folder
        newFolderid = tool.invokeFactory("Folder", id="folderroadequipments", title=_("folderroadequipments_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['folderroadequipments']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    if not hasattr(tool, "folderroadcoatings"):
        #add RoadCoatings folder
        newFolderid = tool.invokeFactory("Folder", id="folderroadcoatings", title=_("folderroadcoatings_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['folderroadcoatings']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add Zones folder
    if not hasattr(tool, "folderzones"):
        newFolderid = tool.invokeFactory("Folder", id="folderzones", title=_("folderzones_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['folderzones']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the RCU folder
    if not hasattr(tool, "rcu"):
        newFolderid = tool.invokeFactory("Folder", id="rcu", title=_("rcu_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['rcu']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the SSC folder
    if not hasattr(tool, "ssc"):
        newFolderid = tool.invokeFactory("Folder", id="ssc", title=_("ssc_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['ssc']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the exploitation conditions folder
    if not hasattr(tool, "exploitationconditions"):
        conditionsid = tool.invokeFactory("Folder", id="exploitationconditions", title=_("exploitationconditions_folder_title", 'urban', context=site.REQUEST))
        conditions = getattr(tool, conditionsid)
        setFolderAllowedTypes(conditions, 'Folder')
        #add the 'integral and sectorial conditions' folder
    else:
        conditions = getattr(tool, "exploitationconditions")

    #add the 'integral and sectorial conditions' folder
    if not hasattr(conditions, "i_and_s_conditions"):
        newFolderid = conditions.invokeFactory("Folder", id="i_and_s_conditions", title=_("i_and_s_conditions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(conditions, newFolderid)
        setFolderAllowedTypes(newFolder, 'UrbanVocabularyTerm')

    #add the integral conditions folder
    if not hasattr(conditions, "integralconditions"):
        newFolderid = conditions.invokeFactory("Folder", id="integralconditions", title=_("integralconditions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(conditions, newFolderid)
        setFolderAllowedTypes(newFolder, 'UrbanVocabularyTerm')

    #add the sectorial conditions folder
    if not hasattr(conditions, "sectorialconditions"):
        newFolderid = conditions.invokeFactory("Folder", id="sectorialconditions", title=_("sectorialconditions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(conditions, newFolderid)
        setFolderAllowedTypes(newFolder, 'UrbanVocabularyTerm')

    #add the additional_layers folder
    if not hasattr(tool, "additional_layers"):
        newFolderid = tool.invokeFactory("Folder", id="additional_layers", title=_("additonal_layers_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        setFolderAllowedTypes(newFolder, 'UrbanVocabularyTerm')
        #additional layers are added in the extra step "setupExtra"

    #add the persons_titles folder
    if not hasattr(tool, "persons_titles"):
        newFolderid = tool.invokeFactory("Folder", id="persons_titles", title=_("persons_titles_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['persons_titles']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the persons_grades folder
    if not hasattr(tool, "persons_grades"):
        newFolderid = tool.invokeFactory("Folder", id="persons_grades", title=_("persons_grades_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['persons_grades']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the country folder
    if not hasattr(tool, "country"):
        newFolderid = tool.invokeFactory("Folder", id="country", title=_("country_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['country']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the decisions folder
    if not hasattr(tool, "decisions"):
        newFolderid = tool.invokeFactory("Folder", id="decisions", title=_("decisions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['decisions']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)

    #add the external opinions decisions folder
    if not hasattr(tool, "externaldecisions"):
        newFolderid = tool.invokeFactory("Folder", id="externaldecisions", title=_("external_decisions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        vocabulary_list = default_values['externaldecisions']
        portal_type = vocabulary_list[0]
        setFolderAllowedTypes(newFolder, portal_type)
        createFolderVocabulary(newFolder, vocabulary_list, portal_type)


def addUrbanConfigsTopics(context):
    """
      Add the default topics of every urbanConfig
    """
    site = context.getSite()
    tool = site.portal_urban

    for urban_type in URBAN_TYPES:
        if not hasattr(tool, urban_type.lower()):
            continue
        urbanConfig = getattr(tool, urban_type.lower())
        topicsInfo = (
            #this will be used in the urban_view
            # Portlet search "every licences"
            (
                'searchalllicences',
                (
                    ('Type', 'ATPortalTypeCriterion', urban_type),
                    ('path', 'ATPathCriterion', ''),
                ),
                None, ['Title', 'CreationDate', 'Creator']
            ),
            # Portlet search "in_progress licences"
            (
                'searchinprogresslicences',
                (
                    ('Type', 'ATPortalTypeCriterion', urban_type),
                    ('path', 'ATPathCriterion', ''),
                ),
                ('in_progress', ), ['Title', 'CreationDate', 'Creator']
            ),
            # Portlet search "retired licences"
            (
                'searchretiredlicences',
                (
                    ('Type', 'ATPortalTypeCriterion', urban_type),
                    ('path', 'ATPathCriterion', ''),
                ),
                ('retired', ),
                ['Title', 'CreationDate', 'Creator']
            ),
            # Portlet search "incomplete licences"
            (
                'searchincompletelicences',
                (
                    ('Type', 'ATPortalTypeCriterion', urban_type),
                    ('path', 'ATPathCriterion', ''),
                ),
                ('incomplete', ), ['Title', 'CreationDate', 'Creator']
            ),
            # Portlet search "accepted licences"
            (
                'searchacceptedlicences',
                (
                    ('Type', 'ATPortalTypeCriterion', urban_type),
                    ('path', 'ATPathCriterion', ''),
                ),
                ('accepted', ), ['Title', 'CreationDate', 'Creator']
            ),
            # Portlet search "refused licences"
            (
                'searchrefusedlicences',
                (
                    ('Type', 'ATPortalTypeCriterion', urban_type),
                    ('path', 'ATPathCriterion', ''),
                ),
                ('refused', ), ['Title', 'CreationDate', 'Creator']
            ),
        )
        if not "topics" in urbanConfig.objectIds():
            topicsFolderId = urbanConfig.invokeFactory("Folder", id="topics", title=_("topics", 'urban', context=site.REQUEST))
            topicsFolder = getattr(urbanConfig, topicsFolderId)
            #restrict the addable types to "ATTopic"
            #Add these searches by meeting config
            topicsFolder.setConstrainTypesMode(1)
            topicsFolder.setLocallyAllowedTypes(['Topic'])
            topicsFolder.setImmediatelyAddableTypes(['Topic'])
            for topicId, topicCriteria, stateValues, topicViewFields in topicsInfo:
                topicsFolder.invokeFactory('Topic', topicId)
                topic = getattr(topicsFolder, topicId)
                topic.setExcludeFromNav(True)
                topic.setTitle(topicId)
                for criterionName, criterionType, criterionValue in topicCriteria:
                    criterion = topic.addCriterion(field=criterionName, criterion_type=criterionType)
                    criterion.setValue([criterionValue])
                    #add a property defining if the topic is relative to a BuildLicence or a ParcelOutLicence or a PortionOut
                    if criterionType == 'ATPortalTypeCriterion':
                        topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
                #add a review_state criterion if needed...
                if stateValues:
                    stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
                    stateCriterion.setValue(stateValues)
                topic.setTitle(_("%s_%s" % (urban_type.lower(), topicId), 'urban', context=site.REQUEST))
                topic.setLimitNumber(True)
                topic.setItemCount(20)
                #set the sort criterion as reversed
                topic.setSortCriterion('created', True)
                topic.setCustomView(True)
                topic.setCustomViewFields(topicViewFields)
                topic.reindexObject()


def installUrbanskin(context):
    """
       Install Products.urbanskin if available
    """
    site = context.getSite()
    try:
        site.portal_setup.runAllImportStepsFromProfile('profile-Products.urbanskin:default')
        logger.info("installUrbanskin : Done")
    except KeyError:
        logger.info("installUrbanskin : Products.urbanskin not found, skin not installed!")


def adaptDefaultPortal(context):
    """
       Adapt some properties of the portal
    """
    #deactivate tabs auto generation in navtree_properties
    site = context.getSite()
    site.portal_properties.site_properties.disable_folder_sections = True
    #remove default created objects like events, news, ...
    try:
        site.manage_delObjects(ids=['events', ])
    except AttributeError:
        #the 'events' object does not exist...
        pass
    try:
        site.manage_delObjects(ids=['news', ])
    except AttributeError:
        #the 'news' object does not exist...
        pass

    #change the content of the front-page
    try:
        frontpage = getattr(site, 'front-page')
        frontpage.setTitle(_("front_page_title", 'urban', context=site.REQUEST))
        frontpage.setDescription(_("front_page_descr", 'urban', context=site.REQUEST))
        frontpage.setText(_("front_page_text", 'urban', context=site.REQUEST), mimetype='text/html')
        #remove the presentation mode
        frontpage.setPresentation(False)
        frontpage.reindexObject()
    except AttributeError:
        #the 'front-page' object does not exist...
        pass

    #hide de sendto action
    #set visible = 0
    try:
        site.portal_actions.document_actions.sendto.manage_changeProperties(visible=False)
    except AttributeError:
        #the 'front-page' object does not exist...
        pass


def addApplicationFolders(context):
    """
    Add the application folders like 'urban' and 'architects'
    """
    site = context.getSite()

    if not hasattr(aq_base(site), "urban"):
        newFolderid = site.invokeFactory("Folder", id="urban", title=_("urban", 'urban', context=site.REQUEST))
        newFolder = getattr(site, newFolderid)
        newFolder.setLayout('urban_view')
    else:
        newFolder = getattr(site, 'urban')

    for urban_type in URBAN_TYPES:
        if not hasattr(newFolder, urban_type.lower() + 's'):
            newFolderid = newFolder.invokeFactory("Folder", id=urban_type.lower() + 's', title=_(urban_type.lower() + 's', 'urban', context=site.REQUEST))
            newSubFolder = getattr(newFolder, newFolderid)
            alsoProvides(newSubFolder, ILicenceContainer)
            newSubFolder.setConstrainTypesMode(1)
            newSubFolder.setLocallyAllowedTypes([urban_type])
            newSubFolder.setImmediatelyAddableTypes([urban_type])
            #set the layout to "urban_view"
            newSubFolder.setLayout('urban_view')
            #manage the 'Add' permissions...
            try:
                newSubFolder.manage_permission('urban: Add %s' % urban_type, ['Manager', 'Editor', ], acquire=0)
            except ValueError:
                #exception for some portal_types having a different meta_type
                if urban_type in ['UrbanCertificateOne', 'NotaryLetter', ]:
                    newSubFolder.manage_permission('urban: Add UrbanCertificateBase', ['Manager', 'Editor', ], acquire=0)
                if urban_type in ['EnvClassThree', ]:
                    newSubFolder.manage_permission('urban: Add EnvironmentBase', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains architects
    if not hasattr(newFolder, "architects"):
        newFolderid = newFolder.invokeFactory("Folder", id="architects", title=_("architects_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Architect'])
        newSubFolder.setImmediatelyAddableTypes(['Architect'])
        newSubFolder.setLayout('architects_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains geometricians
    if not hasattr(newFolder, "geometricians"):
        newFolderid = newFolder.invokeFactory("Folder", id="geometricians", title=_("geometricians_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Geometrician'])
        newSubFolder.setImmediatelyAddableTypes(['Geometrician'])
        newSubFolder.setLayout('geometricians_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Geometrician', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains notaries
    if not hasattr(newFolder, "notaries"):
        newFolderid = newFolder.invokeFactory("Folder", id="notaries", title=_("notaries_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Notary'])
        newSubFolder.setImmediatelyAddableTypes(['Notary'])
        newSubFolder.setLayout('notaries_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains parcellings
    if not hasattr(newFolder, "parcellings"):
        newFolderid = newFolder.invokeFactory("Folder", id="parcellings", title=_("parcellings_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['ParcellingTerm'])
        newSubFolder.setImmediatelyAddableTypes(['ParcellingTerm'])
        newSubFolder.setLayout('parcellings_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add ParcellingTerm', ['Manager', 'Editor', ], acquire=0)

    #add default links to searches
    search_links = [('searchbyparcel', 'urban_searchbyparcel'), ('searchbyapplicant', 'urban_searchbyapplicant?foldertypes=BuildLicence&foldertypes=Declaration&foldertypes=ParcelOutLicence'), ('searchbystreet', 'urban_searchbystreet?foldertypes=BuildLicence&foldertypes=Declaration&foldertypes=ParcelOutLicence'), ]
    for search_link in search_links:
        if not hasattr(newFolder, search_link[0]):
            #add a link and translate his title
            newFolder.invokeFactory("Link", id=search_link[0], title=_('urban_%s_descr' % search_link[0], 'urban', context=site.REQUEST), remoteUrl=search_link[1])


def addTestUsers(context):
    site = context.getSite()
    is_mountpoint = len(site.absolute_url_path().split('/')) > 2
    try:
        password = 'urbanmanager'
        if is_mountpoint:
            password = generatePassword(8)
        member = site.portal_registration.addMember(id="urbanmanager", password=password)
        member.setMemberProperties({'ext_editor': True})
        password = 'urbanreader'
        if is_mountpoint:
            password = generatePassword(8)
        site.portal_registration.addMember(id="urbanreader", password=password)
        password = 'urbaneditor'
        if is_mountpoint:
            password = generatePassword(8)
        member = site.portal_registration.addMember(id="urbaneditor", password=password)
        member.setMemberProperties({'ext_editor': True})
        password = 'urbanmapreader'
        if is_mountpoint:
            password = generatePassword(8)
        site.portal_registration.addMember(id="urbanmapreader", password=password)
        #put users in the correct group
        site.acl_users.source_groups.addPrincipalToGroup("urbanmanager", "urban_managers")
        site.acl_users.source_groups.addPrincipalToGroup("urbanreader", "urban_readers")
        site.acl_users.source_groups.addPrincipalToGroup("urbaneditor", "urban_editors")
        site.acl_users.source_groups.addPrincipalToGroup("urbanmapreader", "urban_map_readers")
    except:
        #if something wrong happens (one object already exists), we pass...
        pass


def addDefaultObjects(context):
    """
       Add some users and objects for test purpose...
    """
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    #add some users, some architects and some foldermanagers...
    #add 3 users, one as manager, one as reader and one as editor...
    site = context.getSite()
    addTestUsers(context)
        #add some architects...
    urbanFolder = getattr(site, "urban")
    notFolder = getattr(urbanFolder, "architects")
    if not notFolder.objectIds():
        #create some architects using the Extensions.imports script
        from Products.urban.Extensions.imports import import_architects
        import_architects(context.getSite().portal_urban)

    #add some notaries...
    urbanFolder = getattr(site, "urban")
    notFolder = getattr(urbanFolder, "notaries")
    if not notFolder.objectIds():
        notFolder.invokeFactory("Notary", id="notary1", name1="NotaryName1", name2="NotarySurname1")
        notFolder.invokeFactory("Notary", id="notary2", name1="NotaryName2", name2="NotarySurname2")
        notFolder.invokeFactory("Notary", id="notary3", name1="NotaryName3", name2="NotarySurname3")
        logger.info("Notaries examples have been added")

    #add some geometricians...
    urbanFolder = getattr(site, "urban")
    geoFolder = getattr(urbanFolder, "geometricians")
    if not geoFolder.objectIds():
        geoFolder.invokeFactory("Geometrician", id="geometrician1", name1="GeometricianName1", name2="GeometricianSurname1")
        geoFolder.invokeFactory("Geometrician", id="geometrician2", name1="GeometricianName2", name2="GeometricianSurname2")
        geoFolder.invokeFactory("Geometrician", id="geometrician3", name1="GeometricianName3", name2="GeometricianSurname3")
        logger.info("Geometricians examples have been added")

    #add some parcellings...
    urbanFolder = getattr(site, "urban")
    parcelFolder = getattr(urbanFolder, "parcellings")
    if not parcelFolder.objectIds():
        parcelFolder.invokeFactory("ParcellingTerm", id="p1", title=u"Lotissement 1 (André Ledieu - 01/01/2005 - 10)", label="Lotissement 1", subdividerName="André Ledieu", authorizationDate="2005/01/01", approvaleDate="2005/01/12", numberOfParcels=10)
        parcelFolder.invokeFactory("ParcellingTerm", id="p2", title=u"Lotissement 2 (Ets Tralala - 01/06/2007 - 8)", label="Lotissement 2", subdividerName="Ets Tralala", authorizationDate="2007/06/01", approvaleDate="2007/06/12", numberOfParcels=8)
        parcelFolder.invokeFactory("ParcellingTerm", id="p3", title=u"Lotissement 3 (SPRL Construction - 02/05/2001 - 15)", label="Lotissement 3", subdividerName="SPRL Construction", authorizationDate="2001/05/02", approvaleDate="2001/05/10", numberOfParcels=15)
        logger.info("ParcellingTerms examples have been added")

    #add some folder managers
    tool = site.portal_urban
    fmFolder = getattr(tool, "foldermanagers")
    if not fmFolder.objectIds():
        #import ipdb; ipdb.set_trace()
        fmFolder.invokeFactory("FolderManager", id="foldermanager1", name1="Dumont", name2="Jean",
                               grade='agent-technique', manageableLicences=URBAN_TYPES, ploneUserId='admin')
        fmFolder.invokeFactory("FolderManager", id="foldermanager2", name1="Schmidt", name2="Alain",
                               grade='directeur-general', manageableLicences=URBAN_TYPES)
        fmFolder.invokeFactory("FolderManager", id="foldermanager3", name1="Robert", name2="Patrick",
                               grade='responsable-administratif', manageableLicences=URBAN_TYPES)

    #create some streets using the Extensions.imports script
    if not tool.streets.objectIds('City'):
        from Products.urban.Extensions.imports import import_streets_fromfile, import_localities_fromfile
        import_streets_fromfile(tool)
        import_localities_fromfile(tool)


def addDefaultEventTypesAndTemplates(context):
    """
     Add default urban event types and their default document templates
    """
    site = context.getSite()
    tool = site.portal_urban
    #add global templates, default UrbanEventTypes and their templates for documents generation
    updateAllUrbanTemplates(context)
    #add OpinionRequest UrbanEventTypes by notifying the creation of their corresponding OrganisationTerm
    for licence_type in ['BuildLicence', 'UrbanCertificateTwo', 'ParcelOutLicence', 'EnvClassThree']:
        for organisation_term in getattr(tool, licence_type.lower()).foldermakers.objectValues():
            event.notify(ObjectInitializedEvent(organisation_term))


def importStreets(context):
    #site = context.getSite()
    #cat = getToolByName(site, 'portal_catalog')
    #portal_url=getToolByName(site, 'portal_url')
    #cities = [c.Title for c in cat(path=portal_url.getPortalPath()+'/portal_urban/streets/')]
    #streetsfolder=site.portal_urban.streets
    #filePath = '%s/streets.csv' % (context._profile_path)
    #fstreets=open (filePath, 'r')
    #for line in fstreets.readlines():
    #    items=line.split(';')
    #    if not items[2] in cities:
    #        streetsfolder.invokeFactory("City", id=items[2].lower(), title=items[2], zipCode=items[1])
    #        cities = [c.Title for c in cat(path=portal_url.getPortalPath()+'/portal_urban/streets/')]
    #    cityfolder=getattr(streetsfolder, items[2].lower())
    #    newStreet=cityfolder.invokeFactory("Street", id=site.generateUniqueId('Street'), streetName=items[0], streetCode=items[3])
    #fstreets.close()
    pass


def setDefaultValues(context):
    """
    Set some default values in the config
    """
    if context.readDataFile('urban_marker.txt') is None:
        return

    site = context.getSite()
    urban_tool = site.portal_urban

    #set default values for text fields
    for licencetype, defaulttexts in DefaultTexts.iteritems():
        licence_config = getattr(urban_tool, licencetype.lower())
        licence_config.setTextDefaultValues([{'text': text, 'fieldname': field} for field, text in defaulttexts.iteritems()])


def addDemoLicences(context):
    """
    Create one dummy licence of each type, and generate all their associated events and documents.
    """
    if context.readDataFile('urban_demo_marker.txt') is None:
        return

    site = context.getSite()
    urban_tool = site.portal_urban
    urban_folder = site.urban

    def getDummyValueForField(field, licence):
        if field.getName() in ['contributors', 'creators', 'language',
                               'effectiveDate', 'expirationDate', 'creation_date']:
            return None
        if field.type == 'boolean':
            return True
        elif field.type == 'string' or field.type == 'text' or field.type == 'lines':
            if hasattr(field, 'vocabulary') and field.vocabulary:
                if type(field.vocabulary) == str:
                    voc_list = getattr(licence, field.vocabulary)()
                else:
                    voc_list = field.vocabulary.getDisplayList(licence)
                if len(voc_list) > 1:
                    return voc_list[1]
                elif len(voc_list):
                    return voc_list[0]
            if field.type != 'lines':
                return '[%s XXX]' % field.getName()
        elif field.type == 'reference':
            if field.widget.startup_directory:
                ref_folder = site
                for directory in field.widget.startup_directory.split('/'):
                    ref_folder = getattr(ref_folder, directory)
                return [ref_folder.objectValues()[0]]
            elif field.widget.base_query:
                catalog = getToolByName(licence, 'portal_catalog')
                query = getattr(licence, field.widget.base_query)
                brains = catalog(query())
                if brains:
                    return [brains[0].getObject()]
        elif field.type == 'datagrid':
            dummy_value = {}
            for column_name in field.columns:
                column = field.widget.columns[column_name]
                if str(type(column)) == "<class 'Products.DataGridField.SelectColumn.SelectColumn'>":
                    dummy_value[column_name] = column.getVocabulary(licence)[0]
                elif str(type(column)) == "<class 'Products.DataGridField.Column.Column'>":
                    dummy_value[column_name] = '[%s XXX]' % column_name
            return tuple([dummy_value])
        elif field.type == 'integer':
            return 42
        elif field.type == 'datetime':
            return str(date.today())
        return None

    available_licence_types = {
        'BuildLicence': {
            'licenceSubject': "Exemple Permis Urbanisme",
            'contact_type': 'Applicant',
            'contact_data':  {
                'personTitle': 'masters', 'name1': 'Smith &', 'name2': 'Wesson',
                'street': 'Rue du porc dans le yaourt', 'number': '42', 'zipcode': '5032',
                'city': 'Couillet'
            },
        },
        'ParcelOutLicence': {
            'licenceSubject': "Exemple Permis d'urbanisation",
            'contact_type': 'Applicant',
        },
        'Declaration': {
            'licenceSubject': "Exemple Déclaration",
            'contact_type': 'Applicant',
        },
        'Division': {
            'licenceSubject': 'Exemple Division',
            'contact_type': 'Proprietary',
        },
        'UrbanCertificateOne': {
            'licenceSubject': 'Exemple Certificat Urbanisme 1',
            'contact_type': 'Proprietary',
        },
        'UrbanCertificateTwo': {
            'licenceSubject': 'Exemple Certificat Urbanisme 2',
            'contact_type': 'Proprietary',
        },
        'NotaryLetter': {
            'licenceSubject': 'Exemple Lettre de notaire',
            'contact_type': 'Proprietary',
        },
        'MiscDemand': {
            'licenceSubject': 'Exemple Demande diverse',
            'contact_type': 'Applicant',
        },
    }

    odt_files = []
    for licence_type, values in available_licence_types.iteritems():
        licence_folder = getattr(urban_folder, "%ss" % licence_type.lower())
        #create the licence
        licence_id = site.generateUniqueId('test_%s' % licence_type.lower())
        licence_folder.invokeFactory(licence_type, id=licence_id)
        logger.info('creating test %s' % licence_type)
        licence = getattr(licence_folder, licence_id)
        #fill each licence field with a dummy value
        logger.info('   test %s --> fill fields with dummy values' % licence_type)
        for field in licence.schema.fields():
            field_name = field.getName()
            mutator = field.getMutator(licence)
            if field_name in values.keys():
                mutator(values[field_name])
            elif field_name not in ['id', 'reference', 'contributors', 'creators', 'language', ]:
                field_value = getDummyValueForField(field, licence)
                if field_value:
                    mutator(field_value)
        licence.processForm()
        # add an applicant or a proprietary
        logger.info('   test %s --> add an applicant and a dummy parcel' % licence_type)
        contact_data = {
            'personTitle': 'mister', 'name1': '[Prénom XXX]', 'name2': '[Nom XXX]', 'street': '[Nom de rue XXX]',
            'number': '[n° XXX]', 'zipcode': '[code postal XXX]', 'city': '[Ville XXX]'
        }
        if 'contact_data' in values:
            contact_data = values['contact_data']
        licence.invokeFactory(values['contact_type'], id=site.generateUniqueId('contact'), **contact_data)
        # call post script
        licence.at_post_create_script()
        # add a dummy portion out
        portionout_data = {
            'divisionCode': '[code XX]', 'division': '[division XX]', 'section': '[section XX]', 'radical': '[radical XX]',
            'bis': '[bis XX]', 'exposant': '[exposant XX]', 'puissance': '[puissance XX]', 'partie': False
        }
        if 'portionout_data' in values:
            portionout_data = values['portionout_data']
        portionout_id = licence.invokeFactory('PortionOut', id=site.generateUniqueId('parcelle'), **portionout_data)
        portionout = getattr(licence, portionout_id)
        portionout._renameAfterCreation()
        licence.reindexObject(idxs=['parcelInfosIndex'])
        #generate all the urban events
        logger.info('   test %s --> create all the events' % licence_type)
        eventtype_uids = [brain.UID for brain in urban_tool.listEventTypes(licence, urbanConfigId=licence_type.lower())]
        for event_type_uid in eventtype_uids:
            urban_tool.createUrbanEvent(licence.UID(), event_type_uid)
        #fill each event with dummy values and generate all its documents
        logger.info('   test %s --> generate all the documents' % licence_type)
        for urban_event in licence.objectValues(['UrbanEvent', 'UrbanEventInquiry', 'UrbanEventOpinionRequest']):
            event.notify(ObjectInitializedEvent(urban_event))
            if urban_event.getPortalTypeName() == 'UrbanEventOpinionRequest':
                event.notify(EditBegunEvent(urban_event))
            #fill with dummy values
            for field in urban_event.schema.getSchemataFields('default'):
                field_name = field.getName()
                mutator = field.getMutator(urban_event)
                if field_name not in ['id', 'title']:
                    field_value = getDummyValueForField(field, urban_event)
                    if field_value:
                        mutator(field_value)
            #generate the documents
            if not urban_event.objectValues():
                for template in urban_event.getTemplates():
                    urban_tool.createUrbanDoc(template.UID(), urban_event.UID())
            odt_files.extend(urban_event.objectValues('ATBlob'))

    """#this part gathers all the documents generated in one archive
    import zipfile
    urban_docs = zipfile.ZipFile('urban_documents', 'a')
    for odtfile in odt_files:
        temp = open('temp', 'wb')
        temp.write(odtfile.data)
        temp.close()
        urban_docs.write('temp', odtfile.id)
    urban_docs.close()"""


def setupExtra(context):
    if context.readDataFile('urban_extra_marker.txt') is None:
        return

    portal = context.getSite()
    #Setting the user password policy
    if portal.validate_email:
        portal.validate_email = False
        logger.info('user password policy, aka validate_email, set to False')
    else:
        logger.info('user password policy unchanged')

    #we apply a method of CPUtils to configure CKeditor
    logger.info("Configuring CKeditor")
    try:
        from Products.CPUtils.Extensions.utils import configure_ckeditor
        if not hasattr(portal.portal_properties, 'ckeditor_properties') or portal.portal_properties.site_properties.default_editor != 'CKeditor':
            configure_ckeditor(portal, custom='urban')
            properties_tool = getToolByName(portal, 'portal_properties')
            custom_menu_style = u"[\n/* Styles Urban */\n{ name : 'Urban Body'\t\t, element : 'p', attributes : { 'class' : 'UrbanBody' } }, \n{ name : 'Urabn title'\t       , element : 'p', attributes : { 'class' : 'UrbanTitle' } }, \n{ name : 'Urabn title 2'\t, element : 'p', attributes : { 'class' : 'UrbanTitle2' } }, \n{ name : 'Urban title 3'\t, element : 'p', attributes : { 'class' : 'UrbanTitle3' } }, \n{ name : 'Urban address'\t, element : 'p', attributes : { 'class' : 'UrbanAddress' } }, \n{ name : 'Urban table'\t       , element : 'p', attributes : { 'class' : 'UrbanTable' } }, \n/* Block Styles */\n{ name : 'Grey Title'\t\t, element : 'h2', styles : { 'color' : '#888' } }, \n{ name : 'Grey Sub Title'\t, element : 'h3', styles : { 'color' : '#888' } }, \n{ name : 'Discreet bloc'\t, element : 'p', attributes : { 'class' : 'discreet' } }, \n/* Inline styles */\n{ name : 'Discreet text'\t, element : 'span', attributes : { 'class' : 'discreet' } }, \n{ name : 'Marker: Yellow'\t, element : 'span', styles : { 'background-color' : 'Yellow' } }, \n{ name : 'Typewriter'\t\t, element : 'tt' }, \n{ name : 'Computer Code'\t, element : 'code' }, \n{ name : 'Keyboard Phrase'\t, element : 'kbd' }, \n{ name : 'Sample Text'\t\t, element : 'samp' }, \n{ name : 'Variable'\t\t, element : 'var' }, \n{ name : 'Deleted Text'\t\t, element : 'del' }, \n{ name : 'Inserted Text'\t, element : 'ins' }, \n{ name : 'Cited Work'\t\t, element : 'cite' }, \n{ name : 'Inline Quotation'\t, element : 'q' }, \n{ name : 'Language: RTL'\t, element : 'span', attributes : { 'dir' : 'rtl' } }, \n{ name : 'Language: LTR'\t, element : 'span', attributes : { 'dir' : 'ltr' } }, \n/* Objects styles */\n{ name : 'Image on right'\t, element : 'img', attributes : { 'class' : 'image-right' } }, \n{ name : 'Image on left'\t, element : 'img', attributes : { 'class' : 'image-left' } }, \n{ name : 'Image centered'\t, element : 'img', attributes : { 'class' : 'image-inline' } }, \n{ name : 'Borderless Table'    , element : 'table', styles: { 'border-style': 'hidden', 'background-color' : '#E6E6FA' } }, \n{ name : 'Square Bulleted List', element : 'ul', styles : { 'list-style-type' : 'square' } }\n\n]\n"
            ckprops = properties_tool.ckeditor_properties
            ckprops.manage_changeProperties(menuStyles=custom_menu_style)

    except ImportError:
        pass

    #we add additional layers here because we take informations from portal_urban
    #that are set manually after install
    logger.info("Adding additional layers")
    portal_urban = getToolByName(portal, 'portal_urban')
    if not portal_urban:
        logger.error("Could not get the portal_urban tool!")
        return
    nis = portal_urban.getNISNum()
    if not nis:
        logger.error("No NIS defined in portal_urban!")
        return

    #we add the map coordinates
    if not portal_urban.getMapExtent() or portal_urban.getMapExtent().count(', ') != 3:
        dic = portal_urban.queryDB("SELECT (Xmin(ext.extent) ||', '|| Ymin(ext.extent)||', '|| Xmax(ext.extent)||', '|| Ymax(ext.extent)) as coord FROM (SELECT Extent(the_geom) FROM capa) AS ext;")
        if dic and 'coord' in dic[0]:
            portal_urban.setMapExtent(dic[0]['coord'])

    if not hasattr(portal_urban, "additional_layers"):
        logger.warning("No 'additonal_layers' folder found in portal_urban, we create it.")
        additional_layers_id = portal_urban.invokeFactory("Folder", id="additional_layers", title=_("additonal_layers_folder_title", 'urban', context=portal.REQUEST, default="Additional layers"))
        additional_layers = getattr(portal_urban, additional_layers_id)
        additional_layers.setConstrainTypesMode(1)
        additional_layers.setLocallyAllowedTypes(['Layer'])
        additional_layers.setImmediatelyAddableTypes(['Layer'])
    else:
        additional_layers = portal_urban.additional_layers

    if not hasattr(aq_base(additional_layers), 'ppnc'):
        additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://geoservercommon.communesplone.be/geoserver/gwc/service/wms", layers='PPNC', SRS="ESPG:31370", baseLayer=True, layerFormat="image/jpeg", visibility=False)
    """
        if portal_urban.getMapExtent():
            (xmin, ymin, xmax, ymax) = portal_urban.getMapExtent().split(', ')
            already_ppnc = False
            layers = PPNC_LAYERS.keys()
            layers.sort()
            for layer in layers:
                request = "SELECT Intersects(MakeBox2D(MakePoint(%f, %f), MakePoint(%f, %f)), MakeBox2D(MakePoint(%d, %d), MakePoint(%d, %d))) as intersect ;"%(float(xmin), float(ymin), float(xmax), float(ymax), PPNC_LAYERS[layer]['xmin'], PPNC_LAYERS[layer]['ymin'], PPNC_LAYERS[layer]['xmax'], PPNC_LAYERS[layer]['ymax'])
                dic = portal_urban.queryDB(request)
                if dic and dic[0].has_key('intersect') and dic[0]['intersect']:
                    if not already_ppnc:
                        additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers=layer, SRS="ESPG:31370", baseLayer=True, layerFormat="image/png")
                        already_ppnc = True
                        logger.info("Additional layer '%s' added with layer '%s'"%('ppnc', layer))
                    else:
                        logger.info("ALREADY found layer !")
                        additional_layers.invokeFactory("Layer", id=layer, title=layer.upper(), WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers=layer, SRS="ESPG:31370", baseLayer=True, layerFormat="image/png")
                        additional_layers.ppnc.setTitle(additional_layers.ppnc.getLayers().upper())
                        additional_layers.ppnc.reindexObject()
                        logger.info("Additional layer '%s' added with layer '%s'"%(layer, layer))

            if not hasattr(aq_base(additional_layers), 'ppnc'):
                logger.error("Additional layer '%s' added WITHOUT specific layer because no ppnc intersection found"%'ppnc')
                additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers='ppnc', SRS="ESPG:31370", baseLayer=True, layerFormat="image/png")
        else:
            logger.error("Additional layer '%s' not added because the mapExtent is not defined in portal_urban"%'ppnc')
    """
#Layers order
#PPNC
#Parcelles
#Rues
#Batiments
#N° parcelle
#N° maison
    if not hasattr(aq_base(additional_layers), 'parcelles'):
        additional_layers.invokeFactory("Layer", id="parcelles", title=u"Parcelles", layers="urban%s:capa" % nis, SRS="ESPG:31370", transparent=False, visibility=True, layerFormat="image/png")
        logger.info("Additional layer '%s' added" % 'parcelles')
    if not hasattr(aq_base(additional_layers), 'rues'):
        additional_layers.invokeFactory("Layer", id="rues", title=u"Nom des rues", layers="urban%s:toli" % nis, SRS="ESPG:31370", transparent=True, visibility=True, layerFormat="image/png")
        logger.info("Additional layer '%s' added" % 'rues')
    if not hasattr(aq_base(additional_layers), 'batiments'):
        additional_layers.invokeFactory("Layer", id="batiments", title=u"Bâtiments", layers="urban%s:cabu" % nis, SRS="ESPG:31370", transparent=True, visibility=True, layerFormat="image/png")
        logger.info("Additional layer '%s' added" % 'batiments')
    if not hasattr(aq_base(additional_layers), 'num_parcelle'):
        additional_layers.invokeFactory("Layer", id="num_parcelle", title=u"N° de parcelle", layers="urban%s:canu" % nis, styles="ParcelsNum", SRS="ESPG:31370", transparent=True, visibility=False, layerFormat="image/png")
        logger.info("Additional layer '%s' added" % 'num_parcelle')
    if not hasattr(aq_base(additional_layers), 'num_maisons'):
        additional_layers.invokeFactory("Layer", id="num_maisons", title=u"N° de maison", layers="urban%s:canu" % nis, styles="HousesNum", SRS="ESPG:31370", transparent=True, visibility=False, layerFormat="image/png")
        logger.info("Additional layer '%s' added" % 'num_maisons')


def setHTMLContentType(folder, fieldName):
    """
      Set the correct text/html content type for text/html TextFields
    """
    objs = folder.objectValues()
    for obj in objs:
        if hasattr(aq_base(obj), fieldName):
            obj.setContentType('text/html', fieldName)

##/code-section FOOT
