# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
from zope.i18n import translate as _
from Acquisition import aq_base

logger = logging.getLogger('urban: migrations')

def isNoturbanMigrationsProfile(context):
    return context.readDataFile("urban_migrations_marker.txt") is None

def migrateToPlone4(context):
    """
      Launch every migration steps linked to the Plone4 version
    """
    if isNoturbanMigrationsProfile(context): return

    migrateTool(context)
    migrateFormatFieldFromLayers(context)
    migrateRoadEquipments(context)

def migrateToReferenceDataGridField(context):
    """Migrate declaration, division, environmentalDeclaration, ubranCertificateBase, urbanCertificateTwo, buildLicence, parcelOutLicence types
        to use referenceDataGridField product instead of workLocation objects
    """
    if isNoturbanMigrationsProfile(context):
        return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')

    brains = site.portal_catalog(portal_type = ['BuildLicence', 'Declaration', 'Division', 'EnvironmentalDeclaration', 'UrbanCertificateBase',
                    'UrbanCertificateTwo', 'ParcelOutLicence'])
    for brain in brains:
        obj = brain.getObject()
        for previousWorkLocation in obj.objectValues('WorkLocation'):
            linkStreet = previousWorkLocation.getStreet()
            numberStreet = previousWorkLocation.getNumber()

def migrateToContact(context):
    """
      More portal_types are now based on Contact.  Migrate old instances
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')

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
      Migrate the UrbanEventTypes as the urbanType attribute has been removed
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')

    brains = site.portal_catalog(portal_type="UrbanEventType")
    for brain in brains:
        obj = brain.getObject()
        #in case we run this script several time, check that the current
        #BuildLicence has not already been converted
        if not hasattr(obj, 'urbanType'):
            continue
        #else, proceed and remove no more used attributes
        delattr(obj, 'urbanType')
        logger.info('The urbanType attribute has been removed from %s' % portal_url.getRelativeUrl(obj))

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
    tool = getToolByName(site, 'portal_urban')
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
            #we save the ids to delete in 'ids'
            for urbanVocTerm in folderdelays.objectValues('UrbanVocabularyTerm'):
                folderdelays.setConstrainTypesMode(1)
                folderdelays.setLocallyAllowedTypes(['UrbanDelay'])
                folderdelays.setImmediatelyAddableTypes(['UrbanDelay'])
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
    tool = getToolByName(site, 'portal_urban')
    catalog = getToolByName(site, 'portal_catalog')
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
            delattr(tool, 'usePloneTask')
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
