# -*- coding: utf-8 -*-
#
# File: GenericLicence.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
import re
import Levenshtein
from zope.i18n import translate
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.interfaces import IUrbanCertificateBase
from Products.urban import UrbanMessage as _

from plone import api

slave_fields_subdivision = (
    # if in subdivision, display a textarea the fill some details
    {
        'name': 'subdivisionDetails',
        'action': 'show',
        'hide_values': (True, ),
    },
    {
        'name': 'parcellings',
        'action': 'show',
        'hide_values': (True, ),
    },
)

slave_fields_pca = (
    # if in a pca, display a selectbox
    {
        'name': 'pca',
        'action': 'show',
        'hide_values': (True, ),
    },
    {
        'name': 'pcaDetails',
        'action': 'show',
        'hide_values': (True, ),
    },
)

optional_fields = [
    'subdivisionDetails', 'missingParts', 'missingPartsDetails', 'folderZoneDetails', 'folderZone',
    'isInPCA', 'roadType', 'roadCoating', 'roadEquipments',
    'isInSubdivision', 'solicitLocationOpinionsTo', 'technicalRemarks', 'locationTechnicalRemarks',
    'folderCategoryTownship', 'protectedBuilding', 'protectedBuildingDetails', 'folderCategory',
    'pash', 'pashDetails', 'catchmentArea', 'catchmentAreaDetails', 'equipmentAndRoadRequirements',
    'SSC', 'sscDetails', 'RCU', 'rcuDetails', 'floodingLevel', 'floodingLevelDetails', 'solicitRoadOpinionsTo',
    'areParcelsVerified', 'locationFloodingLevel', 'licenceSubject', 'referenceDGATLP',
    'roadMissingParts', 'roadMissingPartsDetails', 'locationMissingParts', 'locationMissingPartsDetails'
]
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
        default_method="getDefaultReference",
        schemata='urban_description',
        validators=('isNotDuplicatedReference',),
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
            columns={'number': Column("Number"), 'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',))},
            helper_js=('datagridwidget.js', 'datagridautocomplete.js'),
            label='Worklocations',
            label_msgid='urban_label_workLocations',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
        validators=('isValidStreetName',),
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
        default_method='getDefaultValue',
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='missingPartsDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Missingpartsdetails',
            label_msgid='urban_label_missingPartsDetails',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label='Description',
            label_msgid='urban_label_description',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_description',
        default_method='getDefaultText',
        default_output_type='text/html',
        accessor="Description",
    ),
    LinesField(
        name='roadMissingParts',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Roadmissingparts',
            label_msgid='urban_label_roadMissingParts',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=True,
        vocabulary=UrbanVocabulary('roadmissingparts'),
        default_method='getDefaultValue',
    ),
    TextField(
        name='roadMissingPartsDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Roadmissingpartsdetails',
            label_msgid='urban_label_roadMissingPartsDetails',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
    ),
    LinesField(
        name='roadType',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Roadtype',
            label_msgid='urban_label_roadType',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary=UrbanVocabulary('folderroadtypes', inUrbanConfig=False, with_empty_value=False),
        default_method='getDefaultValue',
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
        default_method='getDefaultValue',
    ),
    DataGridField(
        name='roadEquipments',
        schemata='urban_road',
        widget=DataGridWidget(
            columns={'road_equipment': SelectColumn("Road equipments", UrbanVocabulary('folderroadequipments', inUrbanConfig=False)), 'road_equipment_details': Column("Road equipment details"),},
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='pashDetails',
        widget=RichWidget(
            label='Pashdetails',
            label_msgid='urban_label_pashDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_road',
        default_method='getDefaultText',
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
        name='catchmentAreaDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Catchmentareadetails',
            label_msgid='urban_label_catchmentAreaDetails',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/plain',
    ),
    StringField(
        name='floodingLevel',
        widget=SelectionWidget(
            label='Floodinglevel',
            label_msgid='urban_label_floodingLevel',
            i18n_domain='urban',
        ),
        enforceVocabulary= True,
        schemata='urban_road',
        vocabulary='listFloodingLevels',
    ),
    TextField(
        name='floodingLevelDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Floodingleveldetails',
            label_msgid='urban_label_floodingLevelDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/plain',
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
        default_method='getDefaultText',
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
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/html',
    ),
    LinesField(
        name='locationMissingParts',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Locationmissingparts',
            label_msgid='urban_label_locationMissingParts',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('locationmissingparts'),
        default_method='getDefaultValue',
    ),
    TextField(
        name='locationMissingPartsDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Locationmissingpartsdetails',
            label_msgid='urban_label_locationMissingPartsDetails',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='folderZoneDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Folderzonedetails',
            label_msgid='urban_label_folderZoneDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='pcaDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pcadetails',
            label_msgid='urban_label_pcaDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
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
        widget=TextAreaWidget(
            description='Number of the lots, ...',
            description_msgid="urban_descr_subdivisionDetails",
            label='Subdivisiondetails',
            label_msgid='urban_label_subdivisionDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
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
        name='locationTechnicalRemarks',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Locationtechnicalremarks',
            label_msgid='urban_label_locationTechnicalRemarks',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
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
        vocabulary=UrbanVocabulary('urbaneventtypes', vocType="OpinionRequestEventType", value_to_use='extraValue'),
        default_method='getDefaultValue',
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='protectedBuildingDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Protectedbuildingdetails',
            label_msgid='urban_label_protectedBuildingDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='sscDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Sscdetails',
            label_msgid='urban_label_sscDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
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
        default_method='getDefaultValue',
    ),
    TextField(
        name='rcuDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Rcudetails',
            label_msgid='urban_label_rcuDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
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
        vocabulary=UrbanVocabulary('urbaneventtypes', vocType="OpinionRequestEventType", value_to_use='extraValue'),
        default_method='getDefaultValue',
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
        default_method='getDefaultValue',
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
            allow_browse=False,
            base_query='foldermanagersBaseQuery',
            show_results_without_query=True,
            wild_card_search=True,
            allow_search=False,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        relationship='licenceFolderManagers',
        required=True,
        schemata='urban_description',
        multiValued=True,
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
            startup_directory="urban/parcellings",
            restrict_browsing_to_startup_directory=True,
            default_search_index='Title',
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
        return self.getUrbanConfig().generateReference(self)

    # Manually created methods

    security.declarePublic('getDefaultValue')
    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return ['']

        urban_tool = api.portal.get_tool('portal_urban')
        vocabulary_name = field.vocabulary.path
        in_urban_config = field.vocabulary.inUrbanConfig

        default_value = urban_tool.getVocabularyDefaultValue(
            vocabulary_name=vocabulary_name,
            context=context,
            in_urban_config=in_urban_config,
            multivalued=field.multiValued
        )
        return default_value

    security.declarePublic('getDefaultText')
    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = api.portal.get_tool('portal_urban')
        return urban_tool.getTextDefaultValue(field.getName(), context)

    security.declarePublic('getUrbanConfig')
    def getUrbanConfig(self):
        licencetype = self.portal_type
        config_id = licencetype.lower()
        portal_urban = api.portal.get_tool('portal_urban')

        config_folder = portal_urban.getUrbanConfig(self)

        return config_folder

    security.declarePublic('attributeIsUsed')
    def attributeIsUsed(self, name):
        """
          Is the attribute named as param name used in this LicenceConfig ?
        """
        licenceConfig = self.getUrbanConfig()
        return (name in licenceConfig.getUsedAttributes())

    security.declarePublic('createUrbanEvent')
    def createUrbanEvent(self, urban_event_type_uid):
        """ Create urban event in this licence """
        uid_catalog = api.portal.get_tool('uid_catalog')
        urban_tool = api.portal.get_tool('portal_urban')

        event_type = uid_catalog(UID=urban_event_type_uid)[0].getObject()
        event_type.checkCreationInLicence(self)

        eventTypeType = event_type.getEventTypeType()
        portal_type = urban_tool.portal_types_per_event_type_type.get(eventTypeType, "UrbanEvent")

        urban_event_id = self.invokeFactory(
            portal_type,
            id=urban_tool.generateUniqueId(portal_type),
            title=event_type.Title(),
            urbaneventtypes=(event_type, )
        )
        urban_event = getattr(self, urban_event_id)
        return urban_event

    def divideList(self, divider, list):
        res = []
        part = len(list) / divider
        remain = len(list) % divider
        for i in range(part):
            res.append(list[i * divider: (i + 1) * divider])
        if remain > 0:
            res.append(list[divider * part: divider * part + remain])
        return tuple(res)

    def templateRoadEquipments(self, tup):
        res = []
        for pair in tup:
            res.append(pair['road_equipment'])
        return tuple(res)

    def templateRoadEquipmentDetail(self, tup):
        res = {}
        for pair in tup:
            res[pair['road_equipment']] = pair['road_equipment_details']
        return res

    def templateAllOpinions(self):
        all_opinions = list(self.getSolicitRoadOpinionsTo())
        location_opinions = self.getSolicitLocationOpinionsTo()
        if hasattr(self, 'getLastInquiry'):
            inquiry = self.getLastInquiry()
        else:
            inquiry = None
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

    security.declarePublic('listCatchmentAreas')
    def listCatchmentAreas(self):
        """
          This vocabulary for field catchmentArea returns a list of
          catchment areas : close prevention area, far prevention area,
          supervision area or outside catchment
        """
        vocab = (
            ('close', translate(_('close_prevention_area'), context=self.REQUEST)),
            ('far', translate(_('far_prevention_area'), context=self.REQUEST)),
            ('supervision', translate(_('supervision_area'), context=self.REQUEST)),
            ('ouside', translate(_('outside_catchment'), context=self.REQUEST)),
        )

        return DisplayList(vocab)

    security.declarePublic('listFloodingLevels')
    def listFloodingLevels(self):
        """
          This vocabulary for field floodingLevel returns a list of
          flooding levels : no risk, low risk, moderated risk, high risk
        """
        vocab = (
            #we add an empty vocab value of type "choose a value"
            ('',  translate(_(EMPTY_VOCAB_VALUE), context=self.REQUEST)),
            ('no', translate(_('flooding_level_no'), context=self.REQUEST)),
            ('low', translate(_('flooding_level_low'), context=self.REQUEST)),
            ('moderate', translate(_('flooding_level_moderate'), context=self.REQUEST)),
            ('high', translate(_('flooding_level_high'), context=self.REQUEST)),
        )

        return DisplayList(vocab)

    security.declarePublic('foldermanagersBaseQuery')
    def foldermanagersBaseQuery(self):
        """
        """
        portal = api.portal.get_tool('portal_url').getPortalObject()
        rootPath = '/'.join(portal.getPhysicalPath())
        urban_tool = api.portal.get_tool('portal_urban')
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

    security.declarePublic('createParcelAndProprietary')
    def createParcelAndProprietary(self, parcel_data, proprietary_data):
        parcel_street = parcel_data.pop('location')
        self.createApplicantFromParcel(parcel_street=parcel_street, **proprietary_data)
        self.createParcel(parcel_data)

    security.declarePublic('createParcelAndProprietary')
    def createParcel(self, parcel_data):
        portal_urban = api.portal.get_tool('portal_urban')
        portal_urban.createPortionOut(container=self, **parcel_data)

    def createApplicantFromParcel(self, proprietary, proprietary_city, proprietary_street, parcel_street):
        """
           Create the PortionOut with given parameters...
        """
        contact_type = 'Applicant'
        if IUrbanCertificateBase.providedBy(self):
            contact_type = 'Proprietary'

        # need: parcel street, proprietary street
        street_and_number = self.extractStreetAndNumber(proprietary_street)
        person_street = street_and_number['street']
        person_number = street_and_number['number']

        street_and_number = self.extractStreetAndNumber(parcel_street)
        parcel_street = street_and_number['street']
        parcel_number = street_and_number['number']

        # compare parcel street to proprietary street
        # if they are the same, means fuzzy match on street name and EXACT match on number
        same_street = Levenshtein.ratio(person_street, parcel_street) > 0.8
        same_number = self.haveSameNumbers(person_number, parcel_number)
        same_address = same_street and same_number
        city = proprietary_city.split()
        zipcode = city[0]
        city = ' '.join(city[1:])

        contacts = proprietary.split('&')
        for contact in contacts:
            names = contact.split(',')
            contact_info = {
                'isSameAddressAsWorks': same_address,
                'name1': names[0],
                'zipcode': zipcode,
                'city': city,
                'street': person_street,
                'number': person_number,
            }
            if len(names) > 1:
                contact_info['name2'] = names[1].split()[0].capitalize()
            self.invokeFactory(contact_type, id=self.generateUniqueId(contact_type), **contact_info)

        self.updateTitle()

    def extractStreetAndNumber(self, address):
        address_words = address.split()
        number = address_words[-1]
        if re.match('\d', number) and number.lower() != '1er':
            street = ' '.join(address_words[0:-1])
            return {'street': street, 'number': number}
        else:
            return {'street': address, 'number': ''}

    def haveSameNumbers(self, num_a, num_b):
        match_expr = '\d+'
        numbers_a = re.findall(match_expr, num_a)
        numbers_b = re.findall(match_expr, num_b)
        common_numbers = list(set(numbers_a).intersection(set(numbers_b)))
        return common_numbers

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to clearly identify the licence
        """
        if self.getApplicants():
            applicantTitle = self.getApplicants()[0].Title()
        else:
            applicantTitle = translate('no_applicant_defined', 'urban', context=self.REQUEST).encode('utf8')
        title = "%s - %s - %s" % (self.getReference(), self.getLicenceSubject(), applicantTitle)
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    security.declarePublic('getAnnoncedDelay')
    def getAnnoncedDelay(self, theObject=False):
        """
          Returns the annonced delay value or the UrbanDelay if theObject=True
        """
        res = self.getField('annoncedDelay').get(self)
        if res and theObject:
            tool = api.portal.get_tool('portal_urban')
            urbanConfig = self.getLicenceConfig()
            res = getattr(urbanConfig.folderdelays, res)
        return res

    security.declarePublic('getPca')
    def getPca(self, theObject=False):
        """
          Returns the pca value or the PcaTerm if theObject=True
        """
        res = self.getField('pca').get(self)
        if res and theObject:
            tool = api.portal.get_tool('portal_urban')
            urbanConfig = self.getLicenceConfig()
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
        urban_tool = api.portal.get_tool('portal_urban')
        listEventTypes = self.getAllAdvices()
        for eventType in listEventTypes:
            eventType.checkCreationInLicence(self)
            eventTypeType = eventType.getEventTypeType()
            portal_type = urban_tool.portal_types_per_event_type_type.get(eventTypeType, "UrbanEvent")

            newUrbanEventId= self.invokeFactory(portal_type, id=urban_tool.generateUniqueId(portal_type),
                                                  title=eventType.Title(), urbaneventtypes=(eventType,))
            newUrbanEventObj=getattr(self, newUrbanEventId)
            newUrbanEventObj.processForm()
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + '/view?#fieldsetlegend-urban_events')

    security.declarePublic('getAllAdvices')
    def getAllAdvices(self):
        """
          Returns all UrbanEvents corresponding to advice on a licence
        """
        tool = api.portal.get_tool('portal_urban')
        urbanConfig = self.getLicenceConfig()
        listEventTypes = tool.listEventTypes(self,urbanConfig.id)
        res = []
        for listEventType in listEventTypes:
            obj = listEventType.getObject()
            #an advice corresponding to IOpinionRequestEvent
            if obj.eventTypeType == 'Products.urban.interfaces.IOpinionRequestEvent':
                res.append(obj)
        return res

    security.declarePublic('hasEventNamed')
    def hasEventNamed(self, title):
        """
        Tells if the licence contains an urbanEvent named 'title'
        """
        catalog = api.portal.get_tool('portal_catalog')
        if catalog(portal_type='UrbanEvent', path=self.absolute_url_path(), Title=title):
            return True
        return False

    security.declarePublic('hasNoEventNamed')
    def hasNoEventNamed(self, title):
        """
        Tells if the licence does not contain any urbanEvent named 'title'
        """
        return not self.hasEventNamed(title)

    security.declarePublic('getLicencesOfTheParcels')
    def getLicencesOfTheParcels(self, licence_type=''):
        history = []
        licence_uids = set([])
        for parcel in self.getParcels():
            for brain in parcel.getRelatedLicences(licence_type=licence_type):
                if brain.UID not in licence_uids:
                    history.append(brain)
                    licence_uids.add(brain.UID)
        return history

    def getLicenceOfTheParcels(self, licence_type, limit_date):
        licences = []
        for brain in self.getLicencesOfTheParcels(licence_type=licence_type):
            licence = brain.getObject()
            delivered = licence.getLastTheLicence()
            if delivered and delivered.getDecisionDate() > limit_date:
                if delivered.getDecision() == 'favorable':
                    licences.append(licence)
                elif licence_type in ['UrbanCertificateTwo', 'UrbanCertificateOne']:
                    licences.append(licence)
        return licences

    security.declarePublic('getUrbanCertificateTwoOfTheParcels')
    def getUrbanCertificateTwoOfTheParcels(self, date=None):
        #cu2 cannot be older than 2 years
        if  self.getLastTheLicence():
            limit_date = self.getLastTheLicence().getEventDate() - 731
        elif date:
            limit_date = date - 731
        else:
            limit_date = self.getLastDeposit().getEventDate() - 731
        return self.getLicenceOfTheParcels('UrbanCertificateTwo', limit_date)



registerType(GenericLicence, PROJECTNAME)
# end of class GenericLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer

