# -*- coding: utf-8 -*-
#
# File: GenericLicence.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo

from collective.faceted.task.interfaces import IFacetedTaskContainer

from collective.task.behaviors import ITask

from eea.facetednavigation.search.interfaces import ICollection
from eea.facetednavigation.subtypes.interfaces import IPossibleFacetedNavigable

from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.utils import is_attachment

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.content.licence.base import UrbanBase
from Products.urban.interfaces import IOpinionRequestEvent
from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import get_interface_by_path
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban import UrbanMessage as _

from zope.component import createObject

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
    {
        'name': 'pcaZone',
        'action': 'show',
        'hide_values': (True, ),
    },
)

optional_fields = [
    'subdivisionDetails', 'missingParts', 'missingPartsDetails', 'folderZoneDetails', 'folderZone',
    'isInPCA', 'roadType', 'roadCoating', 'roadEquipments', 'pcaZone',
    'isInSubdivision', 'solicitLocationOpinionsTo', 'technicalRemarks', 'locationTechnicalRemarks',
    'folderCategoryTownship', 'protectedBuilding', 'protectedBuildingDetails', 'folderCategory',
    'pash', 'pashDetails', 'catchmentArea', 'catchmentAreaDetails', 'equipmentAndRoadRequirements',
    'SSC', 'sscDetails', 'RCU', 'rcuDetails', 'floodingLevel', 'floodingLevelDetails', 'solicitRoadOpinionsTo',
    'areParcelsVerified', 'locationFloodingLevel', 'licenceSubject', 'referenceDGATLP',
    'roadMissingParts', 'roadMissingPartsDetails', 'locationMissingParts', 'locationMissingPartsDetails',
    'PRevU', 'prevuDetails', 'PRenU', 'prenuDetails', 'airportNoiseZone', 'airportNoiseZoneDetails',
    'description', 'rgbsr', 'rgbsrDetails', 'karstConstraints', 'karstConstraintsDetails',
    'concentratedRunoffSRisk', 'concentratedRunoffSRiskDetails', 'sevesoSite', 'natura_2000', 'sewers',
    'sewersDetails', 'roadAnalysis', 'futureRoadCoating', 'expropriation', 'expropriationDetails',
    'preemption', 'preemptionDetails', 'SAR', 'sarDetails', 'enoughRoadEquipment', 'enoughRoadEquipmentDetails',
    'reparcelling', 'reparcellingDetails', 'noteworthyTrees', 'pipelines', 'pipelinesDetails'
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
        required=True,
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
            columns={'number': Column("Number"), 'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',), workflow_states=('enabled',))},
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
        schemata='urban_analysis',
        multiValued=True,
        vocabulary=UrbanVocabulary('missingparts'),
        default_method='getDefaultValue',
    ),
    TextField(
        name='missingPartsDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Missingpartsdetails',
            label_msgid='urban_label_missingPartsDetails',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
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
        allowable_content_types=('text/html',),
        widget=RichWidget(
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
    LinesField(
        name='roadAnalysis',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Roadanalysis',
            label_msgid='urban_label_roadAnalysis',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary=UrbanVocabulary('roadanalysis'),
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
    StringField(
        name='futureRoadCoating',
        widget=SelectionWidget(
            format='select',
            label='Futureroadcoating',
            label_msgid='urban_label_futureRoadCoating',
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
            columns={'road_equipment': SelectColumn("Road equipments", UrbanVocabulary('folderroadequipments', inUrbanConfig=False)), 'road_equipment_details': Column("Road equipment details")},
            label='Roadequipments',
            label_msgid='urban_label_roadEquipments',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=("road_equipment", "road_equipment_details"),
    ),
    StringField(
        name='sewers',
        widget=SelectionWidget(
            format='select',
            label='Sewers',
            label_msgid='urban_label_sewers',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        vocabulary=UrbanVocabulary('sewers', inUrbanConfig=False, with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='sewersDetails',
        widget=RichWidget(
            label='Sewersdetails',
            label_msgid='urban_label_sewersDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_road',
        default_method='getDefaultText',
        default_output_type='text/html',
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
    LinesField(
        name='karstConstraints',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Karstconstraints',
            label_msgid='urban_label_karstConstraints',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary=UrbanVocabulary('karst_constraints', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='karstConstraintsDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Karstconstraintsdetails',
            label_msgid='urban_label_karstConstraintsDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/plain',
    ),
    LinesField(
        name='concentratedRunoffSRisk',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='concentratedrunoffsrisk',
            label_msgid='urban_label_concentratedRunoffSRisk',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary=UrbanVocabulary('concentrated_runoff_s_risk', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='concentratedRunoffSRiskDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='concentratedrunoffsriskdetails',
            label_msgid='urban_label_concentratedRunoffSRiskDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/plain',
    ),
    LinesField(
        name='sevesoSite',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='sevesosite',
            label_msgid='urban_label_sevesoSite',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary=UrbanVocabulary('seveso_site', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    LinesField(
        name='pipelines',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='pipelines',
            label_msgid='urban_label_pipelines',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary=UrbanVocabulary('pipelines', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='pipelinesDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Pipelinesdetails',
            label_msgid='urban_label_pipelinesDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/plain',
    ),
    LinesField(
        name='natura_2000',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='natura_2000',
            label_msgid='urban_label_natura_2000',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        multiValued=1,
        vocabulary_factory='urban.vocabulary.Natura2000',
        default_method='getDefaultValue',
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
        allowable_content_types=('text/html',),
        widget=RichWidget(
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
    LinesField(
        name='pcaZone',
        widget=MultiSelectionWidget(
            size=10,
            label='Pcazone',
            label_msgid='urban_label_pcaZone',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary_factory='urban.vocabulary.PCAZones',
        default_method='getDefaultValue',
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
    BooleanField(
        name='expropriation',
        default=False,
        widget=BooleanField._properties['widget'](
            label='expropriation',
            label_msgid='urban_label_expropriation',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='expropriationDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Expropriationdetails',
            label_msgid='urban_label_expropriationDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
    ),
    BooleanField(
        name='preemption',
        default=False,
        widget=BooleanField._properties['widget'](
            label='preemption',
            label_msgid='urban_label_preemption',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='preemptionDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Preemptiondetails',
            label_msgid='urban_label_preemptionDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
    ),
    BooleanField(
        name='SAR',
        default=False,
        widget=BooleanField._properties['widget'](
            label='sar',
            label_msgid='urban_label_SAR',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='sarDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Sardetails',
            label_msgid='urban_label_sarDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
    ),
    BooleanField(
        name='enoughRoadEquipment',
        default=False,
        widget=BooleanField._properties['widget'](
            label='enoughRoadEquipment',
            label_msgid='urban_label_enoughRoadEquipment',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='enoughRoadEquipmentDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Enoughroadequipmentdetails',
            label_msgid='urban_label_enoughRoadEquipmentDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
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
        schemata='urban_analysis',
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
        vocabulary_factory='urban.vocabulary.ProtectedBuilding',
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
            size=15,
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
            size=10,
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
        name='PRenU',
        widget=MultiSelectionWidget(
            size=5,
            label='Prenu',
            label_msgid='urban_label_PRenU',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('prenu', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='prenuDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Prenudetails',
            label_msgid='urban_label_prenuDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    LinesField(
        name='PRevU',
        widget=MultiSelectionWidget(
            size=5,
            label='Prevu',
            label_msgid='urban_label_PRevU',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('prevu', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='prevuDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Prevudetails',
            label_msgid='urban_label_prevuDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    LinesField(
        name='reparcelling',
        widget=MultiSelectionWidget(
            size=5,
            label='Prevu',
            label_msgid='urban_label_reparcelling',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary_factory='urban.vocabulary.Reparcelling',
        default_method='getDefaultValue',
    ),
    TextField(
        name='reparcellingDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Reparcellingdetails',
            label_msgid='urban_label_reparcellingDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    StringField(
        name='rgbsr',
        widget=SelectionWidget(
            label='Rgbsr',
            label_msgid='urban_label_rgbsr',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        vocabulary=UrbanVocabulary('rgbsr', inUrbanConfig=False, with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='rgbsrDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Rgbsrdetails',
            label_msgid='urban_label_rgbsrDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    LinesField(
        name='airportNoiseZone',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Airportnoisezone',
            label_msgid='urban_label_airportNoiseZone',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('airportnoisezone', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='airportNoiseZoneDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Airportnoisezonedetails',
            label_msgid='urban_label_airportNoiseZoneDetails',
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
        multiValued=True,
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
            available_indexes={'Title': 'Nom'},
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
    LinesField(
        name='noteworthyTrees',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Noteworthytrees',
            label_msgid='urban_label_noteworthyTrees',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('noteworthytrees', inUrbanConfig=False),
        default_method='getDefaultValue',
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


class GenericLicence(BaseFolder, UrbanBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(
        interfaces.IGenericLicence,
        IFacetedTaskContainer,
        ICollection,
        IPossibleFacetedNavigable
    )

    meta_type = 'GenericLicence'
    _at_rename_after_creation = True
    # block local roles acquisition and let the workflow handle that
    __ac_local_roles_block__ = True

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

    security.declarePublic('getRepresentatives')

    def getRepresentatives(self):
        """
        To override per licence type
        """
        return []

    security.declarePublic('getDefaultValue')

    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return ['']

        urban_tool = api.portal.get_tool('portal_urban')

        default_value = urban_tool.getVocabularyDefaultValue(
            vocabulary=field.vocabulary or field.vocabulary_factory,
            context=context,
            multivalued=field.multiValued
        )
        return default_value

    security.declarePublic('getDefaultText')

    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = api.portal.get_tool('portal_urban')
        return urban_tool.getTextDefaultValue(field.getName(), context, html)

    security.declarePublic('getUrbanConfig')

    def getUrbanConfig(self):
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

    def createUrbanEvent(self, urban_event_type, **kwargs):
        """
         urban_event_type can either be an id, an uid or the object
        """
        urban_event = createObject('UrbanEvent', self, urban_event_type, **kwargs)
        return urban_event

    security.declarePublic('getRawQuery')

    def getRawQuery(self):
        """ """
        query = [
            {
                'i': 'object_provides',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ITask.__identifier__
            },
            {
                'i': 'path',
                'o': 'plone.app.querystring.operation.string.relativePath',
                'v': '.'
            },
        ]
        return query

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
            ('very low', translate(_('flooding_level_verylow'), context=self.REQUEST)),
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
        ids = []
        for foldermanager in urban_tool.foldermanagers.objectValues():
            if self.getPortalTypeName() in foldermanager.getManageableLicences():
                ids.append(foldermanager.getId())
        dict = {}
        dict['path'] = {'query': '%s/portal_urban/foldermanagers' % (rootPath)}
        dict['id'] = ids
        return dict

    security.declarePublic('getParcels')

    def getParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        return self.objectValues('PortionOut')

    security.declarePublic('getOfficialParcels')

    def getOfficialParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        parcels = [prc for prc in self.getParcels() if prc.getIsOfficialParcel()]
        return parcels

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

    security.declarePublic('getAttachments')

    def getAttachments(self):
        """
          Return the attachments (File) of the UrbanEvent
        """
        attachments = [obj for obj in self.objectValues() if is_attachment(obj)]
        return attachments

    security.declarePublic('getAnnoncedDelay')

    def getAnnoncedDelay(self, theObject=False):
        """
          Returns the annonced delay value or the UrbanDelay if theObject=True
        """
        res = self.getField('annoncedDelay').get(self)
        if res and theObject:
            urbanConfig = self.getLicenceConfig()
            res = getattr(urbanConfig.folderdelays, res)
        return res

    security.declarePublic('getPca')

    def getPca(self, theObject=False):
        """
          Returns the pca value or the PcaTerm if theObject=True
        """
        res = self.getField('pca').get(self)
        if type(res) is str and theObject:
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
            portal_type = eventType.getEventPortalType() or 'UrbanEvent'

            newUrbanEventId = self.invokeFactory(
                portal_type, id=urban_tool.generateUniqueId(portal_type),
                title=eventType.Title(), urbaneventtypes=(eventType,)
            )
            newUrbanEventObj = getattr(self, newUrbanEventId)
            if eventType.id in self.solicitOpinionsToOptional:
                newUrbanEventObj.isOptional = True
            newUrbanEventObj.processForm()
        return self.REQUEST.RESPONSE.redirect(self.absolute_url() + '/view?#fieldsetlegend-urban_events')

    security.declarePublic('getAllAdvices')

    def getAllAdvices(self):
        """
          XXX need to be refactor (do not work)
          Returns all UrbanEvents corresponding to advice on a licence
        """
        tool = api.portal.get_tool('portal_urban')
        urbanConfig = self.getLicenceConfig()
        listEventTypes = tool.listEventTypes(self, urbanConfig.id)
        res = []
        for eventType in listEventTypes:
            obj = eventType.getObject()
            if obj.eventTypeType and obj.eventTypeType != 'UrbanEvent':
                for type_interface_path in obj.getEventTypeType():
                    type_interface = get_interface_by_path(type_interface_path)
                    #an advice corresponding to IOpinionRequestEvent
                    if type_interface.isOrExtends(IOpinionRequestEvent):
                        res.append(obj)
        return res

    security.declarePublic('hasEventNamed')

    def hasEventNamed(self, title):
        """
        Tells if the licence contains an urbanEvent named 'title'
        """
        for obj in self.objectValues():
            if IUrbanEvent.providedBy(obj) and obj.Title() == title:
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
        # cu2 cannot be older than 2 years
        if self.getLastTheLicence():
            limit_date = self.getLastTheLicence().getEventDate() - 731
        elif date:
            limit_date = date - 731
        else:
            limit_date = self.getLastDeposit().getEventDate() - 731
        return self.getLicenceOfTheParcels('UrbanCertificateTwo', limit_date)

    def getFirstDeposit(self):
        return self.getFirstEvent(interfaces.IDepositEvent)

    def getLastSimpleCollege(self):
        return self.getLastEvent(interfaces.ISimpleCollegeEvent)

    def getAllEvents(self, eventInterface=IUrbanEvent):
        return self.getAllEventsByObjectValues(eventInterface)

    def getAllEventsByObjectValues(self, eventInterface):
        return [evt for evt in self.objectValues() if not eventInterface or eventInterface.providedBy(evt)]

    def getLastEvent(self, eventInterface=None):
        events = self.getAllEvents(eventInterface)
        if events:
            return events[-1]

    def getFirstEvent(self, eventInterface=None):
        events = self.getAllEvents(eventInterface)
        if events:
            return events[0]

registerType(GenericLicence, PROJECTNAME)
# end of class GenericLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer
