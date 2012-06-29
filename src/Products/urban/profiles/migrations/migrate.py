# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging

from zope.interface import alsoProvides
from zope import event

from Acquisition import aq_base

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator, InplaceATItemMigrator
from Products.urban.events.urbanEventInquiryEvents import setLinkedInquiry
from Products.urban.events.urbanEventEvents import setEventTypeType, setCreationDate
from Products.urban.utils import getMd5Signature
from Products.urban.config import URBAN_TYPES
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
    #this field is now a DataGridField
    migrateRoadEquipments(context)
    #delays were UrbanVocabularyTerms, now they are UrbanDelays
    migrateFolderDelays(context)
    #we have now PersonTitleTerms instead of UrbanVocabularyTerms to manage persons titles
    migratePersonTitles(context)
    #workLocations object disappeared, we now use a workLocations DataGridField
    migrateToWorkLocationsDataGridField(context)
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
    #migrate the foldermakers UrbanVocabularyTerms to allow them to link an UrbanEventType
    migrateFoldermakersTerms(context)
    #Move all the FolderManager objects into a single folder at the root of urban config
    migrateFoldermanagers(context)
    #Declarations need an extra value to be defined on UrbanVocabularyTerms in portal_urban.decisions
    migrateDecisionsForDeclarations(context)
    #some UrbanVocabularyTerms have been added afterward, we need to add them now
    addMissingUrbanVocabularyTerms(context)
    #Divisions used a 'comments' field that is now replaced by the default 'description' field
    migrateDivisionsCommentsToDescription(context)
    #Migrate the tal expression in the UrbanEvenType of opinions request
    migrateOpinionRequestTalExpression(context)
    #Update all the templates
    #We must run this step separately, to keep log inside portal_setup
    #updateUrbanTemplates(context)
    migrateConfigFoldersAllowedTypes(context)
    #restore the linked urbaneventype of the organisationTerms in foldermakers
    restoreOrganisationTermsLink(context)
    #migrate applicants of CUs to proprietaries
    migrateApplicantToProprietaryForCU(context)
    #migrate templates and generated files portal_type from 'File' to 'UrbanDoc'
    migrateFilesToUrbanDoc(context)

def migrateToWorkLocationsDataGridField(context):
    """
      Migrate Declaration, Division, EnvironmentalDeclaration, UbranCertificateOne,
      UrbanCertificateTwo, BuildLicence, ParcelOutLicence types to use workLocations DataGridField
      instead of workLocation objects
    """
    if isNoturbanMigrationsProfile(context):
        return

    site = context.getSite()

    if not site.portal_catalog(portal_type='WorkLocation'): return

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
    logger.info("%d licences migrated"%count)

def migrateUrbanEventTypes(context):
    """
      Migrate the UrbanEventTypes :
      - remove the 'urbanType' attribute
      - remove 'eventDate' from activatedFields if needed
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_url = getToolByName(site, 'portal_url')

    logger = context.getLogger('migrateUrbanEventTypes')
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
    logger = context.getLogger('addMissingUrbanVocabularyTerms')

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
#        else:
#            logger.info("'%s' already exists in '%s'" % (data['id'], '/'.join(destFolder.getPhysicalPath())))

def migrateFolderDelays(context):
    """
      Delays were UrbanVocabularyTerms, now they are UrbanDelays
    """
    #walk into every UrbanConfigs and look for a 'folderdelays' folder
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    logger = context.getLogger('migrateFolderDelays')
    count = 0
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
                count += 1
                logger.info("UrbanVocabularyTerm at '%s' has been migrated" % newObj.absolute_url())
    if count:
        logger.info("Do not forget to adapt the alert delay on migrated elements!")

def migrateTool(context):
    """
        Necessary adaptations about portal_urban
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    logger = context.getLogger('migrateTool')
    try:
        delattr(tool, 'usePloneTask')
        logger.info("The 'usePloneTask' attribute has been removed from portal_urban")
    except AttributeError:
        pass

def migrateRoadEquipments(context):
    """
        This field is now a DataGridField
    """
    if isNoturbanMigrationsProfile(context): return

    from types import DictType

    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    #adapt the roadEquipments field
    logger = context.getLogger('migrateRoadEquipments')
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
    logger = context.getLogger('migratePersonTitles')
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

def migrateArchitectToContact(context):
    """
        We replace architect objects (based on Architect meta_type) by new objects (based on Contact meta_type)
    """
    if isNoturbanMigrationsProfile(context): return
    portal = context.getSite()
    architect_folder = portal.urban.architects
    path = "%s/urban/architects" % '/'.join(portal.getPhysicalPath())
    if not portal.portal_catalog(portal_type=['Architect'], query={'path':path}): return
    #from plone.app.referenceintegrity.config import DisableRelationshipsProtectionTemporarily
    portal.portal_properties.site_properties.enable_link_integrity_checks = False
    logger = context.getLogger('migrateArchitectToContact')
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

def migrateSpecificContactInterfaces(context):
    """
        Migration of contact type objects to provides specific interfaces
    """
    if isNoturbanMigrationsProfile(context): return

    logger = context.getLogger('migrateSpecificContactInterfaces')
    from Products.urban.interfaces import CONTACT_INTERFACES
    portal = context.getSite()
    brains = portal.portal_catalog(portal_type = CONTACT_INTERFACES.keys())
    for brain in brains:
        contact = brain.getObject()
        if not contact.__provides__(CONTACT_INTERFACES[brain.Type]):
            alsoProvides(contact, CONTACT_INTERFACES[brain.Type])
            contact.reindexObject(['object_provides'])
            logger.info("Adding interface on '%s'"%contact.absolute_url())

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

    logger = context.getLogger('migrationToUrbanEventInquiries')
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
    logger.info("content migration done!")

def addMd5SignatureAndProfileNameProperties(context):
    """
      Add md5Signature and profileName properties for each template if not exist
    """
    if isNoturbanMigrationsProfile(context): return

    logger = context.getLogger('addMd5SignatureAndProfileNameProperties')
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
            if fileTemplate.getContentType() == 'application/zip':
                fileTemplate.setFormat("application/vnd.oasis.opendocument.text")
                logger.info("Content type corrected on '%s'"%fileTemplate.absolute_url())
            dictProperties=dict(fileTemplate.propertyItems())
            if dictProperties.has_key("md5Signature"):
                hex = dictProperties["md5Signature"].encode('hex')
                fileTemplate._delProperty("md5Signature")
            else:
                hex = getMd5Signature('cannot say if template has been modified !?')
            if not dictProperties.has_key("md5Modified"):
                fileTemplate.manage_addProperty("md5Modified", hex, "string")
                logger.info("Property md5Modified has been added on '%s'"%fileTemplate.absolute_url())
            if not dictProperties.has_key("md5Loaded"):
                fileTemplate.manage_addProperty("md5Loaded", hex, "string")
                logger.info("Property md5Loaded has been added on '%s'"%fileTemplate.absolute_url())

            if not dictProperties.has_key("profileName"):
                fileTemplate.manage_addProperty("profileName","tests","string")
            fileTemplate.reindexObject()

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
          We have to link the OrganisationTerm to its corresponding UrbanEventType
        """
        attrs = ['title', 'description', 'extraValue']
        for attr in attrs:
            setattr(self.new, attr, getattr(self.old, attr))
        catalog = getToolByName(self.new, 'portal_catalog')
        brains = catalog(portal_type=('UrbanEventType',))
        for brain in brains:
            if brain.id.startswith("%s-" % self.new_id) or brain.id.endswith("-%s" % self.new_id):
                self.new.setLinkedOpinionRequestEvent(brain.getObject())
                logger.info("OrganisationTerm '%s' has been migrated" % self.new_id)
                return
        event.notify(ObjectInitializedEvent(self.new))
        logger.info("OrganisationTerm '%s' has been migrated" % self.new_id)

def migrateFoldermakersTerms(context):
    """
      Run the UrbanVocabularyTermToOrganisationTermMigrator
    """
    if isNoturbanMigrationsProfile(context): return

    logger = context.getLogger('migrateFoldermakersTerms')

    migrators = (UrbanVocabularyTermToOrganisationTermMigrator,)

    portal = context.getSite()

    #Run the migrations
    for migrator in migrators:
        folder_path = "%s/portal_urban/buildlicence/foldermakers" % '/'.join(portal.getPhysicalPath())
        walker = migrator.walker(portal, migrator, query={'path':folder_path,})
        walker.go()
        # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
        walker.__class__.additionalQuery = {}
    logger.info("content migration done!")

def migrateFoldermanagers(context):
    """
      Move all the FolderManager objects into a single folder at the root of urban config
      and set value to the field 'manageableLicences' depending on where we found the foldermanager
      to move
    """
    if isNoturbanMigrationsProfile(context): return

    from Products.urban.config import URBAN_TYPES
    logger = context.getLogger('migrateFoldermanagers')

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
            continue
        old_folder = licence_cfg_folder.foldermanagers
        logger.info("'%s' will be  migrated!" % old_folder.absolute_url())
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
            logger.info("Foldermanager '%s' has been migrated" % foldermanager.Title())

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

    portal.portal_properties.site_properties.enable_link_integrity_checks = True

def migrateDivisionsCommentsToDescription(context):
    """
      Divisions used a 'comments' field that is now replaced by the default 'description' field
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()

    portal_catalog = getToolByName(site, 'portal_catalog')
    brains = portal_catalog(portal_type=('Division', ))
    logger = context.getLogger('migrateDivisionsCommentsToDescription')

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

def migrateDecisionsForDeclarations(context):
    """
      Declarations need an extra value to be defined on UrbanVocabularyTerms in portal_urban.decisions
    """
    if isNoturbanMigrationsProfile(context): return

    site = context.getSite()
    logger = context.getLogger('migrateDecisionsForDeclarations')
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
                logger.warning("Unknown term with id '%s', no extra value added!!!'" % obj.id)
#        else:
#            logger.info("Extra value already exists for '%s' and is '%s'" % (obj.id, extraValue))

def updateUrbanTemplates(context):
    setup = getToolByName(context.getSite(), 'portal_setup')
    setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')

def migrateOpinionRequestTalExpression(context):
    """
    The tal expression used in the opinion request UrbanEventType has changed so it should be updated
    """
    if isNoturbanMigrationsProfile(context): return

    logger = context.getLogger('migrateOpinionRequestTalExpression')
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
                    logger.info("Migrated expression of '%s'"%opinion_request_cfg.absolute_url())
                    opinion_request_cfg.setTALCondition(tal_condition)

def migrateConfigFoldersAllowedTypes(context):
    """
    Some object types have changed throughout urban evolution: the allowed content types of some config folder should
    follow these changes accordingly.
    """
    site = context.getSite()
    logger = context.getLogger('migrateConfigFoldersAllowedTypes')
    urban_tool = getToolByName(site, 'portal_urban')
    changes = [
        {'oldtype':('UrbanVocabularyTerm',) , 'newtype':('OrganisationTerm',), 'foldername':'foldermakers'},
    ]
    for change in changes:
        for licence_type in URBAN_TYPES:
            licence_cfg= getattr(urban_tool, licence_type.lower(), None)
            if licence_cfg and hasattr(licence_cfg, change['foldername']):
                folder = getattr(licence_cfg, change['foldername'])
                if folder.getImmediatelyAddableTypes() == folder.getLocallyAllowedTypes() == change['oldtype']:
                    folder.setImmediatelyAddableTypes(change['newtype'])
                    folder.setLocallyAllowedTypes(change['newtype'])
                    logger.info("Replaced addable types on folder '%s': value '%s'"%('/'.join(folder.getPhysicalPath()), change['newtype']))

def restoreOrganisationTermsLink(context):
    """
    Check that the organisationTerm are correctly linked to an urbaneventype,
    If its not the case, search for the correct urbanEventType to link.
    If we couldnt find any, create a new one and link it.
    """
    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    urban_tool = getToolByName(site, 'portal_urban')
    logger = context.getLogger('restoreOrganisationTermsLink')
    for licence_type in  URBAN_TYPES:
        licence_cfg= getattr(urban_tool, licence_type.lower(), None)
        if licence_cfg and hasattr(licence_cfg, 'foldermakers'):
            fm_folder = getattr(licence_cfg, 'foldermakers')
            uet_path = '/'.join(licence_cfg.urbaneventtypes.getPhysicalPath())
            for vocterm in fm_folder.objectValues('OrganisationTerm'):
                linked_uet = vocterm.getLinkedOpinionRequestEvent()
                #no link or not linked to the good urbanEventType
                if not linked_uet or (not linked_uet.id.startswith("%s-" % vocterm.id) and not linked_uet.id.endswith("-%s" % vocterm.id)):
                    brains = catalog(portal_type=('UrbanEventType',), path=uet_path)
                    #search for an existing corresponding urbanEventType
                    for brain in brains:
                        if brain.id.startswith("%s-" % vocterm.id) or brain.id.endswith("-%s" % vocterm.id):
                            #if we find one, we link it
                            vocterm.setLinkedOpinionRequestEvent(brain.getObject())
                            logger.info("Link event '%s' to organisation term '%s'"%(brain.getPath(), '/'.join(vocterm.getPhysicalPath())))
                            break
                    #if we could not find any, create a new one and link it
                    event.notify(ObjectInitializedEvent(vocterm))
                    logger.info("Create a new eventtype for organisation term '%s'"%'/'.join(vocterm.getPhysicalPath()))

def migrateApplicantToProprietaryForCU(context):
    """
    for notary letters, CU1 and CU2, the contacts portal_type should be "proprietary" and not "applicant"
    """
    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    urban = getattr(site, 'urban')
    for licence_type in  ['notaries', 'urbancertificateones', 'urbancertificatetwos']:
        licence_folder = getattr(urban, licence_type, None)
        path = '/'.join(licence_folder.getPhysicalPath())
        for brain in catalog(portal_type=('Applicant',), path=path, depth=2):
            applicant = brain.getObject()
            applicant.portal_type = 'Proprietary'
            applicant.reindexObject()
            logger.info("Migrated applicant %s to a proprietary" % applicant.Title())

def migrateFilesToUrbanDoc(context):
    """
    we need our own portal_type for the generated urban documents (at least to distinguish them from annex documents
    which are added manually)
    """
    if isNoturbanMigrationsProfile(context): return

    logger = context.getLogger('migrationToUrbanDoc')
    portal = context.getSite()
    path = "%s/portal_urban/globaltemplates"%'/'.join(portal.getPhysicalPath())
    migrators = (
                    (FilesToUrbanDocMigrator, {'SearchableText':['cu1 OR cu2 OR decl OR div OR lot OR miscdemand OR "not" OR urb OR peb OR declaenv']}),
                    (FilesToUrbanDocMigrator, {'path':path}),
                )
    #to avoid link integrity problems, disable checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = False

    #Run the migrations
    for migrator, query in migrators:
        walker = migrator.walker(portal, migrator, query=query)
        walker.go()
        # we need to reset the class variable to avoid using current query in next use of CustomQueryWalker
        walker.__class__.additionalQuery = {}
    #enable linkintegrity checks
    portal.portal_properties.site_properties.enable_link_integrity_checks = True
    logger.info("content migration done!")


class FilesToUrbanDocMigrator(object, InplaceATItemMigrator):
    """
    migrate urbaneventypes templates and genrated documents to UrbanDoc type
    """
    walker = CustomQueryWalker
    src_meta_type = "ATBlob"
    src_portal_type = "File"
    dst_meta_type = "UrbanDoc"
    dst_portal_type = "UrbanDoc"

    def __init__(self, *args, **kwargs):
        InplaceATItemMigrator.__init__(self, *args, **kwargs)
