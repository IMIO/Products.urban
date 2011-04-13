from Products.CMFCore.utils import getToolByName
import logging
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService
logger = logging.getLogger('urban: migrations')

def isNoturbanMigrationsProfile(context):
    return context.readDataFile("urban_migrations_marker.txt") is None

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
    service = getGlobalTranslationService()
    configFolder=getattr(tool,'parceloutlicence')
    newFolderid = configFolder.invokeFactory("Folder",id="equipmenttypes",title=service.translate("urban","folderequipmenttypes_folder_title",context=site,default="EquipmentTypes"))
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

def migrateFolderDelays(context):
    """
      Delays were UrbanVocabularyTerms, no they are UrbanDelays
    """
    pass

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
    service = getGlobalTranslationService()
    for urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', ]:
        configFolder=getattr(tool,urban_type.lower())
        #we add the specific features folder
        newFolderid = configFolder.invokeFactory("Folder",id="specificfeatures",title=service.translate("urban","urban_label_specificFeatures",context=site,default="Specific features"))
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

