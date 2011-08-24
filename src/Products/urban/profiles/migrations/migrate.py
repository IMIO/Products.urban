# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
from zope.i18n import translate as _
from Acquisition import aq_base
from Products.CMFPlone.utils import base_hasattr
from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator
from Products.urban.events.urbanEventInquiryEvents import setLinkedInquiry
from Products.urban.events.urbanEventEvents import setEventTypeType, setCreationDate

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
    #remove investigationStart and investigationEnd attributes and replace it by investigationsDates
    migrateInvestigations(context)
    #migrateToReferenceDataGridField(context)
    #We replace licence folders from portal_urban to LicenceConfig objects
    migrateToLicenceConfig(context)
    #we replace architect objects (based on Architect meta_type) by new objects (based on Contact meta_type)
    migrateArchitectToContact(context)
    #Migration of contact type objects to provides specific interfaces
    migrateSpecificContactInterfaces(context)
    #Migration of UrbanEvents with id 'enquete-publique' to UrbanEventinquiry
    migrationToUrbanEventInquiries(context)
    #remove 'eventDate' from UrbanEventType.activatedFields
    migrateUrbanEventTypes(context)
    #Add md5Signature and profileName properties for each template
    addMd5SignatureAndProfileNameProperties(context)

def migrateToReferenceDataGridField(context):
    """
      Migrate Declaration, Division, EnvironmentalDeclaration, UbranCertificateBase,
      UrbanCertificateTwo, BuildLicence, ParcelOutLicence types to use ReferenceDataGridField
      product instead of workLocation objects
    """
    if isNoturbanMigrationsProfile(context):
        return

    site = context.getSite()

    brains = site.portal_catalog(portal_type = ['BuildLicence', 'Declaration', 'Division', 'EnvironmentalDeclaration', 'UrbanCertificateBase',
                    'UrbanCertificateTwo', 'ParcelOutLicence'])
    for brain in brains:
        obj = brain.getObject()
        for previousWorkLocation in obj.objectValues('WorkLocation'):
            linkStreet = previousWorkLocation.getStreet()
            numberStreet = previousWorkLocation.getNumber()
            #to be continued ?????

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

def addEquipmentTypes(context):
    """
        Add EquipmentTypes in the urban config
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    configFolder=getattr(tool,'parceloutlicence')
    newFolderid = configFolder.invokeFactory("Folder",id="equipmenttypes",title=_("urban","folderequipmenttypes_folder_title",context=site,default="EquipmentTypes"))
    newFolder = getattr(configFolder, newFolderid)
    newFolder.setConstrainTypesMode(1)
    newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
    newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
    newFolder.invokeFactory("UrbanVocabularyTerm",id="telecom",title=u"Télécomunication")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="electricity",title=u"Electricité")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="gas",title=u"Gaz")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="teledistribution",title=u"Télédistribution")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="sewers",title=u"Egouttage")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="water",title=u"Eau")

def addPebMissingPart(context):
    """
      Add an element 'peb' in the 'buildlicence' UrbanConfig 'missingparts' folder
    """
    #walk into every UrbanConfigs and look for a 'missingparts' folder
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    if not hasattr(site.portal_urban.buildlicence, 'missingparts'):
        logger.error("No 'msisingparts' folder found in 'portal_urban.buildlicence' !!!")
        return
    missingPartsFolder = site.portal_urban.buildlicence.missingparts
    if not hasattr(missingPartsFolder, 'peb'):
        missingPartsFolder.invokeFactory("UrbanVocabularyTerm",id="peb",title=u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires")
        logger.info("Added a missing part 'peb' for UrbanConfig 'buildlicence'")
    else:
        logger.error("A missing part 'peb' already exists in 'portal_urban.buildlicence' !!!")

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
                data = {
                        'id': urbanVocTerm.getId(),
                        'title': urbanVocTerm.Title(),
                        'deadLineDelay': urbanVocTerm.getTermKey(),
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

def addSpecificFeatures(context):
    """
        Add specific features for UrbanCertificateOne,
        UrbanCertificateTwo and NotaryLetters urban configs
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    for urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', ]:
        configFolder=getattr(tool,urban_type.lower())
        #we add the specific features folder
        newFolderid = configFolder.invokeFactory("Folder",id="specificfeatures",title=_("urban","urban_label_specificFeatures",context=site,default="Specific features"))
        newFolder = getattr(configFolder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="reglement-regional-urbanisme",title=u"Règlement régional d'urbanisme")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="projet-expropriation",title=u"Projet d'expropriation")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="plan-remembrement",title=u"Plan de remembrement")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ordonnance-insalubrite",title=u"Ordoncance d'insalubrité")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="legislation-monuments-desaffectes",title=u"Législation monuments désaffectés")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="tuyauterie-gaz-naturel",title=u"Prise souterraine tuyauterie gaz naturel (loi du 12 avril 1965)")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="site-natura-2000",title=u"Site Natura 2000")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="infractions-legislation-urbanisme",title=u"Infractions à la législation sur l'urbanisme ou droit de l'environnement connues")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="perimetre-art-136-136bis",title=u"Périmètre visés aux articles 136 et 136bis du CWATUPE")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="droit-preemption",title=u"Un droit de préemption (article 175 du CWATUPE)")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="liste-sauvegarde-art-193",title=u"Inscrit sur la liste des sauvegardes (article 193 du CWATUPE)")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="classe-art-196",title=u"Classé (article 196 du CWATUPE)")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-de-protection-art-209",title=u"Zone de protection (article 209 du CWATUPE)")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-inondable",title=u"Zone à risque inondable (plan P.L.U.I.E.S.)")

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

def migrateInvestigations(context):
    """
        Remove investigations attributes
        investigationStart and investigationEnd are now in investigationsDates
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    brains = site.portal_catalog(portal_type = ['BuildLicence', 'ParcelOutLicence', ])
    logger.info("Migrating investigations: starting...")
    for brain in brains:
        licence = brain.getObject()
        if hasattr(aq_base(licence), 'investigationStart'):
            investigationsDates = ({
                                   'startdate': licence.getInvestigationStart(),
                                   'enddate': licence.getInvestigationEnd(),
            },)
            licence.setInvestigationsDates(investigationsDates)
            logger.info("%s at '%s' has been migrated" % (licence.portal_type, licence.absolute_url()))
    logger.info("Migrating investigations: done!")

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

    from Products.urban.config import URBAN_TYPES
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
    for architect in architect_folder.objectValues('Architect'):
        #first we create a new architect
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

def migrateSpecificContactInterfaces(context):
    """
        Migration of contact type objects to provides specific interfaces
    """
    if isNoturbanMigrationsProfile(context): return

    from Products.urban.interfaces import CONTACT_INTERFACES
    from zope.interface import alsoProvides
    portal = context.getSite()
    brains = portal.portal_catalog(portal_type = CONTACT_INTERFACES.keys())
    for brain in brains:
        contact = brain.getObject()
        if not contact.__provides__(CONTACT_INTERFACES[brain.Type]):
            alsoProvides(contact, CONTACT_INTERFACES[brain.Type])
            contact.reindexObject(['object_provides'])

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

    migrators = (UrbanEventToUrbanEventInquiryMigrator,)

    portal = context.getSite()

    #Run the migrations
    for migrator in migrators:
        walker = migrator.walker(portal, migrator, query={'id': 'enquete-publique'})
        walker.go()

def addMd5SignatureAndProfileNameProperties(context):
    """
      Add md5Signature and profileName properties for each template if not exist
    """
    portal = context.getSite()
    tool = getToolByName(portal, 'portal_urban')    
    try:
        #uetFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=None), "urbaneventtypes")
        blFolder = getattr(tool, 'buildlicence')
        uetFolder = getattr(blFolder,'urbaneventtypes')
    except AttributeError:
        #if we can not get the urbaneventtypes folder, we pass ...
        logger.warn("An error occured while trying to get the urbaneventtypes in urbanConfig")
        return
    import hashlib
    # for each urbanEventType
    for objid in uetFolder.objectIds():
        uet = getattr(uetFolder, objid)
        # for each template in this urbanEventType
        for templateid in uet:
            fileTemplate=getattr(uet,templateid,None)
            if fileTemplate:
                dictProperties=dict(fileTemplate.propertyItems())
                #add properties if not exist
                if not dictProperties.has_key("md5Signature"):
                    md5 = hashlib.md5(fileTemplate.data)
                    md5Signature=md5.digest()
                    fileTemplate.manage_addProperty("md5Signature",md5Signature,"string")
                if not dictProperties.has_key("profileName"):
                    fileTemplate.manage_addProperty("profileName","tests","string")
                fileTemplate.reindexObject()
