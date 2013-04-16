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
from Products.urban.config import PROJECTNAME
from Products.urban.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
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
    """hide tools"""
    if isNoturbanProfile(context): return
    # uncatalog tools
    site = context.getSite()
    toolnames = ['portal_urban']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
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
    if isNoturbanProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code

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
    #install the urbanskin if available
    #urbanskin should be installed before the call of 'adaptDefaultPortal'
    logger.info("installUrbanskin : starting...")
    installUrbanskin(context)
    logger.info("installUrbanskin : Done")
    logger.info("setDefaultApplicationSecurity : starting...")
    setDefaultApplicationSecurity(context)
    logger.info("setDefaultApplicationSecurity : Done")
    logger.info("addUrbanGroups : starting...")
    addUrbanGroups(context)
    logger.info("addUrbanGroups : Done")
    logger.info("adaptDefaultPortal : starting...")
    adaptDefaultPortal(context)
    logger.info("adaptDefaultPortal : Done")
    #refresh catalog after all these objects have been added...
    logger.info("Refresh portal_catalog : starting...")
    site.portal_catalog.refreshCatalog(clear=True)
    logger.info("Refresh portal_catalog : Done!")



##code-section FOOT
def _(msgid, domain, context):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default='')


def extraPostInstall(context, refresh=True):
    # all installation custom code not required for tests
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    site = context.getSite()
    logger.info("addUrbanConfigs : starting...")
    addUrbanConfigs(context)
    logger.info("addUrbanConfigs : Done")
    logger.info("addGlobalFolders : starting...")
    addGlobalFolders(context)
    logger.info("addGlobalFolders : Done")
    logger.info("addDefaultObjects : starting...")
    addDefaultObjects(context)
    logger.info("addDefaultObjects : Done")
    logger.info("addEventTypesAndTemplates : starting...")
    addEventTypesAndTemplates(context)
    logger.info("addEventTypesAndTemplates : Done")
    logger.info("addUrbanConfigsTopics : starting...")
    addUrbanConfigsTopics(context)
    logger.info("addUrbanConfigsTopics : Done")
    logger.info("addLicencesCollection: starting...")
    addLicencesCollection(context)
    logger.info("addLicencesCollection : Done")
    if refresh:
        #refresh catalog after all these objects have been added...
        logger.info("Refresh portal_catalog : starting...")
        site.portal_catalog.refreshCatalog(clear=True)
        logger.info("Refresh portal_catalog : Done!")


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


def createFolderDefaultValues(folder, objects_list, portal_type=''):
    """
     Create all the objects
    """
    if not portal_type:
        portal_type = objects_list[0]
    for obj in objects_list:
        if type(obj) is dict:
            folder.invokeFactory(portal_type, **obj)


def createFolderWithDefaultValues(container, folder_id, site, default_objects=[], portal_type='Folder', content_portal_type='', licence_type=''):
    """
    """
    newFolderid = container.invokeFactory(portal_type, id=folder_id, title=_("%s_folder_title" % folder_id, 'urban', context=site.REQUEST))
    newFolder = getattr(container, newFolderid)
    if not content_portal_type:
        if folder_id in default_objects:
            vocabulary_list = default_objects[folder_id]
            content_portal_type = vocabulary_list[0]
            if licence_type:
                if licence_type in vocabulary_list[1]:
                    vocabulary_list = vocabulary_list[1][licence_type]
                else:
                    return
            setFolderAllowedTypes(newFolder, content_portal_type)
            createFolderDefaultValues(newFolder, vocabulary_list, content_portal_type)
    else:
        setFolderAllowedTypes(newFolder, content_portal_type)
    return newFolder


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
            # no mutator available because the field is defined with 'read only' property
            configFolder.licencePortalType = urban_type
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
            createFolderWithDefaultValues(configFolder, 'townshipfoldercategories', site, default_values)

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
                createFolderWithDefaultValues(configFolder, 'articles', site, default_values)

        if urban_type == 'ParcelOutLicence':
            if not hasattr(aq_base(configFolder), 'lotusages'):
                createFolderWithDefaultValues(configFolder, 'lotusages', site, default_values)

            if not hasattr(aq_base(configFolder), 'equipmenttypes'):
                createFolderWithDefaultValues(configFolder, 'equipmenttypes', site, default_values)

        if urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter']:
            #we add the specific features folder
            if not hasattr(aq_base(configFolder), 'specificfeatures'):
                newFolder = createFolderWithDefaultValues(configFolder, 'specificfeatures', site, default_values)
                setHTMLContentType(newFolder, 'description')

            if not hasattr(aq_base(configFolder), 'roadspecificfeatures'):
                createFolderWithDefaultValues(configFolder, 'roadspecificfeatures', site, default_values)

            if not hasattr(aq_base(configFolder), 'locationspecificfeatures'):
                createFolderWithDefaultValues(configFolder, 'locationspecificfeatures', site, default_values)

            #we add the custom township specific features folder
            if not hasattr(aq_base(configFolder), 'townshipspecificfeatures'):
                createFolderWithDefaultValues(configFolder, 'townshipspecificfeatures', site, default_values)

            if not hasattr(aq_base(configFolder), 'opinionstoaskifworks'):
                #add "Ask opinions to in case of works" folder
                newFolder = createFolderWithDefaultValues(configFolder, 'opinionstoaskifworks', site, default_values)
                #now, we need to specify that the description's mimetype is 'text/html'
                setHTMLContentType(newFolder, 'description')

        if not hasattr(aq_base(configFolder), 'missingparts'):
            createFolderWithDefaultValues(configFolder, 'missingparts', site, default_values, licence_type=urban_type)

        if not hasattr(aq_base(configFolder), 'roadmissingparts'):
            createFolderWithDefaultValues(configFolder, 'roadmissingparts', site, default_values, licence_type=urban_type)

        if not hasattr(aq_base(configFolder), 'locationmissingparts'):
            createFolderWithDefaultValues(configFolder, 'locationmissingparts', site, default_values, licence_type=urban_type)

        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateTwo', 'EnvClassThree']:
            if not hasattr(aq_base(configFolder), 'foldermakers'):
                newFolder = createFolderWithDefaultValues(configFolder, 'foldermakers', site, default_values)
                #now, we need to specify that the description's mimetype is 'text/html'
                setHTMLContentType(newFolder, 'description')

        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateTwo']:
            if not hasattr(aq_base(configFolder), 'investigationarticles'):
                newFolder = createFolderWithDefaultValues(configFolder, 'investigationarticles', site, default_values)
                #now, we need to specify that the description's mimetype is 'text/html'
                setHTMLContentType(newFolder, 'description')

            if not hasattr(aq_base(configFolder), 'folderdelays'):
                createFolderWithDefaultValues(configFolder, 'folderdelays', site, default_values)

            if not hasattr(aq_base(configFolder), 'derogations'):
                createFolderWithDefaultValues(configFolder, 'derogations', site, default_values)

            if not hasattr(aq_base(configFolder), 'folderbuildworktypes'):
                createFolderWithDefaultValues(configFolder, 'folderbuildworktypes', site, default_values)

        if urban_type in ['BuildLicence', ]:
            #add PEB categories folder
            #this is done by a method because the migrateToUrban115
            #migration step will use it too
            addPEBCategories(context, configFolder)

        if urban_type in ['EnvClassThree', ]:
            if not hasattr(aq_base(configFolder), 'rubrics'):
                newFolderid = configFolder.invokeFactory("Folder", id="rubrics", title=_("rubrics_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                setFolderAllowedTypes(newFolder, 'Folder')
                addRubricValues(context, 3, newFolder)

            if not hasattr(aq_base(configFolder), 'inadmissibilityreasons'):
                createFolderWithDefaultValues(configFolder, 'inadmissibilityreasons', site, default_values)


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

    licencesfolder_names = [
        'buildlicences', 'parceloutlicences', 'declarations', 'divisions', 'urbancertificateones',
        'urbancertificatetwos', 'notaryletters', 'envclassthrees', 'miscdemands'
    ]
    #licence folder : "urban_readers" can read and "urban_editors" can edit...
    for folder_name in licencesfolder_names:
        if hasattr(app_folder, folder_name):
            folder = getattr(app_folder, folder_name)
            #we add a property usefull for portal_urban.getUrbanConfig
            try:
                #we try in case we apply the profile again...
                folder.manage_addProperty('urbanConfigId', folder_name.strip('s'), 'string')
            except BadRequest:
                pass
            folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
            folder.manage_addLocalRoles("urban_readers", ("Reader", ))
            folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))

    #objects application folder : "urban_readers" can read and "urban_editors" can edit...
    objectsfolder_names = ['architects', 'geometricians', 'notaries', 'parcellings']
    for folder_name in objectsfolder_names:
        if hasattr(app_folder, folder_name):
            folder = getattr(app_folder, folder_name)
            app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
            folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader", ))
            folder.manage_addLocalRoles("urban_readers", ("Reader", ))
            folder.manage_addLocalRoles("urban_editors", ("Editor", "Contributor"))


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

    if not hasattr(tool, "topics"):
        topicsFolder = createFolderWithDefaultValues(tool, 'topics', site, content_portal_type='Topic')
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

    if not hasattr(tool, "globaltemplates"):
        createFolderWithDefaultValues(tool, 'globaltemplates', site, content_portal_type='UrbanDoc')

    if not hasattr(tool, "foldermanagers"):
        createFolderWithDefaultValues(tool, 'foldermanagers', site, content_portal_type='FolderManager')

    if not hasattr(tool, "streets"):
        createFolderWithDefaultValues(tool, 'streets', site, default_values, content_portal_type='City')

    folder_names = ['pcas', 'pashs', 'folderroadtypes', 'folderprotectedbuildings',
                    'folderroadequipments', 'folderroadcoatings', 'folderzones', 'rcu', 'ssc']
    for folder_name in folder_names:
        if not hasattr(tool, folder_name):
            createFolderWithDefaultValues(tool, folder_name, site, default_values)

    if not hasattr(tool, "exploitationconditions"):
        conditions = createFolderWithDefaultValues(tool, 'exploitationconditions', site, content_portal_type='Folder')
    else:
        conditions = getattr(tool, "exploitationconditions")
    #add the exploitation conditions subfolders
    for folder_name in ['i_and_s_conditions', 'integralconditions', 'sectorialconditions']:
        if not hasattr(conditions, folder_name):
            createFolderWithDefaultValues(conditions, folder_name, site, content_portal_type='UrbanVocabularyTerm')
    if not hasattr(tool, "additional_layers"):
        createFolderWithDefaultValues(tool, 'additional_layers', site, content_portal_type='UrbanVocabularyTerm')

    folder_names = ['persons_titles', 'persons_grades', 'country', 'decisions', 'externaldecisions']
    for folder_name in folder_names:
        if not hasattr(tool, folder_name):
            createFolderWithDefaultValues(tool, folder_name, site, default_values)


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
            setFolderAllowedTypes(newSubFolder, urban_type)
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
        setFolderAllowedTypes(newSubFolder, 'Architect')
        newSubFolder.setLayout('architects_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains geometricians
    if not hasattr(newFolder, "geometricians"):
        newFolderid = newFolder.invokeFactory("Folder", id="geometricians", title=_("geometricians_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        setFolderAllowedTypes(newSubFolder, 'Geometrician')
        newSubFolder.setLayout('geometricians_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains notaries
    if not hasattr(newFolder, "notaries"):
        newFolderid = newFolder.invokeFactory("Folder", id="notaries", title=_("notaries_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        setFolderAllowedTypes(newSubFolder, 'Notary')
        newSubFolder.setLayout('notaries_folderview')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains parcellings
    if not hasattr(newFolder, "parcellings"):
        newFolderid = newFolder.invokeFactory("Folder", id="parcellings", title=_("parcellings_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        setFolderAllowedTypes(newSubFolder, 'ParcellingTerm')
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

    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.default_objects' % profile_name
    attribute = 'default_objects'
    module = __import__(module_name, fromlist=[attribute])
    default_objects = getattr(module, attribute)

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
        objects_list = default_objects['notaries']
        createFolderDefaultValues(notFolder, objects_list)
        logger.info("Notaries examples have been added")

    #add some geometricians...
    urbanFolder = getattr(site, "urban")
    geoFolder = getattr(urbanFolder, "geometricians")
    if not geoFolder.objectIds():
        objects_list = default_objects['geometricians']
        createFolderDefaultValues(geoFolder, objects_list)
        logger.info("Geometricians examples have been added")

    #add some parcellings...
    urbanFolder = getattr(site, "urban")
    parcelFolder = getattr(urbanFolder, "parcellings")
    if not parcelFolder.objectIds():
        objects_list = default_objects['parcellings']
        createFolderDefaultValues(parcelFolder, objects_list)
        logger.info("ParcellingTerms examples have been added")

    #add some folder managers
    tool = site.portal_urban
    fmFolder = getattr(tool, "foldermanagers")
    if not fmFolder.objectIds():
        objects_list = default_objects['foldermanagers']
        for obj in objects_list[1:]:
            obj.update({'manageableLicences': URBAN_TYPES})
        createFolderDefaultValues(fmFolder, objects_list)

    #create some streets using the Extensions.imports script
    if not tool.streets.objectIds('City'):
        from Products.urban.Extensions.imports import import_streets_fromfile, import_localities_fromfile
        import_streets_fromfile(tool)
        import_localities_fromfile(tool)


def addEventTypesAndTemplates(context):
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

    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.licences_data' % profile_name
    attribute = 'licences_data'
    module = __import__(module_name, fromlist=[attribute])
    licences_data = getattr(module, attribute)

    site = context.getSite()

    for licence_type, values in licences_data.iteritems():
        createLicence(site, licence_type, values)


def createLicence(site, licence_type, data):
    """
    """
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

    licence_folder = getattr(urban_folder, "%ss" % licence_type.lower())
    #create the licence
    licence_id = site.generateUniqueId('test_%s' % licence_type.lower())
    licence_folder.invokeFactory(licence_type, id=licence_id)
    logger.info('creating test %s' % licence_type)
    licence = getattr(licence_folder, licence_id)
    #fill each licence field with a dummy value
    logger.info('   test %s --> fill fields with dummy data' % licence_type)
    if type(data) is tuple:
        data = data[0]
    for field in licence.schema.fields():
        field_name = field.getName()
        mutator = field.getMutator(licence)
        if field_name in data.keys():
            mutator(data[field_name])
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
    if 'contact_data' in data:
        contact_data = data['contact_data']
    licence.invokeFactory(data['contact_type'], id=site.generateUniqueId('contact'), **contact_data)
    # call post script
    licence.at_post_create_script()
    # add a dummy portion out
    portionout_data = {
        'divisionCode': '[code XX]', 'division': '[division XX]', 'section': '[section XX]', 'radical': '[radical XX]',
        'bis': '[bis XX]', 'exposant': '[exposant XX]', 'puissance': '[puissance XX]', 'partie': False
    }
    if 'portionout_data' in data:
        portionout_data = data['portionout_data']
    portionout_id = licence.invokeFactory('PortionOut', id=site.generateUniqueId('parcelle'), **portionout_data)
    portionout = getattr(licence, portionout_id)
    portionout._renameAfterCreation()
    licence.reindexObject(idxs=['parcelInfosIndex'])
    #generate all the urban events
    logger.info('   test %s --> create all the events' % licence_type)
    eventtype_uids = [brain.UID for brain in urban_tool.listEventTypes(licence, urbanConfigId=licence_type.lower())]
    for event_type_uid in eventtype_uids:
        urban_tool.createUrbanEvent(licence.UID(), event_type_uid)
    #fill each event with dummy data and generate all its documents
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
    return licence


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
            custom_menu_style = u"[\n/* Styles Urban */\n{ name : 'Urban Body'\t\t, element : 'p', attributes : { 'class' : 'UrbanBody' } }, \n{ name : 'Urban title'\t       , element : 'p', attributes : { 'class' : 'UrbanTitle' } }, \n{ name : 'Urabn title 2'\t, element : 'p', attributes : { 'class' : 'UrbanTitle2' } }, \n{ name : 'Urban title 3'\t, element : 'p', attributes : { 'class' : 'UrbanTitle3' } }, \n{ name : 'Urban address'\t, element : 'p', attributes : { 'class' : 'UrbanAddress' } }, \n{ name : 'Urban table'\t       , element : 'p', attributes : { 'class' : 'UrbanTable' } }, \n/* Block Styles */\n{ name : 'Grey Title'\t\t, element : 'h2', styles : { 'color' : '#888' } }, \n{ name : 'Grey Sub Title'\t, element : 'h3', styles : { 'color' : '#888' } }, \n{ name : 'Discreet bloc'\t, element : 'p', attributes : { 'class' : 'discreet' } }, \n/* Inline styles */\n{ name : 'Discreet text'\t, element : 'span', attributes : { 'class' : 'discreet' } }, \n{ name : 'Marker: Yellow'\t, element : 'span', styles : { 'background-color' : 'Yellow' } }, \n{ name : 'Typewriter'\t\t, element : 'tt' }, \n{ name : 'Computer Code'\t, element : 'code' }, \n{ name : 'Keyboard Phrase'\t, element : 'kbd' }, \n{ name : 'Sample Text'\t\t, element : 'samp' }, \n{ name : 'Variable'\t\t, element : 'var' }, \n{ name : 'Deleted Text'\t\t, element : 'del' }, \n{ name : 'Inserted Text'\t, element : 'ins' }, \n{ name : 'Cited Work'\t\t, element : 'cite' }, \n{ name : 'Inline Quotation'\t, element : 'q' }, \n{ name : 'Language: RTL'\t, element : 'span', attributes : { 'dir' : 'rtl' } }, \n{ name : 'Language: LTR'\t, element : 'span', attributes : { 'dir' : 'ltr' } }, \n/* Objects styles */\n{ name : 'Image on right'\t, element : 'img', attributes : { 'class' : 'image-right' } }, \n{ name : 'Image on left'\t, element : 'img', attributes : { 'class' : 'image-left' } }, \n{ name : 'Image centered'\t, element : 'img', attributes : { 'class' : 'image-inline' } }, \n{ name : 'Borderless Table'    , element : 'table', styles: { 'border-style': 'hidden', 'background-color' : '#E6E6FA' } }, \n{ name : 'Square Bulleted List', element : 'ul', styles : { 'list-style-type' : 'square' } }\n\n]\n"
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
