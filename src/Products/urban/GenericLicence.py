# -*- coding: utf-8 -*-
#
# File: GenericLicence.py
#
# Copyright (c) 2012 by CommunesPlone
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
import warnings
from zope.i18n import translate
from zope.component import createObject
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

slave_fields_subdivision = (
    # if in subdivision, display a textarea the fill some details
    {'name': 'subdivisionDetails',
     'action': 'show',
     'hide_values': (True, ),
    },
    {'name': 'parcellings',
     'action': 'show',
     'hide_values': (True, ),
     'hide_values': (True, ),
    },
)

slave_fields_pca= (
    # if in a pca, display a selectbox
    {'name': 'pca',
     'action': 'show',
     'hide_values': (True, ),
    },
)

optional_fields = ['subdivisionDetails', 'missingParts', 'missingPartsDetails','folderZoneDetails','derogationDetails','isInPCA',
                   'annoncedDelayDetails','roadType','roadCoating','roadEquipments',
                   'protectedBuildingDetails','investigationDetails','investigationReasons',
                   'pashDetails','catchmentArea','equipmentAndRoadRequirements','technicalRemarks',
                   'pca','SSC','RCU','floodingLevel','solicitRoadOpinionsTo', 'areParcelsVerified', 'locationFloodingLevel']
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
    DataGridField(
        name='workLocations',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'number' : Column("Number"), 'street' : SelectColumn("Street", UrbanVocabulary('streets', vocType=("Street", "Locality", ), id_to_use="UID", sort_on='sortable_title', inUrbanConfig=False, allowedStates=['enabled'])),},
            label='Worklocations',
            label_msgid='urban_label_workLocations',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
    ),
    StringField(
        name='folderCategory',
        widget=SelectionWidget(
            format='select',
            label='Foldercategory',
            label_msgid='urban_label_folderCategory',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        vocabulary=UrbanVocabulary('foldercategories', with_empty_value=True),
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
        vocabulary=UrbanVocabulary('missingparts'),
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
        vocabulary=UrbanVocabulary('folderzones', inUrbanConfig=False),
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
        vocabulary=UrbanVocabulary('folderdelays', vocType='UrbanDelay', with_empty_value=True),
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
        vocabulary=UrbanVocabulary('folderroadtypes', inUrbanConfig=False, with_empty_value=True),
    ),
    StringField(
        name='roadCoating',
        widget=SelectionWidget(
            format='select',
            label='Roadcoating',
            label_msgid='urban_label_roadCoating',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        vocabulary=UrbanVocabulary('folderroadcoatings', inUrbanConfig=False, with_empty_value=True),
    ),
    DataGridField(
        name='roadEquipments',
        schemata='urban_road',
        widget=DataGridWidget(
            columns={'road_equipment' : SelectColumn("Road equipments", UrbanVocabulary('folderroadequipments', inUrbanConfig=False)), 'road_equipment_details' : Column("Road equipment details"),},
            label='Roadequipments',
            label_msgid='urban_label_roadEquipments',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=("road_equipment", "road_equipment_details"),
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
        vocabulary=UrbanVocabulary('pashs', inUrbanConfig=False),
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
    StringField(
        name='locationFloodingLevel',
        widget=SelectionWidget(
            label='Locationfloodinglevel',
            label_msgid='urban_label_locationFloodingLevel',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_location',
        vocabulary='listFloodingLevels',
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
    BooleanField(
        name='isInPCA',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_pca,
            label='Isinpca',
            label_msgid='urban_label_isInPCA',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    StringField(
        name='pca',
        widget=SelectionWidget(
            label='Pca',
            label_msgid='urban_label_pca',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        vocabulary=UrbanVocabulary('pcas', vocType="PcaTerm", inUrbanConfig=False),
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
        vocabulary=UrbanVocabulary('foldermakers', vocType="OrganisationTerm"),
    ),
    BooleanField(
        name='isInSubdivision',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_subdivision,
            label='Isinsubdivision',
            label_msgid='urban_label_isInSubdivision',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='subdivisionDetails',
        allowable_content_types="('text/plain',)",
        schemata='urban_location',
        widget=TextAreaWidget(
            description='Number of the lots, ...',
            description_msgid="urban_descr_subdivisionDetails",
            label='Subdivisiondetails',
            label_msgid='urban_label_subdivisionDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        default_content_type='text/plain',
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
        vocabulary=UrbanVocabulary('folderprotectedbuildings', inUrbanConfig=False),
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
        name='SSC',
        widget=MultiSelectionWidget(
            size= 15,
            label='Ssc',
            label_msgid='urban_label_SSC',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('ssc', inUrbanConfig=False),
    ),
    LinesField(
        name='RCU',
        widget=MultiSelectionWidget(
            size= 10,
            label='Rcu',
            label_msgid='urban_label_RCU',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('rcu', inUrbanConfig=False),
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
        vocabulary=UrbanVocabulary('foldermakers', vocType="OrganisationTerm"),
    ),
    StringField(
        name='folderCategoryTownship',
        widget=SelectionWidget(
            label='Foldercategorytownship',
            label_msgid='urban_label_folderCategoryTownship',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_location',
        vocabulary=UrbanVocabulary('townshipfoldercategories', with_empty_value=True, sort_on='sortable_title'),
    ),
    BooleanField(
        name='areParcelsVerified',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Areparcelsverified',
            label_msgid='urban_label_areParcelsVerified',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    ReferenceField(
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            allow_browse=0,
            base_query='restrictFolderManagerSearch',
            show_results_without_query=True,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        relationship='licenceFolderManagers',
        required=True,
        schemata='urban_description',
        multiValued=1,
        allowed_types=('FolderManager',),
    ),
    ReferenceField(
        name='parcellings',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=True,
            allow_search=True,
            allow_browse=True,
            show_indexes=True,
            available_indexes={'Title':'Nom'},
            show_index_selector=True,
            wild_card_search=True,
            startup_directory="portal_urban/parcellings",
            restrict_browsing_to_startup_directory=True,
            label='Parcellings',
            label_msgid='urban_label_parcellings',
            i18n_domain='urban',
        ),
        allowed_types=('ParcellingTerm',),
        schemata='urban_location',
        multiValued=False,
        relationship='licenceParcelling',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

GenericLicence_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
GenericLicence_schema['title'].searchable = True
GenericLicence_schema['title'].widget.visible = False
##/code-section after-schema

class GenericLicence(BaseFolder, UrbanIndexes,  UrbanBase, BrowserDefaultMixin):
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

    security.declarePublic('getDefaultReference')
    def getDefaultReference(self):
        """
          Returns the reference for the new element
        """
        tool = getToolByName(self, 'portal_urban')
        return tool.generateReference(self)

    # Manually created methods

    def divideList (self, divider, list):
        res = []
        part = len(list)/divider
        remain = len(list)%divider
        for i in range(part):
            res.append(list[i*divider:(i+1)*divider])
        if remain > 0:
            res.append(list[divider*part:divider*part+remain])
        return tuple(res)

    security.declarePublic('templateListFolderCategories')
    def templateListFolderCategories(self):
        """
          Return a list of folder categories from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return urbantool.listVocabulary('foldercategories', self)

    security.declarePublic('templateListRoadTypes')
    def templateListRoadTypes(self):
        """
          Return a list of road types from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return urbantool.listVocabulary('folderroadtypes', self)

    security.declarePublic('templateListRoadEquipments')
    def templateListRoadEquipments(self):
        """
          Return a list of road equipments from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return urbantool.listVocabulary('folderroadequipments', self)

    def templateRoadEquipments(self, tup):
        res = []
        for pair in tup:
            res.append(pair['road_equipment'])
        return tuple(res)

    def templateRoadEquipmentDetail(self, tup):
        res = {}
        for pair in tup:
            res[pair['road_equipment']]=pair['road_equipment_details']
        return res

    security.declarePublic('templateListProtectedBuilding')
    def templateListProtectedBuilding(self):
        """
          Return a list of protected buildings mode from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return urbantool.listVocabulary('folderprotectedbuildings', self)

    security.declarePublic('templateMissingPartsFullname')
    def templateMissingPartsFullname(self, abreviation):
        urbantool = getToolByName(self, 'portal_urban')
        listVoc = urbantool.listVocabulary('missingparts', self)
        for pair in listVoc:
            if abreviation in pair:
                return pair[1]
        return ''

    security.declarePublic('templateZonesFullname')
    def templateZonesFullname(self, abreviation):
        urbantool = getToolByName(self,'portal_urban')
        listVoc = urbantool.listVocabulary(vocToReturn='folderzones', context=self, inUrbanConfig=False)
        for pair in listVoc:
            if abreviation in pair:
                return pair[1]
        return ''

    def templateRoadCoatingFullname(self, abreviation):
        urbantool = getToolByName(self,'portal_urban')
        listV = urbantool.listVocabulary('folderroadcoatings', self)
        for pair in listV:
            if abreviation in pair:
                return pair[1]
        return ''

    security.declarePublic('templateListMakers')
    def templateListMakers(self):
        """
          Return a list of folder makers from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return urbantool.listVocabulary('foldermakers', self)

    def templateOpinionGiverFullname(self, abreviation):
        for pair in self.templateListMakers():
            if abreviation in pair:
                return pair[1]
        return None

    def templateAllOpinions(self):
        all_opinions = list(self.getSolicitRoadOpinionsTo())
        location_opinions = self.getSolicitLocationOpinionsTo()
        inquiry = self.getLastInquiry()
        inquiry_opinions = None
        if inquiry is not None:
            inquiry_opinions = inquiry.getLinkedInquiry().getSolicitOpinionsTo()
        opinion_tank_list = [location_opinions, inquiry_opinions]
        for opinion_tank in opinion_tank_list:
            if opinion_tank is not None:
                for opinion in opinion_tank:
                    if opinion not in all_opinions:
                        all_opinions.append(opinion)
        return tuple(all_opinions)

    def templateListDerogations(self):
        urbantool = getToolByName(self,'portal_urban')
        return urbantool.listVocabulary('derogations', self)

    security.declarePublic('listCatchmentAreas')
    def listCatchmentAreas(self):
        """
          This vocabulary for field catchmentArea returns a list of
          catchment areas : close prevention area, far prevention area,
          supervision area or outside catchment
        """
        lst=[
             ['close', translate('close_prevention_area', 'urban', context=self.REQUEST)],
             ['far', translate('far_prevention_area', 'urban', context=self.REQUEST)],
             ['supervision', translate('supervision_area', 'urban', context=self.REQUEST)],
             ['ouside', translate('outside_catchment', 'urban', context=self.REQUEST)],
            ]

        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('listFloodingLevels')
    def listFloodingLevels(self):
        """
          This vocabulary for field floodingLevel returns a list of
          flooding levels : no risk, low risk, moderated risk, high risk
        """
        lst=[
             ['no', translate('flooding_level_no', 'urban', context=self.REQUEST)],
             ['low', translate('flooding_level_low', 'urban', context=self.REQUEST)],
             ['moderate', translate('flooding_level_moderate', 'urban', context=self.REQUEST)],
             ['high', translate('flooding_level_high', 'urban', context=self.REQUEST)],
            ]

        vocab = []
        #we add an empty vocab value of type "choose a value"
        val = translate('urban', EMPTY_VOCAB_VALUE, context=self, default=EMPTY_VOCAB_VALUE)
        vocab.append(('', val))
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('restrictFolderManagerSearch')
    def restrictFolderManagerSearch(self):
        """
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        rootPath = '/'.join(portal.getPhysicalPath())
        urban_tool = getToolByName(self, 'portal_urban')
        ids =  []
        for foldermanager in urban_tool.foldermanagers.objectValues():
            if self.getPortalTypeName() in foldermanager.getManageableLicences():
                ids.append(foldermanager.getId())
        dict = {}
        dict['path'] = {'query':'%s/portal_urban/foldermanagers' % (rootPath)}
        dict['id'] = ids
        return dict

    def getParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        return self.objectValues('PortionOut')

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
            applicantTitle = translate('no_applicant_defined', 'urban', context=self.REQUEST)
        title = "%s - %s - %s" % (self.getReference(), self.getLicenceSubject(), applicantTitle)
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex',))

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

    security.declarePublic('getPca')
    def getPca(self, theObject=False):
        """
          Returns the pca value or the PcaTerm if theObject=True
        """
        res = self.getField('pca').get(self)
        if res and theObject:
            tool = getToolByName(self, 'portal_urban')
            urbanConfig = tool.getUrbanConfig(self)
            res = getattr(urbanConfig.pcas, res)
        return res

    security.declarePublic('getOpinionRequests')
    def getOpinionRequests(self, organisation=''):
        """
          Returns the existing opinion requests
        """
        opinionRequests = self.objectValues('UrbanEventOpinionRequest')
        if organisation == '':
            return opinionRequests
        res = []
        for opinionRequest in opinionRequests:
            if opinionRequest.getLinkedOrganisationTermId() == organisation:
                res.append(opinionRequest)
        return res

    security.declarePublic('createAllAdvices')
    def createAllAdvices(self):
        """
          Create all urbanEvent corresponding to advice on a licence
        """
        listEventTypes = self.getAllAdvices()
        for listEventType in listEventTypes:
            createObject('UrbanEvent', listEventType.id, self)
        return self.REQUEST.RESPONSE.redirect(self.absolute_url()+'/view?#fieldsetlegend-urban_events')

    security.declarePublic('getAllAdvices')
    def getAllAdvices(self):
        """
          Returns all UrbanEvents corresponding to advice on a licence
        """
        tool = getToolByName(self, 'portal_urban')
        urbanConfig = tool.getUrbanConfig(self)
        listEventTypes = tool.listEventTypes(self,urbanConfig.id)
        res = []
        for listEventType in listEventTypes:
            obj = listEventType.getObject()
            #an advice corresponding to IOpinionRequestEvent
            if obj.eventTypeType == 'Products.urban.interfaces.IOpinionRequestEvent':
                res.append(obj)
        return res



registerType(GenericLicence, PROJECTNAME)
# end of class GenericLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer

