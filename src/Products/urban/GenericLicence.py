# -*- coding: utf-8 -*-
#
# File: GenericLicence.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
import warnings
from DateTime import DateTime
from zope.i18n import translate as _
from collective.referencedatagridfield import ReferenceDataGridField, ReferenceDataGridWidget
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import technicalRemarksDefaultValue, \
equipmentAndRoadRequirementsDefaultValue
from Products.urban.utils import setOptionalAttributes

optional_fields = ['missingPartsDetails','folderZoneDetails','derogationDetails','annoncedDelayDetails','roadType','roadCoating','roadEquipments','protectedBuildingDetails','investigationDetails','investigationReasons','pashDetails','catchmentArea','equipmentAndRoadRequirements','technicalRemarks','pca','SSC','RCU','floodingLevel','solicitRoadOpinionsTo' ]
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
        required= True,
        schemata='urban_description',
        accessor="Title",
    ),
    StringField(
        name='licenceSubject',
        widget=StringField._properties['widget'](
            size=50,
            label='Licencesubject',
            label_msgid='urban_label_licenceSubject',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    StringField(
        name='reference',
        widget=StringField._properties['widget'](
            size=30,
            label='Reference',
            label_msgid='urban_label_reference',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        default_method="getDefaultReference",
    ),
    StringField(
        name='referenceDGATLP',
        widget=StringField._properties['widget'](
            size=30,
            label='Referencedgatlp',
            label_msgid='urban_label_referenceDGATLP',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    StringField(
        name='folderCategory',
        widget=SelectionWidget(
            label='Foldercategory',
            label_msgid='urban_label_folderCategory',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        vocabulary='listFolderCategories',
    ),
    LinesField(
        name='missingParts',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Missingparts',
            label_msgid='urban_label_missingParts',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=True,
        vocabulary='listMissingParts',
    ),
    TextField(
        name='missingPartsDetails',
        allowable_content_types=('text/plain',),
        default_content_type='text/plain',
        widget=TextAreaWidget(
            label='Missingpartsdetails',
            label_msgid='urban_label_missingPartsDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        schemata='urban_description',
    ),
    TextField(
        name='description',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Description',
            label_msgid='urban_label_description',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        schemata='urban_description',
        default_output_type='text/html',
        accessor="Description",
    ),
    LinesField(
        name='folderZone',
        widget=MultiSelectionWidget(
            size=10,
            label='Folderzone',
            label_msgid='urban_label_folderZone',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary='listZones',
    ),
    TextField(
        name='folderZoneDetails',
        allowable_content_types=('text/plain',),
        schemata='urban_location',
        widget=TextAreaWidget(
            label='Folderzonedetails',
            label_msgid='urban_label_folderZoneDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        default_content_type='text/plain',
    ),
    StringField(
        name='annoncedDelay',
        widget=SelectionWidget(
            label='Annonceddelay',
            label_msgid='urban_label_annoncedDelay',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary='listDelayToAnnonce',
    ),
    TextField(
        name='annoncedDelayDetails',
        allowable_content_types=('text/plain',),
        default_content_type='text/plain',
        widget=TextAreaWidget(
            label='Annonceddelaydetails',
            label_msgid='urban_label_annoncedDelayDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        schemata='urban_description',
    ),
    BooleanField(
        name='impactStudy',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Impactstudy',
            label_msgid='urban_label_impactStudy',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    StringField(
        name='roadType',
        widget=SelectionWidget(
            label='Roadtype',
            label_msgid='urban_label_roadType',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        vocabulary='listRoadTypes',
    ),
    StringField(
        name='roadCoating',
        widget=SelectionWidget(
            label='Roadcoating',
            label_msgid='urban_label_roadCoating',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        vocabulary='listRoadCoatings',
    ),
    DataGridField(
        name='roadEquipments',
        widget=DataGridWidget(
            columns={'road_equipment' : SelectColumn("Road equipments", vocabulary="listRoadEquipments"), 'road_equipment_details' : Column("Road equipment details"),},
            label='Roadequipments',
            label_msgid='urban_label_roadEquipments',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        columns=("road_equipment", "road_equipment_details"),
    ),
    LinesField(
        name='protectedBuilding',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Protectedbuilding',
            label_msgid='urban_label_protectedBuilding',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary='listProtectedBuilding',
    ),
    TextField(
        name='protectedBuildingDetails',
        allowable_content_types=('text/plain',),
        schemata='urban_location',
        widget=TextAreaWidget(
            label='Protectedbuildingdetails',
            label_msgid='urban_label_protectedBuildingDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        default_content_type='text/plain',
    ),
    LinesField(
        name='pash',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Pash',
            label_msgid='urban_label_pash',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary='listPashs',
    ),
    TextField(
        name='pashDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pashdetails',
            label_msgid='urban_label_pashDetails',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        default_content_type='text/html',
        default_output_type='text/html',
    ),
    LinesField(
        name='catchmentArea',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Catchmentarea',
            label_msgid='urban_label_catchmentArea',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary='listCatchmentAreas',
    ),
    TextField(
        name='equipmentAndRoadRequirements',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Equipmentandroadrequirements',
            label_msgid='urban_label_equipmentAndRoadRequirements',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default=equipmentAndRoadRequirementsDefaultValue,
        schemata='urban_road',
        default_output_type='text/html',
    ),
    TextField(
        name='technicalRemarks',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Technicalremarks',
            label_msgid='urban_label_technicalRemarks',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default=technicalRemarksDefaultValue,
        schemata='urban_road',
        default_output_type='text/html',
    ),
    StringField(
        name='pca',
        widget=SelectionWidget(
            label='Pca',
            label_msgid='urban_label_pca',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        vocabulary='listPcas',
    ),
    StringField(
        name='SSC',
        widget=StringField._properties['widget'](
            label='Ssc',
            label_msgid='urban_label_SSC',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    StringField(
        name='RCU',
        widget=StringField._properties['widget'](
            label='Rcu',
            label_msgid='urban_label_RCU',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    StringField(
        name='floodingLevel',
        widget=SelectionWidget(
            label='Floodinglevel',
            label_msgid='urban_label_floodingLevel',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_road',
        vocabulary='listFloodingLevels',
    ),
    LinesField(
        name='solicitRoadOpinionsTo',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Solicitroadopinionsto',
            label_msgid='urban_label_solicitRoadOpinionsTo',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary='listMakers',
    ),
    LinesField(
        name='solicitLocationOpinionsTo',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Solicitlocationopinionsto',
            label_msgid='urban_label_solicitLocationOpinionsTo',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary='listMakers',
    ),
    ReferenceDataGridField(
        name='workLocations',
        widget=ReferenceDataGridWidget(
            startup_directory="/portal_urban/streets",
            label="street",
            visible={'edit' : 'visible', 'view' : 'visible'},
            macro="street_referencedatagridwidget",
            label_msgid='urban_label_workLocations',
            i18n_domain='urban',
        ),
        allowed_types=('Street', 'Locality'),
        schemata="default",
        relationship="Street",
        columns=('numero','title' ,'link' ,'uid'),
    ),
    ReferenceField(
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            allow_browse=1,
            show_indexes=1,
            available_indexes={'Title':'Nom'},
            startup_directory_method="foldermanagersStartupDirectory",
            restrict_browsing_to_startup_directory=1,
            wild_card_search=True,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        required=True,
        schemata='urban_description',
        multiValued=1,
        relationship='licenceFolderManagers',
        allowed_types=('FolderManager',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

GenericLicence_schema = BaseFolderSchema.copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
GenericLicence_schema['title'].searchable = True
GenericLicence_schema['title'].widget.visible = False
#put the the fields coming from Inquiry in a specific schemata
inquiryFields = Inquiry.schema.filterFields(isMetadata=False)
#do not take the 2 first fields into account, this is 'id' and 'title'
inquiryFields = inquiryFields[2:]
for inquiryField in inquiryFields:
    GenericLicence_schema[inquiryField.getName()].schemata = 'urban_investigation_and_advices'
##/code-section after-schema

class GenericLicence(BaseFolder, UrbanIndexes,  UrbanBase, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IGenericLicence)

    meta_type = 'GenericLicence'
    _at_rename_after_creation = True

    schema = GenericLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('listFolderCategories')
    def listFolderCategories(self):
        """
          Return a list of folder categories from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('foldercategories', self))

    security.declarePublic('listRoadTypes')
    def listRoadTypes(self):
        """
          Return a list of road types from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderroadtypes', self))

    security.declarePublic('listRoadEquipments')
    def listRoadEquipments(self):
        """
          Return a list of road equipments from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderroadequipments', self))

    security.declarePublic('listProtectedBuilding')
    def listProtectedBuilding(self):
        """
          Return a list of protected buildings mode from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderprotectedbuildings', self))

    security.declarePublic('listZones')
    def listZones(self):
        """
          Return a list of zones from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderzones', self))

    security.declarePublic('listDivisions')
    def listDivisions(self):
        """
          Return a list of divisions from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderdivisions', self))

    security.declarePublic('listRoadCoatings')
    def listRoadCoatings(self):
        """
          Return a list of road coatings from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderroadcoatings', self))

    security.declarePublic('listMakers')
    def listMakers(self):
        """
          Return a list of folder makers from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('foldermakers', self))

    security.declarePublic('listDelayToAnnonce')
    def listDelayToAnnonce(self):
        """
          Return a list of delays from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderdelays', self, vocType="UrbanDelay"))

    security.declarePublic('defaultInvestigationArticle')
    def defaultInvestigationArticle(self):
        """
          This return the default investigation article
        """
        return '330'

    security.declarePublic('listPcas')
    def listPcas(self):
        """
          Return a list of PCA from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('pcas', self, vocType="PcaTerm", inUrbanConfig=False))

    security.declarePublic('listDerogations')
    def listDerogations(self):
        """
          Return a list of derogations from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('derogations', self))

    security.declarePublic('getDefaultReference')
    def getDefaultReference(self):
        """
          Returns the reference for the new element
        """
        tool = getToolByName(self, 'portal_urban')
        return tool.generateReference(self)

    security.declarePublic('listPashs')
    def listPashs(self):
        """
          Return a list of PASHs
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('pashs', self))

    # Manually created methods

    security.declarePublic('listCatchmentAreas')
    def listCatchmentAreas(self):
        """
          This vocabulary for field catchmentArea returns a list of
          catchment areas : close prevention area, far prevention area,
          supervision area or outside catchment
        """
        lst=[
             ['close', _('close_prevention_area', 'urban', context=self.REQUEST)],
             ['far', _('far_prevention_area', 'urban', context=self.REQUEST)],
             ['supervision', _('supervision_area', 'urban', context=self.REQUEST)],
             ['ouside', _('outside_catchment', 'urban', context=self.REQUEST)],
            ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('listInvestigationArticles')
    def listInvestigationArticles(self):
        """
          Return a list of investigation articles from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('investigationarticles', self))

    security.declarePublic('listFloodingLevels')
    def listFloodingLevels(self):
        """
          This vocabulary for field floodingLevel returns a list of
          flooding levels : no risk, low risk, moderated risk, high risk
        """
        lst=[
             ['no', _('flooding_level_no', 'urban', context=self.REQUEST)],
             ['low', _('flooding_level_low', 'urban', context=self.REQUEST)],
             ['moderate', _('flooding_level_moderate', 'urban', context=self.REQUEST)],
             ['high', _('flooding_level_high', 'urban', context=self.REQUEST)],
            ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('listMissingParts')
    def listMissingParts(self):
        """
          Return a list of necessary documents from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('missingparts', self))

    security.declarePublic('foldermanagersStartupDirectory')
    def foldermanagersStartupDirectory(self):
        """
          Return the folder were are stored folder managers
          This depend on the real portal_type
        """
        return '/portal_urban/%s/foldermanagers' % self.getPortalTypeName().lower()

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
           Return the list of applicants for the Licence
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Applicant':
                res.append(obj)
        return res

    def getParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        return self.objectValues('PortionOut')

    def getBeginDate(self):
        """
          Return the beginDate of the Licence
        """
        #try to get the beginDate of the UrbanEvent that start the Licence
        try:
            urbanevent = getattr(self, "depot-de-la-demande")
            return urbanevent.getBeginDate()
        except AttributeError:
            #if we can not get it, we return the CreationDate
            return DateTime(self.CreationDate())

    def getEndDate(self):
        """
          Return the endDate of the Licence
        """
        delay = self.getAnnoncedDelay()
        if delay and str(delay).isdigit():
            return self.getBeginDate() + delay
        else:
            return self.getBeginDate()

    security.declarePublic('getDatesString')
    def getDatesString(self):
        """
          Produces a string representation of begin and end date for sorting purposes
        """
        return str(self.getBeginDate()) + '-' + str(self.getEndDate())

    security.declarePublic('adapted')
    def adapted(self):
        """
          Gets the "adapted" version of myself. If no custom adapter is found, this methods returns me
        """
        return getCustomAdapter(self, isTask=True)

    security.declarePublic('getEventById')
    def getEventById(self, eventId):
        """
          Return an event with the passed id
          This method is duplicated from UrbanTool but is kept here for backward compatibility
        """
        warnings.warn("The use of GenericLicence.getEventById is deprecated, "
                      "please use UrbanTool.getEventByEventTypeId.",
                      DeprecationWarning, 1)
        try:
            urban_event = getattr(self, eventId)
        except AttributeError:
            urban_event = None
        return urban_event

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        tool = getToolByName(self,'portal_urban')
        #increment the numerotation in the tool
        tool.incrementNumerotation(self)
        #there is no need for other users than Managers to List folder contents
        #set this permission here if we use the simple_publication_workflow...
        self.manage_permission('List folder contents', ['Manager', ], acquire=0)
        self.updateTitle()

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to clearly identify the licence
        """
        if self.getApplicants():
            applicantTitle = self.getApplicants()[0].Title()
        else:
            applicantTitle = _('no_applicant_defined', 'urban', context=self.REQUEST)
        title = "%s - %s - %s" % (self.getReference(), self.getLicenceSubject(), str(applicantTitle))
        self.setTitle(title)
        self.reindexObject()

    security.declarePublic('constructPortalMessage')
    def constructPortalMessage(self):
        """
           Return a supplementary portal message
        """
        parcels = self.getParcels()
        applicants = self.getApplicants()
        messages=[]
        parcel_message = "warning_add_a_parcel"
        applicant_message = "warning_add_an_applicant"
        if not parcels:
            #we warn the user that no parcel have been added...
            messages.append(parcel_message)
        if not applicants:
            #we warn the user that no applicant have been added...
            messages.append(applicant_message)
        return messages

    security.declarePublic('getAnnoncedDelay')
    def getAnnoncedDelay(self, theObject=False):
        """
          Returns the annonced delay value or the UrbanDelay if theObject=True
        """
        res = self.getField('annoncedDelay').get(self)
        if res and theObject:
            tool = getToolByName(self, 'portal_urban')
            urbanConfig = tool.getUrbanConfig(self)
            res = getattr(urbanConfig.folderdelays, res)
        return res

    security.declarePublic('getInquiries')
    def getInquiries(self):
        """
          Returns the existing inquiries
        """
        #the first inquiry is the one defined on self itself
        #and the others are extra Inquiry object added
        return [self, ] + self.objectValues('Inquiry')

    security.declarePublic('getUrbanEventInquiries')
    def getUrbanEventInquiries(self):
        """
          Returns the existing UrbanEventInquiries
        """
        return self.listFolderContents({'portal_type': 'UrbanEventInquiry',})



registerType(GenericLicence, PROJECTNAME)
# end of class GenericLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer

