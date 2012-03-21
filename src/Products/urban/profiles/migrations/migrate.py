# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from zope.interface import alsoProvides
from zope import event

from Acquisition import aq_base

from Products.CMFPlone.utils import base_hasattr
from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator, InplaceATItemMigrator
from Products.urban.events.urbanEventInquiryEvents import setLinkedInquiry
from Products.urban.events.urbanEventEvents import setEventTypeType, setCreationDate
from Products.urban.interfaces import ILicenceContainer
from Products.urban.utils import getMd5Signature
from Products.urban.config import GLOBAL_TEMPLATES, URBAN_TYPES
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFPlone.utils import safe_hasattr
from re import search

logger = logging.getLogger('urban: migrations')

def isNoturbanMigrationsProfile(context):
    return context.readDataFile("urban_migrations_marker.txt") is None

def migrateToPlone4(context):
    """
      Launch every migration steps linked to the Plone4 version
    """
    if isNoturbanMigrationsProfile(context): return

    #remove useless attribute 'usePloneTask'
    migrateTool(context)
    #remove the 'format' attribute as it is replaced now by layerFormat
    #because the name 'format' for a field is problematic...
    migrateFormatFieldFromLayers(context)
    #this field is now a DataGridField
    migrateRoadEquipments(context)
    #delays were UrbanVocabularyTerms, now they are UrbanDelays
    migrateFolderDelays(context)
    #before, BuildLicence.annoncedDelay was UrbanVocabularyTerms, now they are UrbanDelays
    migrateAnnoncedDelays(context)
    #we have now PersonTitleTerms instead of UrbanVocabularyTerms to manage persons titles
    migratePersonTitles(context)
    #remove useless fields 'termKey' and 'termKeyStr'
    migrateUrbanVocabularyTerms(context)
    #workLocations object disappeared, we now use a workLocations DataGridField
    migrateToWorkLocationsDataGridField(context)
    #we replace licence folders from portal_urban to LicenceConfig objects
    migrateToLicenceConfig(context)
    #we replace architect objects (based on Architect meta_type) by new objects (based on Contact meta_type)
    migrateArchitectToContact(context)
    #migration of contact type objects to provides specific interfaces
    migrateSpecificContactInterfaces(context)
    #migration of UrbanEvents with id 'enquete-publique' to UrbanEventinquiry
    migrationToUrbanEventInquiries(context)
    #remove 'eventDate' from UrbanEventType.activatedFields
    migrateUrbanEventTypes(context)
    #add md5Signature and profileName properties for each template
    addMd5SignatureAndProfileNameProperties(context)
    #every folder that will contain licences need to provide ILicenceContainer
    migrateLicenceContainers(context)
    #migration of Event objects to provides marker interfaces
    provideEventMarkerInterfaces(context)
    #get rid of the Proprietary portal_type, we use Applicant
    migrationProprietaryToContact(context)
    #migration of Layers
    #migrateLayersForMapfish(context) #no more needeed
    #migrate the foldermakers UrbanVocabularyTerms to allow them to link an UrbanEventType
    migrateFoldermakersTerms(context)
    #Move all the FolderManager objects into a single folder at the root of urban config
    migrateFoldermanagers(context)
    #some templates where defined as attributes on the tool, now we store them in a specific folder
    migrateGlobalTemplates(context)
    #Some folders defined on LicenceConfigs are now at the portal_urban root
    migrateSomeLocalFoldersAsGlobal(context)
    #Before, there was several xxxSubject fields, now we use licenceSubject
    migrateSubjectFields(context)
    #Declarations need an extra value to be defined on UrbanVocabularyTerms in portal_urban.decisions
    migrateDecisionsForDeclarations(context)
    #some UrbanVocabularyTerms have been added afterward, we need to add them now
    addMissingUrbanVocabularyTerms(context)
    #Divisions used a 'comments' field that is now replaced by the default 'description' field
    migrateDivisionsCommentsToDescription(context)
    #Migrate the foldermanager references
    #migrateFoldermanagersReferenceField(context) #no more needed
    #Migrate the tal expression in the UrbanEvenType of opinions request
    migrateOpinionRequestTalExpression(context)
    #Update all the templates
    #We must run this step separately, to keep log inside portal_setup
    #updateUrbanTemplates(context)

def migrateToWorkLocationsDataGridField(context):
    """
      Migrate Declaration, Division, EnvironmentalDeclaration, UbranCertificateOne,
      UrbanCertificateTwo, BuildLicence, ParcelOutLicence types to use workLocations DataGridField
      instead of workLocation objects
    """
    if isNoturbanMigrationsProfile(context):
        return

    site = context.getSite()

    brains = site.portal_catalog(portal_type = ['BuildLicence', 'Declaration',
                    'Division', 'EnvironmentalDeclaration', 'UrbanCertificateOne',
                    'UrbanCertificateTwo', 'ParcelOutLicence'])
    count = 0
    for brain in brains:
        locations = []
        objectToDeleteIds = []
        obj = brain.getObject()
        for previousWorkLocation in obj.objectValues('WorkLocation'):
            dict = {}
            street = previousWorkLocation.getStreet()
            streetUID = ''
            if street:
                streetUID = street.UID()
            dict['street'] = streetUID
            dict['number'] = previousWorkLocation.getNumber()
            locations.append(dict)
            objectToDeleteIds.append(previousWorkLocation.getId())
        if objectToDeleteIds:
            #remove old WorkLocation objects
            obj.manage_delObjects(objectToDeleteIds)
            #set the new workLocations
            obj.setWorkLocations(locations)
            count += 1
    logger = context.getLogger('migrateToWorkLocationsDataGridField (replacing WorkLocation object by datagrid field)')
    logger.info(" %d licences migrated"%count)

def migrateToContact(context):
    """
      More portal_types are now based on Contact.  Migrate old instances
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    brains = site.portal_catalog(portal_type=["Applicant", "Proprietary", "Notary", ])
    
    for brain in brains:
        obj = brain.getObject()
        if obj.meta_type == "Contact":
            continue
        data = {
                'personTitle': obj.getPersonTitle(),
                'name1': obj.getName1(),
                'name2': obj.getName2(),
                'society': obj.getSociety(),
                'street': obj.getStreet(),
                'number': obj.getNumber(),
                'zipcode': obj.getZipcode(),
                'city': obj.getCity(),
                'email': obj.getEmail(),
                'phone': obj.getPhone(),
                'fax': obj.getFax(),
                'nationRegister': obj.getNationalRegister(),
               }
        parent = obj.aq_inner.aq_parent
        oldId = obj.getId()
        oldPortalType = obj.portal_type
        newId = parent.invokeFactory(type_name=oldPortalType, id=oldId + '_new', **data)
        newObj = getattr(parent, newId)
        #keep references for Notary
        if oldPortalType == "Notary":
            brefs = obj.getBRefs()
            for bref in brefs:
                bref.setNotaryContact(newObj)
        newObj.reindexObject()
        #remove the old object
        parent.manage_delObjects(oldId)

def migrateToMultiStreets(context):
    """
      Migrate to multiple addresses.  Remove existing workLocation and
      workLocationHouseNumber attributes and create a primary WorkLocation
      instead
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')
    reference_catalog = getToolByName(site, 'reference_catalog')

    types_to_migrate = ['BuildLicence', 'ParcelOutLicence', 'Declaration',\
                        'Division', 'NotaryLetter', 'UrbanCertificateOne',\
                        'UrbanCertificateTwo', 'EnvironmentalDeclaration', ]

    brains = site.portal_catalog(portal_type=types_to_migrate)
    for brain in brains:
        obj = brain.getObject()
        #in case we run this script several time, check that the current
        #element has not already been converted
        if not hasattr(obj, 'workLocationHouseNumber'):
            continue
        #else, proceed : add a primary WorkLocation and remove no more used attributes
        #get the street...
        objuid = obj.UID()
        refbrain = reference_catalog(relationship='street', sourceUID=objuid)
        #if we did not found the street, we continue to the next element
        if not refbrain:
            continue
        workLocationStreetObj = refbrain[0].getObject().getTargetObject()
        workLocationNumber = obj.workLocationHouseNumber
        normalizedNumber = site.plone_utils.normalizeString(workLocationNumber)
        id = "%s-%s" % (workLocationStreetObj.getId(), normalizedNumber)
        i = 1
        while id in obj.objectIds():
            id = "%s-%d" % (id, i)
            i = i + 1
        data = {
                'street': workLocationStreetObj,
                'number': workLocationNumber,
                'isSupplementary': False,
                }
        newId = obj.invokeFactory("WorkLocation", id=id, **data)
        newObj = getattr(obj, newId)
        newObj.at_post_create_script()

        #the workLocation attribute was a ReferenceField
        delattr(obj, 'workLocationHouseNumber')
        logger.info('%s element is now multiple addresses aware' % portal_url.getRelativeUrl(obj))

def migrateWorkLocation(context):
    """
      Migrate the workLocation attribute.  Check if a workLocation street is
      already selected and remove old workLocationStreet, workLocationZipCode
      and workLocationCity attributes
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')

    brains = site.portal_catalog(portal_type="BuildLicence")
    for brain in brains:
        obj = brain.getObject()
        #in case we run this script several time, check that the current
        #BuildLicence has not already been converted
        if not hasattr(obj, 'workLocationStreet'):
            continue
        #else, proceed and remove no more used attributes
        delattr(obj, 'workLocationStreet')
        delattr(obj, 'workLocationZipCode')
        delattr(obj, 'workLocationCity')
        logger.info('%s workLocation* attributes have been migrated' % portal_url.getRelativeUrl(obj))

def migratePersonTitle(context):
    """
      personTitle was hardcoded in french on Contacts...  Map old values to new...
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    mapping = {
               'Madame':'madam',
               'Monsieur':'mister',
               'Mademoiselle':'miss',
               'Monsieur et Madame':'madam_and_mister',
               'Maître':'master',
              }
    portal_catalog = getToolByName(site, 'portal_catalog')
    brains = portal_catalog(portal_type=('Applicant', 'Architect',))
    for brain in brains:
        obj = brain.getObject()
        personTitle = obj.getPersonTitle()
        for key in mapping.keys():
            if key == personTitle:
                obj.setPersonTitle(mapping[key])
                logger.info('%s personTitle attribute has been migrated to %s' % (site.portal_url.getRelativeUrl(obj), key))
                obj.reindexObject()

def migrateFolderZone(context):
    """
      folderZone is now multiValued
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_catalog = getToolByName(site, 'portal_catalog')
    brains = portal_catalog(portal_type=('BuildLicence', 'ParcelOutLicence',))
    for brain in brains:
        obj = brain.getObject()
        fz = obj.folderZone
        obj.setFolderZone((fz,))
        logger.info("%s's folder zone has been migrated" % obj.Title())

def migrateBuildLicencesInvestigationArticles(context):
    """
      investigationArticles is now a MultiSelection and replace
      both investigationArticle and investigationPoint fields
      We only care about default 330/1 to 330/13
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    #first, be sure that we have the right defined values in the configuration
    if not hasattr(site.portal_urban.buildlicence, 'investigationarticles'):
        from Products.urban.setuphandlers import addInvestigationArticles
        addInvestigationArticles(context, site.portal_urban.buildlicence)

    portal_catalog = getToolByName(site, 'portal_catalog')
    brains = portal_catalog(portal_type=('BuildLicence','ParcelOutLicence'))
    for brain in brains:
        obj = brain.getObject()
        if not hasattr(obj, 'investigationArticle'):
            continue
        article = obj.investigationArticle
        point = obj.investigationPoint
        if point and article == 330:
            obj.setInvestigationArticles(('330-%s' % str(point),))
        #remove old useless fields
        delattr(obj, 'investigationArticle')
        delattr(obj, 'investigationPoint')
        logger.info("%s's investigation article has been migrated" % obj.Title())

def migrateUrbanEventTypes(context):
    """
      Migrate the UrbanEventTypes :
      - remove the 'urbanType' attribute
      - remove 'eventDate' from activatedFields if needed
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')

    brains = site.portal_catalog(portal_type="UrbanEventType")
    for brain in brains:
        obj = brain.getObject()
        #in case we run this script several time, check that the current
        #BuildLicence has not already been converted
        if hasattr(obj, 'urbanType'):
            delattr(obj, 'urbanType')
            logger.info("The 'urbanType' attribute has been removed from %s" % portal_url.getRelativeUrl(obj))
        activatedFields = list(obj.getActivatedFields())
        if 'eventDate' in activatedFields:
            activatedFields.remove('eventDate')
            obj.setActivatedFields(activatedFields)
            logger.info("'eventDate' has been removed from the activatedFields of %s" % portal_url.getRelativeUrl(obj))

def addMissingUrbanVocabularyTerms(context):
    """
      Some UrbanVocabularyTerms have been added afterward, we need to add them now
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    logger.info("Adding missing UrbanVocabularyTerms : starting...")

    #list of sublists of two elements
    #first element is the folder to add the element in
    #second element is a dict containing the informations about the element to add
    termsToAdd = (
                  (site.portal_urban.buildlicence.missingparts, {'id': 'peb', 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"}),
                  (site.portal_urban.folderprotectedbuildings, {'id': 'certificatpatrimoine', 'title': u"certificat de patrimoine délivré"}),
                  (site.portal_urban.folderzones, {'id': 'zhcrza', 'title': u"zone d’habitat à caractère rural sur +/- 50 m et le surplus en zone agricole"}),
                 )

    for destFolder, data in termsToAdd:
        if not hasattr(destFolder, data['id']):
            destFolder.invokeFactory("UrbanVocabularyTerm", **data)
            logger.info("Added a missing UrbanVocabularyTerm '%s' in '%s'" % (data['id'], '/'.join(destFolder.getPhysicalPath())))
        else:
            logger.info("'%s' already exists in '%s'" % (data['id'], '/'.join(destFolder.getPhysicalPath())))
    logger.info("Adding missing UrbanVocabularyTerms : done!")

def migrateFolderDelays(context):
    """
      Delays were UrbanVocabularyTerms, now they are UrbanDelays
    """
    #walk into every UrbanConfigs and look for a 'folderdelays' folder
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    logger.info("Migrating folderdelays : starting...")
    #look in every UrbanConfigs
    for urbanConfig in tool.objectValues('ATFolder'):
        #check if a "folderdelays" folder exists
        if hasattr(aq_base(urbanConfig), 'folderdelays'):
            folderdelays = getattr(urbanConfig, 'folderdelays')
            folderdelays.setConstrainTypesMode(1)
            folderdelays.setLocallyAllowedTypes(['UrbanDelay'])
            folderdelays.setImmediatelyAddableTypes(['UrbanDelay'])
            for urbanVocTerm in folderdelays.objectValues('UrbanVocabularyTerm'):
                termKey = ''
                if hasattr(urbanVocTerm, 'termKey'):
                    termKey = getattr(urbanVocTerm, 'termKey')
                data = {
                        'id': urbanVocTerm.getId(),
                        'title': urbanVocTerm.Title(),
                        'deadLineDelay': termKey,
                        }
                if not isinstance(data['deadLineDelay'], int):
                    data['deadLineDelay'] = 0
                #remove the old object before creating the new
                folderdelays.manage_delObjects(data['id'])
                newObjId = folderdelays.invokeFactory('UrbanDelay', **data)
                newObj = getattr(folderdelays, newObjId)
                logger.info("UrbanVocabularyTerm at '%s' has been migrated" % newObj.absolute_url())
    logger.info("Migrating folderdelays : do not forget to adapt the alert delay on migrated elements!")
    logger.info("Migrating folderdelays : done!")

def migrateTopicsAddPathCriterion(context):
    """
      We need some topics to have a path criterion now, so add it if necessary
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    catalog = getToolByName(site, 'portal_catalog')
    portal_urban = getToolByName(site, 'portal_urban')
    #find the topics
    brains = catalog(path='/'.join(portal_urban.getPhysicalPath()), portal_type='Topic')
    topicsToAdaptIds = ['searchalllicences', 'searchinprogresslicences', 'searchretiredlicences', 'searchincompletelicences', 'searchacceptedlicences', 'searchrefusedlicences', ]
    for brain in brains:
        if brain.id in topicsToAdaptIds:
            topic = brain.getObject()
            #check if the criterion is already there
            if not 'crit__path_ATPathCriterion' in topic.objectIds():
                criterion = topic.addCriterion(field='path', criterion_type='ATPathCriterion')
                criterion.setValue(['',])

def migrateTool(context):
    """
        Necessary adaptations about portal_urban
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    try:
        delattr(tool, 'usePloneTask')
        logger.info("The 'usePloneTask' attribute has been removed from portal_urban")
    except AttributeError:
        logger.info("The 'usePloneTask' attribute does not exist on portal_urban!")

def migrateFormatFieldFromLayers(context):
    """
        The field named 'format' on content_type Layer has been renamed to layerFormat
        The problem is that it was never stored, so always empty
        This migration just delete the atribute so...
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    for layer in tool.additional_layers.objectValues('Layer'):
        try:
            delattr(layer, 'format')
            logger.info("The layer '%s' format's attribute has been removed" % layer.getId())
        except AttributeError:
            logger.info("The layer '%s' has no 'format' attribute!" % layer.getId())

def migrateRoadEquipments(context):
    """
        This field is now a DataGridField
    """
    if isNoturbanMigrationsProfile(context): return

    from types import DictType

    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    #adapt the roadEquipments field
    brains = catalog(portal_type=('BuildLicence', 'ParcelOutLicence',))
    for brain in brains:
        obj = brain.getObject()
        roadEquipments = obj.getRoadEquipments()
        #data was stored as a list, now it is a list of dict...
        if roadEquipments and not isinstance(roadEquipments[0], DictType):
            #migrate data
            res = []
            for roadEquipment in roadEquipments:
                dict = {}
                dict['road_equipment'] = roadEquipment
                dict['road_equipment_details'] = ''
                res.append(dict)
            obj.setRoadEquipments(res)
            logger.info("The roadEquipments for '%s' has been migrated" % obj.getId())
        else:
            logger.info("The roadEquipments for '%s' was already migrated!" % obj.getId())

def migrateAnnoncedDelays(context):
    """
        Before, BuildLicence.annoncedDelay was UrbanVocabularyTerms, now they are UrbanDelays
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    catalog = getToolByName(site, 'portal_catalog')
    tool = getToolByName(site, 'portal_urban')
    #adapt the annoncedDelay field
    portalTypesToConsider = ('BuildLicence', 'ParcelOutLicence',)
    for portalTypeToConsider in portalTypesToConsider:
        brains = catalog(portal_type=portalTypeToConsider)
        urbanConfigId = portalTypeToConsider.lower()
        urbanConfig = getattr(tool, urbanConfigId)
        delays = urbanConfig.folderdelays.objectValues('UrbanDelay')
        for brain in brains:
            obj = brain.getObject()
            annoncedDelay = obj.getAnnoncedDelay()
            #before, the saved value was a digit (an integer in a string)
            if annoncedDelay.isdigit():
                #get the corresponding UrbanDelay
                for delay in delays:
                    if str(delay.getDeadLineDelay()) == str(annoncedDelay):
                        #adapt the annoncedDelay
                        obj.setAnnoncedDelay(delay.getId())
                        logger.info("The annoncedDelay for '%s' has been migrated" % obj.getId())

def migratePersonTitles(context):
    """
        personTitles are now defined in the configuration as PersonTitleTerms, before it was UrbanVocabularyTerms
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    personTitlesFolder = site.portal_urban.persons_titles
    personTitlesFolder.setConstrainTypesMode(1)
    personTitlesFolder.setLocallyAllowedTypes(['PersonTitleTerm'])
    personTitlesFolder.setImmediatelyAddableTypes(['PersonTitleTerm'])
    logger.info("Migrating persontitles: starting...")
    for personTitle in personTitlesFolder.objectValues('UrbanVocabularyTerm'):
        data = {
                'id': personTitle.getId(),
                'title': personTitle.Title(),
                'abbreviation': personTitle.termKeyStr,
                }
        #remove the old object before creating the new
        personTitlesFolder.manage_delObjects(data['id'])
        newObjId = personTitlesFolder.invokeFactory('PersonTitleTerm', **data)
        newObj = getattr(personTitlesFolder, newObjId)
        logger.info("UrbanVocabularyTerm at '%s' has been migrated to PersonTitleTerm" % newObj.absolute_url())
    logger.info("Migrating persontitles: done!")

def migrateUrbanVocabularyTerms(context):
    """
        Remove useless 'termKey' and 'termKeyStr' fields
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    brains = site.portal_catalog(portal_type = ['UrbanVocabularyTerm',])
    logger.info("Migrating UrbanVocabularyTerms: starting...")
    for brain in brains:
        term = brain.getObject()
        migrated = False
        if hasattr(term, 'termKey'):
            delattr(term, 'termKey')
            migrated = True
        if hasattr(term, 'termKeyStr'):
            delattr(term, 'termKeyStr')
            migrated = True
        if migrated:
            logger.info("UrbanVocabularyTerm at '%s' has been migrated" % term.absolute_url())
    logger.info("Migrating UrbanVocabularyTerms: done!")

def migrateToLicenceConfig(context):
    """
        We replace licence folders from portal_urban to LicenceConfig objects
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    logger.info("Migrating to LicenceConfigs: starting...")
    for urban_type in URBAN_TYPES:
        lcid = urban_type.lower()
        if not base_hasattr(tool, lcid):
            continue
        fid = "%s-old"%lcid
        oldobj = getattr(tool, lcid)
        #we skip if urbanconfig isn't more Folder
        if oldobj.getPortalTypeName() != 'Folder':
            continue
        #we rename existing folder
        oldobj.setId(fid)
        oldobj.reindexObject()
        #we create a LicenceConfig with same id and title
        lcid = tool.invokeFactory("LicenceConfig", id=lcid, title=oldobj.Title())
        lcobj = getattr(tool, lcid)
        lcobj.licence_portal_type = urban_type
        #lcobj.setUsedAttributes(lcobj.listUsedAttributes().keys())   #no optional fields selected !
        #lcobj.reindexObject()
        #we move the content of original folder to the LicenceConfig obj
        ids = oldobj.contentIds()
        cutdata = oldobj.manage_cutObjects(ids)
        lcobj.manage_pasteObjects(cutdata)
        #we delete old folder
        tool.manage_delObjects(ids=[fid])
        logger.info("LicenceConfig '%s' has been migrated" % urban_type)
    logger.info("Migrating to LicenceConfigs: done!")

def migrateArchitectToContact(context):
    """
        We replace architect objects (based on Architect meta_type) by new objects (based on Contact meta_type)
    """
    if isNoturbanMigrationsProfile(context): return
    portal = context.getSite()
    architect_folder = portal.urban.architects
    #from plone.app.referenceintegrity.config import DisableRelationshipsProtectionTemporarily
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    logger.info("Migrating Architects to Contacts: starting...")
    architects = architect_folder.objectValues('Architect')
    lenArchitects = len(architects)
    i = 0
    for architect in architects:
        i = i + 1
        #first we create a new architect
        logger.info("Migrating Architect %d/%d" % (i, lenArchitects))
        attribs = {
            'title': architect.Title(),
            'personTitle' : architect.getPersonTitle(),
            'name1' : architect.getName1(),
            'name2' : architect.getName2(),
            'society' : architect.getSociety(),
            'street' : architect.getStreet(),
            'number' : architect.getNumber(),
            'zipcode' : architect.getZipcode(),
            'city' : architect.getCity(),
            'email' : architect.getEmail(),
            'phone' : architect.getPhone(),
            'fax' : architect.getFax(),
            'nationalRegister' : architect.getNationalRegister(),
            'representedBy' : architect.getRepresentedBy(),
        }
        id = architect.getId()
        architect.setId("%s-old"%id)
        architect_folder.invokeFactory("Architect", id=id, **attribs)
        contact = getattr(architect_folder, id)
        #secondly we search and adapt licences referencing the architect
        licences = architect.getBRefs()
        for licence in licences:
            ref_architects = licence.getArchitects()
            try:
                i = ref_architects.index(architect)
                ref_architects[i] = contact
                licence.setArchitects(ref_architects)
                licence.reindexObject()
            except ValueError, msg:
                logger.error("Error on licence '%s' when searching architect '%s', msg='%s'"%(licence.Title(), architect.Title(),msg))
        #endly we remove the original architect and replace id of the new one
        #with DisableRelationshipsProtectionTemporarily(['licenceArchitects']):
        architect_folder.manage_delObjects(ids=["%s-old"%id])
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    logger.info("Migrating Architects to Contacts: done!")

def migrateSpecificContactInterfaces(context):
    """
        Migration of contact type objects to provides specific interfaces
    """
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating Specific Contact interfaces: starting...")

    from Products.urban.interfaces import CONTACT_INTERFACES
    portal = context.getSite()
    brains = portal.portal_catalog(portal_type = CONTACT_INTERFACES.keys())
    for brain in brains:
        contact = brain.getObject()
        if not contact.__provides__(CONTACT_INTERFACES[brain.Type]):
            alsoProvides(contact, CONTACT_INTERFACES[brain.Type])
            contact.reindexObject(['object_provides'])
    logger.info("Migrating Specific Contact interfaces: done!")

class UrbanEventToUrbanEventInquiryMigrator(object, InplaceATFolderMigrator):
    """
      Migrate the UrbanEvent having an id of 'enquete-publique'
      to UrbanEventInquiries
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanEvent"
    src_portal_type = "UrbanEvent"
    dst_meta_type = "UrbanEventInquiry"
    dst_portal_type = "UrbanEventInquiry"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)

    def custom(self):
        """
          Events are not raised, we need to call them manually
        """
        setLinkedInquiry(self.new, '')
        setEventTypeType(self.new, '')
        setCreationDate(self.new, '')

def migrationToUrbanEventInquiries(context):
    """
      Call UrbanEventToUrbanEventInquiryMigrator
    """    
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating to UrbanEventInquiries: starting...")

    migrators = (UrbanEventToUrbanEventInquiryMigrator,)

    portal = context.getSite()

    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    for migrator in migrators:
        walker = migrator.walker(portal, migrator, query={'id': 'enquete-publique'})
        walker.go()
        # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
        walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

    logger.info("Migrating to UrbanEventInquiries: done!")

class ProprietaryToApplicantMigrator(object, InplaceATItemMigrator):
    """
      Migrate the Contact with portal_type Proprietary to Contact with portal_type Applicant
    """
    walker = CustomQueryWalker
    src_meta_type = "Contact"
    src_portal_type = "Proprietary"
    dst_meta_type = "Contact"
    dst_portal_type = "Applicant"

    def __init__(self, *args, **kwargs):
        InplaceATItemMigrator.__init__(self, *args, **kwargs)

def migrationProprietaryToContact(context):
    """
      Call ProprietaryToApplicantMigrator
    """    
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating Proprietary portal_type to Applicant portal_type: starting...")

    migrators = (ProprietaryToApplicantMigrator,)

    portal = context.getSite()

    #Run the migrations
    for migrator in migrators:
        walker = migrator.walker(portal, migrator)
        walker.go()
        # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
        walker.__class__.additionalQuery = {}
    logger.info("Migrating Proprietary portal_type to Applicant portal_type: done!")

def addMd5SignatureAndProfileNameProperties(context):
    """
      Add md5Signature and profileName properties for each template if not exist
    """
    if isNoturbanMigrationsProfile(context): return

    logger.info("Adding md5 signature and 'profileName' property on templates: starting...")

    portal = context.getSite()
    tool = getToolByName(portal, 'portal_urban')

    folders = []
    for urban_type in URBAN_TYPES:
        licenceConfigId = urban_type.lower()
        if not safe_hasattr(tool, licenceConfigId): return
        configFolder = getattr(tool, licenceConfigId)
        if not safe_hasattr(configFolder, 'urbaneventtypes'): return
        uetfolder = getattr(configFolder, 'urbaneventtypes')
        for obj in uetfolder.objectValues('UrbanEventType'):
            folders.append(obj)
    if safe_hasattr(tool, 'globaltemplates'):
        folders.append(getattr(tool, 'globaltemplates'))

    # for each template in an urbanEventType or globaltemplates folder
    for folder in folders:
        for fileTemplate in folder.objectValues('ATBlob'):
            dictProperties=dict(fileTemplate.propertyItems())
            if dictProperties.has_key("md5Signature"):
                hex = dictProperties["md5Signature"].encode('hex')
                fileTemplate._delProperty("md5Signature")
            else:
                hex = getMd5Signature('cannot say if template has been modified !?')
            if not dictProperties.has_key("md5Modified"):
                fileTemplate.manage_addProperty("md5Modified", hex, "string")
            if not dictProperties.has_key("md5Loaded"):
                fileTemplate.manage_addProperty("md5Loaded", hex, "string")

            if not dictProperties.has_key("profileName"):
                fileTemplate.manage_addProperty("profileName","tests","string")
            fileTemplate.reindexObject()
    logger.info("Adding md5 signature and 'profileName' property on templates: done!")

def migrateLicenceContainers(context):
    """
      Every folder that will contain licences need to provide ILicenceContainer
    """
    #folders in the 'urban' application folder are licence containers
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating licence containers: starting...")

    portal = context.getSite()
    #we are migrating, so we have an urban folder at the root of portal
    for subFolder in portal.urban.objectValues('ATFolder'):
        alsoProvides(subFolder, ILicenceContainer)
        logger.info("Licence folder '%s' now provides IILicenceContainer" % subFolder.getId())
    logger.info("Migrating licence containers: done!")

def provideEventMarkerInterfaces(context):
    """
      implements a marker interface to each event who has it defined in its corresponding EventTypeType
    """
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating Specific Event interfaces: starting...")
    from zope.interface import alsoProvides
    from zope.component.interface import getInterface
    portal = context.getSite()
    brains = portal.portal_catalog.searchResults(portal_type='UrbanEvent') 
    for brain in brains:
        urbanevent = brain.getObject()
        event_type = urbanevent.getUrbaneventtypes()
        interfacepath = event_type.getEventTypeType()
        interface = None
        if interfacepath != '':
            interface = getInterface('', interfacepath)
        if interface is not None and not urbanevent.__provides__(interface):
            alsoProvides(urbanevent, interface)
            urbanevent.reindexObject(['object_provides'])
    logger.info("Migrating Specific Event interfaces: done!")

def migrateLayersForMapfish(context):
    """
      Removes useless layers and change format option
    """
    if isNoturbanMigrationsProfile(context): return

    portal = context.getSite()
    brains = portal.portal_catalog.searchResults(portal_type='Layer') 
    for brain in brains:
        layer = brain.getObject()
        if brain.id.startswith('ppnc'):
            #layer.aq_inner.aq_parent.manage_delObjects(brain.id)
            continue
        if not layer.getLayerFormat():
            layer.setLayerFormat('image/png')

class UrbanVocabularyTermToOrganisationTermMigrator(object, InplaceATItemMigrator):
    """
      Migrate UrbanVocabularyTerms to OrganisationTerm and link them to their coresponding UrbanEventType
    """
    walker = CustomQueryWalker
    src_meta_type = "UrbanVocabularyTerm"
    src_portal_type = "UrbanVocabularyTerm"
    dst_meta_type = "OrganisationTerm"
    dst_portal_type = "OrganisationTerm"

    def __init__(self, *args, **kwargs):
        InplaceATItemMigrator.__init__(self, *args, **kwargs)

    def custom(self):
        """
          We have to link the OrganisationTerm to its coresponding UrbanEventType 
        """
        attrs = ['title', 'description', 'extraValue']
        for attr in attrs:
            setattr(self.new, attr, getattr(self.old, attr))
        catalog = getToolByName(self.new, 'portal_catalog')
        brains = catalog(portal_type=('UrbanEventType',))
        for brain in brains:
            if self.new_id in brain.id:
                self.new.setLinkedOpinionRequestEvent(brain.getObject())
                return
        event.notify(ObjectInitializedEvent(self.new))
     
def migrateFoldermakersTerms(context):
    """
      Run the UrbanVocabularyTermToOrganisationTermMigrator
    """
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating UrbanVocabularyterms 'foldermakers': starting...")

    migrators = (UrbanVocabularyTermToOrganisationTermMigrator,)

    portal = context.getSite()

    #Run the migrations
    for migrator in migrators:
        folder_path = "%s/portal_urban/buildlicence/foldermakers" % '/'.join(portal.getPhysicalPath())
        walker = migrator.walker(portal, migrator, query={'path':folder_path,})
        walker.go()
        # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
        walker.__class__.additionalQuery = {}
    logger.info("Migrating UrbanVocabularyterms 'foldermakers': done!")

def migrateFoldermanagers(context):
    """
      Move all the FolderManager objects into a single folder at the root of urban config
      and set value to the field 'manageableLicences' depending on where we found the foldermanager
      to move
    """
    if isNoturbanMigrationsProfile(context): return

    from Products.urban.config import URBAN_TYPES
    logger.info("Migrating Foldermanagers: starting...")

    portal = context.getSite()
    #from plone.app.referenceintegrity.config import DisableRelationshipsProtectionTemporarily
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    tool = portal.portal_urban
    if not hasattr(tool, 'foldermanagers'):
        raise KeyError, "Migrating Foldermanagers objects to a single folder, no 'foldermanagers' folder in portal_urban : You must reinstall 'urban' before launching this step!"

    #move the foldermanagers spread in the config into the new folder
    foldermanager_ids = {}
    for licence_type in  URBAN_TYPES:
        ids_to_move = []
        licence_cfg_folder = getattr(tool, licence_type.lower())
        if not hasattr(aq_base(licence_cfg_folder), 'foldermanagers'):
            logger.info("Migrating Foldermanagers: %s was already migrated!" % licence_type)
            continue
        old_folder = licence_cfg_folder.foldermanagers
        #set the value for the field 'ManageableLicences' depending on the licence type 
        #where we found the foldermanagers
        for old_foldermanager in old_folder.objectValues():
            foldermanager_id = old_foldermanager.getId()
            if foldermanager_id not in foldermanager_ids.keys():
                foldermanager = old_foldermanager
                foldermanager.setManageableLicences([licence_type])
                foldermanager_ids[foldermanager_id] = foldermanager
                ids_to_move.append(foldermanager_id)
            else:
                foldermanager = foldermanager_ids[foldermanager_id]
                manageable_licences = []
                for licence in foldermanager.getManageableLicences():
                    manageable_licences.append(licence)
                manageable_licences.append(licence_type)
                foldermanager.setManageableLicences(manageable_licences)

            for licence in old_foldermanager.getBRefs():
                ref_foldermanagers = licence.getFoldermanagers()
                try:
                    i = ref_foldermanagers.index(old_foldermanager)
                    ref_foldermanagers[i] = foldermanager
                    licence.setFoldermanagers(ref_foldermanagers)
                    licence.reindexObject()
                except ValueError, msg:
                    logger.error("Error on licence '%s' when searching architect '%s', msg='%s'"%(licence.Title(), foldermanager.Title(),msg))

        #move the foldermanager objects
        cut_data = old_folder.manage_cutObjects(ids_to_move)
        tool.foldermanagers.manage_pasteObjects(cut_data)
        #delete the old folder
        licence_cfg_folder.manage_delObjects(['foldermanagers'])

    logger.info("Migrating Foldermanagers: done!")
    portal.portal_properties.site_properties.enable_link_integrity_checks = True

def addInvestigationArticlesToBuildLicenceConfig(context):
    """
      Helper method for updating investigations articles in the investigationArticles
      of the BuildLicences LicenceConfig
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    configFolder = getattr(site.portal_urban, 'buildlicence')
    logger.info("Adding default investigation articles in the BuildLicence LicenceConfig: starting...")
    from Products.urban.setuphandlers import addInvestigationArticles
    addInvestigationArticles(context, configFolder)
    logger.info("Adding default investigation articles in the BuildLicence LicenceConfig: done!")

def migrateGlobalTemplates(context):
    """
    Helper method to move the global templates of urbanTool in the globaltemplates folder
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getattr(site, 'portal_urban')
    if not hasattr(tool, 'templateHeader'):
        #the migration has already been runned, return
        return
    templates_folder = getattr(tool, 'globaltemplates')
    GT = GLOBAL_TEMPLATES
    old_templates = {
        'header.odt':(tool.templateHeader, GT[0]),
        'footer.odt':(tool.templateFooter, GT[1]),
        'reference.odt':(tool.templateReference, GT[2]),
        'signatures.odt':(tool.templateSignatures, GT[3]),
        'statsins.odt':(tool.templateStatsINS, GT[4]),
    }
    #depending on the version of the Data.fs
    #there could be a portal_urban.templateStyles attribute or not...
    if hasattr(aq_base(tool), 'templateStyles'):
        old_templates['styles.odt'] = (tool.templateStyles, GT[5])

    for template_id, template_infos in old_templates.items():
        newtemplate_id = templates_folder.invokeFactory("File", id=template_id, title=template_infos[1]['title'], file=template_infos[0].data)
        delattr(tool, template_infos[0].getId())

def migrateSomeLocalFoldersAsGlobal(context):
    """
      Some folders defined on LicenceConfigs are now at the portal_urban root
      This is the case for 'folderroadtypes', 'pashs' and 'foldercoatings'
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    #urban must have been reinstalled before running this step
    site.portal_properties.site_properties.enable_link_integrity_checks = False
    tool = getToolByName(site, 'portal_urban')

    #ids of local folders that are now global folders
    localFolderIds = ['folderroadtypes', 'folderroadcoatings', 'pashs', 'folderroadequipments', 'folderprotectedbuildings']
    for localFolderId in localFolderIds:
        if not hasattr(tool, localFolderId):
            raise KeyError, "Migrating some local LicenceConfigs folder to the portal_urban root : You must reinstall 'urban' before launching this step!"

    logger.info("Migrating some local LicenceConfigs folder to the portal_urban root : starting...")
    for urban_type in URBAN_TYPES:
        urban_type_id = urban_type.lower()
        configFolder = getattr(tool, urban_type_id)
        for localFolderId in localFolderIds:
            if hasattr(aq_base(configFolder), localFolderId):
                #a local folder exists, migrate it
                localFolder = getattr(configFolder, localFolderId)
                globalFolder = getattr(tool, localFolderId)
                ids_to_cut = []
                for obj in localFolder.objectValues():
                    #if the element does not already exist in the folder at the root
                    #of portal_urban, we cut and paste it
                    objId = obj.id
                    if not hasattr(globalFolder, objId):
                        ids_to_cut.append(objId)
                if ids_to_cut:
                    #cut and paste elements that does not exist in the global folder
                    cutdata = localFolder.manage_cutObjects(ids_to_cut)
                    globalFolder.manage_pasteObjects(cutdata)
                #delete the useless localFolder
                configFolder.manage_delObjects([localFolderId,])
                logger.info("The '%s' folder of '%s' has been migrated.  Additional ids where '%s'" % (localFolderId, configFolder.id, str(ids_to_cut)))

    logger.info("Migrating some local LicenceConfigs folder to the portal_urban root : done!")
    site.portal_properties.site_properties.enable_link_integrity_checks = True

def migrateSubjectFields(context):
    """
      Before there was a "declarationSubject", a "divisionSubject", ... field
      we will use the default "licenceSubject" field now
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_catalog = getToolByName(site, 'portal_catalog')
    brains = portal_catalog(portal_type=('Declaration', 'Division', ))

    logger.info("Migrating the 'xxxSubject' fields to 'licenceSubject' : starting...")
    for brain in brains:
        obj = brain.getObject()
        if not hasattr(obj, 'declarationSubject') and not hasattr(obj, 'divisionSubject'):
            #this type is already migrated, migrate the next one if necessary
            continue
        subject = ''
        if obj.portal_type == 'Declaration':
            subject = obj.declarationSubject
            delattr(obj, 'declarationSubject')
        else:
            #Divisions
            subject = obj.divisionSubject
            delattr(obj, 'divisionSubject')
        obj.setLicenceSubject(subject)
        logger.info("%s's licenceSubject has been migrated" % obj.Title())

    logger.info("Migrating the 'xxxSubject' fields to 'licenceSubject': done!")

def migrateDivisionsCommentsToDescription(context):
    """
      Divisions used a 'comments' field that is now replaced by the default 'description' field
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_catalog = getToolByName(site, 'portal_catalog')
    brains = portal_catalog(portal_type=('Division', ))

    logger.info("Migrating the 'comments' field of Divisions to 'description' : starting...")

    for brain in brains:
        obj = brain.getObject()
        if not hasattr(aq_base(obj), 'comments'):
            #stop the migration, it is already migrated...
            break
        description = obj.Description()
        comments = aq_base(obj).comments
        newDescription = str(description) + str(comments)
        obj.setDescription(newDescription, mimetype='text/html')
        logger.info("%s's 'comments' field has been migrated" % obj.Title())

    logger.info("Migrating the 'comments' field of Divisions to 'description' : done!")

def migrateDecisionsForDeclarations(context):
    """
      Declarations need an extra value to be defined on UrbanVocabularyTerms in portal_urban.decisions
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    logger.info("Migrating the 'decisions UrbanVocabularyTems' for Declarations: starting...")

    tool = getToolByName(site, 'portal_urban')

    for obj in tool.decisions.objectValues('UrbanVocabularyTerm'):
        extraValue = obj.getExtraValue()
        if not extraValue:
            if obj.id == 'favorable':
                obj.setExtraValue('Recevable')
                logger.info("Extra value added for '%s'" % obj.id)
            elif obj.id == 'defavorable':
                obj.setExtraValue('Irrecevable')
                logger.info("Extra value added for '%s'" % obj.id)
            else:
                logger.warn("Unknown term with id '%s', no extra value added!!!'" % obj.id)
            logger.info("Extra value added for '%s'" % obj.id)
        else:
            logger.info("Extra value already exists for '%s' and is '%s'" % (obj.id, extraValue))

    logger.info("Migrating the 'decisions UrbanVocabularyTems' for Declarations: done!!!")

def migrateFoldermanagersReferenceField(context):
    """
      Run the FoldermanagersReferenceMigrator
    """
    if isNoturbanMigrationsProfile(context): return

    logger.info("Migrating foldermanagers referencefield for divisions, urbancertificates an environmental declarations: starting...")

    meta_types = {
                    'UrbanCertificateBase':'certificateFolderManagers',
                    'Declaration':'declarationFolderManagers',
                    'EnvironmentalDeclaration':'environmentalDeclarationFolderManagers',
                    'Division':'division_foldermanager',
                   }
    site = context.getSite() 
    portal_catalog = getToolByName(site, 'portal_catalog')
    reference_catalog = getToolByName(site, 'reference_catalog')

    for meta_type, relationship in meta_types.iteritems():
        licences_brains = portal_catalog(meta_type=meta_type)
        for brain in licences_brains:
            ref_brains = reference_catalog(sourceUID=brain['UID'], relationship=relationship)
            old_foldermanagers_ids = [brain['targetId'] for brain in ref_brains]
            if old_foldermanagers_ids:
                licence = brain.getObject()
                licence.setFoldermanagers([brain.getObject() for brain in portal_catalog(id=old_foldermanagers_ids)])
            #remove the old references from the reference_catalog
            for ref_brain in ref_brains:
                reference_catalog.uncatalog_object(ref_brain.getPath())
    
    logger.info("Migrating foldermanagers referencefield for divisions, urbancertificates an environmental declarations: done!")

def updateUrbanTemplates(context):
    setup = getToolByName(context.getSite(), 'portal_setup')
    setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')

def migrateOpinionRequestTalExpression(context):
    """
    The tal expression used in the opinion request UrbanEventType has changed so it should be updated
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    urban_tool = getToolByName(site, 'portal_urban')
    for licence_type in  URBAN_TYPES:
        licence_cfg= getattr(urban_tool, licence_type.lower(), None)
        if licence_cfg:
            opinion_request_events = [event for event in licence_cfg.urbaneventtypes.objectValues() if event.id.endswith('opinion-request')]
            for opinion_request_cfg in opinion_request_events[1:]:
                tal_condition = opinion_request_cfg.getTALCondition()
                match = search("'(.*?)' in here.getSolicitOpinionsTo()", tal_condition)
                if match:
                    tal_condition = "python: here.mayAddOpinionRequestEvent('%s')" % match.group(1)
                    opinion_request_cfg.setTALCondition(tal_condition)
