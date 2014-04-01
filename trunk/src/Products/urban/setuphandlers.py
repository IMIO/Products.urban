# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2014 by CommunesPlone
# Generator: ArchGenXML Version 2.7
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
from Products.urban.config import DefaultTexts
from zExceptions import BadRequest
from Products.urban.config import URBAN_TYPES
from Products.urban.utils import getAllLicenceFolderIds
from Products.urban.utils import getLicenceFolderId
from Products.urban.interfaces import ILicenceContainer, IContactFolder
from zope.interface import alsoProvides, directlyProvides
from zope.component import queryUtility
from zope.component import createObject
from zope.component.interface import getInterface
from zope.i18n.interfaces import ITranslationDomain
from zope import event
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import EditBegunEvent
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from exportimport import updateAllUrbanTemplates
from Products.urban.utils import generatePassword
from datetime import date
import pickle
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
        'EnvClassOne': 1,
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
    logger.info("addGlobalFolders : starting...")
    addGlobalFolders(context)
    logger.info("addGlobalFolders : Done")
    logger.info("addUrbanConfigFolders : starting...")
    addUrbanConfigFolders(context)
    logger.info("addUrbanConfigFolders : Done")
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
    logger.info("addUrbanVocabularies : starting...")
    addUrbanVocabularies(context)
    logger.info("addUrbanVocabularies : Done")
    logger.info("addDefaultObjects : starting...")
    addDefaultObjects(context)
    logger.info("addDefaultObjects : Done")
    logger.info("addEventTypesAndTemplates : starting...")
    addEventTypesAndTemplates(context)
    logger.info("addEventTypesAndTemplates : Done")
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
            if obj['id'] not in folder.objectIds():
                folder.invokeFactory(portal_type, **obj)


def createVocabularyFolder(container, folder_id, site, allowedtypes='UrbanVocabularyTerm', foldertype='Folder'):
    if folder_id not in container.objectIds():
        new_folder_id = container.invokeFactory(foldertype, id=folder_id, title=_("%s_folder_title" % folder_id, 'urban', context=site.REQUEST))
        new_folder = getattr(container, new_folder_id)
        setFolderAllowedTypes(new_folder, allowedtypes)
    else:
        new_folder = getattr(container, folder_id)
    return new_folder


def createVocabularyFolders(container, vocabularies, site):
    for vocname, voc in vocabularies.iteritems():
        allowedtypes = voc[0]
        createVocabularyFolder(container, vocname, site, allowedtypes)


def getSharedVocabularies(urban_type, licence_vocabularies):
    shared_vocs = licence_vocabularies.get('shared_vocabularies')
    vocabularies_to_return = {}
    for voc_name, voc in shared_vocs.iteritems():
        urban_types = voc[1]
        if urban_type in urban_types:
            voc_type = voc[0]
            voc_terms = voc[2:]
            vocabulary = [voc_type] + voc_terms
            vocabularies_to_return[voc_name] = vocabulary
    return vocabularies_to_return


def createVocabularies(container, vocabularies):
    for voc_name, vocabulary in vocabularies.iteritems():
        voc_folder = getattr(container, voc_name)
        createFolderDefaultValues(voc_folder, vocabulary)


def addUrbanConfigFolders(context):
    """
      Add the different urban configs
    """
    if context.readDataFile('urban_marker.txt') is None:
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
            config_folder_id = tool.invokeFactory("LicenceConfig", id=licenceConfigId, title=_("%s_urbanconfig_title" % urban_type.lower(), 'urban', context=site.REQUEST))
            config_folder = getattr(tool, config_folder_id)
            # no mutator available because the field is defined with 'read only' property
            config_folder.licencePortalType = urban_type
            config_folder.setUsedAttributes(config_folder.listUsedAttributes().keys())
            config_folder.reindexObject()
        else:
            config_folder = getattr(tool, licenceConfigId)
            config_folder.licencePortalType = urban_type
            config_folder.reindexObject()

        #we just created the urbanConfig, proceed with other parameters...
        #parameters for every LicenceConfigs
        #add UrbanEventTypes folder
        if not hasattr(aq_base(config_folder), 'urbaneventtypes'):
            newFolderid = config_folder.invokeFactory("Folder", id="urbaneventtypes", title=_("urbaneventtypes_folder_title", 'urban', context=site.REQUEST))
            newFolder = getattr(config_folder, newFolderid)
            setFolderAllowedTypes(newFolder, ['UrbanEventType', 'OpinionRequestEventType'])

        licence_vocabularies = default_values.get(urban_type, {})
        createVocabularyFolders(container=config_folder, vocabularies=licence_vocabularies, site=site)

        shared_vocabularies = getSharedVocabularies(urban_type, default_values)
        createVocabularyFolders(container=config_folder, vocabularies=shared_vocabularies, site=site)


def addUrbanVocabularies(context):
    """ Add the vocabularyTerm objects """
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')

    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.config_default_values' % profile_name
    attribute = 'default_values'
    module = __import__(module_name, fromlist=[attribute])
    default_values = getattr(module, attribute)
    vocabularies_with_HTML_description = getattr(module, 'vocabularies_with_HTML_description')

    global_vocabularies = default_values['global']
    createVocabularies(container=tool, vocabularies=global_vocabularies)

    conditions = getattr(tool, "exploitationconditions")
    #add the exploitation conditions subfolders
    addExploitationConditions(context, conditions)

    for urban_type in URBAN_TYPES:
        licenceConfigId = urban_type.lower()
        config_folder = getattr(tool, licenceConfigId)

        licence_vocabularies = default_values.get(urban_type, {})
        createVocabularies(container=config_folder, vocabularies=licence_vocabularies)

        shared_vocabularies = getSharedVocabularies(urban_type, default_values)
        createVocabularies(container=config_folder, vocabularies=shared_vocabularies)

        for voc_folder_id in config_folder.objectIds():
            if voc_folder_id in vocabularies_with_HTML_description:
                voc_folder = getattr(config_folder, voc_folder_id)
                setHTMLContentType(voc_folder, 'description')

        if urban_type in ['EnvClassOne', 'EnvClassTwo', 'EnvClassThree']:
            rubric_folder = getattr(config_folder, 'rubrics')
            mapping = {
                'EnvClassOne': '1',
                'EnvClassTwo': '2',
                'EnvClassThree': '3',
            }
            addRubricValues(context, [mapping[urban_type], ''], rubric_folder)


def addRubricValues(context, class_type, config_folder):

    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    pickled_dgrne_slurp = context.openDataFile('slurped_dgrne.pickle')
    dgrne_slurp = pickle.load(pickled_dgrne_slurp)

    categories = dgrne_slurp['main_rubrics']
    rubric_terms = dgrne_slurp['rubric_terms']
    mapping = dgrne_slurp['mapping']

    for category in categories:

        category_id = category['id']

        if category_id in config_folder.objectIds():
            rubric_folder = getattr(config_folder, category_id)
        else:
            rubricfolder_id = config_folder.invokeFactory("Folder", **category)
            rubric_folder = getattr(config_folder, rubricfolder_id)
            rubric_folder.setConstrainTypesMode(1)
            rubric_folder.setLocallyAllowedTypes(['EnvironmentRubricTerm'])
            rubric_folder.setImmediatelyAddableTypes(['EnvironmentRubricTerm'])

        rubrics = {}
        for r_id, rubric in rubric_terms.iteritems():
            # we add the rubric if it fits the category folder and if the
            # classtype match the licence class number
            if r_id.startswith(category_id) and rubric['extraValue'] in class_type:
                rubrics[r_id] = rubric
        sorted_rubrics = [rubrics[r_id] for r_id in sorted(rubrics)]

        for rubric in sorted_rubrics:

            rubric_id = rubric['id']
            if rubric_id not in rubric_folder:
                rubric_id = rubric_folder.invokeFactory('EnvironmentRubricTerm', **rubric)
            else:
                old_rubric = getattr(rubric_folder, rubric_id)
                rubric.pop('id')
                for fieldname, newvalue in rubric.iteritems():
                    field = old_rubric.getField(fieldname)
                    mutator = field.getMutator(old_rubric)
                    mutator(newvalue)

            bound_condition = mapping[rubric_id]
            if bound_condition:
                condition_type = bound_condition['type'].replace('/', '_').replace('-', '_')
                condition_id = bound_condition['id']
                condition_path = '/'.join(site.portal_urban.exploitationconditions.getPhysicalPath())
                condition_path = '%s/%s' % (condition_path, condition_type)
                condition = catalog(id=condition_id, path={'query': condition_path, 'depth': 1})[0]
                condition_uid = condition.getObject().UID()

                rubric = getattr(rubric_folder, rubric_id)
                rubric.setExploitationCondition(condition_uid)


def addExploitationConditions(context, config_folder):
    """ add sectorial and integral conditions vocabulary terms """

    site = context.getSite()
    pickled_dgrne_slurp = context.openDataFile('slurped_dgrne.pickle')
    dgrne_slurp = pickle.load(pickled_dgrne_slurp)

    all_conditions = dgrne_slurp['conditions']

    for condition_type, conditions in all_conditions.iteritems():
        conditionsfolder_id = condition_type.replace('/', '_').replace('-', '_')
        if conditionsfolder_id not in config_folder.objectIds():
            config_folder.invokeFactory(
                'Folder',
                id=conditionsfolder_id,
                title=_("%s_folder_title" % conditionsfolder_id, 'urban', context=site.REQUEST)
            )
            conditions_folder = getattr(config_folder, conditionsfolder_id)
            setFolderAllowedTypes(conditions_folder, 'UrbanVocabularyTerm')
        else:
            conditions_folder = getattr(config_folder, conditionsfolder_id)

        sorted_conditions = [conditions[c_id] for c_id in sorted(conditions)]

        for condition in sorted_conditions:
            condition_id = condition['id']
            if condition_id not in conditions_folder:
                condition_id = conditions_folder.invokeFactory('UrbanVocabularyTerm', extraValue=condition_type, **condition)
                vocterm = getattr(conditions_folder, condition_id)
                field = vocterm.getField('description')
                field.setContentType(vocterm, 'text/html')
                vocterm.setDescription(condition['description'])
            else:
                old_condition = getattr(conditions_folder, condition_id)
                condition.pop('id')
                for fieldname, newvalue in condition.iteritems():
                    field = old_condition.getField(fieldname)
                    mutator = field.getMutator(old_condition)
                    mutator(newvalue)



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

    licencesfolder_names = getAllLicenceFolderIds()

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
            # mark them with IContactFolder interface use some view methods, like 'getemails', on it
            directlyProvides(folder, IContactFolder)


def addGlobalFolders(context):
    """
    Add folders with properties used by several licence types
    """
    if context.readDataFile('urban_marker.txt') is None:
        return
    site = context.getSite()
    tool = site.portal_urban

    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.config_default_values' % profile_name
    attribute = 'default_values'
    module = __import__(module_name, fromlist=[attribute])
    default_values = getattr(module, attribute)

    vocabularies = default_values['global']
    createVocabularyFolders(container=tool, vocabularies=vocabularies, site=site)

    if not hasattr(tool, "globaltemplates"):
        templates_id = tool.invokeFactory("Folder", id="globaltemplates", title=_("globaltemplates_folder_title", 'urban', context=site.REQUEST))
        templates = getattr(tool, templates_id)
        templates.setConstrainTypesMode(1)
        templates.setLocallyAllowedTypes(['UrbanDoc', 'Folder'])
        templates.setImmediatelyAddableTypes(['UrbanDoc', 'Folder'])

    folder = tool.globaltemplates
    if not hasattr(folder, "urbantemplates"):
        templates_id = folder.invokeFactory("Folder", id="urbantemplates", title=_("urbantemplates_folder_title", 'urban', context=site.REQUEST))
        templates = getattr(folder, templates_id)
        templates.setConstrainTypesMode(1)
        templates.setLocallyAllowedTypes(['UrbanDoc'])
        templates.setImmediatelyAddableTypes(['UrbanDoc'])

    if not hasattr(folder, "environmenttemplates"):
        templates_id = folder.invokeFactory("Folder", id="environmenttemplates", title=_("environmenttemplates_folder_title", 'urban', context=site.REQUEST))
        templates = getattr(folder, templates_id)
        templates.setConstrainTypesMode(1)
        templates.setLocallyAllowedTypes(['UrbanDoc'])
        templates.setImmediatelyAddableTypes(['UrbanDoc'])

    if not hasattr(tool, "additional_layers"):
        additional_layers_id = tool.invokeFactory("Folder", id="additional_layers", title=_("additonal_layers_folder_title", 'urban', context=site.REQUEST))
        additional_layers = getattr(tool, additional_layers_id)
        additional_layers.setConstrainTypesMode(1)
        additional_layers.setLocallyAllowedTypes(['Layer'])
        additional_layers.setImmediatelyAddableTypes(['Layer'])

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

    #change the layout of the Plone site
    site.setLayout('redirectto_urban_root_view')

    if not hasattr(aq_base(site), "urban"):
        newFolderid = site.invokeFactory("Folder", id="urban", title=_("urban", 'urban', context=site.REQUEST))
        newFolder = getattr(site, newFolderid)
        newFolder.setLayout('urban_root_view')
    else:
        newFolder = getattr(site, 'urban')

    # Set INavigationRoot interface on urban folder so its considered as the root folder
    # in the navigation breadcrumb.
    navigationRootInterface = getInterface('', 'plone.app.layout.navigation.interfaces.INavigationRoot')
    alsoProvides(site.urban, navigationRootInterface)

    for urban_type in URBAN_TYPES:
        if not hasattr(newFolder, urban_type.lower() + 's'):
            licence_folder_id = getLicenceFolderId(urban_type)
            newFolderid = newFolder.invokeFactory(
                "Folder", id=licence_folder_id,
                title=_(urban_type, 'urban', context=site.REQUEST)
            )
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
                if urban_type in ['EnvClassOne', 'EnvClassTwo']:
                    newSubFolder.manage_permission('urban: Add EnvironmentLicence', ['Manager', 'Editor', ], acquire=0)

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

def addTestUsers(site):
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
    addTestUsers(site)
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
    # add global templates, default UrbanEventTypes and their templates for documents generation
    updateAllUrbanTemplates(context)


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
    catalog = getToolByName(site, 'portal_catalog')

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
                query = getattr(licence, field.widget.base_query)
                brains = catalog(query())
                if brains:
                    return [brains[0].getObject()]
        elif field.type == 'datagrid':
            dummy_value = {}
            for column_name in field.columns:
                column = field.widget.columns[column_name]
                if str(type(column)) == "<class 'Products.DataGridField.SelectColumn.SelectColumn'>":
                    vocabulary = column.getVocabulary(licence)
                    dummy_value[column_name] = vocabulary and vocabulary[0] or ('none', 'none')
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
            field_value = None
            if field_name == 'workLocations':
                field_value = ({'number': '42', 'street': catalog(portal_type='Street')[0].UID},)
            elif field_name != 'folderCategory' or field.vocabulary.getDisplayList(licence):
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
    division_code = division = str(urban_tool.findDivisions(all=False)[0]['da'])
    portionout_data = {
        'divisionCode': division_code, 'division': division, 'section': 'A', 'radical': '84',
        'exposant': 'C', 'partie': False
    }
    if 'portionout_data' in data:
        portionout_data = data['portionout_data']
    portionout_id = licence.invokeFactory('PortionOut', id=site.generateUniqueId('parcelle'), **portionout_data)
    portionout = getattr(licence, portionout_id)
    #portionout._renameAfterCreation()
    portionout.updateTitle()
    portionout.reindexObject()
    licence.reindexObject(idxs=['parcelInfosIndex'])
    #generate all the urban events
    logger.info('   test %s --> create all the events' % licence_type)
    eventtypes = [brain.getObject() for brain in urban_tool.listEventTypes(licence, urbanConfigId=licence_type.lower())]
    for event_type in eventtypes:
        licence.createUrbanEvent(event_type)
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
                createObject('GeneratedUrbanDoc', urban_event, template)
    return licence


def configurePMWSClientForUrban(context):
    """ set some default values for pm.wsclient """
    if context.readDataFile('urban_pm-wsclient_marker.txt') is None:
        return

    site = context.getSite()

    registry = getToolByName(site, 'portal_registry')

    view = site.restrictedTraverse('@@ws4pmclient-settings')
    connected = view._soap_connectToPloneMeeting()
    if not connected:
        registry['imio.pm.wsclient.browser.settings.IWS4PMClientSettings.pm_username'] = u'siteadmin'

        locality_name = registry.getPhysicalPath()[-2]
        pm_url = u'http://%s-pm.imio.be/ws4pm.wsdl' % locality_name
        registry['imio.pm.wsclient.browser.settings.IWS4PMClientSettings.pm_url'] = pm_url

    #we need to be connected to plonemeeting, else it will cause issues to display the config form
    if not connected:
        return 'you must set the plonemeeting user first'

    field_mappings = [
        {
            'expression': u'python:context.Title().upper()',
            'field_name': u'title'
        },
        {
            'expression': u'context/Title',
            'field_name': u'description'
        },
        {
            'expression': u'context/getDecisionText',
            'field_name': u'decision'
        }
    ]

    # validation on vocabulary cannot be done since we are not connected to plone meeting yet
    # dirty trick to skip validation
    from zope.schema._field import AbstractCollection
    old_validate = AbstractCollection._validate

    def _validate(self, value):
        return
    AbstractCollection._validate = _validate
    # dirty trick to skip validation end
    registry['imio.pm.wsclient.browser.settings.IWS4PMClientSettings.field_mappings'] = field_mappings

    action_condition = [
        {
            'pm_meeting_config_id': u'meeting-config-college',
            'condition': u'context/pm.wsclient/isDecisionCollegeEvent',
            'permissions': 'SOAP Client Send'
        }
    ]
    registry['imio.pm.wsclient.browser.settings.IWS4PMClientSettings.generated_actions'] = action_condition
    #restore validation
    AbstractCollection._validate = old_validate

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
        additional_layers_id = portal_urban.invokeFactory("Folder", id="additional_layers", title=_("additonal_layers_folder_title", 'urban', context=portal.REQUEST))
        additional_layers = getattr(portal_urban, additional_layers_id)
        additional_layers.setConstrainTypesMode(1)
        additional_layers.setLocallyAllowedTypes(['Layer'])
        additional_layers.setImmediatelyAddableTypes(['Layer'])
    else:
        additional_layers = portal_urban.additional_layers

    if not base_hasattr(additional_layers, 'orthophoto2009'):
        additional_layers.invokeFactory("Layer", id="orthophoto2009", title=u"Orthophoto2009", WMSUrl="http://geowebcache1.communesplone.be/geoserver/gwc/service/wms", layers='rw-2009-2010', SRS="ESPG:31370", baseLayer=True, layerFormat="image/jpeg", visibility=False)

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
